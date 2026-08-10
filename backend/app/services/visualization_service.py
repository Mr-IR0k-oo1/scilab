import os
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.data.models import TransformationPipeline
from app.db.models import VisualizationModel
from app.repositories.project_repository import ProjectRepository
from app.repositories.visualization_repository import VisualizationRepository
from app.services.dataset_service import DatasetService
from app.visualization.models import ChartDataResponse, VisualizationOptions, VisualizationSpec
from app.visualization.service import VisualizationDataService
from app.visualization.validators import VisualizationValidator


class VisualizationService:
    @staticmethod
    def create_visualization(db: Session, spec: VisualizationSpec) -> VisualizationModel:
        schema = DatasetService.inspect_dataset_schema(db, spec.project_id, spec.dataset_id)
        VisualizationValidator.validate_spec(spec, schema)

        repo = VisualizationRepository(db)
        return repo.create(spec, dataset_hash=schema.content_hash)

    @staticmethod
    def get_visualization(db: Session, project_id: str, visualization_id: str) -> VisualizationSpec:
        repo = VisualizationRepository(db)
        model = repo.get_by_id(visualization_id)
        if not model or model.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "VISUALIZATION_NOT_FOUND", "message": f"Visualization '{visualization_id}' not found"},
            )
        return repo.to_spec(model)

    @staticmethod
    def list_visualizations(db: Session, project_id: str) -> List[VisualizationSpec]:
        repo = VisualizationRepository(db)
        models = repo.get_by_project(project_id)
        return [repo.to_spec(m) for m in models]

    @staticmethod
    def update_visualization(db: Session, project_id: str, visualization_id: str, spec: VisualizationSpec) -> VisualizationSpec:
        schema = DatasetService.inspect_dataset_schema(db, project_id, spec.dataset_id)
        VisualizationValidator.validate_spec(spec, schema)

        repo = VisualizationRepository(db)
        model = repo.update(visualization_id, spec, dataset_hash=schema.content_hash)
        if not model:
            raise HTTPException(status_code=404, detail="Visualization not found")
        return repo.to_spec(model)

    @staticmethod
    def delete_visualization(db: Session, project_id: str, visualization_id: str) -> None:
        repo = VisualizationRepository(db)
        success = repo.delete(visualization_id)
        if not success:
            raise HTTPException(status_code=404, detail="Visualization not found")

    @staticmethod
    def generate_visualization_data(db: Session, project_id: str, visualization_id: str) -> ChartDataResponse:
        spec = VisualizationService.get_visualization(db, project_id, visualization_id)
        repo = VisualizationRepository(db)
        model = repo.get_by_id(visualization_id)
        stored_hash = model.dataset_hash if model else ""

        schema = DatasetService.inspect_dataset_schema(db, project_id, spec.dataset_id)
        dataset_rows = DatasetService.get_dataset_preview(db, project_id, spec.dataset_id, max_rows=10000)

        return VisualizationDataService.generate_chart_data(
            spec=spec,
            raw_rows=dataset_rows,
            current_hash=schema.content_hash,
            stored_hash=stored_hash,
        )
