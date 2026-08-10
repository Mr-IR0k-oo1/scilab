import importlib.util
import os
import sys
from typing import Any, Tuple
from app.sdk.plugin import Plugin


class PluginLoader:
    @staticmethod
    def load_plugin_class(plugin_dir: str, entrypoint: str) -> Tuple[Any, str]:
        """
        Dynamically imports entrypoint (e.g. 'plugin:ExamplePlugin') from plugin_dir.
        Returns (plugin_instance, error_message).
        """
        try:
            if ":" not in entrypoint:
                return (None, f"Invalid entrypoint format '{entrypoint}'. Must be 'module:ClassName'")

            module_name, class_name = entrypoint.split(":", 1)
            module_file = os.path.join(plugin_dir, f"{module_name}.py")

            if not os.path.exists(module_file):
                return (None, f"Module file '{module_file}' does not exist.")

            spec = importlib.util.spec_from_file_location(f"scilab_plugin_{os.path.basename(plugin_dir)}", module_file)
            if spec is None or spec.loader is None:
                return (None, f"Could not create import spec for '{module_file}'")

            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)

            if not hasattr(mod, class_name):
                return (None, f"Class '{class_name}' not found in module '{module_name}'")

            cls = getattr(mod, class_name)
            instance = cls()
            if not isinstance(instance, Plugin):
                return (None, f"Class '{class_name}' does not inherit from app.sdk.Plugin")

            return (instance, "")

        except Exception as e:
            return (None, f"Failed to load plugin: {str(e)}")
