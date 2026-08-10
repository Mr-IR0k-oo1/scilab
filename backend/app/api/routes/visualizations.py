from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.data.models import TransformationPipeline
from app.schemas.visualization import VisualizationCreateRequest, VisualizationUpdateRequest
from app.services.visualization_service import VisualizationService
from app.visualization.models import ChartDataResponse, VisualizationOptions, VisualizationSpec

router = APIRouter()


@router.post("/projects/{project_id}/visualizations", response_model=VisualizationSpec, status_code=status.HTTP_201_CREATED)
def create_visualization(project_id: str, req: VisualizationCreateRequest, db: Session = Depends(get_db)):
    trans = TransformationPipeline.model_validate(req.transformations) if req.transformations else TransformationPipeline()
    opts = VisualizationOptions.model_validate(req.options) if req.options else VisualizationOptions()

    spec = VisualizationSpec(
        project_id=project_id,
        dataset_id=req.dataset_id,
        experiment_id=req.experiment_id,
        name=req.name,
        type=req.type,
        x_column=req.x_column,
        y_columns=req.y_columns,
        group_column=req.group_column,
        transformations=trans,
        options=opts,
    )
    model = VisualizationService.create_visualization(db, spec)
    return VisualizationService.get_visualization(db, project_id, model.id)


@router.get("/projects/{project_id}/visualizations", response_model=List[VisualizationSpec])
def list_visualizations(project_id: str, db: Session = Depends(get_db)):
    return VisualizationService.list_visualizations(db, project_id)


@router.get("/projects/{project_id}/visualizations/{visualization_id}", response_model=VisualizationSpec)
def get_visualization(project_id: str, visualization_id: str, db: Session = Depends(get_db)):
    return VisualizationService.get_visualization(db, project_id, visualization_id)


@router.put("/projects/{project_id}/visualizations/{visualization_id}", response_model=VisualizationSpec)
def update_visualization(project_id: str, visualization_id: str, req: VisualizationUpdateRequest, db: Session = Depends(get_db)):
    existing = VisualizationService.get_visualization(db, project_id, visualization_id)

    if req.name is not None:
        existing.name = req.name
    if req.type is not None:
        existing.type = req.type
    if req.x_column is not None:
        existing.x_column = req.x_column
    if req.y_columns is not None:
        existing.y_columns = req.y_columns
    if req.group_column is not None:
        existing.group_column = req.group_column
    if req.transformations is not None:
        existing.transformations = TransformationPipeline.model_validate(req.transformations)
    if req.options is not None:
        existing.options = VisualizationOptions.model_validate(req.options)

    return VisualizationService.update_visualization(db, project_id, visualization_id, existing)


@router.delete("/projects/{project_id}/visualizations/{visualization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_visualization(project_id: str, visualization_id: str, db: Session = Depends(get_db)):
    VisualizationService.delete_visualization(db, project_id, visualization_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/projects/{project_id}/visualizations/{visualization_id}/data", response_model=ChartDataResponse)
def get_visualization_data(project_id: str, visualization_id: str, db: Session = Depends(get_db)):
    return VisualizationService.generate_visualization_data(db, project_id, visualization_id)
