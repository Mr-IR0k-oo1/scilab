import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import VisualizationModel
from app.visualization.models import ChartType, TransformationPipeline, VisualizationOptions, VisualizationSpec


class VisualizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, spec: VisualizationSpec, dataset_hash: Optional[str] = None) -> VisualizationModel:
        model = VisualizationModel(
            project_id=spec.project_id,
            dataset_id=spec.dataset_id,
            experiment_id=spec.experiment_id,
            name=spec.name,
            type=spec.type.value if hasattr(spec.type, "value") else str(spec.type),
            x_column=spec.x_column,
            y_columns=json.dumps(spec.y_columns),
            group_column=spec.group_column,
            transformations=spec.transformations.model_dump_json(),
            options=spec.options.model_dump_json(),
            schema_version=spec.schema_version,
            dataset_hash=dataset_hash,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_id(self, visualization_id: str) -> Optional[VisualizationModel]:
        return self.db.query(VisualizationModel).filter(VisualizationModel.id == visualization_id).first()

    def get_by_project(self, project_id: str) -> List[VisualizationModel]:
        return self.db.query(VisualizationModel).filter(VisualizationModel.project_id == project_id).all()

    def update(self, visualization_id: str, spec: VisualizationSpec, dataset_hash: Optional[str] = None) -> Optional[VisualizationModel]:
        model = self.get_by_id(visualization_id)
        if not model:
            return None

        model.name = spec.name
        model.type = spec.type.value if hasattr(spec.type, "value") else str(spec.type)
        model.x_column = spec.x_column
        model.y_columns = json.dumps(spec.y_columns)
        model.group_column = spec.group_column
        model.transformations = spec.transformations.model_dump_json()
        model.options = spec.options.model_dump_json()
        if dataset_hash:
            model.dataset_hash = dataset_hash

        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, visualization_id: str) -> bool:
        model = self.get_by_id(visualization_id)
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True

    @staticmethod
    def to_spec(model: VisualizationModel) -> VisualizationSpec:
        y_cols = json.loads(model.y_columns) if model.y_columns else []
        trans_dict = json.loads(model.transformations) if model.transformations else {}
        opts_dict = json.loads(model.options) if model.options else {}

        return VisualizationSpec(
            id=model.id,
            project_id=model.project_id,
            dataset_id=model.dataset_id,
            experiment_id=model.experiment_id,
            name=model.name,
            type=ChartType(model.type),
            x_column=model.x_column,
            y_columns=y_cols,
            group_column=model.group_column,
            transformations=TransformationPipeline.model_validate(trans_dict),
            options=VisualizationOptions.model_validate(opts_dict),
            schema_version=model.schema_version,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
