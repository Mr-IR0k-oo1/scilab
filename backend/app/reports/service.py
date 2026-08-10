import hashlib
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.reports.exporters import ReportExporter
from app.reports.models import EngineeringReportResponse, ReportConfiguration, ReportReproducibilityInfo
from app.reports.renderer import ReportRenderer
from app.reports.validators import ReportValidator
from app.repositories.report_repository import ReportRepository
from app.repositories.visualization_repository import VisualizationRepository
from app.results.service import ResultService
from app.services.dataset_service import DatasetService
from app.services.scilab_service import ScilabService


class ReportService:
    @staticmethod
    def generate_report(
        db: Session,
        project_id: str,
        result_id: str,
        config: ReportConfiguration,
    ) -> EngineeringReportResponse:
        res = ResultService.get_result(db, project_id, result_id)
        validated = ReportValidator.validate_report_inputs(
            db=db,
            project_id=project_id,
            experiment_id=res.experiment_id,
            execution_id=res.execution_id,
        )

        project = validated["project"]
        experiment = validated["experiment"]
        execution = validated["execution"]

        # Fetch visualizations if available
        v_repo = VisualizationRepository(db)
        viz_models = v_repo.get_by_project(project_id)
        visualizations = [v_repo.to_spec(v) for v in viz_models]

        # Fetch dataset if available
        dataset_info = None
        dataset_id = None
        dataset_hash = None
        from app.repositories.dataset_repository import DatasetRepository
        d_repo = DatasetRepository(db)
        datasets = d_repo.get_by_project(project_id)
        if datasets:
            d = datasets[0]
            dataset_id = d.id
            dataset_hash = d.content_hash
            dataset_info = {
                "filename": d.filename,
                "path": d.path,
                "size_bytes": d.size_bytes,
                "row_count": d.row_count,
                "column_count": d.column_count,
                "content_hash": d.content_hash,
            }

        # Build Reproducibility Info
        reproducibility = ReportReproducibilityInfo(
            project_id=project.id,
            experiment_id=experiment.id,
            execution_id=execution.execution_id,
            script_path=experiment.script_path,
            dataset_id=dataset_id,
            dataset_hash=dataset_hash,
            visualization_ids=[v.id for v in visualizations if v.id],
            execution_timestamp=execution.started_at.isoformat() if hasattr(execution.started_at, "isoformat") else str(execution.started_at),
            scilab_version="6.1.1 (Standard Engine)",
            app_version="0.1.0",
            report_schema_version=1,
        )

        # Context for Jinja2 template
        context = {
            "title": config.title,
            "author": config.author or "Scilab Studio User",
            "organization": config.organization or "FOSSEE / Scilab Ecosystem",
            "description": config.description or "Automated technical engineering analysis report generated from experiment execution.",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "project": project,
            "experiment": experiment,
            "execution": execution,
            "dataset": dataset_info,
            "visualizations": visualizations,
            "reproducibility": reproducibility,
        }

        html_content = ReportRenderer.render_html(config.template, context)

        report_id = str(uuid.uuid4())
        rel_output_path = os.path.join("outputs", "reports", report_id, "report.html")
        abs_output_path = os.path.join(project.path, rel_output_path)

        size_bytes = ReportExporter.export_html(html_content, abs_output_path)
        pdf_path = os.path.join(project.path, "outputs", "reports", report_id, "report.pdf")
        ReportExporter.export_pdf(html_content, pdf_path)

        hash_val = hashlib.sha256(html_content.encode("utf-8")).hexdigest()

        repo = ReportRepository(db)
        model = repo.create(
            project_id=project.id,
            result_id=res.id,
            title=config.title,
            author=config.author,
            organization=config.organization,
            description=config.description,
            template=config.template,
            output_path=rel_output_path,
            hash_val=hash_val,
            size_bytes=size_bytes,
            reproducibility=reproducibility,
        )

        return ReportRepository.to_response(model)

    @staticmethod
    def list_reports(db: Session, project_id: str) -> List[EngineeringReportResponse]:
        repo = ReportRepository(db)
        models = repo.get_by_project(project_id)
        return [ReportRepository.to_response(m) for m in models]

    @staticmethod
    def get_report(db: Session, project_id: str, report_id: str) -> EngineeringReportResponse:
        repo = ReportRepository(db)
        model = repo.get_by_id(report_id)
        if not model or model.project_id != project_id:
            raise HTTPException(status_code=404, detail="Report not found")
        return ReportRepository.to_response(model)

    @staticmethod
    def get_report_content(db: Session, project_id: str, report_id: str, format_type: str = "html") -> bytes:
        report = ReportService.get_report(db, project_id, report_id)
        from app.repositories.project_repository import ProjectRepository
        project = ProjectRepository.get_project_by_id_or_name(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        target_file = report.output_path
        if format_type.lower() == "pdf":
            target_file = os.path.join(os.path.dirname(report.output_path), "report.pdf")

        abs_path = os.path.join(project.path, target_file)
        if not os.path.exists(abs_path):
            raise HTTPException(status_code=404, detail="Report file not found on disk")

        with open(abs_path, "rb") as f:
            return f.read()
