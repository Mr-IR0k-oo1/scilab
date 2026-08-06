"""
Project workspace database model.
"""

from sqlalchemy import Column, String, Text
from .database import Base


class ProjectRecord(Base):
    """SQLAlchemy persistent DB model for project metadata."""
    __tablename__ = "projects"

    id = Column(String(64), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    path = Column(Text, nullable=False, unique=True)
    author = Column(String(255), default="")
    description = Column(Text, default="")
    created_at = Column(String(64), nullable=False)
    updated_at = Column(String(64), nullable=False)
