from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import DatasetMetadataModel


class DatasetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, dataset_id: str) -> Optional[DatasetMetadataModel]:
        return self.db.query(DatasetMetadataModel).filter(DatasetMetadataModel.id == dataset_id).first()

    def get_by_project(self, project_id: str) -> List[DatasetMetadataModel]:
        return self.db.query(DatasetMetadataModel).filter(DatasetMetadataModel.project_id == project_id).all()

    def delete(self, dataset: DatasetMetadataModel) -> None:
        self.db.delete(dataset)
        self.db.commit()
