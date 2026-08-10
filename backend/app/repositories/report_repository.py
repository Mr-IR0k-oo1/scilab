import json
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import EngineeringReportModel
from app.reports.models import EngineeringReportResponse, ReportReproducibilityInfo


class ReportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        project_id: str,
        result_id: str,
        title: str,
        author: Optional[str],
        organization: Optional[str],
        description: Optional[str],
        template: str,
        output_path: str,
        hash_val: Optional[str],
        size_bytes: int,
        reproducibility: ReportReproducibilityInfo,
    ) -> EngineeringReportModel:
        model = EngineeringReportModel(
            project_id=project_id,
            result_id=result_id,
            title=title,
            author=author,
            organization=organization,
            description=description,
            template=template,
            status="COMPLETED",
            output_path=output_path,
            hash=hash_val,
            size_bytes=size_bytes,
            schema_version=1,
            reproducibility=reproducibility.model_dump_json(),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def get_by_id(self, report_id: str) -> Optional[EngineeringReportModel]:
        return self.db.query(EngineeringReportModel).filter(EngineeringReportModel.id == report_id).first()

    def get_by_project(self, project_id: str) -> List[EngineeringReportModel]:
        return self.db.query(EngineeringReportModel).filter(EngineeringReportModel.project_id == project_id).all()

    @staticmethod
    def to_response(model: EngineeringReportModel) -> EngineeringReportResponse:
        repro_dict = json.loads(model.reproducibility) if model.reproducibility else {}
        repro_obj = ReportReproducibilityInfo.model_validate(repro_dict) if repro_dict else None

        return EngineeringReportResponse(
            id=model.id,
            project_id=model.project_id,
            result_id=model.result_id,
            title=model.title,
            author=model.author,
            organization=model.organization,
            description=model.description,
            template=model.template,
            status=model.status,
            output_path=model.output_path,
            hash=model.hash,
            size_bytes=model.size_bytes,
            schema_version=model.schema_version,
            reproducibility=repro_obj,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
