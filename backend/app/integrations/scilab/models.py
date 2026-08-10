from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class SessionState(str, Enum):
    CREATED = "CREATED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    EXECUTING = "EXECUTING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"


@dataclass
class ScilabStatusInfo:
    installed: bool
    executable: Optional[str] = None
    version: Optional[str] = None
    status: str = "unavailable"


@dataclass
class ExecutionResult:
    id: str
    command: str
    success: bool
    stdout: str = ""
    stderr: str = ""
    exit_code: Optional[int] = 0
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_ms: float = 0.0
    status: ExecutionStatus = ExecutionStatus.COMPLETED
    truncated: bool = False
