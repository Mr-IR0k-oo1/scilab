from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status
from app.plugins.manager import PluginManager
from app.sdk.capabilities import CapabilityType
from app.sdk.manifest import PluginManifest

router = APIRouter()

# Global plugin manager instance
plugin_manager = PluginManager()
plugin_manager.discover_plugins()
for p in plugin_manager.plugin_registry.list_all():
    if p.status == "VALIDATED":
        plugin_manager.load_plugin(p.manifest.id)


@router.get("/plugins", response_model=List[Dict[str, Any]])
def list_plugins():
    plugins = plugin_manager.plugin_registry.list_all()
    return [
        {
            "id": p.manifest.id,
            "name": p.manifest.name,
            "version": p.manifest.version,
            "api_version": p.manifest.api_version,
            "description": p.manifest.description,
            "author": p.manifest.author,
            "status": p.status.value,
            "capabilities": [c.value for c in p.manifest.capabilities],
            "errors": p.errors,
            "source_path": p.source_path,
        }
        for p in plugins
    ]


@router.get("/plugins/capabilities", response_model=List[str])
def list_capabilities():
    return [c.value for c in CapabilityType]


@router.get("/plugins/gui-components", response_model=List[Dict[str, Any]])
def list_plugin_gui_components():
    res = []
    for p in plugin_manager.plugin_registry.list_all():
        if p.status == "RUNNING" and p.plugin_instance and hasattr(p.plugin_instance, "get_gui_components"):
            comps = p.plugin_instance.get_gui_components()
            for c in comps:
                res.append(c.model_dump() if hasattr(c, "model_dump") else c)
    return res


@router.get("/plugins/visualizations", response_model=List[Dict[str, Any]])
def list_plugin_visualizations():
    res = []
    for p in plugin_manager.plugin_registry.list_all():
        if p.status == "RUNNING" and p.plugin_instance and hasattr(p.plugin_instance, "get_visualizations"):
            vizs = p.plugin_instance.get_visualizations()
            for v in vizs:
                res.append(v.model_dump() if hasattr(v, "model_dump") else v)
    return res


@router.get("/plugins/dataset-loaders", response_model=List[Dict[str, Any]])
def list_plugin_dataset_loaders():
    return []


@router.get("/plugins/report-templates", response_model=List[Dict[str, Any]])
def list_plugin_report_templates():
    return []


@router.get("/plugins/{plugin_id}", response_model=Dict[str, Any])
def get_plugin(plugin_id: str):
    p = plugin_manager.plugin_registry.get(plugin_id)
    if not p:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return {
        "id": p.manifest.id,
        "name": p.manifest.name,
        "version": p.manifest.version,
        "api_version": p.manifest.api_version,
        "description": p.manifest.description,
        "author": p.manifest.author,
        "status": p.status.value,
        "capabilities": [c.value for c in p.manifest.capabilities],
        "errors": p.errors,
        "source_path": p.source_path,
    }


@router.post("/plugins/{plugin_id}/enable", response_model=Dict[str, Any])
def enable_plugin(plugin_id: str):
    p = plugin_manager.plugin_registry.get(plugin_id)
    if not p:
        raise HTTPException(status_code=404, detail="Plugin not found")
    success = plugin_manager.enable_plugin(plugin_id)
    return {"id": plugin_id, "enabled": success, "status": p.status.value}


@router.post("/plugins/{plugin_id}/disable", response_model=Dict[str, Any])
def disable_plugin(plugin_id: str):
    p = plugin_manager.plugin_registry.get(plugin_id)
    if not p:
        raise HTTPException(status_code=404, detail="Plugin not found")
    success = plugin_manager.disable_plugin(plugin_id)
    return {"id": plugin_id, "disabled": success, "status": p.status.value}
