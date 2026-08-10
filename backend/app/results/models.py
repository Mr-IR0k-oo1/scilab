from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ResultStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    PARTIAL = "PARTIAL"


class ArtifactType(str, Enum):
    TEXT = "TEXT"
    TABLE = "TABLE"
    IMAGE = "IMAGE"
    DATASET = "DATASET"
    VISUALIZATION = "VISUALIZATION"
    FILE = "FILE"
    REPORT = "REPORT"


class ResultArtifactCreate(BaseModel):
    type: ArtifactType
    name: str
    path: str
    mime_type: Optional[str] = "text/plain"
    size: Optional[int] = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    hash: Optional[str] = None


class ResultArtifactResponse(BaseModel):
    id: str
    result_id: str
    type: ArtifactType
    name: str
    path: str
    mime_type: str
    size: int
    created_at: datetime
    metadata: Dict[str, Any] = Field(default_factory=dict)
    hash: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ExperimentResultCreate(BaseModel):
    execution_id: str
    summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExperimentResultResponse(BaseModel):
    id: str
    project_id: str
    experiment_id: str
    execution_id: str
    status: ResultStatus
    summary: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    artifact_count: int = 0
    schema_version: int = 1
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ResultSummaryResponse(BaseModel):
    status: ResultStatus
    execution_time_ms: float
    dataset: Optional[Dict[str, Any]] = None
    visualizations: int = 0
    artifacts: int = 0
