# RFC-0002: Plugin API

| Field | Value |
|-------|-------|
| RFC | 0002 |
| Title | Plugin API |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how plugins are discovered, loaded, activated, and how they interact with the platform.

## Motivation

The plugin system is the primary extensibility mechanism. Third-party developers need a stable, well-documented API to build plugins without depending on internal implementation details.

## Detailed Design

### Plugin Lifecycle

```
Discovery → Activation → Running → Deactivation → Cleanup
```

1. **Discovery**: Plugin Manager scans configured directories for `plugin.json` manifests.
2. **Activation**: Plugin is loaded into a sandboxed context. `onActivate()` is called.
3. **Running**: Plugin is active. Subscribes to events, registers commands, renders UI.
4. **Deactivation**: `onDeactivate()` is called. Plugin releases resources.
5. **Cleanup**: Plugin context is torn down. Event subscriptions are removed.

### Plugin Manifest (plugin.json)

```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "A brief description",
  "author": "Author Name",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "scilab_version": ">=7.0",
  "main": "index.js",
  "permissions": ["scilab.execute", "storage.read", "ui.panel"],
  "dependencies": {},
  "contributes": {
    "commands": [],
    "menus": [],
    "panels": [],
    "settings": []
  }
}
```

### Plugin Context

Every plugin receives a `PluginContext` object:

```typescript
interface PluginContext {
  readonly id: string;
  readonly version: string;

  // Event system
  on(event: string, handler: EventHandler): Disposable;
  emit(event: string, data?: any): void;

  // Commands
  registerCommand(id: string, handler: CommandHandler): Disposable;

  // UI
  registerPanel(panel: PanelDescriptor): Disposable;
  registerMenu(menu: MenuDescriptor): Disposable;
  registerStatusBar(statusBar: StatusBarItem): Disposable;

  // Storage
  getStorage(): PluginStorage;

  // Scilab
  executeScilab(code: string): Promise<ScilabResult>;

  // Logger
  getLogger(): Logger;

  // Utilities
  showInformationMessage(message: string): void;
  showErrorMessage(message: string): void;
  showWarningMessage(message: string): void;
}
```

### Plugin Permissions

| Permission | Description |
|------------|-------------|
| `scilab.execute` | Execute Scilab commands |
| `scilab.read` | Read Scilab workspace variables |
| `scilab.write` | Write Scilab workspace variables |
| `storage.read` | Read plugin storage |
| `storage.write` | Write plugin storage |
| `ui.panel` | Register UI panels |
| `ui.menu` | Register menu items |
| `ui.statusbar` | Register status bar items |
| `ui.dialog` | Show dialog boxes |
| `file.read` | Read project files |
| `file.write` | Write project files |
| `network` | Make network requests |

### Sandboxing

- Plugins run in isolated JavaScript contexts.
- No access to Node.js APIs or file system outside plugin storage.
- Permissions are checked at runtime. Violations throw `PermissionDeniedError`.
- Plugins cannot access other plugins' storage or contexts.

### Error Handling

- Plugin errors are caught and logged. They do not crash the application.
- A plugin that throws repeatedly is automatically deactivated.
- Error details are shown in the plugin's output panel.

### Versioning

- Plugin API version follows the platform version.
- Plugins declare compatibility range in `scilab_studio_version`.
- Breaking changes increment the major version.
- Deprecated APIs are removed after 2 major versions.

## Alternatives Considered

1. **Web Worker sandboxing**: Stronger isolation but no access to DOM or shared state. Too restrictive.
2. **No sandboxing**: Simpler but risky. A bad plugin can crash the entire application.

## Security Considerations

- Permissions are requested in manifest and reviewed by user during installation.
- Network access requires explicit permission.
- File access is restricted to project directory.
- Plugins cannot modify other plugins or the core platform.

## Testing Strategy

- Unit tests for plugin loading and lifecycle.
- Integration tests for permission enforcement.
- Fuzzing tests for malicious plugin inputs.
- Performance tests for loading 50+ plugins.

## Rollout

- v0.1: Plugin system available but disabled (behind feature flag).
- v0.2: Plugin system enabled. Plugin Marketplace launches.
