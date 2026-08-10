# Scilab Studio Plugin Development Guide

**SDK Version:** 0.1.0  
**API Version:** 1  

---

## 1. Quickstart: Creating a Plugin

Create a directory inside `plugins/examples/my_plugin/`:

### `plugin.json` Manifest
```json
{
  "id": "my.engineering.plugin",
  "name": "My Custom Engineering Plugin",
  "version": "0.1.0",
  "api_version": "1",
  "description": "Adds custom engineering components",
  "entrypoint": "plugin:MyPlugin",
  "capabilities": ["GUI_COMPONENT", "VISUALIZATION"]
}
```

### `plugin.py` Code
```python
from app.sdk import Plugin, PluginContext, GUIComponentMetadata

class MyPlugin(Plugin):
    def initialize(self, context: PluginContext) -> None:
        super().initialize(context)
        self.context.logger.info("Initializing MyPlugin...")

    def start(self) -> None:
        self.context.logger.info("MyPlugin started.")
```
