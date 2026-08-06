"""
Execution Result models.

Defines immutable ExecutionResult model and SQLAlchemy ExecutionRecord table.
"""

from dataclasses import dataclass, field
import datetime
from typing import Optional
from sqlalchemy import Column, Float, Integer, String, Text, DateTime
from .database import Base


@dataclass(frozen=True)
class ExecutionResult:
    """
    Immutable Execution Result value object.
    """
    id: str
    command_or_file: str
    status: str  # 'completed', 'failed', 'cancelled', 'timeout'
    exit_code: Optional[int]
    stdout: str
    stderr: str
    execution_time_ms: float
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class ExecutionRecord(Base):
    """SQLAlchemy persistent DB model for execution history."""
    __tablename__ = "execution_records"

    id = Column(String(64), primary_key=True, index=True)
    command_or_file = Column(Text, nullable=False)
    status = Column(String(32), nullable=False)
    exit_code = Column(Integer, nullable=True)
    stdout = Column(Text, default="")
    stderr = Column(Text, default="")
    execution_time_ms = Column(Float, default=0.0)
    created_at = Column(String(64), nullable=False)
