import re
from typing import List, Tuple
from app.sdk.manifest import PluginManifest
from app.sdk.version import PLUGIN_API_VERSION


class PluginValidator:
    @staticmethod
    def validate_manifest(manifest: PluginManifest) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        if not manifest.id or not re.match(r"^[a-zA-Z0-9_\-\.]+$", manifest.id):
            errors.append(f"Invalid plugin ID '{manifest.id}'. Must contain alphanumeric, dot, hyphen, underscore.")

        if not manifest.name:
            errors.append("Plugin name cannot be empty.")

        # API Version compatibility check
        if str(manifest.api_version) != str(PLUGIN_API_VERSION):
            errors.append(f"Incompatible Plugin API version '{manifest.api_version}'. Required: '{PLUGIN_API_VERSION}'.")

        # Basic SemVer check
        if not re.match(r"^\d+\.\d+\.\d+", manifest.version):
            errors.append(f"Invalid semantic version string '{manifest.version}'. Must follow X.Y.Z format.")

        return (len(errors) == 0, errors)
