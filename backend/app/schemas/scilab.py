from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.integrations.scilab.models import ExecutionStatus, SessionState


class ScilabStatusResponse(BaseModel):
    installed: bool
    executable: Optional[str] = None
    version: Optional[str] = None
    status: str
    session_state: SessionState = SessionState.STOPPED

    model_config = ConfigDict(from_attributes=True)


class ScilabCommandRequest(BaseModel):
    command: str = Field(..., min_length=1, description="Scilab command string to execute")
    timeout: Optional[float] = Field(None, gt=0, description="Optional custom execution timeout in seconds")


class ScilabScriptRequest(BaseModel):
    path: str = Field(..., min_length=1, description="Path to Scilab script file (.sci or .sce)")
    timeout: Optional[float] = Field(None, gt=0, description="Optional custom execution timeout in seconds")


class ExecutionResultResponse(BaseModel):
    id: str
    command: str
    success: bool
    stdout: str = ""
    stderr: str = ""
    exit_code: Optional[int] = 0
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_ms: float = 0.0
    status: ExecutionStatus
    truncated: bool = False

    model_config = ConfigDict(from_attributes=True)


class CancelExecutionResponse(BaseModel):
    execution_id: str
    status: str = "cancelled"
    message: str = "Execution cancelled successfully"
