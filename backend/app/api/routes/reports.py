from typing import List
from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.reports.models import EngineeringReportResponse, ReportConfiguration
from app.reports.service import ReportService
from app.schemas.report import ReportCreateRequest

router = APIRouter()


@router.post("/projects/{project_id}/reports", response_model=EngineeringReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(project_id: str, req: ReportCreateRequest, db: Session = Depends(get_db)):
    config = ReportConfiguration(
        title=req.title,
        author=req.author,
        organization=req.organization,
        description=req.description,
        visualization_ids=req.visualization_ids,
        artifact_ids=req.artifact_ids,
        include_dataset_stats=req.include_dataset_stats,
        include_execution_details=req.include_execution_details,
        template=req.template,
    )
    return ReportService.generate_report(db, project_id, req.result_id, config)


@router.get("/projects/{project_id}/reports", response_model=List[EngineeringReportResponse])
def list_reports(project_id: str, db: Session = Depends(get_db)):
    return ReportService.list_reports(db, project_id)


@router.get("/projects/{project_id}/reports/{report_id}", response_model=EngineeringReportResponse)
def get_report(project_id: str, report_id: str, db: Session = Depends(get_db)):
    return ReportService.get_report(db, project_id, report_id)


@router.get("/projects/{project_id}/reports/{report_id}/download")
def download_report(
    project_id: str,
    report_id: str,
    format: str = Query("html", pattern="^(html|pdf)$"),
    db: Session = Depends(get_db),
):
    content = ReportService.get_report_content(db, project_id, report_id, format_type=format)
    mime = "application/pdf" if format.lower() == "pdf" else "text/html"
    filename = f"report_{report_id}.{format.lower()}"

    return Response(
        content=content,
        media_type=mime,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
