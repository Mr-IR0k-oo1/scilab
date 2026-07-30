# 20 — Technical Architecture

This document describes the Scilab Studio runtime: how the application starts, how components are wired together, how they communicate, how they shut down, and what happens when things go wrong.

For the project file format, see [22 — Project File Format](22_Project_File_Format.md). For the event system, see [23 — Event System](23_Event_System.md). For individual component specifications, see [21 — Component Specification](21_Component_Specification.md).

---

## 1. System Overview

Scilab Studio is a desktop application built on Tauri. It has three processes:

```
┌──────────────────────────────────────────────────────────────┐
│                         Tauri Shell                           │
│                                                              │
│  ┌────────────────┐    IPC     ┌──────────────────────────┐  │
│  │ Renderer        │◄─────────►│ Core Process              │  │
│  │ (Svelte + TS)   │           │ (Rust)                    │  │
│  │                  │           │                           │  │
│  │ UI Components    │           │ Core Runtime              │  │
│  │ Widget Runtime   │           │ Module Loader             │  │
│  │ Layout Engine    │           │ Event Bus                 │  │
│  └────────────────┘           │ Service Registry           │  │
│                                │ Plugin Runtime             │  │
│                                │ Storage Layer              │  │
│                                └─────────┬────────────────┘  │
│                                          │ IPC               │
│                                ┌─────────▼────────────────┐  │
│                                │ Sidecar Process           │  │
│                                │ (Rust)                    │  │
│                                │                           │  │
│                                │ Scilab Runtime            │  │
│                                │ Command Queue             │  │
│                                │ Result Parser             │  │
│                                └─────────┬────────────────┘  │
│                                          │ stdio             │
│                                ┌─────────▼────────────────┐  │
│                                │ Scilab Engine             │  │
│                                │ (External, user-installed)│  │
│                                └──────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

| Process | Language | Responsibility |
|---------|----------|---------------|
| Renderer | TypeScript + Svelte | UI rendering, user interaction, layout management |
| Core | Rust (Tauri) | Business logic, plugin hosting, persistence, event routing |
| Sidecar | Rust | Scilab process lifecycle, JSON-RPC translation, command queuing |

The Renderer never touches the filesystem, network, or Scilab directly. Everything goes through Tauri IPC to the Core Process.

---

## 2. Core Runtime

The Core Runtime is the central coordinator. It owns all shared state and is responsible for wiring components together during startup and tearing them down during shutdown.

### 2.1 Components

```
Application
├── Core Runtime              Orchestrates startup, shutdown, and error recovery
├── Module Loader             Discovers, validates, and activates feature modules
├── Event Bus                 Routes events between all components
├── Service Registry          Maps service names to implementations
├── Workspace Manager         Manages layout, panels, tabs, and persistence
├── Plugin Runtime            Hosts third-party plugins in sandboxed contexts
├── Widget Runtime            Manages widget lifecycle and rendering bridge
├── Scilab Runtime            Commands Scilab through the sidecar process
└── Storage Layer             SQLite database, file system, and cache
```

### 2.2 Dependency Graph

Dependencies flow downward. A component can only depend on components above it in this list:

```
Core Runtime
    ↓
Module Loader
    ↓
Event Bus ←→ Service Registry
    ↓
Workspace Manager
    ↓
Plugin Runtime    Widget Runtime    Scilab Runtime
    ↓                  ↓                  ↓
              Storage Layer
```

No component below the Event Bus may call a component above it directly. All upward communication goes through events.

---

## 3. Lifecycle

### 3.1 Startup Sequence

The application follows a strict ordered startup. Each phase must complete before the next begins.

```
Phase 1: Bootstrap
├── Load user settings from disk
├── Initialize SQLite database
├── Run schema migrations if needed
└── Create Event Bus and Service Registry

Phase 2: Infrastructure
├── Register core services (fs, config, ipc)
├── Initialize Storage Layer
├── Start file watchers
└── Validate Scilab installation

Phase 3: Scilab Connection
├── Locate Scilab binary (env → config → PATH → defaults)
├── Spawn sidecar process
├── Wait for Scilab ready signal (30s timeout)
├── Run initialization script
└── Emit engine:connected

Phase 4: Module Loading
├── Scan bundled modules directory
├── Scan user-installed plugins directory
├── Parse and validate all manifests
├── Resolve dependency graph
├── Detect circular dependencies (fatal if found)
└── Sort into activation order

Phase 5: Module Activation
├── For each module in dependency order:
│   ├── Call module.activate(context)
│   ├── Register contributed panels, commands, menus
│   ├── Subscribe to events
│   └── Emit module:activated
└── Emit all:ready

Phase 6: UI Rendering
├── Load last workspace layout (or welcome screen)
├── Restore open tabs and panel states
├── Render initial UI
└── Application is interactive
```

### 3.2 Shutdown Sequence

Shutdown is the reverse of startup, with explicit resource cleanup.

```
Phase 1: User Intent
├── User clicks Quit or sends OS signal
├── Emit app:shutting-down (allows modules to save state)

Phase 2: Module Deactivation
├── For each module in reverse dependency order:
│   ├── Save any unsaved module state
│   ├── Unregister contributed panels, commands, menus
│   ├── Unsubscribe from events
│   ├── Call module.deactivate()
│   └── Emit module:deactivated

Phase 3: Persistence
├── Save current workspace layout
├── Save project.json (if project is open)
├── Flush SQLite WAL to disk
├── Close file watchers
└── Save user settings if modified

Phase 4: Scilab Cleanup
├── Send abort if computation is running
├── Send SIGTERM to Scilab process
├── Wait up to 5 seconds for graceful exit
├── Send SIGKILL if still running
└── Close sidecar process

Phase 5: Final
├── Close SQLite connection
├── Stop Event Bus
└── Exit process
```

### 3.3 Crash Recovery

If the application crashes:

1. The OS-level process terminates. No cleanup runs.
2. On next startup, the Core Runtime checks for a lock file in the project directory.
3. If a lock file exists, the project was not cleanly closed. The platform:
   - Recovers the last auto-save from `.scstudio/emergency/`.
   - Offers the user a "Restore Session" dialog.
   - If accepted, restores tabs, layout, and unsaved changes.
   - If declined, opens the project normally (last clean state).
4. The lock file is removed.

Lock file format: `.scstudio/lock` containing `{ "pid": 12345, "started": "ISO8601" }`.

---

## 4. Dependency Injection

Scilab Studio uses a service locator pattern (not constructor injection) because modules are loaded dynamically and cannot have compile-time dependencies on each other.

### 4.1 Service Registry

The Service Registry is a global map of named service interfaces to implementations.

```typescript
interface ServiceRegistry {
  register(name: string, service: any): void;
  get<T>(name: string): T;
  has(name: string): boolean;
  unregister(name: string): void;
}
```

### 4.2 Core Services

| Service Name | Interface | Provided By |
|-------------|-----------|-------------|
| `fs` | File system access | Storage Layer |
| `config` | Settings and project configuration | Core Runtime |
| `ipc` | Tauri IPC bridge | Core Runtime |
| `engine` | Scilab command execution | Scilab Runtime |
| `events` | Event Bus | Core Runtime |
| `workspace` | Layout and panel management | Workspace Manager |
| `plugins` | Plugin lifecycle management | Plugin Runtime |
| `widgets` | Widget lifecycle management | Widget Runtime |
| `db` | SQLite database access | Storage Layer |
| `logger` | Structured logging | Core Runtime |

### 4.3 Module Context

When a module is activated, it receives a `ModuleContext` object that provides access to the Service Registry and module-specific APIs:

```typescript
interface ModuleContext {
  // Service access
  getService<T>(name: string): T;

  // Registration
  registerPanel(config: PanelConfig): void;
  registerCommand(config: CommandConfig): void;
  registerMenu(config: MenuConfig): void;

  // Events
  subscribe(eventType: string, handler: EventHandler): Subscription;
  emit(eventType: string, payload: any): void;

  // Settings
  getSetting(key: string): any;
  setSetting(key: string, value: any): Promise<void>;

  // Scilab
  eval(code: string, timeout?: number): Promise<EvalResult>;
}
```

Modules never hold references to other modules. They discover services by name at runtime.

---

## 5. Error Handling

### 5.1 Error Categories

| Category | Example | Severity | Recovery |
|----------|---------|----------|----------|
| User Error | Invalid file name | Low | Inline validation message |
| Data Error | Malformed CSV | Medium | Import error dialog with details |
| Module Error | Plugin threw exception | Medium | Disable module, notify user |
| Scilab Error | Runtime exception | Medium | Show in console, preserve workspace |
| Bridge Error | Scilab process crashed | High | Auto-restart, notify user |
| Platform Error | SQLite corruption | High | System error dialog, offer recovery |
| Fatal Error | Out of memory | Critical | Emergency snapshot, crash dialog |

### 5.2 Error Propagation

```
Error Origin
    │
    ├──► Tagged with category + severity
    │
    ├──► Logged to SQLite errors table
    │    (timestamp, category, message, stack, context)
    │
    ├──► Published to Event Bus as system:error
    │
    └──► Displayed to user via notification system
         (toast for low/medium, modal for high/critical)
```

### 5.3 Error Boundaries

Each major component has an error boundary. If a component throws during initialization:

1. The error is caught by the Core Runtime.
2. The component is marked as `failed`.
3. Dependent components are notified and enter degraded mode.
4. The user sees which features are unavailable and why.
5. The application continues running with remaining components.

No single component failure should crash the entire application (except Core Runtime itself).

### 5.4 Retry Policy

| Scenario | Retries | Delay | Backoff |
|----------|---------|-------|---------|
| Scilab crash | 3 in 60s | 2s | Fixed |
| Plugin activation failure | 1 | 0s | None |
| File write (disk full) | 0 | — | Show error |
| Marketplace fetch | 3 | 1s, 2s, 4s | Exponential |
| SQLite busy | 5 | 100ms | Fixed |

---

## 6. Concurrency Model

### 6.1 Renderer Process

Single-threaded (browser main thread). Svelte's reactivity system batches DOM updates. Long-running computations (large chart renders, data processing) are offloaded to Web Workers where possible.

### 6.2 Core Process

Async I/O via Tokio. Key long-running tasks:

| Task | Lifetime | Purpose |
|------|----------|---------|
| `ipc_listener` | Application | Receives commands from Renderer |
| `event_dispatcher` | Application | Routes events to subscribers |
| `plugin_supervisor` | Application | Monitors plugin health |
| `sidecar_supervisor` | Application | Monitors Scilab process |
| `file_watcher` | Project | Watches project directory |
| `sqlite_pool` | Application | Database connection pool |

### 6.3 Thread Safety Rules

- The Event Bus is the only cross-thread communication mechanism.
- Shared state is protected by `tokio::sync::RwLock` (multiple readers, single writer).
- File writes are serialized per-file (advisory locking).
- Plugin state is isolated per-plugin (no shared mutable state between plugins).

---

## 7. Configuration

### 7.1 Configuration Sources (priority order)

```
1. Project settings     (.scstudio/project.json → settings)
2. User settings        (~/.config/scilab-studio/settings.json)
3. Platform defaults    (compiled into binary)
```

### 7.2 User Settings

```jsonc
{
  "engine": {
    "path": null,                      // Auto-detect if null
    "mode": "child-process",           // "child-process" | "managed"
    "timeout": 60000,
    "autoStart": true
  },
  "editor": {
    "fontSize": 14,
    "tabSize": 2,
    "wordWrap": "on",
    "theme": "dark",
    "fontFamily": "JetBrains Mono, monospace"
  },
  "plugins": {
    "autoUpdate": true,
    "sandboxMemoryMB": 200
  },
  "visualization": {
    "renderer": "webgl",
    "defaultTheme": "dark"
  },
  "data": {
    "maxPreviewRows": 1000,
    "csvDelimiter": "auto",
    "csvEncoding": "auto"
  },
  "reports": {
    "defaultFormat": "pdf",
    "pageSize": "A4"
  },
  "ui": {
    "sidebarWidth": 250,
    "rightPanelWidth": 300,
    "bottomPanelHeight": 200
  }
}
```

### 7.3 Settings Resolution

When a setting is accessed:
1. Check project `settings` in `project.json`.
2. If absent, check user `settings.json`.
3. If absent, use compiled default.

Settings changes are persisted immediately. Project-level changes go to `project.json`. User-level changes go to `settings.json`.

---

## 8. Performance Budgets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cold start | < 3s | Launch to first paint |
| Warm start | < 1s | Launch to restored workspace |
| Panel switch | < 100ms | Click to panel fully rendered |
| File open | < 500ms | Double-click to editor tab |
| Scilab eval (simple) | < 500ms | Request to result displayed |
| Chart render (10k points) | < 1s | Data load to visible |
| Project save | < 500ms | Ctrl+S to saved indicator |
| Memory (idle) | < 300 MB | Renderer + Core + Sidecar |
| Memory (active) | < 800 MB | With Scilab running, one project open |
| Plugin activation | < 200ms | activate() call to registered |

---

## 9. Platform Abstractions

### 9.1 File System

All file operations go through a platform abstraction that handles:
- Path normalization (forward slashes internally, OS-native for display)
- Case sensitivity (case-sensitive Linux/macOS, case-insensitive Windows)
- Symbolic link resolution
- File permission checks

### 9.2 Scilab Discovery

The Sidecar locates Scilab through a search order:

1. `SCILAB_PATH` environment variable
2. User setting `engine.path`
3. Platform default paths:
   - Linux: `/usr/bin/scilab`, `/usr/local/bin/scilab`, `/opt/scilab/bin/scilab`
   - macOS: `/Applications/Scilab.app/Contents/MacOS/bin/scilab`
   - Windows: `C:\Program Files\Scilab\bin\scilab.exe`
4. System PATH lookup
5. Not found → show Scilab Setup Dialog, block engine features

### 9.3 Window Management

Tauri handles cross-platform windowing transparently. The application does not use platform-specific windowing APIs directly.

| Platform | Webview | Notes |
|----------|---------|-------|
| Linux | WebKitGTK | Default on most distributions |
| macOS | WKWebView | Native Cocoa integration |
| Windows | WebView2 | Edge Chromium, auto-installed |
