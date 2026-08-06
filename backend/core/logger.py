"""
Structured Logging configuration module for Scilab Studio Backend.
"""

import logging
import sys

logger = logging.getLogger("scilab_studio_backend")

def setup_logging(level: int = logging.INFO) -> None:
    """Configure structured logging for the FastAPI application."""
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)

setup_logging()
