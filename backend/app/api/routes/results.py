from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.results.models import (
    ExperimentResultCreate,
    ExperimentResultResponse,
    ResultArtifactCreate,
    ResultArtifactResponse,
    ResultSummaryResponse,
)
from app.results.service import ResultService

router = APIRouter()


@router.post("/projects/{project_id}/experiments/{experiment_id}/results", response_model=ExperimentResultResponse, status_code=status.HTTP_201_CREATED)
def create_experiment_result(project_id: str, experiment_id: str, req: ExperimentResultCreate, db: Session = Depends(get_db)):
    return ResultService.create_result(db, project_id, experiment_id, req)


@router.get("/projects/{project_id}/results", response_model=List[ExperimentResultResponse])
def list_results(project_id: str, db: Session = Depends(get_db)):
    return ResultService.list_results(db, project_id)


@router.get("/projects/{project_id}/results/{result_id}", response_model=ExperimentResultResponse)
def get_result(project_id: str, result_id: str, db: Session = Depends(get_db)):
    return ResultService.get_result(db, project_id, result_id)


@router.get("/projects/{project_id}/results/{result_id}/artifacts", response_model=List[ResultArtifactResponse])
def list_artifacts(project_id: str, result_id: str, db: Session = Depends(get_db)):
    return ResultService.list_artifacts(db, project_id, result_id)


@router.post("/projects/{project_id}/results/{result_id}/artifacts", response_model=ResultArtifactResponse, status_code=status.HTTP_201_CREATED)
def add_artifact(project_id: str, result_id: str, req: ResultArtifactCreate, db: Session = Depends(get_db)):
    return ResultService.add_artifact(db, project_id, result_id, req)


@router.delete("/projects/{project_id}/results/{result_id}/artifacts/{artifact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_artifact(project_id: str, result_id: str, artifact_id: str, db: Session = Depends(get_db)):
    ResultService.delete_artifact(db, project_id, result_id, artifact_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/projects/{project_id}/results/{result_id}/summary", response_model=ResultSummaryResponse)
def get_result_summary(project_id: str, result_id: str, db: Session = Depends(get_db)):
    return ResultService.get_result_summary(db, project_id, result_id)
