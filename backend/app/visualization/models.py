from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.data.models import TransformationPipeline


class ChartType(str, Enum):
    LINE = "line"
    SCATTER = "scatter"
    BAR = "bar"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"


class VisualizationOptions(BaseModel):
    title: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    color_palette: Optional[str] = "default"
    show_grid: bool = True
    bins: Optional[int] = 10  # For Histogram
    aggregation: Optional[str] = "mean"  # For Heatmap / Bar


class VisualizationSpec(BaseModel):
    id: Optional[str] = None
    project_id: str
    dataset_id: str
    experiment_id: Optional[str] = None
    name: str
    type: ChartType
    x_column: Optional[str] = None
    y_columns: List[str] = []
    group_column: Optional[str] = None
    transformations: TransformationPipeline = Field(default_factory=TransformationPipeline)
    options: VisualizationOptions = Field(default_factory=VisualizationOptions)
    schema_version: int = Field(1, description="Specification schema version")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ChartDataPoint(BaseModel):
    x: Any
    y: Dict[str, Any]


class ChartSeries(BaseModel):
    name: str
    data: List[Dict[str, Any]]


class ChartDataResponse(BaseModel):
    visualization_id: str
    type: ChartType
    series: List[ChartSeries]
    sample_count: int
    sampled: bool = False
    dataset_hash_changed: bool = False
    warning: Optional[str] = None
