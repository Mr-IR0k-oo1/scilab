from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.domain.enums.project_status import ProjectStatus


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    workspace_id: Optional[str] = None
    path: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


ProjectCreateRequest = ProjectCreate


class ProjectMetadataResponse(BaseModel):
    id: str
    key: str
    value: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    workspace_id: Optional[str] = None
    path: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    metadata_records: List[ProjectMetadataResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
