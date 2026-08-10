from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.project_repository import ProjectRepository
from app.services.experiment_service import ExperimentService


class ReportValidator:
    @staticmethod
    def validate_report_inputs(db: Session, project_id: str, experiment_id: str, execution_id: str) -> Dict[str, Any]:
        project = ProjectRepository.get_project_by_id_or_name(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "PROJECT_NOT_FOUND", "message": f"Project '{project_id}' not found"},
            )

        experiment = ExperimentService.get_experiment(db, experiment_id)
        if not experiment or experiment.project_id != project.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "EXPERIMENT_NOT_FOUND", "message": f"Experiment '{experiment_id}' not found"},
            )

        execution = ExperimentService.get_execution(db, execution_id)
        if not execution or execution.project_id != project.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "EXECUTION_NOT_FOUND", "message": f"Execution record '{execution_id}' not found"},
            )

        return {
            "project": project,
            "experiment": experiment,
            "execution": execution,
        }
