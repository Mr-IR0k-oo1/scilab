import os
import pytest
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.models import Base
from app.reports.models import ReportConfiguration
from app.reports.service import ReportService
from app.repositories.project_repository import ProjectRepository
from app.results.models import ArtifactType, ExperimentResultCreate, ResultArtifactCreate
from app.results.service import ResultService
from app.services.experiment_service import ExperimentService


@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_experiment_result_and_report_generation(setup_db: Session):
    db = setup_db

    # 1. Create test project
    project = ProjectRepository.create_project(db, name="Report Test Project", path=os.path.abspath("./tmp_report_proj"))
    
    # 2. Create experiment & execution
    exp = ExperimentService.create_experiment(db, project, name="Test Thermal Exp", script_path="scripts/main.sce")
    exec_rec = ExperimentService.create_execution_record(
        db, project_id=project.id, experiment_id=exp.id, script_path="scripts/main.sce", status="COMPLETED", stdout="Simulated output ok"
    )

    # 3. Create Experiment Result
    res_req = ExperimentResultCreate(execution_id=exec_rec.execution_id, summary="Thermal simulation test success")
    result = ResultService.create_result(db, project.id, exp.id, res_req)
    assert result.id is not None
    assert result.status == "SUCCESS"

    # 4. Add Artifact
    art_req = ResultArtifactCreate(type=ArtifactType.TEXT, name="output.txt", path="outputs/output.txt", size=120)
    art = ResultService.add_artifact(db, project.id, result.id, art_req)
    assert art.id is not None
    assert art.type == ArtifactType.TEXT

    # 5. Generate Engineering Report
    config = ReportConfiguration(
        title="Thermal Analysis Test Report",
        author="Architect Lead",
        organization="Scilab Ecosystem",
        description="Engineering verification report for Phase 5",
    )
    report = ReportService.generate_report(db, project.id, result.id, config)

    assert report.id is not None
    assert report.title == "Thermal Analysis Test Report"
    assert report.hash is not None
    assert len(report.hash) == 64
    assert report.reproducibility.project_id == project.id
    assert report.reproducibility.execution_id == exec_rec.execution_id

    # 6. Content retrieval test
    html_content = ReportService.get_report_content(db, project.id, report.id, format_type="html")
    assert b"Thermal Analysis Test Report" in html_content
    assert b"Architect Lead" in html_content

    # Clean up project dir
    ProjectRepository.delete_project(db, project.id)
