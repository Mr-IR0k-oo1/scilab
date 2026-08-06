"""
Pydantic v2 schemas for Scilab Runtime endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class RuntimeStatusResponse(BaseModel):
    """Response DTO for GET /runtime/status."""
    installed: bool = Field(description="Is Scilab executable detected on system")
    running: bool = Field(description="Is Scilab runtime process currently active")
    pid: Optional[int] = Field(default=None, description="Scilab process ID if running")
    scilab_version: Optional[str] = Field(default=None, description="Detected Scilab version string")
    executable_path: Optional[str] = Field(default=None, description="Path to Scilab executable binary")


class CommandExecuteRequest(BaseModel):
    """Request DTO for POST /runtime/execute."""
    command: str = Field(description="Scilab command string to execute")
    timeout_seconds: Optional[float] = Field(default=30.0, description="Execution timeout in seconds")


class ScriptExecuteRequest(BaseModel):
    """Request DTO for POST /runtime/execute-file."""
    file_path: str = Field(description="Absolute path to .sce or .sci script file")
    timeout_seconds: Optional[float] = Field(default=60.0, description="Execution timeout in seconds")


class ExecutionResultResponse(BaseModel):
    """Response DTO for execution endpoints."""
    id: str
    command_or_file: str
    status: str
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: float = 0.0
    created_at: str


class RuntimeControlResponse(BaseModel):
    """Generic response DTO for control endpoints (start, stop, restart, cancel)."""
    success: bool
    message: str
