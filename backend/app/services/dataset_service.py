import os
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.data.loaders.csv_loader import CSVDataLoader
from app.data.loaders.json_loader import JSONDataLoader
from app.data.models import DatasetSchema, DatasetValidationResult
from app.data.validators.validator import DatasetValidator
from app.db.models import DatasetMetadataModel, ProjectModel
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.project_repository import ProjectRepository


class DatasetService:
    @staticmethod
    def get_loader(file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".json":
            return JSONDataLoader()
        return CSVDataLoader()

    @staticmethod
    def get_dataset(db: Session, project_id: str, dataset_id: str) -> DatasetMetadataModel:
        repo = DatasetRepository(db)
        dataset = repo.get_by_id(dataset_id)
        if not dataset or dataset.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "DATASET_NOT_FOUND", "message": f"Dataset '{dataset_id}' not found in project '{project_id}'"},
            )
        return dataset

    @staticmethod
    def inspect_dataset_schema(db: Session, project_id: str, dataset_id: str) -> DatasetSchema:
        dataset = DatasetService.get_dataset(db, project_id, dataset_id)
        project = ProjectRepository.get_project_by_id_or_name(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        abs_path = os.path.join(project.path, dataset.path)
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="Dataset file missing from project storage")

        loader = DatasetService.get_loader(abs_path)
        schema = loader.inspect_schema(abs_path)

        # Update stored content hash if missing
        if not dataset.content_hash and schema.content_hash:
            dataset.content_hash = schema.content_hash
            db.commit()

        return schema

    @staticmethod
    def get_dataset_preview(db: Session, project_id: str, dataset_id: str, max_rows: int = 100) -> List[Dict[str, Any]]:
        dataset = DatasetService.get_dataset(db, project_id, dataset_id)
        project = ProjectRepository.get_project_by_id_or_name(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        abs_path = os.path.join(project.path, dataset.path)
        loader = DatasetService.get_loader(abs_path)
        return loader.load_rows(abs_path, max_rows=max_rows)

    @staticmethod
    def get_dataset_statistics(db: Session, project_id: str, dataset_id: str) -> DatasetValidationResult:
        schema = DatasetService.inspect_dataset_schema(db, project_id, dataset_id)
        return DatasetValidator.validate(schema)
