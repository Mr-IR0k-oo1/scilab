from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.db.models import ProjectModel
from app.templates.installer import TemplateInstaller
from app.templates.models import TemplateCreateProjectRequest, TemplateManifest, TemplateValidationResult
from app.templates.registry import TemplateRecord, TemplateRegistry


class TemplateService:
    def __init__(self, registry: Optional[TemplateRegistry] = None):
        self.registry = registry or TemplateRegistry()
        self.registry.discover_templates()

    def list_templates(self, category: Optional[str] = None, difficulty: Optional[str] = None, query: Optional[str] = None) -> List[TemplateManifest]:
        records = self.registry.search(category=category, difficulty=difficulty, query=query)
        return [r.manifest for r in records]

    def get_categories(self) -> List[str]:
        return self.registry.get_categories()

    def get_template(self, template_id: str) -> Optional[TemplateRecord]:
        return self.registry.get(template_id)

    def validate_template(self, template_id: str) -> TemplateValidationResult:
        record = self.registry.get(template_id)
        if not record:
            return TemplateValidationResult(valid=False, errors=[f"Template '{template_id}' not found"])
        valid, errors = self.registry.validate_template(record)
        return TemplateValidationResult(valid=valid, errors=errors)

    def create_project_from_template(self, db: Session, template_id: str, req: TemplateCreateProjectRequest) -> ProjectModel:
        return TemplateInstaller.create_project_from_template(
            db=db,
            registry=self.registry,
            template_id=template_id,
            project_name=req.project_name,
            workspace_id=req.workspace_id,
            description=req.description,
            parameters=req.parameters,
        )
