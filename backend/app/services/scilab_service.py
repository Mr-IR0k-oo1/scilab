import asyncio
from typing import Dict, List, Optional
from app.core.logging import logger
from app.events.scilab_events import (
    SCILAB_DETECTED,
    SCILAB_EXECUTION_CANCELLED,
    SCILAB_EXECUTION_FAILED,
    SCILAB_EXECUTION_FINISHED,
    SCILAB_EXECUTION_STARTED,
    SCILAB_OUTPUT_RECEIVED,
    SCILAB_STARTED,
    SCILAB_STOPPED,
    publish_scilab_event,
)
from app.integrations.scilab.detector import ScilabDetector
from app.integrations.scilab.exceptions import ScilabNotFoundException
from app.integrations.scilab.executor import ScilabExecutor
from app.integrations.scilab.models import ExecutionResult, ExecutionStatus, ScilabStatusInfo, SessionState
from app.integrations.scilab.session import ScilabSession


class ScilabService:
    _session_instance: Optional[ScilabSession] = None
    _executions_cache: Dict[str, ExecutionResult] = {}
    _websocket_listeners: List[Any] = []

    @classmethod
    def get_detector_info(cls) -> ScilabStatusInfo:
        info = ScilabDetector.detect()
        publish_scilab_event(SCILAB_DETECTED, {
            "installed": info.installed,
            "version": info.version,
            "status": info.status,
        })
        return info

    @classmethod
    def get_session(cls) -> ScilabSession:
        if cls._session_instance is None:
            info = cls.get_detector_info()
            if not info.installed or not info.executable:
                raise ScilabNotFoundException("Scilab executable not found on host machine.")
            cls._session_instance = ScilabSession(executable=info.executable)
        return cls._session_instance

    @classmethod
    async def start_session(cls) -> ScilabStatusInfo:
        info = cls.get_detector_info()
        session = cls.get_session()
        await session.start()
        publish_scilab_event(SCILAB_STARTED, {
            "executable": session.executable,
            "state": session.state.value,
        })
        info.status = "running" if session.can_execute() else "available"
        return info

    @classmethod
    async def stop_session(cls) -> None:
        if cls._session_instance:
            await cls._session_instance.stop()
            publish_scilab_event(SCILAB_STOPPED, {"state": SessionState.STOPPED.value})

    @classmethod
    async def restart_session(cls) -> ScilabStatusInfo:
        await cls.stop_session()
        return await cls.start_session()

    @classmethod
    async def execute_command(
        cls,
        command: str,
        timeout: Optional[float] = None,
        websocket_broadcaster: Optional[Any] = None,
    ) -> ExecutionResult:
        session = cls.get_session()
        if not session.can_execute():
            await session.start()

        def stream_callback(stream_type: str, data: str):
            publish_scilab_event(SCILAB_OUTPUT_RECEIVED, {
                "stream": stream_type,
                "data": data,
            })
            if websocket_broadcaster:
                asyncio.create_task(websocket_broadcaster({
                    "type": stream_type,
                    "data": data,
                }))

        publish_scilab_event(SCILAB_EXECUTION_STARTED, {"command": command})

        result = await ScilabExecutor.execute_command(
            command=command,
            session=session,
            timeout=timeout,
            output_callback=stream_callback,
        )

        cls._executions_cache[result.id] = result

        if result.success:
            publish_scilab_event(SCILAB_EXECUTION_FINISHED, {"execution_id": result.id, "duration_ms": result.duration_ms})
        else:
            publish_scilab_event(SCILAB_EXECUTION_FAILED, {"execution_id": result.id, "error": result.stderr})

        return result

    @classmethod
    async def execute_script(
        cls,
        path: str,
        timeout: Optional[float] = None,
        allowed_base_dirs: Optional[List[str]] = None,
        websocket_broadcaster: Optional[Any] = None,
    ) -> ExecutionResult:
        session = cls.get_session()
        if not session.can_execute():
            await session.start()

        def stream_callback(stream_type: str, data: str):
            publish_scilab_event(SCILAB_OUTPUT_RECEIVED, {
                "stream": stream_type,
                "data": data,
            })
            if websocket_broadcaster:
                asyncio.create_task(websocket_broadcaster({
                    "type": stream_type,
                    "data": data,
                }))

        publish_scilab_event(SCILAB_EXECUTION_STARTED, {"script_path": path})

        result = await ScilabExecutor.execute_script(
            script_path=path,
            session=session,
            timeout=timeout,
            allowed_base_dirs=allowed_base_dirs,
            output_callback=stream_callback,
        )

        cls._executions_cache[result.id] = result

        if result.success:
            publish_scilab_event(SCILAB_EXECUTION_FINISHED, {"execution_id": result.id, "duration_ms": result.duration_ms})
        else:
            publish_scilab_event(SCILAB_EXECUTION_FAILED, {"execution_id": result.id, "error": result.stderr})

        return result

    @classmethod
    def get_execution(cls, execution_id: str) -> Optional[ExecutionResult]:
        return cls._executions_cache.get(execution_id)

    @classmethod
    async def cancel_execution(cls, execution_id: str) -> bool:
        result = cls._executions_cache.get(execution_id)
        if result and result.status == ExecutionStatus.RUNNING:
            result.status = ExecutionStatus.CANCELLED
            result.success = False
            if cls._session_instance:
                await cls._session_instance.process_manager.terminate()
            publish_scilab_event(SCILAB_EXECUTION_CANCELLED, {"execution_id": execution_id})
            return True
        return False
