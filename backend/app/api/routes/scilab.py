import asyncio
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from app.integrations.scilab.exceptions import (
    ScilabException,
    ScilabExecutionTimeoutException,
    ScilabNotFoundException,
    ScilabSecurityException,
    ScilabSessionStateError,
)
from app.schemas.scilab import (
    CancelExecutionResponse,
    ExecutionResultResponse,
    ScilabCommandRequest,
    ScilabScriptRequest,
    ScilabStatusResponse,
)
from app.services.scilab_service import ScilabService

router = APIRouter()


@router.get("/scilab/status", response_model=ScilabStatusResponse)
def get_scilab_status():
    info = ScilabService.get_detector_info()
    session_state = (
        ScilabService._session_instance.state
        if ScilabService._session_instance
        else "STOPPED"
    )
    return ScilabStatusResponse(
        installed=info.installed,
        executable=info.executable,
        version=info.version,
        status=info.status,
        session_state=session_state,
    )


@router.post("/scilab/start", response_model=ScilabStatusResponse)
async def start_scilab_session():
    try:
        info = await ScilabService.start_session()
        return ScilabStatusResponse(
            installed=info.installed,
            executable=info.executable,
            version=info.version,
            status=info.status,
            session_state=ScilabService._session_instance.state if ScilabService._session_instance else "RUNNING",
        )
    except ScilabNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "SCILAB_NOT_FOUND", "message": str(e)},
        )
    except ScilabSessionStateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "SCILAB_SESSION_ERROR", "message": str(e)},
        )


@router.post("/scilab/stop", status_code=status.HTTP_200_OK)
async def stop_scilab_session():
    await ScilabService.stop_session()
    return {"status": "stopped", "message": "Scilab session stopped successfully"}


@router.post("/scilab/restart", response_model=ScilabStatusResponse)
async def restart_scilab_session():
    try:
        info = await ScilabService.restart_session()
        return ScilabStatusResponse(
            installed=info.installed,
            executable=info.executable,
            version=info.version,
            status=info.status,
            session_state=ScilabService._session_instance.state if ScilabService._session_instance else "RUNNING",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "SCILAB_RESTART_FAILED", "message": str(e)},
        )


@router.post("/scilab/execute", response_model=ExecutionResultResponse)
async def execute_command(req: ScilabCommandRequest):
    try:
        result = await ScilabService.execute_command(command=req.command, timeout=req.timeout)
        return ExecutionResultResponse.model_validate(result)
    except ScilabSecurityException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "SCILAB_SECURITY_ERROR", "message": str(e)},
        )
    except ScilabExecutionTimeoutException as e:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail={"code": "SCILAB_TIMEOUT", "message": str(e)},
        )
    except ScilabException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "SCILAB_EXECUTION_ERROR", "message": str(e)},
        )


@router.post("/scilab/execute-script", response_model=ExecutionResultResponse)
async def execute_script(req: ScilabScriptRequest):
    try:
        result = await ScilabService.execute_script(path=req.path, timeout=req.timeout)
        return ExecutionResultResponse.model_validate(result)
    except ScilabSecurityException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "SCILAB_SECURITY_ERROR", "message": str(e)},
        )
    except ScilabExecutionTimeoutException as e:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail={"code": "SCILAB_TIMEOUT", "message": str(e)},
        )
    except ScilabException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "SCILAB_EXECUTION_ERROR", "message": str(e)},
        )


@router.get("/scilab/executions/{execution_id}", response_model=ExecutionResultResponse)
def get_execution(execution_id: str):
    result = ScilabService.get_execution(execution_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "EXECUTION_NOT_FOUND", "message": f"Execution '{execution_id}' was not found"},
        )
    return ExecutionResultResponse.model_validate(result)


@router.post("/scilab/executions/{execution_id}/cancel", response_model=CancelExecutionResponse)
async def cancel_execution(execution_id: str):
    success = await ScilabService.cancel_execution(execution_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "EXECUTION_NOT_CANCELLED", "message": f"Execution '{execution_id}' is not currently running"},
        )
    return CancelExecutionResponse(execution_id=execution_id)
