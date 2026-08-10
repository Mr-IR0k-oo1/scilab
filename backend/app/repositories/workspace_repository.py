from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import WorkspaceModel
from app.schemas.workspace import WorkspaceCreate


class WorkspaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[WorkspaceModel]:
        return self.db.query(WorkspaceModel).order_by(WorkspaceModel.created_at.desc()).all()

    def get_by_id(self, workspace_id: str) -> Optional[WorkspaceModel]:
        return self.db.query(WorkspaceModel).filter(WorkspaceModel.id == workspace_id).first()

    def create(self, data: WorkspaceCreate) -> WorkspaceModel:
        workspace = WorkspaceModel(
            name=data.name,
            description=data.description,
            path=data.path,
        )
        self.db.add(workspace)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace
