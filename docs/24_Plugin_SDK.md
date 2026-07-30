# 24 — Plugin SDK

A plugin should look like this:

```
plugin/
├── manifest.json
├── src/
│   └── index.js
├── assets/
│   └── icon.png
├── widgets/
│   └── my-widget.json
├── templates/
│   └── my-template.json
└── docs/
    └── README.md
```

The Plugin SDK is one of Scilab Studio's strongest selling points. It makes the platform extensible without modifying core code.

For the Plugin Runtime component specification, see [21 — Component Specification §6](21_Component_Specification.md). For the event system that plugins use to communicate, see [23 — Event System](23_Event_System.md).

---

## 1. Plugin Lifecycle

```
Install
  │
  ▼
Validate
  │
  ▼
Register
  │
  ▼
Initialize
  │
  ▼
Execute
  │
  ▼
Unload
```

### 1.1 State Machine

```
                 ┌──────────────┐
      install    │              │
    ────────────►│  Installed   │
                 │              │
                 └──────┬───────┘
                        │ validate + register
                        ▼
                 ┌──────────────┐
                 │              │
                 │  Registered  │
                 │              │
                 └──────┬───────┘
                        │ initialize
                        ▼
                 ┌──────────────┐
     suspend     │              │   resume
    ┌───────────►│   Active     │◄──┐
    │            │              │   │
    │            └──┬───┬───┬──┘   │
    │               │   │   │      │
    │  deactivate   │   │   │ error│
    │  ┌────────────┘   │   └──────┘
    │  │                │
    │  ▼                ▼
    │  ┌──────────────┐ ┌──────────┐
    │  │              │ │          │
    │  │ Deactivating │ │  Error   │
    │  │              │ │          │
    │  └──────┬───────┘ └──────────┘
    │         │
    │         │ unregister
    │         ▼
    │  ┌──────────────┐
    │  │              │
    └──│ Unregistered │
       │              │
       └──────────────┘
```

### 1.2 Transitions

| From | To | Trigger | Actions |
|------|----|---------|---------|
| — | Installed | `install()` | Extract files, validate manifest |
| Installed | Registered | `register()` | Parse contributions, check dependencies |
| Registered | Active | `initialize()` | Call `activate()`, register event handlers |
| Active | Suspended | Memory pressure / user | Pause workers, release resources |
| Suspended | Active | User re-enables | Resume workers, re-register |
| Active | Deactivating | User disables / error | Unregister contributions, stop workers |
| Deactivating | Unregistered | Cleanup complete | Remove files, emit `plugin:uninstalled` |
| Any (except Unregistered) | Error | Unrecoverable error | Emit `plugin:error`, attempt graceful shutdown |

---

## 2. Manifest Schema

```jsonc
{
  "id": "com.example.my-plugin",         // Reverse-domain identifier (required)
  "name": "My Plugin",                   // Display name (required, 1–64 chars)
  "version": "1.0.0",                    // Semver (required)
  "description": "A helpful plugin",     // 0–512 chars (required)
  "author": {
    "name": "Jane Engineer",
    "email": "jane@example.com",
    "url": "https://example.com"
  },
  "license": "GPL-3.0-or-later",        // SPDX identifier (required)
  "repository": "https://github.com/...",
  "engines": {
    "scilab-studio": ">=0.2.0",         // Required platform version
    "scilab": ">=7.0.0"                 // Required Scilab version (if applicable)
  },
  "categories": ["visualization", "data-processing"],
  "keywords": ["chart", "plot", "analysis"],
  "icon": "assets/icon.png",
  "entry": "src/index.js",
  "permissions": [
    "fs:read",
    "engine:eval",
    "ui:panel"
  ],
  "dependencies": {},
  "contributes": {
    "panels": [
      {
        "id": "my-plugin-panel",
        "title": "My Panel",
        "location": "left",
        "icon": "chart-bar",
        "component": "MyPanel"
      }
    ],
    "commands": [
      {
        "id": "my-plugin.doSomething",
        "label": "Do Something",
        "category": "My Plugin",
        "shortcut": "Ctrl+Shift+M"
      }
    ],
    "menus": [
      {
        "path": "view/my-plugin",
        "label": "My Plugin Panel",
        "command": "my-plugin.doSomething"
      }
    ],
    "eventHandlers": [
      { "event": "engine:eval", "handler": "onEngineEval" }
    ],
    "rpcHandlers": [
      { "type": "my-plugin:process", "handler": "onProcessRequest" }
    ],
    "widgets": [
      { "path": "widgets/my-widget.json" }
    ],
    "templates": [
      { "path": "templates/my-template.json" }
    ],
    "settings": {
      "myPlugin.option1": {
        "type": "string",
        "default": "hello",
        "description": "A string option"
      },
      "myPlugin.option2": {
        "type": "number",
        "default": 42,
        "minimum": 0,
        "maximum": 100
      }
    }
  }
}
```

---

## 3. Entry Point API

```javascript
const { Plugin, logger } = require('@scilab-studio/sdk');

class MyPlugin extends Plugin {
  async activate(context) {
    // Register a panel
    context.registerPanel({
      id: 'my-plugin-panel',
      title: 'My Panel',
      location: 'left',
      icon: 'chart-bar',
      component: MyPanelComponent
    });

    // Register a command
    context.registerCommand({
      id: 'my-plugin.doSomething',
      label: 'Do Something',
      action: () => this.doSomething()
    });

    // Subscribe to events
    context.subscribe('engine:eval', (event) => {
      this.onEngineEval(event);
    });

    // Register an RPC handler
    context.handle('my-plugin:process', async (request) => {
      return await this.processData(request.payload);
    });

    logger.info('My Plugin activated');
  }

  async deactivate() {
    logger.info('My Plugin deactivated');
  }

  async suspend() {
    logger.info('My Plugin suspended');
  }

  async resume() {
    logger.info('My Plugin resumed');
  }
}

module.exports = MyPlugin;
```

---

## 4. Context API

### 4.1 Registration

```typescript
interface ModuleContext {
  registerPanel(config: PanelConfig): void;
  registerCommand(config: CommandConfig): void;
  registerMenu(config: MenuConfig): void;
  subscribe(eventType: string, handler: EventHandler): Subscription;
  handle(requestType: string, handler: RpcHandlerFn): Subscription;
}
```

### 4.2 Service Access

```typescript
interface ModuleContext {
  engine: {
    eval(code: string, timeout?: number): Promise<EvalResult>;
    getVariable(name: string): Promise<Variable>;
    setVariable(name: string, value: any): Promise<void>;
  };
  project: {
    getPath(): string;
    readFile(path: string): Promise<Uint8Array>;
    writeFile(path: string, content: Uint8Array | string): Promise<void>;
    listDir(path: string): Promise<FileEntry[]>;
  };
  data: {
    importFile(path: string, options?: ImportOptions): Promise<DataPreview>;
    exportData(data: any, path: string, format: string): Promise<void>;
  };
  ui: {
    showNotification(message: string, type: string): void;
    showOpenDialog(options: any): Promise<string | null>;
    showSaveDialog(options: any): Promise<string | null>;
    showConfirm(message: string): Promise<boolean>;
  };
  settings: {
    get(key: string): any;
    set(key: string, value: any): Promise<void>;
  };
  eventBus: EventBusEmitter & EventBusSubscriber;
}
```

---

## 5. Permissions

| Permission | Scope | Enforcement |
|------------|-------|-------------|
| `fs:read` | Read files within project directory | Path validation |
| `fs:write` | Write files within project directory | Path validation + file lock |
| `engine:eval` | Execute Scilab code | Timeout enforcement |
| `ui:panel` | Register UI panels | Panel ID registration |
| `ui:menu` | Add menu items | Menu path validation |
| `ui:notification` | Show notifications | Rate limiting (10/min) |
| `data:import` | Import external data | File type validation |
| `data:export` | Export data | Path validation |
| `network:http` | HTTP requests | Allowlist (marketplace only) |
| `system:exec` | OS commands | Blocked by default, runtime approval |

Plugins that attempt operations beyond their declared permissions are blocked and notified.

---

## 6. Sandboxing

- Plugins run in a sandboxed JavaScript context (V8 isolate).
- No access to Node.js APIs (`fs`, `child_process`, etc.).
- No access to browser APIs (`fetch`, `localStorage`, etc.).
- File access is limited to the project directory via `context.project.*`.
- Network access goes through `context.network.*` (allowlisted domains only).

---

## 7. Packaging

### 7.1 Archive Format

A plugin is packaged as a `.zip` file:

```
my-plugin-1.0.0.zip
└── my-plugin/
    ├── manifest.json
    ├── src/index.js
    ├── assets/icon.png
    └── ...
```

### 7.2 Publishing

```bash
scilab-studio plugin publish my-plugin/
```

1. Validate manifest.
2. Generate checksums.
3. Create archive.
4. Upload to marketplace registry.

### 7.3 Installation

Plugins are installed from:
1. **Marketplace:** Click "Install" in Plugin Manager.
2. **Local file:** Drag `.zip` onto Plugin Manager.
3. **CLI:** `scilab-studio plugin install path/to/plugin.zip`

Installation: extract to `~/.scilab-studio/plugins/<plugin-id>/`.

---

## 8. SDK Package

```typescript
export { Plugin } from './plugin';
export { logger } from './logger';
export type { ModuleContext, PanelConfig, CommandConfig, MenuConfig } from './types';
export type { EventHandler, RpcHandlerFn, Subscription } from './types';
export { debounce, throttle, generateId, validateManifest } from './utils';
```

The SDK is distributed with Scilab Studio. Plugins do not install it separately.

---

## 9. Testing

### Local Development

Place plugin directory in `~/.scilab-studio/plugins-dev/`. Run Scilab Studio with `--dev-plugins`. Dev plugins have relaxed sandboxing.

### Unit Testing

```javascript
const { createMockContext } = require('@scilab-studio/sdk/testing');

describe('MyPlugin', () => {
  let plugin, context;

  beforeEach(() => {
    plugin = new MyPlugin();
    context = createMockContext();
  });

  it('should activate successfully', async () => {
    await plugin.activate(context);
    expect(context.registerPanel).toHaveBeenCalled();
  });
});
```
