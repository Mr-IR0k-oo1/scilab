"""
Project module for Scilab Studio workspace system.

Defines ProjectMetaData DTO and Project object encapsulating the '.scstudio'
project standard structure on disk.

Standard Project Layout:
------------------------
MyProject/
  ├── project.scstudio   (JSON metadata file)
  ├── assets/            (Graphic assets, images, icons)
  ├── scripts/           (Scilab .sce / .sci scripts)
  ├── datasets/          (CSV, MAT, HDF5, SQLite datasets)
  ├── reports/           (Generated PDF / HTML / Markdown reports)
  ├── layouts/           (Saved UI dock & GUI Builder layout JSONs)
  └── docs/              (Project documentation & notes)
"""

from dataclasses import asdict, dataclass, field
import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

REQUIRED_SUBDIRECTORIES: List[str] = [
    "assets",
    "scripts",
    "datasets",
    "reports",
    "layouts",
    "docs",
]
PROJECT_MANIFEST_NAME = "project.scstudio"


@dataclass
class ProjectMetaData:
    """Project metadata structure serialized into project.scstudio."""
    name: str
    version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    author: str = ""
    description: str = ""
    scilab_version: str = "7.0.0"
    settings: Dict[str, Any] = field(default_factory=dict)


class Project:
    """
    Represents an active Scilab Studio engineering project.
    """

    def __init__(self, root_path: Path, metadata: ProjectMetaData) -> None:
        self.root_path = root_path.resolve()
        self.metadata = metadata

    @property
    def manifest_path(self) -> Path:
        """Path to the project.scstudio manifest file."""
        return self.root_path / PROJECT_MANIFEST_NAME

    @classmethod
    def create(cls, name: str, parent_dir: Path, author: str = "", description: str = "") -> "Project":
        """
        Create a new Scilab Studio project on disk with standard folder structure.
        
        Args:
            name: Project name.
            parent_dir: Directory where project folder will be instantiated.
            author: Optional author name.
            description: Optional project description.
            
        Returns:
            Newly created Project instance.
        """
        project_dir = parent_dir / name
        if project_dir.exists() and any(project_dir.iterdir()):
            raise FileExistsError(f"Directory is not empty: {project_dir}")

        project_dir.mkdir(parents=True, exist_ok=True)
        for sub in REQUIRED_SUBDIRECTORIES:
            (project_dir / sub).mkdir(parents=True, exist_ok=True)

        meta = ProjectMetaData(
            name=name,
            author=author,
            description=description,
        )

        project = cls(root_path=project_dir, metadata=meta)
        project.save()
        logger.info("Created project '%s' at %s", name, project_dir)
        return project

    @classmethod
    def load(cls, path: Path) -> "Project":
        """
        Load an existing project from a directory or .scstudio manifest file path.
        
        Args:
            path: Path to directory or project.scstudio file.
            
        Returns:
            Loaded Project instance.
        """
        path = path.resolve()
        if path.is_file():
            if path.name != PROJECT_MANIFEST_NAME and not path.name.endswith(".scstudio"):
                raise ValueError(f"Invalid project file: {path}")
            project_dir = path.parent
            manifest_file = path
        else:
            project_dir = path
            manifest_file = project_dir / PROJECT_MANIFEST_NAME

        if not manifest_file.exists():
            raise FileNotFoundError(f"Project manifest missing: {manifest_file}")

        with open(manifest_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        meta = ProjectMetaData(
            name=data.get("name", project_dir.name),
            version=data.get("version", "1.0.0"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            author=data.get("author", ""),
            description=data.get("description", ""),
            scilab_version=data.get("scilab_version", "7.0.0"),
            settings=data.get("settings", {}),
        )

        # Ensure required subdirectories exist
        for sub in REQUIRED_SUBDIRECTORIES:
            (project_dir / sub).mkdir(parents=True, exist_ok=True)

        logger.info("Loaded project '%s' from %s", meta.name, project_dir)
        return cls(root_path=project_dir, metadata=meta)

    def save(self) -> None:
        """Persist metadata updates to project.scstudio."""
        self.metadata.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        data = asdict(self.metadata)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.debug("Saved project manifest for '%s'", self.metadata.name)
