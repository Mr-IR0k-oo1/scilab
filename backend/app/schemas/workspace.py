from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    path: str = Field(..., min_length=1, max_length=1024)


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceResponse(WorkspaceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkspaceListResponse(BaseModel):
    workspaces: List[WorkspaceResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)
