import os
import tempfile
import pytest
from app.plugins.lifecycle import PluginStatus
from app.plugins.manager import PluginManager
from app.plugins.validator import PluginValidator
from app.sdk.capabilities import CapabilityType
from app.sdk.manifest import PluginManifest
from app.sdk.version import PLUGIN_API_VERSION


def test_manifest_validation():
    valid_manifest = PluginManifest(
        id="test.plugin",
        name="Test Plugin",
        version="1.0.0",
        api_version=PLUGIN_API_VERSION,
        entrypoint="plugin:TestPlugin",
    )
    is_valid, errors = PluginValidator.validate_manifest(valid_manifest)
    assert is_valid is True
    assert len(errors) == 0

    # Incompatible API version
    invalid_manifest = PluginManifest(
        id="test.plugin",
        name="Test Plugin",
        version="1.0.0",
        api_version="999",
        entrypoint="plugin:TestPlugin",
    )
    is_valid_inv, errors_inv = PluginValidator.validate_manifest(invalid_manifest)
    assert is_valid_inv is False
    assert any("Incompatible Plugin API version" in err for err in errors_inv)


def test_plugin_discovery_and_lifecycle():
    pm = PluginManager()
    discovered = pm.discover_plugins()
    assert len(discovered) >= 1

    rec = pm.plugin_registry.get("example.engineering")
    assert rec is not None
    assert rec.manifest.name == "Example Engineering Extension Plugin"

    # Test load and lifecycle
    loaded = pm.load_plugin("example.engineering")
    assert loaded is True
    assert rec.status == PluginStatus.RUNNING
    assert rec.plugin_instance is not None

    # Test registered GUI components and visualizations
    comps = pm.gui_registry.list_all()
    vizs = pm.visualization_registry.list_all()

    # Test disable
    disabled = pm.disable_plugin("example.engineering")
    assert disabled is True
    assert rec.status == PluginStatus.DISABLED

    # Test re-enable
    enabled = pm.enable_plugin("example.engineering")
    assert enabled is True
    assert rec.status == PluginStatus.RUNNING


def test_plugin_failure_isolation():
    pm = PluginManager()
    # Attempt to load nonexistent broken plugin
    res = pm.load_plugin("nonexistent.plugin")
    assert res is False
