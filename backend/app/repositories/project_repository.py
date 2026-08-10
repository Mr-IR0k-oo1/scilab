import os
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import ProjectMetadataModel, ProjectModel
from app.domain.enums.project_status import ProjectStatus
from app.schemas.project import ProjectCreate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ProjectModel]:
        return self.db.query(ProjectModel).filter(ProjectModel.status != ProjectStatus.DELETED.value).order_by(ProjectModel.created_at.desc()).all()

    def get_by_id(self, project_id: str) -> Optional[ProjectModel]:
        return self.db.query(ProjectModel).filter(
            ProjectModel.id == project_id,
            ProjectModel.status != ProjectStatus.DELETED.value
        ).first()

    def get_by_name(self, name: str) -> Optional[ProjectModel]:
        return self.db.query(ProjectModel).filter(
            ProjectModel.name == name,
            ProjectModel.status != ProjectStatus.DELETED.value
        ).first()

    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[ProjectModel]:
        return db.query(ProjectModel).filter(ProjectModel.status != ProjectStatus.DELETED.value).order_by(ProjectModel.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def count_projects(db: Session) -> int:
        return db.query(ProjectModel).filter(ProjectModel.status != ProjectStatus.DELETED.value).count()

    @staticmethod
    def get_project_by_id_or_name(db: Session, identifier: str) -> Optional[ProjectModel]:
        return db.query(ProjectModel).filter(
            (ProjectModel.id == identifier) | (ProjectModel.name == identifier),
            ProjectModel.status != ProjectStatus.DELETED.value
        ).first()

    @staticmethod
    def create_project(db: Session, name: str, description: Optional[str] = None, workspace_id: Optional[str] = None, path: Optional[str] = None) -> ProjectModel:
        calc_path = path or os.path.abspath(os.path.join(".", "projects", name.replace(" ", "_")))
        project = ProjectModel(
            name=name,
            description=description,
            workspace_id=workspace_id,
            path=calc_path,
            status=ProjectStatus.ACTIVE.value,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete_project(db: Session, identifier: str) -> bool:
        project = ProjectRepository.get_project_by_id_or_name(db, identifier)
        if not project:
            return False
        project.status = ProjectStatus.DELETED.value
        db.commit()
        return True
