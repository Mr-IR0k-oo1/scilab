import os
from dataclasses import dataclass, field
from typing import Optional
from app.core.config import settings


@dataclass
class ScilabConfig:
    executable: Optional[str] = field(default_factory=lambda: os.getenv("SCILAB_EXECUTABLE"))
    timeout_seconds: float = field(default_factory=lambda: float(os.getenv("SCILAB_TIMEOUT", "30.0")))
    working_directory: str = field(default_factory=lambda: os.getenv("SCILAB_WORKING_DIRECTORY", os.getcwd()))
    max_output_size: int = field(default_factory=lambda: int(os.getenv("SCILAB_MAX_OUTPUT_SIZE", str(1024 * 1024))))


scilab_config = ScilabConfig()
