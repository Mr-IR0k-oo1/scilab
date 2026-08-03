from fastapi import APIRouter
from pydantic import BaseModel

from ..scilab import scilab_manager
from ..models import ExecuteResult, ScilabStatus

router = APIRouter(prefix="/api/scilab", tags=["scilab"])

class ExecuteRequest(BaseModel):
    code: str

@router.post("/start", response_model=ScilabStatus)
async def start_scilab():
    return await scilab_manager.start()

@router.post("/stop")
async def stop_scilab():
    await scilab_manager.stop()
    return {"success": True}

@router.post("/execute", response_model=ExecuteResult)
async def execute_code(req: ExecuteRequest):
    return await scilab_manager.execute(req.code)

@router.get("/status", response_model=ScilabStatus)
async def scilab_status():
    return await scilab_manager.status()
