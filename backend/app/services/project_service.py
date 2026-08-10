import csv
import json
import mimetypes
import os
import shutil
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.models import DatasetMetadataModel, ProjectModel
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_manifest import ProjectManifest


class ProjectService:
    @staticmethod
    def _validate_safe_relative_path(project_path: str, relative_path: str) -> str:
        """
        Validates that relative_path is safely contained within project_path.
        Prevents path traversal (..), absolute path escape, and symlink escape.
        """
        if not relative_path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_PATH", "message": "Relative path cannot be empty"},
            )

        # Normalize relative path
        clean_rel = os.path.normpath(relative_path).lstrip("/\\")
        if clean_rel.startswith("..") or ".." in clean_rel.split("/") or ".." in clean_rel.split("\\"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "PATH_TRAVERSAL_DETECTED", "message": "Path traversal (..) is prohibited"},
            )

        abs_project = os.path.abspath(os.path.normpath(project_path))
        target_abs = os.path.abspath(os.path.join(abs_project, clean_rel))

        if not target_abs.startswith(abs_project):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "PATH_ESCAPE_DETECTED", "message": "Target path escapes project root directory"},
            )

        # Check real path for symlink escapes if file/folder exists
        if os.path.exists(target_abs):
            real_target = os.path.realpath(target_abs)
            real_project = os.path.realpath(abs_project)
            if not real_target.startswith(real_project):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"code": "SYMLINK_ESCAPE_DETECTED", "message": "Symlink escapes project root boundary"},
                )

        return target_abs

    @staticmethod
    def validate_project(project_path: str, expected_id: Optional[str] = None) -> ProjectManifest:
        """
        Validates project directory structure and project.json manifest.
        Raises HTTP 400 error if validation fails.
        """
        if not os.path.exists(project_path) or not os.path.isdir(project_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_PROJECT_DIRECTORY", "message": f"Project directory '{project_path}' does not exist"},
            )

        manifest_path = os.path.join(project_path, "project.json")
        if not os.path.exists(manifest_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "MISSING_MANIFEST", "message": "project.json manifest file is missing from project root"},
            )

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            manifest = ProjectManifest.model_validate(data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_MANIFEST_SCHEMA", "message": f"Failed to parse project.json manifest: {str(e)}"},
            )

        if manifest.schema_version != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "UNSUPPORTED_SCHEMA_VERSION", "message": f"Unsupported schema_version '{manifest.schema_version}' in manifest"},
            )

        if expected_id and manifest.id != expected_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "PROJECT_ID_MISMATCH", "message": f"Manifest project ID '{manifest.id}' does not match expected ID '{expected_id}'"},
            )

        return manifest

    @staticmethod
    def create_project(db: Session, name: str, description: Optional[str] = None, workspace_id: Optional[str] = None) -> ProjectModel:
        # Create Project record in DB first
        project = ProjectRepository.create_project(db, name, description, workspace_id)

        # Ensure project directory exists
        os.makedirs(project.path, exist_ok=True)

        # Create subdirectories when needed
        for sub_dir in ["scripts", "datasets", "assets", "experiments", "outputs", "reports"]:
            os.makedirs(os.path.join(project.path, sub_dir), exist_ok=True)

        # Generate default main.sce script
        main_script_path = os.path.join(project.path, "scripts", "main.sce")
        if not os.path.exists(main_script_path):
            with open(main_script_path, "w", encoding="utf-8") as f:
                f.write("// Main Scilab Script\ndisp('Hello from Scilab Studio Project!');\n")

        # Create portable project.json manifest
        manifest = ProjectManifest(
            schema_version=1,
            id=project.id,
            name=project.name,
            description=project.description,
            version="0.1.0",
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )

        manifest_path = os.path.join(project.path, "project.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest.model_dump_json(indent=2))

        return project

    @staticmethod
    def get_project_tree(project_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(project_path):
            return []

        def _scan_dir(current_abs: str, base_abs: str) -> List[Dict[str, Any]]:
            items = []
            try:
                entries = sorted(os.listdir(current_abs))
            except PermissionError:
                return []

            for entry in entries:
                if entry.startswith("."):
                    continue
                abs_entry = os.path.join(current_abs, entry)
                rel_path = os.path.relpath(abs_entry, base_abs).replace("\\", "/")
                is_dir = os.path.isdir(abs_entry)
                stat = os.stat(abs_entry)

                items.append({
                    "name": entry,
                    "path": rel_path,
                    "is_dir": is_dir,
                    "size": stat.st_size if not is_dir else 0,
                    "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "children": _scan_dir(abs_entry, base_abs) if is_dir else None,
                })
            return items

        return _scan_dir(project_path, project_path)

    @staticmethod
    def create_project_file(project_path: str, relative_path: str, content: str = "") -> Dict[str, Any]:
        target_abs = ProjectService._validate_safe_relative_path(project_path, relative_path)
        os.makedirs(os.path.dirname(target_abs), exist_ok=True)
        with open(target_abs, "w", encoding="utf-8") as f:
            f.write(content)

        rel = os.path.relpath(target_abs, project_path).replace("\\", "/")
        return {"path": rel, "size": len(content.encode("utf-8"))}

    @staticmethod
    def read_project_file(project_path: str, relative_path: str) -> str:
        target_abs = ProjectService._validate_safe_relative_path(project_path, relative_path)
        if not os.path.exists(target_abs) or not os.path.isfile(target_abs):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "FILE_NOT_FOUND", "message": f"File '{relative_path}' was not found in project"},
            )
        with open(target_abs, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def update_project_file(project_path: str, relative_path: str, content: str) -> Dict[str, Any]:
        target_abs = ProjectService._validate_safe_relative_path(project_path, relative_path)
        with open(target_abs, "w", encoding="utf-8") as f:
            f.write(content)
        rel = os.path.relpath(target_abs, project_path).replace("\\", "/")
        return {"path": rel, "size": len(content.encode("utf-8"))}

    @staticmethod
    def delete_project_file(project_path: str, relative_path: str) -> None:
        target_abs = ProjectService._validate_safe_relative_path(project_path, relative_path)
        if not os.path.exists(target_abs):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "FILE_NOT_FOUND", "message": f"Target path '{relative_path}' does not exist"},
            )
        if os.path.isdir(target_abs):
            shutil.rmtree(target_abs)
        else:
            os.remove(target_abs)

    @staticmethod
    async def upload_dataset(db: Session, project: ProjectModel, file: UploadFile) -> DatasetMetadataModel:
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filename cannot be empty")

        clean_filename = os.path.basename(file.filename)
        ext = os.path.splitext(clean_filename)[1].lower()
        if ext not in [".csv", ".json", ".txt"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_DATASET_EXTENSION", "message": f"Dataset extension '{ext}' not supported. Allowed: .csv, .json, .txt"},
            )

        datasets_dir = os.path.join(project.path, "datasets")
        os.makedirs(datasets_dir, exist_ok=True)

        target_abs = ProjectService._validate_safe_relative_path(project.path, os.path.join("datasets", clean_filename))

        # Stream save file
        size_bytes = 0
        with open(target_abs, "wb") as buffer:
            while chunk := await file.read(8192):
                size_bytes += len(chunk)
                buffer.write(chunk)

        # Fast line & column count for CSV without loading whole file into memory
        row_count = None
        column_count = None
        mime_type = mimetypes.guess_type(target_abs)[0] or "text/plain"

        if ext == ".csv":
            mime_type = "text/csv"
            try:
                with open(target_abs, "r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.reader(f)
                    first_row = next(reader, None)
                    if first_row is not None:
                        column_count = len(first_row)
                        row_count = 1 + sum(1 for _ in reader)
            except Exception:
                pass

        rel_path = os.path.relpath(target_abs, project.path).replace("\\", "/")

        dataset_meta = DatasetMetadataModel(
            project_id=project.id,
            filename=clean_filename,
            path=rel_path,
            size_bytes=size_bytes,
            mime_type=mime_type,
            row_count=row_count,
            column_count=column_count,
        )
        db.add(dataset_meta)
        db.commit()
        db.refresh(dataset_meta)
        return dataset_meta
