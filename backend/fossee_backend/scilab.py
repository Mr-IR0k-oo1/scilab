import asyncio
import time
from typing import Optional

from .models import ExecuteResult, ScilabStatus

class ScilabManager:
    def __init__(self):
        self.process: Optional[asyncio.subprocess.Process] = None
        self.lock = asyncio.Lock()

    async def start(self) -> ScilabStatus:
        async with self.lock:
            if self.process is not None and self.process.returncode is None:
                raise Exception("Scilab is already running")

            try:
                self.process = await asyncio.create_subprocess_exec(
                    "scilab-cli", "--nw", "--noecho",
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                return ScilabStatus(running=True, pid=self.process.pid)
            except Exception as e:
                raise Exception(f"Failed to start Scilab: {e}")

    async def stop(self):
        async with self.lock:
            if self.process is not None and self.process.returncode is None:
                self.process.terminate()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=2.0)
                except asyncio.TimeoutError:
                    self.process.kill()
                self.process = None

    async def status(self) -> ScilabStatus:
        if self.process is not None and self.process.returncode is None:
            return ScilabStatus(running=True, pid=self.process.pid)
        return ScilabStatus(running=False)

    async def execute(self, code: str) -> ExecuteResult:
        async with self.lock:
            if self.process is None or self.process.returncode is not None:
                # Auto-recovery
                try:
                    self.process = await asyncio.create_subprocess_exec(
                        "scilab-cli", "--nw", "--noecho",
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                except Exception:
                    return ExecuteResult(output="", error="Scilab crashed and auto-recovery failed", success=False)

            delimiter = "__SCILAB_END__"
            wrapped_code = f"{code}\ndisp('{delimiter}');\n"

            try:
                self.process.stdin.write(wrapped_code.encode('utf-8'))
                await self.process.stdin.drain()
            except Exception as e:
                return ExecuteResult(output="", error=f"Failed to write to stdin: {e}", success=False)

            output_lines = []
            found_delimiter = False
            start_time = time.time()
            timeout = 30.0

            while time.time() - start_time < timeout:
                try:
                    line_bytes = await asyncio.wait_for(self.process.stdout.readline(), timeout=0.5)
                    if not line_bytes: # EOF
                        break
                    
                    line = line_bytes.decode('utf-8')
                    if delimiter in line:
                        found_delimiter = True
                        break
                    output_lines.append(line)
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    return ExecuteResult(output="", error=f"Read error: {e}", success=False)

            if not found_delimiter:
                return ExecuteResult(
                    output="".join(output_lines), 
                    error="Execution timed out", 
                    success=False
                )

            return ExecuteResult(
                output="".join(output_lines).strip(),
                variables={},
                success=True
            )

# Global instance
scilab_manager = ScilabManager()
