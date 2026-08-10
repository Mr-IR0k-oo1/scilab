from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.sdk.capabilities import CapabilityType


class PluginManifest(BaseModel):
    id: str = Field(..., description="Unique plugin identifier (e.g. org.scilab.plugin)")
    name: str = Field(..., description="Human-readable plugin name")
    version: str = Field("0.1.0", description="Semantic version string")
    api_version: str = Field("1", description="Required Plugin API version")
    description: str = Field("", description="Plugin description")
    author: Optional[str] = Field(None, description="Author or organization name")
    entrypoint: str = Field("plugin:PluginClass", description="Module:ClassName entrypoint specifier")
    capabilities: List[CapabilityType] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
