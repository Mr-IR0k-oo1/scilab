from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.plugins.lifecycle import PluginStatus
from app.sdk.interfaces import DatasetLoaderExtension, GUIComponentMetadata, ReportTemplateExtensionMetadata, VisualizationExtensionMetadata
from app.sdk.manifest import PluginManifest


class PluginRecord(BaseModel):
    manifest: PluginManifest
    status: PluginStatus = PluginStatus.DISCOVERED
    source_path: str
    errors: List[str] = Field(default_factory=list)
    plugin_instance: Any = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, PluginRecord] = {}

    def register(self, record: PluginRecord) -> bool:
        if record.manifest.id in self._plugins:
            return False
        self._plugins[record.manifest.id] = record
        return True

    def unregister(self, plugin_id: str) -> bool:
        if plugin_id in self._plugins:
            del self._plugins[plugin_id]
            return True
        return False

    def get(self, plugin_id: str) -> Optional[PluginRecord]:
        return self._plugins.get(plugin_id)

    def list_all(self) -> List[PluginRecord]:
        return list(self._plugins.values())


class GUIComponentRegistry:
    def __init__(self):
        self._components: Dict[str, GUIComponentMetadata] = {}

    def register(self, plugin_id: str, comp: GUIComponentMetadata) -> None:
        key = f"{plugin_id}:{comp.component_type}"
        self._components[key] = comp

    def list_all(self) -> List[GUIComponentMetadata]:
        return list(self._components.values())

    def clear_by_plugin(self, plugin_id: str) -> None:
        prefix = f"{plugin_id}:"
        self._components = {k: v for k, v in self._components.items() if not k.startswith(prefix)}


class VisualizationExtensionRegistry:
    def __init__(self):
        self._visualizations: Dict[str, VisualizationExtensionMetadata] = {}

    def register(self, plugin_id: str, viz: VisualizationExtensionMetadata) -> None:
        key = f"{plugin_id}:{viz.type}"
        self._visualizations[key] = viz

    def list_all(self) -> List[VisualizationExtensionMetadata]:
        return list(self._visualizations.values())

    def clear_by_plugin(self, plugin_id: str) -> None:
        prefix = f"{plugin_id}:"
        self._visualizations = {k: v for k, v in self._visualizations.items() if not k.startswith(prefix)}


class DatasetLoaderRegistry:
    def __init__(self):
        self._loaders: Dict[str, DatasetLoaderExtension] = {}

    def register(self, plugin_id: str, loader: DatasetLoaderExtension) -> None:
        self._loaders[plugin_id] = loader

    def list_all(self) -> List[DatasetLoaderExtension]:
        return list(self._loaders.values())

    def clear_by_plugin(self, plugin_id: str) -> None:
        if plugin_id in self._loaders:
            del self._loaders[plugin_id]


class ReportTemplateRegistry:
    def __init__(self):
        self._templates: Dict[str, ReportTemplateExtensionMetadata] = {}

    def register(self, plugin_id: str, tmpl: ReportTemplateExtensionMetadata) -> None:
        key = f"{plugin_id}:{tmpl.id}"
        self._templates[key] = tmpl

    def list_all(self) -> List[ReportTemplateExtensionMetadata]:
        return list(self._templates.values())

    def clear_by_plugin(self, plugin_id: str) -> None:
        prefix = f"{plugin_id}:"
        self._templates = {k: v for k, v in self._templates.items() if not k.startswith(prefix)}
