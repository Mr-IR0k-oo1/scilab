# Scilab Studio — Platform Architecture

**Version:** 1.0.0
**Status:** Normative
**Last Updated:** 2026-07-27

This document describes the platform infrastructure that powers Scilab Studio. For user-facing feature modules (GUI Builder, Visualization Studio, Data Studio, etc.), see [Feature Modules](05_Feature_Modules.md).

---

## 1. Overview

Scilab Studio is built on a set of platform services that provide the infrastructure for all feature modules. These services handle layout management, inter-module communication, extension management, scientific computation, project organization, configuration, state, file I/O, and rendering. Feature modules delegate to these services rather than implementing their own infrastructure.

| Service | Responsibility |
|---------|---------------|
| Workspace Manager | Panel layout, tabs, window state |
| Event Bus | Inter-module communication |
| Plugin Manager | Extension lifecycle and sandboxing |
| Scilab Integration Layer | Scientific computation bridge |
| Project Manager | Project structure and metadata |
| Configuration System | Settings hierarchy and merge |
| State Management | Shared observable state |
| File System Service | File operations and caching |
| Visualization Engine | Chart rendering pipeline |

---

## 2. Workspace Manager

**Purpose:** Manage the user's workspace layout — panels, tabs, toolbars, and window state.

**Responsibilities:**
- Render the workbench shell (menu bar, sidebar, editor area, status bar)
- Manage panel layout (left, right, bottom panels with resize)
- Manage tab lifecycle (open, close, reorder, activate)
- Persist workspace state across sessions
- Handle responsive breakpoints for window resize
- Provide the command palette (fuzzy search, keyboard shortcuts)
- Render notifications (toast, persistent)

**Inputs:**
- User actions (click, drag, keyboard)
- Module contributions (panels, menus, commands, toolbar items)
- Configuration changes (theme, layout preferences)

**Outputs:**
- Workspace state (panel visibility, sizes, active tabs)
- Events: `ui:panel:opened`, `ui:panel:closed`, `ui:theme:changed`, `ui:layout:changed`
- Layout snapshots (saved to `layouts/` directory)

**Dependencies:**
- Configuration System (for theme, layout preferences)
- State Management (for reactive layout state)

**Component Map:**
```
WorkspaceManager
├── MenuBar.svelte
├── Sidebar.svelte
│   ├── FileExplorer.svelte
│   ├── ModuleList.svelte
│   └── SearchPanel.svelte
├── EditorArea.svelte
│   ├── TabBar.svelte
│   └── TabContent.svelte
├── InspectorPanel.svelte
├── StatusBar.svelte
├── CommandPalette.svelte
└── NotificationCenter.svelte
```

---

## 3. Event Bus

**Purpose:** Provide the communication backbone for all inter-module interaction.

**Responsibilities:**
- Route events from emitters to subscribers
- Handle request/response patterns with timeout
- Manage shared state store
- Log events for debugging
- Enforce error handling (subscribers don't crash the bus)

**Inputs:**
- Module event emissions
- Module event subscriptions
- Request/response calls

**Outputs:**
- Dispatched events to subscribers
- Response values to requesters
- State change notifications
- Error events

**Dependencies:**
- None (this IS the dependency — everything depends on it)

**Communication Patterns:**

Pattern A — Event Bus (Fire-and-Forget):
```
Emitter → EventBus → Listener A
                   → Listener B
                   → Listener C
```

Pattern B — Request/Response:
```
Caller → EventBus → Provider
Caller ← EventBus ← Provider
```

Pattern C — Shared State:
```
Producer → Store.set() → Store → Consumer.get()
                                → Consumer.subscribe()
```

**Event Naming:** `domain:action[:detail]`

| Domain | Scope |
|--------|-------|
| system | Platform-wide |
| project | Current project |
| data | Data operations |
| engine | Scilab bridge |
| viz | Visualization |
| ui | User interface |
| plugin | Plugin system |

---

## 4. Plugin Manager

**Purpose:** Manage the lifecycle, permissions, and sandboxing of platform extensions.

**Responsibilities:**
- Discover plugins from the plugin directory
- Parse and validate plugin manifests (`plugin.json`)
- Resolve plugin dependencies
- Manage plugin lifecycle (install → load → activate → suspend → deactivate → uninstall)
- Enforce permissions via capability-based sandboxing
- Provide plugin APIs (menus, panels, commands, editors, visualizations)
- Handle plugin errors and recovery

**Inputs:**
- Plugin manifests (from filesystem or marketplace)
- User actions (install, enable, disable, uninstall)
- System events (startup, shutdown, memory pressure)

**Outputs:**
- Plugin state changes
- Registered contributions (menus, panels, commands)
- Plugin API surface for other plugins
- Events: `plugin:installed`, `plugin:activated`, `plugin:error`

**Dependencies:**
- Configuration System (plugin settings)
- File System Service (plugin file access)
- State Management (plugin state)

**Plugin Lifecycle:**
```
Discovered → Installed → Loaded → Active → Suspended → Deactivating → Uninstalled
```

**Contribution Points:**
| Point | Description |
|-------|-------------|
| menu | Application menu items |
| panel | UI panel components |
| command | Callable commands with keybindings |
| editor | Custom language support |
| visualization | Chart/visualization types |

---

## 5. Scilab Integration Layer

**Purpose:** Bridge the platform to the Scilab numerical computing engine.

**Responsibilities:**
- Manage Scilab process lifecycle (start, monitor, restart, stop)
- Send commands and receive results via JSON-RPC 2.0
- Marshal variables between Scilab and JSON types
- Handle computation timeouts and aborts
- Cache evaluation results
- Support multiple execution modes (embedded, child process, remote)

**Inputs:**
- Code evaluation requests
- Variable read/write requests
- Function call requests
- Working directory changes

**Outputs:**
- Evaluation results (typed JSON)
- Variable values
- Scilab output (stdout/stderr)
- Engine status (busy, idle, error)
- Events: `engine:eval:started`, `engine:eval:completed`, `engine:error`

**Dependencies:**
- File System Service (working directory)
- State Management (engine status)

**Protocol:** JSON-RPC 2.0 over stdin/stdout

**Methods:**
| Method | Description |
|--------|-------------|
| eval | Execute Scilab code |
| getVariable | Get variable value |
| setVariable | Set variable value |
| callFunction | Call Scilab function |
| getWorkingDirectory | Get current dir |
| setWorkingDirectory | Set current dir |
| getVariableNames | List variables |
| isBusy | Check engine status |
| abort | Abort computation |

---

## 6. Project Manager

**Purpose:** Manage the structure, metadata, and lifecycle of engineering projects.

**Responsibilities:**
- Create new projects (generate `project.json` + directory structure)
- Open existing projects (validate, load, emit events)
- Save projects (update `modified` timestamp, persist workspace state)
- Close projects (cleanup, release resources)
- Manage project metadata (name, description, modules, plugins)
- Validate project integrity

**Inputs:**
- User actions (create, open, save, close)
- Module state changes (module enable/disable)
- Plugin changes (install/uninstall)

**Outputs:**
- Project state (current project, metadata, settings)
- Events: `project:created`, `project:opened`, `project:saved`, `project:closed`
- `project.json` file updates

**Dependencies:**
- File System Service (read/write project files)
- Configuration System (project settings)
- State Management (project state)

---

## 7. Configuration System

**Purpose:** Manage platform and project settings with a three-level hierarchy.

**Responsibilities:**
- Merge global defaults → user overrides → project overrides
- Provide resolved configuration to all modules
- Detect and apply configuration changes
- Validate configuration values

**Three-Level Hierarchy:**
```
Global Defaults (built into binary)
    ↓ merged with (user wins)
User Overrides (~/.config/scilab-studio/user.json)
    ↓ merged with (project wins)
Project Overrides (<project>/project.json → "settings")
    ↓
Resolved Configuration
```

**Merge Rules:**
- Scalar values: higher level replaces lower
- Objects: recursive merge (higher adds/overrides keys)
- Arrays: replaced entirely (not concatenated)
- `undefined` does NOT delete lower-level keys

---

## 8. State Management

**Purpose:** Provide a shared observable state store for cross-module data access.

**Responsibilities:**
- Store key-value pairs with type safety
- Notify subscribers when values change
- Provide synchronous reads from cache
- Support reactive subscriptions

**API:**
```typescript
store.set(key: string, value: any): void
store.get(key: string): any
store.subscribe(key: string, callback: (value: any) => void): Unsubscribe
store.delete(key: string): void
```

**Use Cases:**
- Current project settings
- Active panel state
- Workspace layout
- Engine connection status
- Selected component in GUI Builder

---

## 9. File System Service

**Purpose:** Provide file operations with caching, watching, and project-scoped access.

**Responsibilities:**
- Read/write files within project directory
- Watch for file changes (hot reload)
- Cache frequently accessed files
- Provide file metadata (size, modified, type)
- Enforce project-scoped access (no reading outside project)

**Inputs:**
- Module file operations (read, write, delete, rename)
- File watch registrations

**Outputs:**
- File contents
- File metadata
- File change events: `fs:file:created`, `fs:file:modified`, `fs:file:deleted`

**Dependencies:**
- Tauri `fs` plugin (actual I/O)
- State Management (file cache)

---

## 10. Visualization Engine

**Purpose:** Provide the rendering infrastructure for all charts and visualizations.

**Responsibilities:**
- Manage canvas elements (create, reuse, destroy)
- Handle rendering pipeline (data → transform → render → export)
- Support Canvas 2D and WebGL renderers
- Manage animation frames (requestAnimationFrame)
- Handle chart export (PNG, SVG, PDF)
- Provide zoom, pan, tooltip interactions

**Inputs:**
- Chart configuration (type, data, styling)
- User interactions (zoom, pan, hover)
- Resize events

**Outputs:**
- Rendered charts (canvas elements)
- Exported images (PNG, SVG, PDF)
- Interaction events: `viz:clicked`, `viz:hovered`, `viz:zoomed`

**Dependencies:**
- State Management (chart state)
- Configuration System (default themes)

---

## 11. Cross-Cutting Concerns

These concerns span multiple platform services and are enforced consistently across the system.

### 11.1 Error Handling

All platform services follow a uniform error model:
- **Recoverable errors** are caught, logged, and surfaced via the Event Bus (`system:error`)
- **Fatal errors** (engine crash, corrupt project) trigger graceful degradation — the affected service enters an error state while the rest of the application remains responsive
- **Plugin errors** are isolated — a crashing plugin does not propagate to the host or other plugins

### 11.2 Lifecycle Management

Platform services respect a strict startup and shutdown order:

```
Startup:  Config → State → EventBus → FileSystem → Scilab → Plugins → Workspace
Shutdown: Workspace → Plugins → Scilab → FileSystem → State → EventBus → Config
```

Each service must implement `start()` and `stop()` methods. The Application Shell orchestrates this sequence and ensures all services are ready before accepting user input.

### 11.3 Performance Budget

| Metric | Target |
|--------|--------|
| Cold start (first paint) | < 2 seconds |
| Workspace restore | < 500ms |
| Event dispatch latency | < 5ms |
| File save to disk | < 100ms |
| Scilab eval (simple) | < 500ms |
| Chart render (1k points) | < 100ms |
| Memory baseline | < 200MB |

### 11.4 Security Model

- **Project sandboxing:** File System Service enforces project-scoped access — modules cannot read or write outside the active project directory
- **Plugin sandboxing:** Plugins run in a restricted capability model — they declare required permissions in `plugin.json` and are denied access to undeclared resources
- **Engine isolation:** Scilab runs as a child process with limited system access; communication is strictly JSON-RPC 2.0
- **No remote code execution:** All computation occurs locally — there is no mechanism for remote code injection

---

## 12. Service Interaction Map

```
┌─────────────────────────────────────────────────────────┐
│                    Application Shell                     │
│                   (Workspace Manager)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   ┌──────────┐   ┌──────────┐   ┌──────────────────┐   │
│   │  Plugin   │   │ Project  │   │  Scilab Engine   │   │
│   │ Manager   │◄──┤ Manager  │──►│    Integration   │   │
│   └────┬─────┘   └────┬─────┘   └────────┬─────────┘   │
│        │              │                   │              │
│        ▼              ▼                   ▼              │
│   ┌─────────────────────────────────────────────────┐   │
│   │                   Event Bus                      │   │
│   └─────────────────────────────────────────────────┘   │
│        ▲              ▲                   ▲              │
│        │              │                   │              │
│   ┌────┴─────┐   ┌────┴─────┐   ┌────────┴─────────┐   │
│   │  Config   │   │  State   │   │   File System    │   │
│   │  System   │   │Management│   │     Service      │   │
│   └──────────┘   └──────────┘   └──────────────────┘   │
│                                                          │
│   ┌─────────────────────────────────────────────────┐   │
│   │            Visualization Engine                   │   │
│   └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Appendix A: Technology Stack

| Layer | Technology |
|-------|------------|
| Desktop shell | Tauri 2.x (Rust backend, webview frontend) |
| Frontend | TypeScript + Svelte 5 |
| Sidecar | Rust (Scilab process management) |
| Storage | SQLite (project metadata, cache) |
| IPC protocol | JSON-RPC 2.0 |
| File watching | Tauri `fs` plugin (notify-based) |
| Canvas rendering | HTML5 Canvas 2D, WebGL 2.0 |
| Build system | Vite (frontend), Cargo (backend) |
| Package format | `.sxt` (Scilab Studio Extension) |
