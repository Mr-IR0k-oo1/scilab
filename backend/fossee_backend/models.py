from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ExecuteResult(BaseModel):
    output: str
    variables: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    success: bool

class ScilabStatus(BaseModel):
    running: bool
    version: Optional[str] = None
    pid: Optional[int] = None

class FileInfo(BaseModel):
    name: str
    is_dir: bool
    path: str
    size: Optional[int] = None
    last_modified: Optional[float] = None

class ProjectMetadata(BaseModel):
    name: str
    description: Optional[str] = None
    created_at: Optional[float] = None
    updated_at: Optional[float] = None

class ChartOptions(BaseModel):
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    grid: Optional[bool] = None
    legend: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None

class ColumnDefinition(BaseModel):
    name: str
    type: str

class DataDescriptor(BaseModel):
    source: str
    expression: Optional[str] = None
    columns: Optional[List[ColumnDefinition]] = None
    variables: Optional[List[str]] = None

class Chart(BaseModel):
    id: str
    type: str
    data: DataDescriptor
    options: ChartOptions

class WidgetProperty(BaseModel):
    name: str
    type: str
    label: str
    default: Optional[Any] = None
    options: Optional[List[str]] = None

class WidgetType(BaseModel):
    type: str
    name: str
    category: str
    properties: List[WidgetProperty]

class WidgetProperties(BaseModel):
    name: Optional[str] = None
    value: Optional[Any] = None
    label: Optional[str] = None
    text: Optional[str] = None
    placeholder: Optional[str] = None
    default_value: Optional[Any] = None
    max_length: Optional[int] = None
    min: Optional[float] = None
    max: Optional[float] = None
    step: Optional[float] = None
    checked: Optional[bool] = None
    options: Optional[List[str]] = None
    default_index: Optional[int] = None
    chart_reference: Optional[str] = None
    aspect_ratio: Optional[float] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    data_source: Optional[str] = None
    border_style: Optional[str] = None
    background_color: Optional[str] = None
    children: Optional[List[str]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    font_size: Optional[int] = None
    color: Optional[str] = None
    align: Optional[str] = None

class WidgetInstance(BaseModel):
    id: str
    type: str
    properties: WidgetProperties
