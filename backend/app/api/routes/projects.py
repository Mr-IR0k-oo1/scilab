from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.project_repository import ProjectRepository
from app.schemas.dataset import DatasetMetadataResponse
from app.schemas.experiment import ExecutionRecordResponse, ExperimentCreate, ExperimentResponse
from app.schemas.project import ProjectCreateRequest, ProjectListResponse, ProjectResponse
from app.services.experiment_service import ExperimentService
from app.services.project_service import ProjectService

router = APIRouter()


class FileCreateUpdateRequest(BaseModel):
    content: str = ""


@router.get("/projects", response_model=ProjectListResponse)
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = ProjectRepository.get_projects(db, skip=skip, limit=limit)
    total = ProjectRepository.count_projects(db)
    return ProjectListResponse(projects=[ProjectResponse.model_validate(p) for p in projects], total=total)


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(req: ProjectCreateRequest, db: Session = Depends(get_db)):
    project = ProjectService.create_project(db, name=req.name, description=req.description, workspace_id=req.workspace_id)
    return ProjectResponse.model_validate(project)


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "PROJECT_NOT_FOUND", "message": f"Project '{project_id}' not found"},
        )
    return ProjectResponse.model_validate(project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    success = ProjectRepository.delete_project(db, project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "PROJECT_NOT_FOUND", "message": f"Project '{project_id}' not found"},
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Phase 3: Project Tree & File System Endpoints
@router.get("/projects/{project_id}/tree")
def get_project_tree(project_id: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"tree": ProjectService.get_project_tree(project.path)}


@router.post("/projects/{project_id}/files")
def create_project_file(project_id: str, relative_path: str, req: FileCreateUpdateRequest, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectService.create_project_file(project.path, relative_path, req.content)


@router.get("/projects/{project_id}/files/{path:path}")
def read_project_file(project_id: str, path: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    content = ProjectService.read_project_file(project.path, path)
    return {"path": path, "content": content}


@router.put("/projects/{project_id}/files/{path:path}")
def update_project_file(project_id: str, path: str, req: FileCreateUpdateRequest, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectService.update_project_file(project.path, path, req.content)


@router.delete("/projects/{project_id}/files/{path:path}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_file(project_id: str, path: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    ProjectService.delete_project_file(project.path, path)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Phase 3: Datasets Endpoints
@router.post("/projects/{project_id}/datasets", response_model=DatasetMetadataResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(project_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    dataset = await ProjectService.upload_dataset(db, project, file)
    return DatasetMetadataResponse.model_validate(dataset)


@router.get("/projects/{project_id}/datasets", response_model=List[DatasetMetadataResponse])
def list_datasets(project_id: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return [DatasetMetadataResponse.model_validate(d) for d in project.datasets]


@router.delete("/projects/{project_id}/datasets/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dataset(project_id: str, dataset_id: str, db: Session = Depends(get_db)):
    from app.db.models import DatasetMetadataModel
    dataset = db.query(DatasetMetadataModel).filter(DatasetMetadataModel.id == dataset_id, DatasetMetadataModel.project_id == project_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    db.delete(dataset)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Phase 3: Experiments & Executions Endpoints
@router.post("/projects/{project_id}/experiments", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
def create_experiment(project_id: str, req: ExperimentCreate, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    exp = ExperimentService.create_experiment(db, project, req.name, req.description, req.script_path)
    return ExperimentResponse.model_validate(exp)


@router.get("/projects/{project_id}/experiments", response_model=List[ExperimentResponse])
def list_experiments(project_id: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    exps = ExperimentService.list_experiments(db, project.id)
    return [ExperimentResponse.model_validate(e) for e in exps]


@router.get("/projects/{project_id}/experiments/{experiment_id}", response_model=ExperimentResponse)
def get_experiment(project_id: str, experiment_id: str, db: Session = Depends(get_db)):
    exp = ExperimentService.get_experiment(db, experiment_id)
    if not exp or exp.project_id != project_id:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return ExperimentResponse.model_validate(exp)


@router.post("/projects/{project_id}/experiments/{experiment_id}/run", response_model=ExecutionRecordResponse)
async def run_experiment(project_id: str, experiment_id: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    exp = ExperimentService.get_experiment(db, experiment_id)
    if not exp or exp.project_id != project.id:
        raise HTTPException(status_code=404, detail="Experiment not found")
    record = await ExperimentService.run_experiment(db, exp, project)
    return ExecutionRecordResponse.model_validate(record)


@router.get("/projects/{project_id}/executions", response_model=List[ExecutionRecordResponse])
def list_executions(project_id: str, db: Session = Depends(get_db)):
    project = ProjectRepository.get_project_by_id_or_name(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    records = ExperimentService.list_executions(db, project.id)
    return [ExecutionRecordResponse.model_validate(r) for r in records]


@router.get("/projects/{project_id}/executions/{execution_id}", response_model=ExecutionRecordResponse)
def get_execution(project_id: str, execution_id: str, db: Session = Depends(get_db)):
    record = ExperimentService.get_execution(db, execution_id)
    if not record or record.project_id != project_id:
        raise HTTPException(status_code=404, detail="Execution record not found")
    return ExecutionRecordResponse.model_validate(record)
