from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class ProjectManifest(BaseModel):
    schema_version: int = Field(1, description="Version of project.json schema specification")
    id: str = Field(..., description="Unique Project ID")
    name: str = Field(..., description="Name of the engineering project")
    description: Optional[str] = Field(None, description="Optional description of project")
    version: str = Field("0.1.0", description="Semantic version of project software")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
