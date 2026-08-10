import asyncio
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Callable, Optional
from app.core.logging import logger
from app.integrations.scilab.configuration import scilab_config
from app.integrations.scilab.exceptions import (
    ScilabExecutionTimeoutException,
    ScilabSecurityException,
    ScilabSessionStateError,
)
from app.integrations.scilab.models import ExecutionResult, ExecutionStatus
from app.integrations.scilab.parser import ScilabOutputParser
from app.integrations.scilab.session import ScilabSession


class ScilabExecutor:
    @staticmethod
    def validate_script_path(script_path: str, allowed_base_dirs: Optional[list[str]] = None) -> str:
        """
        Validates path existence, file type, allowed extensions (.sci, .sce),
        and prevents path traversal attacks outside workspace boundaries.
        """
        if not script_path:
            raise ScilabSecurityException("Script path cannot be empty")

        # Resolve absolute normalized path
        abs_path = os.path.abspath(os.path.normpath(script_path))

        # Check path traversal
        if ".." in script_path.split("/") or ".." in script_path.split("\\"):
            raise ScilabSecurityException("Path traversal (..) is strictly prohibited")

        # Check existence and file type
        if not os.path.exists(abs_path):
            raise ScilabSecurityException(f"Script file does not exist: {script_path}")
        if not os.path.isfile(abs_path):
            raise ScilabSecurityException(f"Target path is not a file: {script_path}")

        # Check extension
        ext = os.path.splitext(abs_path)[1].lower()
        if ext not in [".sci", ".sce"]:
            raise ScilabSecurityException(f"Invalid script file extension '{ext}'. Only .sci and .sce are allowed")

        # Validate against allowed base directories if specified
        if allowed_base_dirs:
            valid_boundary = False
            for base_dir in allowed_base_dirs:
                abs_base = os.path.abspath(os.path.normpath(base_dir))
                if abs_path.startswith(abs_base):
                    valid_boundary = True
                    break
            if not valid_boundary:
                raise ScilabSecurityException(f"Script execution forbidden outside approved workspace directories: {script_path}")

        return abs_path

    @staticmethod
    async def execute_command(
        command: str,
        session: ScilabSession,
        timeout: Optional[float] = None,
        output_callback: Optional[Callable[[str, str], None]] = None,
    ) -> ExecutionResult:
        execution_id = str(uuid.uuid4())
        timeout_val = timeout or scilab_config.timeout_seconds
        started_at = datetime.now(timezone.utc)
        start_time = time.perf_counter()

        if not session.can_execute():
            raise ScilabSessionStateError("Scilab session is not running or ready for execution")

        await session.set_executing()

        stdout_chunks = []
        stderr_chunks = []

        try:
            # Send execution block or temp command execution
            cmd_with_markers = f'{command}\n'
            await session.process_manager.send(cmd_with_markers)

            # Wait for execution response or timeout
            # Non-blocking async read from stdout/stderr
            proc = session.process_manager.process
            if not proc or not proc.stdout:
                raise ScilabSessionStateError("Scilab stdout pipe uninitialized")

            async def read_until_done():
                while True:
                    line = await proc.stdout.readline()
                    if not line:
                        break
                    decoded = line.decode("utf-8", errors="ignore")
                    stdout_chunks.append(decoded)
                    if output_callback:
                        output_callback("stdout", decoded)
                    # Check if line indicates end of execution
                    if "ans =" in decoded or "-->" in decoded or len(stdout_chunks) >= 1:
                        break

            try:
                await asyncio.wait_for(read_until_done(), timeout=timeout_val)
                status = ExecutionStatus.COMPLETED
                success = True
            except asyncio.TimeoutError:
                logger.warning(f"Scilab command timed out after {timeout_val}s. Cleaning up process...")
                status = ExecutionStatus.TIMED_OUT
                success = False
                await session.process_manager.terminate()
                if session.process_manager.is_running():
                    await session.process_manager.kill()

        except Exception as e:
            logger.error(f"Execution error: {e}")
            status = ExecutionStatus.FAILED
            success = False
            stderr_chunks.append(str(e))
        finally:
            await session.set_finished_executing(success=success)

        duration_ms = (time.perf_counter() - start_time) * 1000
        finished_at = datetime.now(timezone.utc)

        raw_stdout = "".join(stdout_chunks)
        raw_stderr = "".join(stderr_chunks)

        cleaned_stdout, cleaned_stderr, is_truncated = ScilabOutputParser.parse_output(
            raw_stdout, raw_stderr, max_size=scilab_config.max_output_size
        )

        return ExecutionResult(
            id=execution_id,
            command=command,
            success=success,
            stdout=cleaned_stdout,
            stderr=cleaned_stderr,
            exit_code=0 if success else 1,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=duration_ms,
            status=status,
            truncated=is_truncated,
        )

    @staticmethod
    async def execute_script(
        script_path: str,
        session: ScilabSession,
        timeout: Optional[float] = None,
        allowed_base_dirs: Optional[list[str]] = None,
        output_callback: Optional[Callable[[str, str], None]] = None,
    ) -> ExecutionResult:
        valid_path = ScilabExecutor.validate_script_path(script_path, allowed_base_dirs)
        cmd = f"exec('{valid_path}', -1);"
        return await ScilabExecutor.execute_command(
            command=cmd,
            session=session,
            timeout=timeout,
            output_callback=output_callback,
        )
