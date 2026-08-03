from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from ..filesystem import project_manager
from ..models import ProjectMetadata

router = APIRouter(prefix="/api/projects", tags=["projects"])

class CreateProjectRequest(BaseModel):
    name: str
    description: str | None = None

@router.get("/dir")
async def get_project_dir():
    try:
        return {"dir": project_manager.get_project_dir()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=ProjectMetadata)
async def create_project(req: CreateProjectRequest):
    try:
        return project_manager.create_project(req.name, req.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[ProjectMetadata])
async def list_projects():
    try:
        return project_manager.list_projects()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{name}", response_model=ProjectMetadata)
async def update_project_metadata(name: str, metadata: ProjectMetadata):
    try:
        return project_manager.update_project_metadata(name, metadata)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{name}")
async def delete_project(name: str):
    try:
        project_manager.delete_project(name)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
