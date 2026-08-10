from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.project import ProjectResponse
from app.templates.models import (
    TemplateCreateProjectRequest,
    TemplateManifest,
    TemplateValidationResult,
)
from app.templates.service import TemplateService

router = APIRouter()
template_service = TemplateService()


@router.get("/templates", response_model=List[TemplateManifest])
def list_templates(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
):
    return template_service.list_templates(category=category, difficulty=difficulty, query=query)


@router.get("/templates/categories", response_model=List[str])
def get_template_categories():
    return template_service.get_categories()


@router.get("/templates/{template_id}", response_model=TemplateManifest)
def get_template(template_id: str):
    record = template_service.get_template(template_id)
    if not record or not record.valid:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Template not found")
    return record.manifest


@router.post("/templates/{template_id}/validate", response_model=TemplateValidationResult)
def validate_template(template_id: str):
    return template_service.validate_template(template_id)


@router.post("/templates/{template_id}/create-project", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_from_template(
    template_id: str,
    req: TemplateCreateProjectRequest,
    db: Session = Depends(get_db),
):
    project = template_service.create_project_from_template(db=db, template_id=template_id, req=req)
    return ProjectResponse.model_validate(project)
