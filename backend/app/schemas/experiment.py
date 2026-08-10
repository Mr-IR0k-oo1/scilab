from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ExperimentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    script_path: str = Field(..., min_length=1, description="Relative path to .sce or .sci script")


class ExperimentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    script_path: Optional[str] = None
    status: Optional[str] = None


class ExperimentResponse(BaseModel):
    id: str
    project_id: str
    name: str
    description: Optional[str] = None
    script_path: str
    status: str
    last_execution_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExecutionRecordResponse(BaseModel):
    id: str
    project_id: str
    experiment_id: Optional[str] = None
    script_path: str
    execution_id: str
    status: str
    started_at: datetime
    finished_at: Optional[datetime] = None
    duration_ms: float
    exit_code: Optional[int] = 0
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
