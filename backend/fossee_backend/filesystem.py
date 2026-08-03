import os
import shutil
import json
import time
from pathlib import Path
from typing import List, Optional

from .config import get_fossee_projects_dir
from .models import FileInfo, ProjectMetadata

class FileSystemManager:
    def read_text_file(self, path: str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_text_file(self, path: str, content: str):
        # Ensure parent exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def list_directory(self, path: str) -> List[FileInfo]:
        items = []
        p = Path(path)
        if not p.exists() or not p.is_dir():
            raise FileNotFoundError(f"Directory not found: {path}")
            
        for child in p.iterdir():
            stat = child.stat()
            items.append(FileInfo(
                name=child.name,
                is_dir=child.is_dir(),
                path=str(child.absolute()),
                size=stat.st_size if child.is_file() else None,
                last_modified=stat.st_mtime
            ))
        return items

    def create_directory(self, path: str):
        Path(path).mkdir(parents=True, exist_ok=True)

    def remove_file(self, path: str):
        p = Path(path)
        if p.exists() and p.is_file():
            p.unlink()
        else:
            raise FileNotFoundError(f"File not found: {path}")

    def remove_directory(self, path: str):
        p = Path(path)
        if p.exists() and p.is_dir():
            shutil.rmtree(str(p))
        else:
            raise FileNotFoundError(f"Directory not found: {path}")

    def file_exists(self, path: str) -> bool:
        return Path(path).exists()

    def path_info(self, path: str) -> FileInfo:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Path not found: {path}")
        stat = p.stat()
        return FileInfo(
            name=p.name,
            is_dir=p.is_dir(),
            path=str(p.absolute()),
            size=stat.st_size if p.is_file() else None,
            last_modified=stat.st_mtime
        )

    def rename_path(self, old_path: str, new_path: str):
        Path(old_path).rename(new_path)

class ProjectManager:
    def __init__(self):
        self.projects_dir = get_fossee_projects_dir()

    def get_project_dir(self) -> str:
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        return str(self.projects_dir.absolute())

    def list_projects(self) -> List[ProjectMetadata]:
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        projects = []
        for child in self.projects_dir.iterdir():
            if child.is_dir():
                meta_path = child / "project.json"
                if meta_path.exists():
                    try:
                        with open(meta_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            projects.append(ProjectMetadata(**data))
                    except Exception:
                        projects.append(ProjectMetadata(name=child.name))
                else:
                    projects.append(ProjectMetadata(name=child.name))
        return projects

    def create_project(self, name: str, description: Optional[str] = None) -> ProjectMetadata:
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        proj_dir = self.projects_dir / name
        if proj_dir.exists():
            raise FileExistsError(f"Project '{name}' already exists")
            
        proj_dir.mkdir(parents=True)
        
        now = time.time()
        meta = ProjectMetadata(
            name=name,
            description=description,
            created_at=now,
            updated_at=now
        )
        
        with open(proj_dir / "project.json", 'w', encoding='utf-8') as f:
            f.write(meta.json())
            
        return meta

    def update_project_metadata(self, name: str, metadata: ProjectMetadata) -> ProjectMetadata:
        proj_dir = self.projects_dir / name
        if not proj_dir.exists():
            raise FileNotFoundError(f"Project '{name}' not found")
            
        metadata.updated_at = time.time()
        with open(proj_dir / "project.json", 'w', encoding='utf-8') as f:
            f.write(metadata.json())
            
        return metadata

    def delete_project(self, name: str):
        proj_dir = self.projects_dir / name
        if not proj_dir.exists():
            raise FileNotFoundError(f"Project '{name}' not found")
        shutil.rmtree(str(proj_dir))

fs_manager = FileSystemManager()
project_manager = ProjectManager()
