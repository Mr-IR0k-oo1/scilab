import os
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import ExecutionRecordModel, ExperimentModel, ProjectModel
from app.services.scilab_service import ScilabService


class ExperimentService:
    @staticmethod
    def create_experiment(
        db: Session,
        project: ProjectModel,
        name: str,
        description: Optional[str] = None,
        script_path: str = "scripts/main.sce",
    ) -> ExperimentModel:
        # Validate script extension and existence inside project
        clean_rel = script_path.replace("\\", "/")
        ext = os.path.splitext(clean_rel)[1].lower()
        if ext not in [".sce", ".sci"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_SCRIPT_EXTENSION", "message": f"Script extension '{ext}' is not supported. Allowed: .sce, .sci"},
            )

        experiment = ExperimentModel(
            project_id=project.id,
            name=name,
            description=description,
            script_path=clean_rel,
            status="CREATED",
        )
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        return experiment

    @staticmethod
    def list_experiments(db: Session, project_id: str) -> List[ExperimentModel]:
        return db.query(ExperimentModel).filter(ExperimentModel.project_id == project_id).all()

    @staticmethod
    def get_experiment(db: Session, experiment_id: str) -> Optional[ExperimentModel]:
        return db.query(ExperimentModel).filter(ExperimentModel.id == experiment_id).first()

    @staticmethod
    async def run_experiment(db: Session, experiment: ExperimentModel, project: ProjectModel) -> ExecutionRecordModel:
        abs_script = os.path.join(project.path, experiment.script_path)

        if not os.path.exists(abs_script):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "SCRIPT_NOT_FOUND", "message": f"Experiment script '{experiment.script_path}' was not found"},
            )

        # Update experiment status to EXECUTING
        experiment.status = "RUNNING"
        db.commit()

        # Execute script via Phase 2 Scilab Runtime Service
        res = await ScilabService.execute_script(
            path=abs_script,
            allowed_base_dirs=[project.path],
        )

        # Persist ExecutionRecord
        record = ExecutionRecordModel(
            project_id=project.id,
            experiment_id=experiment.id,
            script_path=experiment.script_path,
            execution_id=res.id,
            status=res.status.value if hasattr(res.status, "value") else str(res.status),
            started_at=res.started_at,
            finished_at=res.finished_at,
            duration_ms=res.duration_ms,
            exit_code=res.exit_code,
            stdout=res.stdout,
            stderr=res.stderr,
        )
        db.add(record)

        # Update experiment last_execution_id and status
        experiment.last_execution_id = res.id
        experiment.status = "COMPLETED" if res.success else "FAILED"
        db.commit()
        db.refresh(record)

        return record

    @staticmethod
    def list_executions(db: Session, project_id: str) -> List[ExecutionRecordModel]:
        return db.query(ExecutionRecordModel).filter(ExecutionRecordModel.project_id == project_id).order_by(ExecutionRecordModel.created_at.desc()).all()

    @staticmethod
    def create_execution_record(
        db: Session,
        project_id: str,
        experiment_id: str,
        script_path: str = "scripts/main.sce",
        status: str = "COMPLETED",
        stdout: str = "",
        stderr: str = "",
    ) -> ExecutionRecordModel:
        import uuid
        exec_id = str(uuid.uuid4())
        record = ExecutionRecordModel(
            project_id=project_id,
            experiment_id=experiment_id,
            script_path=script_path,
            execution_id=exec_id,
            status=status,
            duration_ms=150.0,
            exit_code=0 if status == "COMPLETED" else 1,
            stdout=stdout,
            stderr=stderr,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_execution(db: Session, execution_id: str) -> Optional[ExecutionRecordModel]:
        return db.query(ExecutionRecordModel).filter(
            (ExecutionRecordModel.id == execution_id) | (ExecutionRecordModel.execution_id == execution_id)
        ).first()
