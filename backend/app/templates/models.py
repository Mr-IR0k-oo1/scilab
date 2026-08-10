from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ParameterType(str, Enum):
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    STRING = "string"
    SELECT = "select"


class TemplateParameter(BaseModel):
    name: str = Field(..., description="Scilab variable name")
    label: str = Field(..., description="Display label")
    type: ParameterType = Field(ParameterType.NUMBER)
    default: Any = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    step: Optional[float] = None
    unit: Optional[str] = None
    options: List[str] = Field(default_factory=list)


class TemplateManifest(BaseModel):
    schema_version: int = Field(1, description="Template manifest schema version")
    id: str = Field(..., description="Unique template identifier (e.g. control.pid_basic)")
    name: str = Field(..., description="Template title")
    version: str = Field("1.0.0", description="Semantic version string")
    category: str = Field("general", description="Category (control_systems, numerical_methods, etc.)")
    description: str = Field("", description="Detailed educational description")
    difficulty: str = Field("intermediate", description="beginner, intermediate, advanced")
    scilab_version: str = Field(">=6.0.0", description="Required Scilab engine version")
    entry_experiment: str = Field("scripts/main.sce", description="Default script/experiment path")
    parameters: List[TemplateParameter] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TemplateValidationResult(BaseModel):
    valid: bool
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class TemplateCreateProjectRequest(BaseModel):
    project_name: str
    workspace_id: Optional[str] = None
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
