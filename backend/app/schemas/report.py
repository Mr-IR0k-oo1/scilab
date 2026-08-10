from typing import List, Optional
from pydantic import BaseModel, Field


class ReportCreateRequest(BaseModel):
    result_id: str
    title: str = Field("Engineering Analysis Report", min_length=1)
    author: Optional[str] = "Scilab Studio User"
    organization: Optional[str] = "FOSSEE / Scilab Ecosystem"
    description: Optional[str] = None
    visualization_ids: List[str] = Field(default_factory=list)
    artifact_ids: List[str] = Field(default_factory=list)
    include_dataset_stats: bool = True
    include_execution_details: bool = True
    template: str = "default_engineering_report"
