"""
Backend Configuration module for Scilab Studio.

Defines Settings DTO utilizing Pydantic BaseSettings / BaseModel to store
server host, port, database URL, Scilab CLI executable path, and execution timeouts.
"""

from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application Settings Schema."""
    app_name: str = "Scilab Studio Runtime Service"
    version: str = "0.1.0"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    
    # SQLite Database Configuration
    database_url: str = "sqlite:///./scilab_studio.db"
    
    # Scilab CLI Process Configuration
    scilab_executable: str = "scilab-cli"
    custom_scilab_path: Optional[str] = None
    execution_timeout_seconds: float = 60.0
    
    # CORS Origins for React Frontend
    cors_origins: list[str] = Field(default_factory=lambda: [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"
    ])


settings = Settings()
