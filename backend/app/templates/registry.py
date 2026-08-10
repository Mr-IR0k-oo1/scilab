import json
import os
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, ConfigDict
from app.templates.models import TemplateManifest, TemplateValidationResult


class TemplateRecord(BaseModel):
    manifest: TemplateManifest
    source_path: str
    valid: bool = True
    errors: List[str] = []

    model_config = ConfigDict(from_attributes=True)


class TemplateRegistry:
    def __init__(self, templates_base_dir: Optional[str] = None):
        self.templates_base_dir = templates_base_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "templates", "engineering")
        )
        self._templates: Dict[str, TemplateRecord] = {}

    def discover_templates(self) -> List[TemplateRecord]:
        discovered = []
        if not os.path.exists(self.templates_base_dir):
            return discovered

        for root, dirs, files in os.walk(self.templates_base_dir):
            if "template.json" in files:
                manifest_path = os.path.join(root, "template.json")
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    manifest = TemplateManifest.model_validate(data)
                    record = TemplateRecord(
                        manifest=manifest,
                        source_path=root,
                        valid=True,
                        errors=[],
                    )
                    valid, errors = self.validate_template(record)
                    record.valid = valid
                    record.errors = errors

                    self._templates[manifest.id] = record
                    discovered.append(record)
                except Exception as e:
                    pass

        return discovered

    def validate_template(self, record: TemplateRecord) -> Tuple[bool, List[str]]:
        errors = []
        manifest = record.manifest

        if not manifest.id:
            errors.append("Template manifest missing required field 'id'")
        if not manifest.name:
            errors.append("Template manifest missing required field 'name'")

        # Path safety check
        real_src = os.path.realpath(record.source_path)
        real_base = os.path.realpath(self.templates_base_dir)
        if not real_src.startswith(real_base):
            errors.append("Security Violation: Template path escapes template directory boundary.")

        # Check required entry experiment script file
        entry_script = os.path.join(record.source_path, manifest.entry_experiment)
        if not os.path.exists(entry_script):
            errors.append(f"Required entry script '{manifest.entry_experiment}' missing from template directory.")

        return (len(errors) == 0, errors)

    def get(self, template_id: str) -> Optional[TemplateRecord]:
        if not self._templates:
            self.discover_templates()
        return self._templates.get(template_id)

    def list_all(self) -> List[TemplateRecord]:
        if not self._templates:
            self.discover_templates()
        return list(self._templates.values())

    def get_categories(self) -> List[str]:
        all_templates = self.list_all()
        categories = list(set(t.manifest.category for t in all_templates if t.valid))
        return sorted(categories)

    def search(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        query: Optional[str] = None,
    ) -> List[TemplateRecord]:
        all_templates = self.list_all()
        res = []
        for t in all_templates:
            if not t.valid:
                continue
            if category and t.manifest.category.lower() != category.lower():
                continue
            if difficulty and t.manifest.difficulty.lower() != difficulty.lower():
                continue
            if query:
                q = query.lower()
                name_match = q in t.manifest.name.lower()
                desc_match = q in t.manifest.description.lower()
                tag_match = any(q in tag.lower() for tag in t.manifest.tags)
                if not (name_match or desc_match or tag_match):
                    continue
            res.append(t)
        return res
