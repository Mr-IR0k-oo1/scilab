import asyncio
from typing import Optional
from app.integrations.scilab.exceptions import ScilabSessionStateError
from app.integrations.scilab.models import SessionState
from app.integrations.scilab.process_manager import ProcessManager


class ScilabSession:
    def __init__(self, executable: str, working_dir: Optional[str] = None):
        self.executable = executable
        self.working_dir = working_dir
        self.state: SessionState = SessionState.CREATED
        self.process_manager: ProcessManager = ProcessManager(executable, working_dir)
        self._lock = asyncio.Lock()

    def can_execute(self) -> bool:
        return self.state == SessionState.RUNNING and self.process_manager.is_running()

    async def start(self) -> None:
        async with self._lock:
            if self.state in [SessionState.RUNNING, SessionState.EXECUTING]:
                return
            if self.state == SessionState.STARTING:
                raise ScilabSessionStateError("Session startup already in progress")

            self.state = SessionState.STARTING
            success = await self.process_manager.start()
            if success:
                self.state = SessionState.RUNNING
            else:
                self.state = SessionState.FAILED
                raise ScilabSessionStateError("Failed to start Scilab process")

    async def stop(self) -> None:
        async with self._lock:
            if self.state in [SessionState.STOPPED, SessionState.CREATED]:
                return
            self.state = SessionState.STOPPING
            await self.process_manager.stop()
            self.state = SessionState.STOPPED

    async def set_executing(self) -> None:
        async with self._lock:
            if self.state != SessionState.RUNNING:
                raise ScilabSessionStateError(f"Cannot execute command when session is in state {self.state}")
            self.state = SessionState.EXECUTING

    async def set_finished_executing(self, success: bool = True) -> None:
        async with self._lock:
            if self.state == SessionState.EXECUTING:
                self.state = SessionState.RUNNING if success else SessionState.FAILED
