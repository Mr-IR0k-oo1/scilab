import os
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.project_repository import ProjectRepository
from app.repositories.result_repository import ResultRepository
from app.results.models import (
    ExperimentResultCreate,
    ExperimentResultResponse,
    ResultArtifactCreate,
    ResultArtifactResponse,
    ResultStatus,
    ResultSummaryResponse,
)
from app.services.experiment_service import ExperimentService


class ResultService:
    @staticmethod
    def create_result(
        db: Session,
        project_id: str,
        experiment_id: str,
        req: ExperimentResultCreate,
    ) -> ExperimentResultResponse:
        project = ProjectRepository.get_project_by_id_or_name(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        experiment = ExperimentService.get_experiment(db, experiment_id)
        if not experiment or experiment.project_id != project.id:
            raise HTTPException(status_code=404, detail="Experiment not found")

        execution = ExperimentService.get_execution(db, req.execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution record not found")

        repo = ResultRepository(db)
        model = repo.create_result(
            project_id=project.id,
            experiment_id=experiment.id,
            execution_id=execution.execution_id,
            status=ResultStatus.SUCCESS if execution.status == "COMPLETED" else ResultStatus.FAILED,
            summary=req.summary or f"Execution of {experiment.name} finished with status {execution.status}",
            metadata=req.metadata,
        )
        return ResultRepository.to_result_response(model)

    @staticmethod
    def list_results(db: Session, project_id: str) -> List[ExperimentResultResponse]:
        repo = ResultRepository(db)
        models = repo.get_results_by_project(project_id)
        return [ResultRepository.to_result_response(m) for m in models]

    @staticmethod
    def get_result(db: Session, project_id: str, result_id: str) -> ExperimentResultResponse:
        repo = ResultRepository(db)
        model = repo.get_result_by_id(result_id)
        if not model or model.project_id != project_id:
            raise HTTPException(status_code=404, detail="Result not found")
        return ResultRepository.to_result_response(model)

    @staticmethod
    def add_artifact(db: Session, project_id: str, result_id: str, req: ResultArtifactCreate) -> ResultArtifactResponse:
        ResultService.get_result(db, project_id, result_id)
        repo = ResultRepository(db)
        model = repo.add_artifact(result_id, req)
        return ResultRepository.to_artifact_response(model)

    @staticmethod
    def list_artifacts(db: Session, project_id: str, result_id: str) -> List[ResultArtifactResponse]:
        ResultService.get_result(db, project_id, result_id)
        repo = ResultRepository(db)
        models = repo.get_artifacts(result_id)
        return [ResultRepository.to_artifact_response(m) for m in models]

    @staticmethod
    def delete_artifact(db: Session, project_id: str, result_id: str, artifact_id: str) -> None:
        ResultService.get_result(db, project_id, result_id)
        repo = ResultRepository(db)
        success = repo.delete_artifact(result_id, artifact_id)
        if not success:
            raise HTTPException(status_code=404, detail="Artifact not found")

    @staticmethod
    def get_result_summary(db: Session, project_id: str, result_id: str) -> ResultSummaryResponse:
        res = ResultService.get_result(db, project_id, result_id)
        execution = ExperimentService.get_execution(db, res.execution_id)
        artifacts = ResultService.list_artifacts(db, project_id, result_id)

        from app.repositories.visualization_repository import VisualizationRepository
        v_repo = VisualizationRepository(db)
        viz_count = len(v_repo.get_by_project(project_id))

        return ResultSummaryResponse(
            status=res.status,
            execution_time_ms=execution.duration_ms if execution else 0.0,
            dataset=None,
            visualizations=viz_count,
            artifacts=len(artifacts),
        )
