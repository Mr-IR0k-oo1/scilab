import json
import os
import shutil
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import ProjectModel
from app.repositories.project_repository import ProjectRepository
from app.services.experiment_service import ExperimentService
from app.templates.models import TemplateManifest
from app.templates.registry import TemplateRecord, TemplateRegistry


class TemplateInstaller:
    @staticmethod
    def create_project_from_template(
        db: Session,
        registry: TemplateRegistry,
        template_id: str,
        project_name: str,
        workspace_id: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        projects_base_dir: str = "./projects",
    ) -> ProjectModel:
        record = registry.get(template_id)
        if not record or not record.valid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "TEMPLATE_NOT_FOUND", "message": f"Template '{template_id}' not found or invalid"},
            )

        manifest = record.manifest
        abs_projects_dir = os.path.abspath(projects_base_dir)
        proj_dir_name = project_name.lower().replace(" ", "_")
        proj_path = os.path.join(abs_projects_dir, proj_dir_name)

        if os.path.exists(proj_path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "PROJECT_EXISTS", "message": f"Project directory '{proj_dir_name}' already exists"},
            )

        # 1. Create DB project record
        project = ProjectRepository.create_project(
            db=db,
            name=project_name,
            description=description or f"Created from template {manifest.name} (v{manifest.version})",
            workspace_id=workspace_id,
            path=proj_path,
        )

        # 2. Copy template directory files safely
        for root, dirs, files in os.walk(record.source_path):
            rel_root = os.path.relpath(root, record.source_path)
            target_dir = os.path.join(proj_path, rel_root) if rel_root != "." else proj_path
            os.makedirs(target_dir, exist_ok=True)

            for f in files:
                if f == "template.json":
                    continue
                src_file = os.path.join(root, f)
                dst_file = os.path.join(target_dir, f)
                shutil.copy2(src_file, dst_file)

        # 3. Write project manifest project.json
        manifest_data = {
            "schema_version": 1,
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_from_template": {
                "template_id": manifest.id,
                "template_version": manifest.version,
                "template_name": manifest.name,
            },
            "parameters": parameters or {},
        }
        with open(os.path.join(proj_path, "project.json"), "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)

        # 4. Register experiment definition
        exp_name = f"{manifest.name} Experiment"
        entry_script = manifest.entry_experiment
        ExperimentService.create_experiment(
            db=db,
            project=project,
            name=exp_name,
            description=f"Starter experiment from template {manifest.id}",
            script_path=entry_script,
        )

        # 5. Prepend parameter binding headers to entry script if parameters provided
        if parameters:
            abs_script = os.path.join(proj_path, entry_script)
            if os.path.exists(abs_script):
                with open(abs_script, "r", encoding="utf-8") as f:
                    orig_content = f.read()

                param_lines = ["// Parameter bindings generated from template"]
                for k, v in parameters.items():
                    if isinstance(v, (int, float)):
                        param_lines.append(f"{k} = {v};")
                    elif isinstance(v, bool):
                        param_lines.append(f"{k} = %{'t' if v else 'f'};")
                    else:
                        param_lines.append(f'{k} = "{v}";')

                param_header = "\n".join(param_lines) + "\n\n"
                with open(abs_script, "w", encoding="utf-8") as f:
                    f.write(param_header + orig_content)

        return project
