# SPEC-005 — Plugin System

## Purpose

Allow third-party developers to extend Scilab Studio with new panels, commands, menu items, event handlers, widgets, and templates — without modifying core code.

---

## Plugin Structure

```
plugin/
├── manifest.json         # Identity, version, permissions, contributions
├── src/
│   └── index.js          # Entry point (exports Plugin subclass)
├── assets/
│   └── icon.png          # Plugin icon (128×128)
├── widgets/              # Optional widget definitions
│   └── my-widget.json
├── templates/            # Optional project templates
│   └── my-template.json
└── docs/
    └── README.md         # Documentation
```

---

## Plugin Manifest

```jsonc
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "Description here",
  "author": { "name": "Author" },
  "license": "GPL-3.0-or-later",
  "engines": {
    "scilab-studio": ">=0.2.0",
    "scilab": ">=7.0.0"
  },
  "permissions": ["fs:read", "engine:eval", "ui:panel"],
  "dependencies": {},
  "contributes": {
    "panels": [],
    "commands": [],
    "menus": [],
    "eventHandlers": [],
    "rpcHandlers": [],
    "widgets": [],
    "templates": [],
    "settings": {}
  }
}
```

---

## Versioning

- Plugins follow Semver (MAJOR.MINOR.PATCH).
- MAJOR: Breaking changes (removed contributions, changed API).
- MINOR: New features (new contribution types, new API methods).
- PATCH: Bug fixes, documentation.
- The platform validates `engines.scilab-studio` range on install.

---

## Dependencies

- Plugins can depend on other plugins via `dependencies` in manifest.
- The Plugin Manager resolves dependency order at activation.
- Circular dependencies are rejected at install time.
- Missing dependencies cause the plugin to enter `pending` state.

---

## Permissions

| Permission | Scope | Enforcement |
|------------|-------|-------------|
| fs:read | Read project files | Path validation |
| fs:write | Write project files | Path validation + lock |
| engine:eval | Execute Scilab code | Timeout enforcement |
| ui:panel | Register panels | Panel ID registration |
| ui:menu | Add menu items | Menu path validation |
| ui:notification | Show notifications | Rate limit (10/min) |
| data:import | Import data | File type validation |
| data:export | Export data | Path validation |
| network:http | HTTP requests | Allowlist only |
| system:exec | OS commands | Blocked by default |

---

## Lifecycle

```
Install → Validate → Register → Initialize → Execute → Unload
```

### State Machine

```
Installed → Registered → Active ↔ Suspended
                │            │
                ▼            ▼
             Error      Deactivating → Unregistered
```

### Transitions

| From | To | Trigger | Actions |
|------|----|---------|---------|
| — | Installed | install() | Extract, validate manifest |
| Installed | Registered | register() | Parse contributions, check deps |
| Registered | Active | initialize() | Call activate(), register handlers |
| Active | Suspended | Memory pressure | Pause workers, release resources |
| Suspended | Active | Resume | Re-register, resume workers |
| Active | Deactivating | Disable / error | Unregister, stop workers |
| Deactivating | Unregistered | Cleanup done | Remove files, emit event |
| Any → Error | Unrecoverable error | Log, notify user |

---

## API

### Plugin Class

```typescript
class Plugin {
  activate(context: ModuleContext): Promise<void>;
  deactivate(): Promise<void>;
  suspend(): Promise<void>;
  resume(): Promise<void>;
}
```

### ModuleContext

```typescript
interface ModuleContext {
  registerPanel(config: PanelConfig): void;
  registerCommand(config: CommandConfig): void;
  registerMenu(config: MenuConfig): void;
  subscribe(eventType: string, handler: EventHandler): Subscription;
  handle(requestType: string, handler: RpcHandlerFn): Subscription;
  getService<T>(name: string): T;
  getSetting(key: string): any;
  setSetting(key: string, value: any): Promise<void>;
}
```

---

## Extension Points

- Custom panel types.
- Custom command types.
- Custom event handlers.
- Custom widget types.
- Custom template types.
- Custom settings schemas.
- Custom export formats.

---

## Sandboxing

- Plugins run in a sandboxed JavaScript context (V8 isolate).
- No access to Node.js or browser APIs.
- File access limited to project directory.
- Network access through allowlisted domains only.
- Memory limit: 200MB per plugin (configurable).
- Heartbeat check every 30s. 3 missed heartbeats → suspended.

---

## Validation

On install:
1. Manifest schema validation.
2. Engine version compatibility check.
3. Dependency resolution.
4. Permission conflict detection.
5. File integrity check (checksums).

On activation:
1. Entry point import.
2. activate() call (with timeout).
3. Contribution registration validation.
4. Event handler registration.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max plugins active simultaneously | 50 |
| Plugin memory limit | 200MB |
| Heartbeat interval | 30s |
| Max missed heartbeats before suspend | 3 |
| Activation timeout | 10s |
| Max contributions per plugin | 100 |
