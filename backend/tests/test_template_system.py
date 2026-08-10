import os
import shutil
import pytest
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.models import Base
from app.services.experiment_service import ExperimentService
from app.templates.models import TemplateCreateProjectRequest
from app.templates.registry import TemplateRegistry
from app.templates.service import TemplateService


@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_template_discovery_and_search():
    service = TemplateService()
    templates = service.list_templates()
    assert len(templates) >= 7

    categories = service.get_categories()
    assert "control_systems" in categories
    assert "numerical_methods" in categories
    assert "signal_processing" in categories

    pid_templates = service.list_templates(category="control_systems")
    assert len(pid_templates) >= 1
    assert pid_templates[0].id == "control.pid_basic"


def test_create_project_from_template(setup_db: Session):
    db = setup_db
    service = TemplateService()

    tmp_projects_dir = os.path.abspath("./tmp_template_projects")
    os.makedirs(tmp_projects_dir, exist_ok=True)

    try:
        req = TemplateCreateProjectRequest(
            project_name="Test PID Project",
            description="Project generated from PID template for testing",
            parameters={"kp": 2.5, "ki": 0.8, "kd": 0.2},
        )

        project = service.create_project_from_template(
            db=db,
            template_id="control.pid_basic",
            req=req,
        )

        assert project.id is not None
        assert project.name == "Test PID Project"
        assert os.path.exists(os.path.join(project.path, "project.json"))
        assert os.path.exists(os.path.join(project.path, "scripts", "main.sce"))

        # Verify parameter bindings written to script
        script_file = os.path.join(project.path, "scripts", "main.sce")
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "kp = 2.5;" in content
        assert "ki = 0.8;" in content
        assert "kd = 0.2;" in content

        # Verify experiment registered
        experiments = ExperimentService.list_experiments(db, project.id)
        assert len(experiments) >= 1
        assert "PID" in experiments[0].name

    finally:
        if os.path.exists(tmp_projects_dir):
            shutil.rmtree(tmp_projects_dir, ignore_errors=True)
