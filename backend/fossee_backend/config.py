import os
from pathlib import Path

def get_fossee_projects_dir() -> Path:
    env_dir = os.environ.get("FOSSEE_PROJECTS_DIR")
    if env_dir:
        return Path(env_dir)
    
    # Fallback to <Documents>/FOSSEE
    # This works on most OSes
    documents_dir = Path.home() / "Documents"
    return documents_dir / "FOSSEE"

FOSSEE_BACKEND_PORT = int(os.environ.get("FOSSEE_BACKEND_PORT", "8747"))

# Parse FOSSEE_CORS_ORIGINS comma separated list
_cors_origins = os.environ.get("FOSSEE_CORS_ORIGINS", "")
EXTRA_CORS_ORIGINS = [o.strip() for o in _cors_origins.split(",")] if _cors_origins else []
