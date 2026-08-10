import json
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import ExperimentResultModel, ResultArtifactModel
from app.results.models import (
    ArtifactType,
    ExperimentResultResponse,
    ResultArtifactCreate,
    ResultArtifactResponse,
    ResultStatus,
)


class ResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_result(
        self,
        project_id: str,
        experiment_id: str,
        execution_id: str,
        status: ResultStatus = ResultStatus.SUCCESS,
        summary: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> ExperimentResultModel:
        model = ExperimentResultModel(
            project_id=project_id,
            experiment_id=experiment_id,
            execution_id=execution_id,
            status=status.value if hasattr(status, "value") else str(status),
            summary=summary,
            result_metadata=json.dumps(metadata or {}),
            artifact_count=0,
            schema_version=1,
            completed_at=datetime.now(timezone.utc),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_result_by_id(self, result_id: str) -> Optional[ExperimentResultModel]:
        return self.db.query(ExperimentResultModel).filter(ExperimentResultModel.id == result_id).first()

    def get_results_by_project(self, project_id: str) -> List[ExperimentResultModel]:
        return self.db.query(ExperimentResultModel).filter(ExperimentResultModel.project_id == project_id).all()

    def add_artifact(self, result_id: str, artifact: ResultArtifactCreate) -> ResultArtifactModel:
        result_model = self.get_result_by_id(result_id)
        model = ResultArtifactModel(
            result_id=result_id,
            type=artifact.type.value if hasattr(artifact.type, "value") else str(artifact.type),
            name=artifact.name,
            path=artifact.path,
            mime_type=artifact.mime_type or "text/plain",
            size=artifact.size or 0,
            artifact_metadata=json.dumps(artifact.metadata or {}),
            hash=artifact.hash,
        )
        self.db.add(model)
        if result_model:
            result_model.artifact_count += 1
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_artifacts(self, result_id: str) -> List[ResultArtifactModel]:
        return self.db.query(ResultArtifactModel).filter(ResultArtifactModel.result_id == result_id).all()

    def delete_artifact(self, result_id: str, artifact_id: str) -> bool:
        art = self.db.query(ResultArtifactModel).filter(ResultArtifactModel.id == artifact_id, ResultArtifactModel.result_id == result_id).first()
        if not art:
            return False
        res = self.get_result_by_id(result_id)
        if res and res.artifact_count > 0:
            res.artifact_count -= 1
        self.db.delete(art)
        self.db.commit()
        return True

    @staticmethod
    def to_result_response(model: ExperimentResultModel) -> ExperimentResultResponse:
        meta = json.loads(model.result_metadata) if model.result_metadata else {}
        return ExperimentResultResponse(
            id=model.id,
            project_id=model.project_id,
            experiment_id=model.experiment_id,
            execution_id=model.execution_id,
            status=ResultStatus(model.status),
            summary=model.summary,
            metadata=meta,
            artifact_count=model.artifact_count,
            schema_version=model.schema_version,
            created_at=model.created_at,
            completed_at=model.completed_at,
        )

    @staticmethod
    def to_artifact_response(model: ResultArtifactModel) -> ResultArtifactResponse:
        meta = json.loads(model.artifact_metadata) if model.artifact_metadata else {}
        return ResultArtifactResponse(
            id=model.id,
            result_id=model.result_id,
            type=ArtifactType(model.type),
            name=model.name,
            path=model.path,
            mime_type=model.mime_type,
            size=model.size,
            created_at=model.created_at,
            metadata=meta,
            hash=model.hash,
        )
