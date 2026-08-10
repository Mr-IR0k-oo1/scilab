from typing import Optional
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    app_name: str
    environment: str

    model_config = ConfigDict(from_attributes=True)


class SystemInfoResponse(BaseModel):
    app_name: str
    version: str = "0.1.0"
    python_version: str
    platform: str
    database_status: str = "connected"

    model_config = ConfigDict(from_attributes=True)
