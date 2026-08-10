from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DatasetMetadataResponse(BaseModel):
    id: str
    project_id: str
    filename: str
    path: str
    size_bytes: int
    mime_type: str
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
