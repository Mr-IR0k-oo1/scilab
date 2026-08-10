from typing import Any, Dict, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.data.models import DatasetSchema, DatasetValidationResult
from app.services.dataset_service import DatasetService

router = APIRouter()


@router.get("/projects/{project_id}/datasets/{dataset_id}/preview", response_model=List[Dict[str, Any]])
def get_dataset_preview(
    project_id: str,
    dataset_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return DatasetService.get_dataset_preview(db, project_id, dataset_id, max_rows=limit)


@router.get("/projects/{project_id}/datasets/{dataset_id}/schema", response_model=DatasetSchema)
def get_dataset_schema(project_id: str, dataset_id: str, db: Session = Depends(get_db)):
    return DatasetService.inspect_dataset_schema(db, project_id, dataset_id)


@router.get("/projects/{project_id}/datasets/{dataset_id}/statistics", response_model=DatasetValidationResult)
def get_dataset_statistics(project_id: str, dataset_id: str, db: Session = Depends(get_db)):
    return DatasetService.get_dataset_statistics(db, project_id, dataset_id)
