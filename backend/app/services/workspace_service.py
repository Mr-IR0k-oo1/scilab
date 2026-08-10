from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.workspace_repository import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceListResponse


class WorkspaceService:
    def __init__(self, db: Session):
        self.repository = WorkspaceRepository(db)

    def list_workspaces(self) -> WorkspaceListResponse:
        workspaces = self.repository.get_all()
        responses = [WorkspaceResponse.model_validate(w) for w in workspaces]
        return WorkspaceListResponse(workspaces=responses, total=len(responses))

    def create_workspace(self, data: WorkspaceCreate) -> WorkspaceResponse:
        workspace = self.repository.create(data)
        return WorkspaceResponse.model_validate(workspace)

    def get_workspace(self, workspace_id: str) -> Optional[WorkspaceResponse]:
        workspace = self.repository.get_by_id(workspace_id)
        if not workspace:
            return None
        return WorkspaceResponse.model_validate(workspace)
