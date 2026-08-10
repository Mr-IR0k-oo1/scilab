from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ReportReproducibilityInfo(BaseModel):
    project_id: str
    experiment_id: str
    execution_id: str
    script_path: str
    dataset_id: Optional[str] = None
    dataset_hash: Optional[str] = None
    visualization_ids: List[str] = []
    execution_timestamp: str
    scilab_version: Optional[str] = None
    app_version: str = "0.1.0"
    report_schema_version: int = 1


class ReportConfiguration(BaseModel):
    title: str = Field("Engineering Analysis Report", min_length=1)
    author: Optional[str] = "Scilab Studio User"
    organization: Optional[str] = "FOSSEE / Scilab Ecosystem"
    description: Optional[str] = None
    visualization_ids: List[str] = Field(default_factory=list)
    artifact_ids: List[str] = Field(default_factory=list)
    include_dataset_stats: bool = True
    include_execution_details: bool = True
    template: str = "default_engineering_report"


class EngineeringReportResponse(BaseModel):
    id: str
    project_id: str
    result_id: str
    title: str
    author: Optional[str] = None
    organization: Optional[str] = None
    description: Optional[str] = None
    template: str
    status: str = "COMPLETED"
    output_path: str
    hash: Optional[str] = None
    size_bytes: int = 0
    schema_version: int = 1
    reproducibility: Optional[ReportReproducibilityInfo] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
