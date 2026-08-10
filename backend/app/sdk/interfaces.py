from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GUIComponentMetadata(BaseModel):
    component_type: str
    display_name: str
    category: str = "Plugin Components"
    schema_def: Dict[str, Any] = Field(default_factory=dict)
    renderer_metadata: Dict[str, Any] = Field(default_factory=dict)
    version: str = "0.1.0"


class VisualizationExtensionMetadata(BaseModel):
    type: str
    name: str
    schema_def: Dict[str, Any] = Field(default_factory=dict)
    input_requirements: Dict[str, Any] = Field(default_factory=dict)
    output_format: str = "chart_series"
    version: str = "0.1.0"


class ReportTemplateExtensionMetadata(BaseModel):
    id: str
    name: str
    version: str = "1.0.0"
    supported_schema: int = 1
    template_path: str


class DatasetLoaderExtension(ABC):
    @abstractmethod
    def supports(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def inspect(self, file_path: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def load(self, file_path: str, max_rows: Optional[int] = None) -> List[Dict[str, Any]]:
        pass
