"""
Scilab Process Manager service.

Manages sub-process lifetime of Scilab CLI binary using asyncio.subprocess,
providing non-blocking asynchronous stream reading, PID monitoring, process controls
(Start, Stop, Restart), and event broadcasting.
"""

import asyncio
import logging
import os
import shutil

from pathlib import Path
from typing import Optional, Tuple

from core.config import settings
from core.event_bus import event_bus, Event
from .parser import ScilabOutputParser

logger = logging.getLogger(__name__)


class ScilabProcessManager:
    """
    Asynchronous Scilab Subprocess Manager.
    """

    def __init__(self) -> None:
        self._process: Optional[asyncio.subprocess.Process] = None
        self._executable_path: Optional[str] = None
        self._parser = ScilabOutputParser()
        self._read_tasks: list[asyncio.Task] = []
        self._lock = asyncio.Lock()

    def detect_scilab(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detect Scilab installation on system.
        
        Returns:
            Tuple of (installed: bool, executable_path: Optional[str], version: Optional[str]).
        """
        if settings.custom_scilab_path and Path(settings.custom_scilab_path).exists():
            return True, settings.custom_scilab_path, "Custom Path"

        # Search system PATH for binaries
        for candidate in ["scilab-cli", "scilab", "scilab-adv-cli"]:
            found = shutil.which(candidate)
            if found:
                return True, found, "7.0+"

        return False, None, None

    @property
    def is_running(self) -> bool:
        """Check if Scilab subprocess is currently active."""
        return self._process is not None and self._process.returncode is None

    @property
    def pid(self) -> Optional[int]:
        """Get PID of active Scilab process."""
        return self._process.pid if self._process else None

    async def start(self) -> bool:
        """
        Start Scilab CLI subprocess.
        
        Returns:
            True if started successfully.
        """
        async with self._lock:
            if self.is_running:
                logger.info("Scilab process already running (PID: %d).", self.pid)
                return True

            installed, exec_path, _ = self.detect_scilab()
            if not installed or not exec_path:
                logger.error("Scilab executable not found on system.")
                return False

            self._executable_path = exec_path
            try:
                logger.info("Starting Scilab subprocess: %s", exec_path)
                self._process = await asyncio.create_subprocess_exec(
                    exec_path,
                    "-nw",  # No window mode (CLI)
                    "-no-welcome",
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                # Start background stream reading tasks
                t1 = asyncio.create_task(self._read_stream(self._process.stdout, is_stderr=False))
                t2 = asyncio.create_task(self._read_stream(self._process.stderr, is_stderr=True))
                self._read_tasks = [t1, t2]

                await event_bus.publish(
                    Event(
                        topic="runtime.status_changed",
                        payload={"running": True, "pid": self._process.pid},
                        sender="ScilabProcessManager",
                    )
                )

                logger.info("Scilab process started successfully (PID: %d).", self._process.pid)
                return True
            except Exception as exc:
                logger.exception("Failed to launch Scilab process: %s", exc)
                self._process = None
                return False

    async def stop(self) -> bool:
        """
        Stop active Scilab subprocess gracefully or terminate.
        
        Returns:
            True if stopped.
        """
        async with self._lock:
            if not self._process or self._process.returncode is not None:
                return True

            logger.info("Stopping Scilab process (PID: %d)...", self.pid)
            try:
                self._process.terminate()
                try:
                    await asyncio.wait_for(self._process.wait(), timeout=3.0)
                except asyncio.TimeoutError:
                    logger.warning("Scilab process termination timed out. Killing process...")
                    self._process.kill()
                    await self._process.wait()

                for task in self._read_tasks:
                    task.cancel()
                self._read_tasks.clear()

                pid = self._process.pid
                self._process = None

                await event_bus.publish(
                    Event(
                        topic="runtime.status_changed",
                        payload={"running": False, "pid": pid},
                        sender="ScilabProcessManager",
                    )
                )

                logger.info("Scilab process stopped.")
                return True
            except Exception as exc:
                logger.exception("Failed to stop Scilab process: %s", exc)
                return False

    async def restart(self) -> bool:
        """Restart Scilab process."""
        await self.stop()
        return await self.start()

    async def send_command_input(self, command_line: str) -> bool:
        """
        Write a command line string into Scilab stdin process.
        """
        if not self.is_running or not self._process or not self._process.stdin:
            logger.warning("Attempted to send input to inactive Scilab process.")
            return False

        try:
            full_input = command_line.rstrip("\n") + "\n"
            self._process.stdin.write(full_input.encode("utf-8"))
            await self._process.stdin.drain()
            return True
        except Exception as exc:
            logger.exception("Error writing input to Scilab process: %s", exc)
            return False

    async def _read_stream(self, stream: Optional[asyncio.StreamReader], is_stderr: bool = False) -> None:
        """Asynchronously read lines from subprocess stream and publish events."""
        if stream is None:
            return

        while True:
            line_bytes = await stream.readline()
            if not line_bytes:
                break

            line_str = line_bytes.decode("utf-8", errors="replace")
            parsed = self._parser.parse_line(line_str, is_stderr=is_stderr)

            # Publish granular stream events
            if parsed.line_type == "progress":
                await event_bus.publish(
                    Event(
                        topic="runtime.progress",
                        payload={"percent": parsed.progress_percent, "text": parsed.clean_text},
                        sender="ScilabProcessManager",
                    )
                )
            elif parsed.line_type == "warning":
                await event_bus.publish(
                    Event(
                        topic="runtime.warning",
                        payload={"text": parsed.clean_text},
                        sender="ScilabProcessManager",
                    )
                )
            elif parsed.line_type == "error":
                await event_bus.publish(
                    Event(
                        topic="runtime.error",
                        payload={"text": parsed.clean_text},
                        sender="ScilabProcessManager",
                    )
                )
            elif is_stderr:
                await event_bus.publish(
                    Event(
                        topic="runtime.stderr",
                        payload={"text": line_str},
                        sender="ScilabProcessManager",
                    )
                )
            else:
                await event_bus.publish(
                    Event(
                        topic="runtime.stdout",
                        payload={"text": line_str},
                        sender="ScilabProcessManager",
                    )
                )
