from typing import List, Optional
from pydantic import BaseModel
from app.visualization.models import ChartDataResponse, ChartType, VisualizationOptions, VisualizationSpec


class VisualizationCreateRequest(BaseModel):
    dataset_id: str
    experiment_id: Optional[str] = None
    name: str
    type: ChartType
    x_column: Optional[str] = None
    y_columns: List[str] = []
    group_column: Optional[str] = None
    transformations: Optional[dict] = None
    options: Optional[dict] = None


class VisualizationUpdateRequest(BaseModel):
    name: Optional[str] = None
    type: Optional[ChartType] = None
    x_column: Optional[str] = None
    y_columns: Optional[List[str]] = None
    group_column: Optional[str] = None
    transformations: Optional[dict] = None
    options: Optional[dict] = None
