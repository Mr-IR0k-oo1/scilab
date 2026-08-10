import asyncio
import os
import signal
import sys
from typing import List, Optional
from app.core.logging import logger


class ProcessManager:
    def __init__(self, executable: str, working_dir: Optional[str] = None):
        self.executable = executable
        self.working_dir = working_dir or os.getcwd()
        self.process: Optional[asyncio.subprocess.Process] = None

    async def start(self, extra_args: Optional[List[str]] = None) -> bool:
        if self.is_running():
            return True

        args = [self.executable, "-nw", "-nb"]
        if extra_args:
            args.extend(extra_args)

        try:
            logger.info(f"Starting Scilab process: args={args} cwd={self.working_dir}")
            self.process = await asyncio.create_subprocess_exec(
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.working_dir,
            )
            return True
        except Exception as e:
            logger.error(f"Failed to start Scilab process: {e}")
            self.process = None
            return False

    def is_running(self) -> bool:
        return self.process is not None and self.process.returncode is None

    async def send(self, data: str) -> bool:
        if not self.is_running() or not self.process.stdin:
            return False
        try:
            payload = data if data.endswith("\n") else data + "\n"
            self.process.stdin.write(payload.encode("utf-8"))
            await self.process.stdin.drain()
            return True
        except Exception as e:
            logger.error(f"Error sending command to Scilab stdin: {e}")
            return False

    async def terminate(self) -> None:
        if self.process and self.is_running():
            try:
                self.process.terminate()
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.warning(f"Error terminating Scilab process: {e}")

    async def kill(self) -> None:
        if self.process and self.is_running():
            try:
                self.process.kill()
                await self.process.wait()
            except Exception as e:
                logger.warning(f"Error killing Scilab process: {e}")

    async def stop(self) -> None:
        if not self.is_running():
            return

        # Attempt graceful exit
        await self.send("exit;\n")
        try:
            if self.process:
                await asyncio.wait_for(self.process.wait(), timeout=2.0)
        except asyncio.TimeoutError:
            logger.warning("Scilab process did not exit gracefully; terminating...")
            await self.terminate()
            if self.is_running():
                await self.kill()
        finally:
            self.process = None

    async def restart(self, extra_args: Optional[List[str]] = None) -> bool:
        await self.stop()
        return await self.start(extra_args)
