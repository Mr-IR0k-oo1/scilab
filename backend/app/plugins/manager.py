import json
import os
from typing import Any, Dict, List, Optional
from app.plugins.lifecycle import PluginStatus
from app.plugins.loader import PluginLoader
from app.plugins.registry import (
    DatasetLoaderRegistry,
    GUIComponentRegistry,
    PluginRecord,
    PluginRegistry,
    ReportTemplateRegistry,
    VisualizationExtensionRegistry,
)
from app.plugins.validator import PluginValidator
from app.sdk.context import PluginContext
from app.sdk.manifest import PluginManifest


class PluginManager:
    def __init__(self, plugin_search_paths: Optional[List[str]] = None):
        self.plugin_search_paths = plugin_search_paths or [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "plugins", "examples"))
        ]
        self.plugin_registry = PluginRegistry()
        self.gui_registry = GUIComponentRegistry()
        self.visualization_registry = VisualizationExtensionRegistry()
        self.dataset_loader_registry = DatasetLoaderRegistry()
        self.report_template_registry = ReportTemplateRegistry()

    def discover_plugins(self) -> List[PluginRecord]:
        discovered = []
        for base_path in self.plugin_search_paths:
            if not os.path.exists(base_path):
                continue
            for root, dirs, files in os.walk(base_path):
                if "plugin.json" in files:
                    manifest_path = os.path.join(root, "plugin.json")
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        manifest = PluginManifest.model_validate(data)
                        record = PluginRecord(
                            manifest=manifest,
                            status=PluginStatus.DISCOVERED,
                            source_path=root,
                        )
                        valid, errors = PluginValidator.validate_manifest(manifest)
                        if valid:
                            record.status = PluginStatus.VALIDATED
                        else:
                            record.status = PluginStatus.FAILED
                            record.errors.extend(errors)

                        if self.plugin_registry.register(record):
                            discovered.append(record)
                    except Exception as e:
                        pass
        return discovered

    def load_and_initialize_plugins(self) -> None:
        self.discover_plugins()
        for p in self.plugin_registry.list_all():
            if p.status == PluginStatus.VALIDATED:
                self.load_plugin(p.manifest.id)

    def load_plugin(self, plugin_id: str) -> bool:
        record = self.plugin_registry.get(plugin_id)
        if not record or record.status in [PluginStatus.FAILED, PluginStatus.RUNNING]:
            return False

        instance, err = PluginLoader.load_plugin_class(record.source_path, record.manifest.entrypoint)
        if err or not instance:
            record.status = PluginStatus.FAILED
            record.errors.append(err or "Failed to load class")
            return False

        record.plugin_instance = instance
        record.status = PluginStatus.LOADED

        ctx = PluginContext(plugin_id=record.manifest.id)
        try:
            instance.initialize(ctx)
            record.status = PluginStatus.INITIALIZED
            instance.start()
            record.status = PluginStatus.RUNNING
            return True
        except Exception as e:
            record.status = PluginStatus.FAILED
            record.errors.append(f"Lifecycle error during start(): {str(e)}")
            return False

    def disable_plugin(self, plugin_id: str) -> bool:
        record = self.plugin_registry.get(plugin_id)
        if not record:
            return False

        if record.plugin_instance:
            try:
                record.plugin_instance.stop()
                record.plugin_instance.dispose()
            except Exception:
                pass

        self.gui_registry.clear_by_plugin(plugin_id)
        self.visualization_registry.clear_by_plugin(plugin_id)
        self.dataset_loader_registry.clear_by_plugin(plugin_id)
        self.report_template_registry.clear_by_plugin(plugin_id)

        record.status = PluginStatus.DISABLED
        return True

    def enable_plugin(self, plugin_id: str) -> bool:
        record = self.plugin_registry.get(plugin_id)
        if not record:
            return False

        if record.status in [PluginStatus.DISABLED, PluginStatus.VALIDATED, PluginStatus.STOPPED]:
            return self.load_plugin(plugin_id)
        return record.status == PluginStatus.RUNNING
