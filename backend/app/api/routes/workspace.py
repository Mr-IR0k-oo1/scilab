from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceListResponse
from app.services.workspace_service import WorkspaceService

router = APIRouter()


@router.get("/workspaces", response_model=WorkspaceListResponse)
def list_workspaces(db: Session = Depends(get_db)):
    service = WorkspaceService(db)
    return service.list_workspaces()


@router.post("/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(data: WorkspaceCreate, db: Session = Depends(get_db)):
    service = WorkspaceService(db)
    return service.create_workspace(data)
