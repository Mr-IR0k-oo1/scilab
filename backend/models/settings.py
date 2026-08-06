"""
Settings database model.
"""

from sqlalchemy import Column, String, Text
from .database import Base


class SettingsRecord(Base):
    """SQLAlchemy persistent DB model for key-value configuration settings."""
    __tablename__ = "settings"

    key = Column(String(255), primary_key=True, index=True)
    value = Column(Text, nullable=False)
