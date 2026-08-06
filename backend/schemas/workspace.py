"""
Workspace, Projects, and Settings Pydantic v2 schemas.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str
    parent_dir: str
    author: Optional[str] = ""
    description: Optional[str] = ""


class ProjectResponse(BaseModel):
    id: str
    name: str
    path: str
    author: Optional[str] = ""
    description: Optional[str] = ""
    created_at: str
    updated_at: str


class WorkspaceStateResponse(BaseModel):
    active_project: Optional[ProjectResponse] = None
    opened_files: List[str] = Field(default_factory=list)
    recent_datasets: List[str] = Field(default_factory=list)
    dock_layout: Optional[str] = None


class SettingItem(BaseModel):
    key: str
    value: str


class SettingsUpdateRequest(BaseModel):
    settings: Dict[str, Any]
