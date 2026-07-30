# Scilab Studio — System Architecture

**Version:** 2.0.0
**Status:** Normative
**Last Updated:** 2026-07-27

---

## 1. Architecture Goals

The following seven principles guide every architectural decision in Scilab Studio. They are ordered by importance — when principles conflict, earlier principles take precedence.

### 1.1 Modular
Every feature is an independent module with well-defined interfaces. Modules communicate through the event bus and shared state, never through direct imports.
**Why it matters:** Teams can develop, test, and ship modules independently.

### 1.2 Plugin-First
Built-in modules and third-party plugins follow the same lifecycle, contribution points, and permission model.
**Why it matters:** The platform grows without core changes.

### 1.3 Event-Driven
Modules communicate through events via fire-and-forget broadcasts, request/response RPC, and observable shared state.
**Why it matters:** Loose coupling lets modules be added, removed, or replaced without refactoring consumers.

### 1.4 Open-Source Friendly
GPL v3, no proprietary dependencies. All dependencies are auditable, all builds reproducible.
**Why it matters:** No license contamination or vendor lock-in.

### 1.5 Educational
Prioritizes learning use cases, guided workflows, and accessible design. The Learning Center and project templates are core features.
**Why it matters:** Students and educators benefit from scaffolding and progressive disclosure of complexity.

### 1.6 Cross-Platform
Linux, macOS, and Windows with identical behavior. Platform differences are abstracted behind Tauri and the Rust sidecar.
**Why it matters:** Heterogeneous environments are the norm in engineering teams and classrooms.

### 1.7 Separation of Concerns
Infrastructure (event bus, plugin manager, configuration, file system) is distinct from user-facing features. Infrastructure knows nothing about features; features depend only on infrastructure.
**Why it matters:** Infrastructure evolves without breaking features; features swap without rebuilding infrastructure.

---

## 2. High-Level Architecture

```
                    Scilab Studio

                ┌──────────────────┐
                │   User Interface │
                │  (Svelte + TS)   │
                └────────┬─────────┘
                         │
                ┌────────▼─────────┐
                │ Workspace Manager│
                │  (layout, tabs,  │
                │   panels)        │
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────────┐
          │              │                  │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌────────▼────────┐
    │GUI Builder│  │ Viz Studio│  │ Project Manager  │
    │           │  │           │  │ (project.json,   │
    │           │  │           │  │  file structure) │
    └─────┬─────┘  └─────┬─────┘  └────────┬────────┘
          │              │                  │
          └──────────────┼──────────────────┘
                         │
                ┌────────▼────────┐
                │   Event Bus     │
                │  (pub/sub +     │
                │   request/resp) │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │ Plugin Manager  │
                │  (load, sandbox,│
                │   lifecycle)    │
                └────────┬────────┘
                         │
                ┌────────▼────────┐
                │ Scilab Engine   │
                │  (via JSON-RPC  │
                │   bridge)       │
                └────────┬────────┘
                         │
              Scientific Computation
                         │
                ┌────────▼────────┐
                │   File System   │
                │  (project dirs, │
                │   SQLite meta)  │
                └─────────────────┘
```

### Layer Descriptions

**User Interface** — The visual layer the user interacts with: panels, menus, toolbars, the command palette, and all rendered components. Built with Svelte 5 and TypeScript, it holds no business logic. It dispatches events and observes shared state, reacting to changes without polling.

**Workspace Manager** — Manages the physical layout of the application: which panels are open, their sizes, the active tab, and layout persistence. It coordinates panel lifecycle without knowing what each panel renders. Layout state is serialized to `project.json` on close and restored on open.

**Feature Modules** — User-facing tools that provide specific capabilities: GUI Builder (drag-and-drop component placement with 9 component types), Visualization Studio (Line, Scatter, Bar, Heatmap charts), Project Manager (file operations and project metadata), Data Studio (CSV/Excel import and transformation), Report Generator (PDF/HTML output), Learning Center (examples and tutorials). Each module owns its UI panels and Scilab interactions but communicates through the event bus.

**Event Bus** — The communication backbone. All inter-module communication flows through the event bus using three patterns described in §4: fire-and-forget broadcasts, request/response RPC, and observable shared state. No module imports another module's code.

**Plugin Manager** — The extension system. Discovers, loads, sandboxes, and manages plugin lifecycles through declared contribution points. Plugins contribute panels, commands, menu items, visualization types, and language support. The manager enforces permissions and handles memory pressure by suspending resource-heavy plugins.

**Scilab Engine** — The scientific computation backend. A Rust sidecar process spawns and communicates with Scilab over JSON-RPC 2.0 via stdin/stdout. All scientific computation — evaluation, variable manipulation, function calls — flows through this layer. The sidecar handles process lifetime, crash recovery, and timeout enforcement.

**File System** — Data persistence. Project directories store user files, scripts, data, and reports. SQLite stores metadata, settings, and plugin registries. The file system layer enforces path restrictions (plugins are sandboxed), provides atomic writes, and watches for external changes.

---

## 3. Core Components

### 3.1 Workspace Manager
**Purpose:** Manages application layout — panels, tabs, split views, and spatial arrangement.
**Responsibilities:** Create/destroy/resize panels; manage tab lifecycle; persist layout to `project.json`; coordinate drag-and-drop; enforce size constraints.
**Inputs:** `ui:panel:open`, `ui:panel:close`, `ui:panel:resize` events; layout state from shared store.
**Outputs:** Panel DOM elements for feature modules; `ui:layout:changed` events; serialized layout for persistence.
**Dependencies:** Event Bus, Shared State, Configuration System.

### 3.2 Event Bus
**Purpose:** All inter-module communication through fire-and-forget, request/response, and observable shared state.
**Responsibilities:** Route events to subscribers by name; route request events to the single provider; enforce naming conventions; log errors without crashing subscribers; maintain error log (last 500); reject events during shutdown.
**Inputs:** `emit(name, payload)`, `request(name, payload, opts?)`, subscriber registrations.
**Outputs:** Dispatched events to subscribers; response promises; error events; `system:event:error` on exceptions.
**Dependencies:** None (standalone infrastructure).

### 3.3 Plugin Manager
**Purpose:** Discovers, loads, sandboxes, and manages the full plugin lifecycle.
**Responsibilities:** Discover plugins from directories; validate `plugin.json` manifests; resolve dependency graphs; enforce lifecycle state machine; apply permission checks; suspend under memory pressure; emit lifecycle events.
**Inputs:** Plugin directories; `plugin:install`, `plugin:activate`, `plugin:deactivate` events; memory pressure signals.
**Outputs:** Registered contribution points; `plugin:installed`, `plugin:activated`, `plugin:error` events; memory usage reports per plugin.
**Dependencies:** Event Bus, Configuration System, File System Service.

### 3.4 Scilab Integration Layer
**Purpose:** Typed API for communicating with the Scilab engine through a Rust sidecar via JSON-RPC 2.0 over stdin/stdout.
**Responsibilities:** Spawn/manage Scilab child process; serialize requests and deserialize responses; marshal Scilab types to/from JSON; enforce timeouts; provide automatic reconnection; expose `eval`, `getVariable`, `setVariable`, `callFunction`, `abort`.
**Inputs:** `engine:eval`, `engine:getVariable`, `engine:setVariable` requests; Scilab stdout; process lifecycle signals.
**Outputs:** JSON-RPC responses; `engine:variable:changed` events; `engine:process:started/stopped` events.
**Dependencies:** File System Service, Configuration System.

### 3.5 Project Manager
**Purpose:** Manages project creation, opening, closing, and metadata. Enforces `project.json` schema.
**Responsibilities:** Create projects with standard directory structure; open/validate `project.json`; save metadata; track recent projects; enforce field constraints; emit lifecycle events.
**Inputs:** `project:create`, `project:open`, `project:save`, `project:close` events.
**Outputs:** Validated project state to shared store; `project:created/opened/saved/closed` events.
**Dependencies:** Event Bus, Configuration System, File System Service.

### 3.6 Configuration System
**Purpose:** Manages three-level hierarchy (global defaults, user overrides, project overrides).
**Responsibilities:** Load all three levels; deep-merge with last-write-wins; expose resolved immutable config; re-merge on changes; emit `system:config:changed`.
**Inputs:** Configuration files; `system:config:change` events.
**Outputs:** Resolved configuration object; `system:config:changed` event.
**Dependencies:** File System Service.

### 3.7 State Management
**Purpose:** Observable shared state for frequently read data.
**Responsibilities:** Store key-value pairs; notify subscribers on changes; provide synchronous cache reads; support reactive subscriptions by key.
**Inputs:** `store.set(key, value)`, `store.subscribe(key, callback)`.
**Outputs:** Synchronous `store.get(key)` reads; `state:changed` events.
**Dependencies:** Event Bus.

### 3.8 File System Service
**Purpose:** Controlled file system access with path restrictions, atomic writes, and file watching.
**Responsibilities:** Enforce path restrictions; atomic write operations; watch directories for changes; manage file caches with LRU eviction; generate integrity hashes.
**Inputs:** File read/write requests; file system watcher callbacks.
**Outputs:** File contents, metadata, hashes; `data:file:changed/created/deleted` events.
**Dependencies:** Configuration System.

### 3.9 Visualization Engine
**Purpose:** Renders charts using Canvas 2D (standard) and WebGL (high-performance/3D).
**Responsibilities:** Render Line, Scatter, Bar, Heatmap charts; manage canvas/WebGL contexts; handle resize, zoom, pan, tooltips; export to PNG/SVG/PDF; downsample large datasets; support plugin-contributed types.
**Inputs:** `viz:render:*` requests; `viz:resize` events; data from Data Studio or Scilab.
**Outputs:** Rendered canvas/WebGL output; `viz:render:completed`, `viz:export:completed` events.
**Dependencies:** Event Bus, Shared State, File System Service.

---

## 4. Module Interaction

### 4.1 Pattern A: Event Bus (Fire-and-Forget)

Use when the emitter does not need a return value.

```
┌──────────┐   emit(event)    ┌──────────┐   dispatch    ┌──────────┐
│ Emitter  │────────────────▶│ EventBus │──────────────▶│ Listener A│
│          │                  │          │──────────────▶│          │
└──────────┘                  └──────────┘               │ Listener B│
                                                         └──────────┘
```

**When to use:** Broadcasting side-effects, logging, UI state changes.
**Example:** After importing a CSV, the Data Studio emits `data:loaded:csv` with row count, column names, and a preview. Multiple listeners react independently.

### 4.2 Pattern B: Request/Response (RPC)

Use when the caller needs a return value.

```
┌──────────┐  request(req)    ┌──────────┐  route      ┌──────────┐
│ Caller   │────────────────▶│ EventBus │────────────▶│ Provider │
│          │  response(val)  │          │◀────────────│          │
│          │◀────────────────│          │  respond     │          │
└──────────┘                  └──────────┘             └──────────┘
```

**When to use:** Evaluating code, exporting charts, reading variables, querying state.
**Timeout:** Default 30s, configurable via `opts.timeout`. Timed-out requests reject with `ErrorCode.TIMEOUT`.

### 4.3 Pattern C: Shared State (Observable Store)

Use for frequently accessed data that multiple consumers read.

```
┌──────────┐  store.set(key, val)  ┌────────────┐
│ Producer │──────────────────────▶│ SharedState │
└──────────┘                       │ Store       │
┌──────────┐  store.get(key)      │             │
│Consumer A│◀─────────────────────│  ┌────────┐ │
└──────────┘  store.subscribe(key)│  │ Cache  │ │
┌──────────┐◀─────────────────────│  └────────┘ │
│Consumer B│                      └────────────┘
└──────────┘
```

**When to use:** Project settings, workspace layout, active panel state.
**Example:** `store.set('workspace.activePanel', 'viz-studio')` triggers `state:changed` for all subscribers.

### 4.4 Event Naming Convention

All events follow `domain:action:detail` (lowercase kebab-case).

| Domain | Scope | Example Events |
|--------|-------|----------------|
| `system` | Platform-wide | `startup`, `shutdown`, `health` |
| `project` | Current project | `saved`, `opened`, `closed` |
| `data` | Data operations | `loaded`, `transformed`, `exported` |
| `engine` | Scilab bridge | `eval`, `variable:changed` |
| `viz` | Visualization | `render`, `resize`, `export` |
| `ui` | User interface | `panel:opened`, `theme:changed` |
| `plugin` | Plugin system | `installed`, `activated`, `error` |

### 4.5 Event Payload Schema

```typescript
interface EventEnvelope<T = unknown> {
  id: string;                    // UUID v4
  name: string;                  // domain:action:detail
  timestamp: string;             // ISO 8601
  correlationId?: string;        // For request/response tracing
  source: string;                // Emitting domain
  payload: T;
  meta?: Record<string, unknown>;
}
```

**Concrete payload examples:**

```typescript
interface DataLoadedCsvPayload {
  sourceId: string;
  filePath: string;
  rowCount: number;
  columnNames: string[];
  columnTypes: ('number' | 'string' | 'boolean' | 'date')[];
  preview: unknown[][];
  totalBytes: number;
}

interface VizRenderLinePayload {
  chartId: string;
  datasetIds: string[];
  config: {
    x: { label: string; axis: 'linear' | 'log' };
    y: { label: string; axis: 'linear' | 'log' };
    color: string;
    lineWidth: number;
    smooth: boolean;
  };
}

interface EngineVariableChangedPayload {
  name: string;
  previousValue: ScilabValue | null;
  newValue: ScilabValue;
  source: 'user' | 'script' | 'ai';
}
```

### 4.6 Error Handling

```typescript
interface EventBusError {
  code: ErrorCode;
  message: string;
  eventName: string;
  cause?: Error;
  retried: boolean;
}

enum ErrorCode {
  NO_HANDLER    = 'EVENT_NO_HANDLER',
  HANDLER_FAILED = 'EVENT_HANDLER_FAILED',
  TIMEOUT       = 'EVENT_TIMEOUT',
  INVALID_NAME  = 'EVENT_INVALID_NAME',
  PAYLOAD_INVALID = 'EVENT_PAYLOAD_INVALID',
  BUS_STOPPED   = 'EVENT_BUS_STOPPED',
}
```

**Rules:** Subscriber errors are caught, logged, and emitted as `system:event:error` — other subscribers continue. Request handler errors reject the caller's promise with an `EventBusError`. The event bus maintains the last 500 errors, accessible via `eventBus.getErrorLog()`. During shutdown, new emits are rejected with `BUS_STOPPED` and in-flight requests are cancelled with `TIMEOUT`.

---

## 5. Plugin Architecture

### 5.1 Plugin Manifest (plugin.json)

Every plugin ships a `plugin.json` at its root. This manifest declares the plugin's identity, dependencies, permissions, and contribution points.

```jsonc
{
  "$schema": "https://scilab-studio.dev/schemas/plugin-v1.json",
  "id": "com.example.signal-analyzer",
  "name": "Signal Analyzer",
  "version": "1.3.0",
  "description": "Advanced signal processing tools for time-series data",
  "author": "Jane Doe <jane@example.com>",
  "license": "MIT",
  "entry": "dist/index.js",
  "engines": {
    "scilab-studio": ">=0.1.0",
    "scilab": ">=2024.0.0"
  },
  "dependencies": {
    "com.example.data-utils": "^2.0.0"
  },
  "permissions": ["fs:read", "fs:write", "engine"],
  "contributions": {
    "menu": [
      { "id": "signal-analyzer.menu.tools", "label": "Signal Analyzer", "command": "signal-analyzer.openPanel" }
    ],
    "panel": [
      { "id": "signal-analyzer.panel.main", "title": "Signal Analyzer", "entry": "dist/panel.js", "location": "right" }
    ],
    "command": [
      { "id": "signal-analyzer.openPanel", "label": "Open Signal Analyzer", "handler": "openPanel", "keybinding": "Ctrl+Shift+S" },
      { "id": "signal-analyzer.analyze", "label": "Run Signal Analysis", "handler": "runAnalysis" }
    ],
    "editor": [
      { "id": "signal-analyzer.lang.scs", "language": "scilab-signal", "entry": "dist/editor.js" }
    ],
    "visualization": [
      { "id": "signal-analyzer.viz.spectrum", "type": "spectrum-plot", "entry": "dist/viz/spectrum.js" }
    ]
  }
}
```

### 5.2 Permission Values

| Permission | Description |
|-----------|-------------|
| `fs:read` | Read within project and plugin data directory |
| `fs:write` | Write within project and plugin data directory |
| `fs:read:global` | Read outside project (sandboxed path list) |
| `fs:write:global` | Write outside project (sandboxed path list) |
| `network` | Outbound HTTP/HTTPS to declared hosts |
| `network:unrestricted` | Outbound requests to any host |
| `engine` | Access Scilab engine (eval, variables, functions) |
| `engine:write` | Modify Scilab variables and workspace state |
| `ui` | Access UI APIs (panels, menus, notifications) |

### 5.3 Contribution Points

| Point | Description | Fields |
|-------|-------------|--------|
| `menu` | Application menu items | `id`, `label`, `command`, `parent?` |
| `panel` | Panel component | `id`, `title`, `entry`, `location` (left/right/bottom) |
| `command` | Callable commands | `id`, `label`, `handler`, `keybinding?` |
| `editor` | Language support | `id`, `language`, `entry` |
| `visualization` | Chart type | `id`, `type`, `entry` |

### 5.4 Lifecycle State Machine

Every plugin follows a strict lifecycle managed by the Plugin Manager. The state machine ensures that plugins are loaded, activated, and deactivated in a controlled manner, preventing resource leaks and ensuring consistent behavior.

```
                   ┌──────────────────────────────────────────┐
                   ▼                                          │
             ┌────────────┐                                   │
             │ Discovered │                                   │
             └─────┬──────┘                                   │
                   │ load manifest, resolve deps              │
                   ▼                                          │
             ┌────────────┐                                   │
             │ Installed  │                                   │
             └─────┬──────┘                                   │
                   │ import entry, register hooks             │
                   ▼                                          │
             ┌────────────┐                                   │
             │   Loaded   │                                   │
             └─────┬──────┘                                   │
                   │ activate contributions                   │
                   ▼                                          │
             ┌────────────┐     memory pressure / user       │
             │   Active   │──────────────────────┐           │
             └─────┬──────┘                       │           │
                   │ disable                      ▼           │
                   ▼                        ┌────────────┐    │
             ┌────────────┐                 │ Suspended  │    │
             │Deactivating│                 └─────┬──────┘    │
             └─────┬──────┘                       │ reactivate│
                   │                              └───────────┘
                   │ uninstall
                   ▼
             ┌────────────┐
             │ Uninstalled│
             └────────────┘
```

**Transitions:**

| From | To | Trigger | Actions |
|------|----|---------|---------|
| — | Discovered | Manifest found | Parse, validate schema |
| Discovered | Installed | Deps resolved, engine compatible | Install to store, copy to `.scilab-studio/plugins/` |
| Installed | Loaded | `plugin.load()` called | Import entry, call `activate()`, register hooks |
| Loaded | Active | `activate()` succeeds | Register contributions, start background tasks |
| Active | Suspended | Memory pressure or user | Pause workers, release resources, keep state |
| Suspended | Active | User re-enables | Resume workers, re-register contributions |
| Active | Deactivating | User disables | Unregister contributions, stop workers |
| Deactivating | Uninstalled | User confirms | Remove files, clean data dir, emit `plugin:uninstalled` |
| Any (except Uninstalled) | — | Unrecoverable error | Emit `plugin:error`, transition to deactivating |

---

## 6. Workspace Structure

### 6.1 Directory Layout

Every Scilab Studio project follows a standard directory structure. This ensures consistency across projects and allows the platform to locate files predictably.

```
project/
├── project.json              # Project manifest
├── layouts/                  # Panel layout snapshots
│   ├── default.json
│   └── simulation.json
├── scripts/                  # User scripts and Scilab code
│   ├── main.sce
│   └── utilities/
├── data/                     # Datasets
│   ├── measurements.csv
│   └── parameters.json
├── assets/                   # Images, icons, static resources
│   └── logo.svg
├── reports/                  # Generated reports
│   └── analysis_v1.pdf
└── plugins/                  # Project-local plugin overrides
    └── custom-chart/
```

### 6.2 project.json Schema

The project manifest is the single source of truth for project metadata, configuration, and workspace state. All fields are validated against this schema on load.

```jsonc
{
  "$schema": "https://scilab-studio.dev/schemas/project-v1.json",
  "version": "1.0.0",
  "name": "My Engineering Project",
  "description": "Vibration analysis of rotating machinery",
  "created": "2026-07-27T10:00:00.000Z",
  "modified": "2026-07-27T14:30:00.000Z",
  "scilab_version": "2024.1.0",
  "modules": ["data-import", "visualization-engine", "signal-processing", "report-generator"],
  "plugins": [
    {
      "id": "com.example.vibration-analyzer",
      "version": "1.2.0",
      "enabled": true,
      "settings": { "samplingRate": 1000, "windowFunction": "hanning" }
    }
  ],
  "settings": {
    "editor": { "fontSize": 14, "tabSize": 2, "wordWrap": "on" },
    "engine": { "mode": "child-process", "timeout": 60000 },
    "visualization": { "renderer": "webgl", "defaultTheme": "dark" }
  },
  "workspace": {
    "layout": "default",
    "panels": {
      "left":   { "visible": true, "width": 250, "activePanel": "project-explorer" },
      "right":  { "visible": true, "width": 300, "activePanel": "inspector" },
      "bottom": { "visible": true, "height": 200, "activePanel": "terminal" }
    },
    "openTabs": ["scripts/main.sce", "data/measurements.csv"],
    "activeTab": "scripts/main.sce"
  }
}
```

### 6.3 Field Constraints

| Field | Type | Required | Constraint |
|-------|------|----------|------------|
| `version` | string | yes | Must be `1.0.0` |
| `name` | string | yes | 1–128 chars, no path separators |
| `description` | string | no | 0–1024 chars |
| `created` | string | yes | ISO 8601, immutable after creation |
| `modified` | string | yes | ISO 8601, updated on every save |
| `scilab_version` | string | yes | Semver of required Scilab engine |
| `modules` | string[] | yes | Unique, sorted module IDs |
| `plugins` | PluginRef[] | no | Installed plugin references |
| `plugins[].id` | string | yes | Reverse-domain identifier |
| `plugins[].version` | string | yes | Semver |
| `plugins[].enabled` | boolean | no | Default `true` |
| `plugins[].settings` | object | no | Plugin-specific overrides |
| `settings` | object | no | Per-project config overrides (see Appendix A) |
| `workspace` | object | no | Panel layout, persisted on close |

### 6.4 Validation Rules

1. `version` must match `^1\.0\.0$` for the v1 schema.
2. `created` must be `<= modified`.
3. `modules` must not contain duplicates.
4. Each `plugins[].id` must be unique.
5. `workspace.layout` must reference an existing file in `layouts/`.
6. On load, the platform validates against the schema and reports errors as `system:validation:failed` events. Invalid projects cannot be opened until the manifest is corrected.

---

## 7. Scilab Integration Layer

### 7.1 Architecture

The Scilab Integration Layer connects the Tauri frontend to the Scilab process through a Rust sidecar. The sidecar manages process lifetime, translates between typed TypeScript requests and raw JSON-RPC, and enforces timeouts and error handling.

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│    Tauri App     │      │   Rust Sidecar  │      │  Scilab Process  │
│   (TS + Svelte) │      │                 │      │                  │
│  eventBus        │◀────▶│  ┌───────────┐  │◀────▶│  ┌────────────┐  │
│  .request(       │ IPC  │  │ JSON-RPC  │  │ stdio│  │  Scilab    │  │
│    "engine:eval" │      │  │  Codec    │  │      │  │  Interpreter│  │
│  )               │      │  └───────────┘  │      │  └────────────┘  │
│  store           │◀────▶│  ┌───────────┐  │      │                  │
│  .get("engine")  │      │  │  Process  │  │      │                  │
│                  │      │  │  Manager  │  │      │                  │
│                  │      │  └───────────┘  │      │                  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

Transport: Newline-delimited JSON over stdin/stdout. Encoding: UTF-8.

### 7.2 Request/Response Format

**Request:**
```jsonc
{ "jsonrpc": "2.0", "id": "req_a1b2c3d4", "method": "eval", "params": { "code": "x = [1, 2, 3]" } }
```

**Success:**
```jsonc
{ "jsonrpc": "2.0", "id": "req_a1b2c3d4", "result": { "type": "matrix", "value": [[1, 2, 3]] } }
```

**Error:**
```jsonc
{
  "jsonrpc": "2.0", "id": "req_a1b2c3d4",
  "error": { "code": -32603, "message": "Scilab evaluation failed",
             "data": { "scilabError": "Undefined variable: y", "line": 2, "column": 5 } }
}
```

### 7.3 Methods

| Method | Params | Result | Description |
|--------|--------|--------|-------------|
| `eval` | `{ code, timeout? }` | `{ type, value, output? }` | Execute Scilab code |
| `getVariable` | `{ name }` | `{ type, value }` | Get variable by name |
| `setVariable` | `{ name, type, value }` | `{ success }` | Set variable value |
| `callFunction` | `{ name, args, timeout? }` | `{ type, value }` | Call Scilab function |
| `getWorkingDirectory` | `{}` | `{ path }` | Get CWD |
| `setWorkingDirectory` | `{ path }` | `{ success }` | Set CWD |
| `getVariableNames` | `{}` | `{ names }` | List all variables |
| `isBusy` | `{}` | `{ busy }` | Check if computing |
| `abort` | `{}` | `{ success }` | Abort current computation |

### 7.4 Variable Marshalling

| Scilab Type | JSON Type | Wire Format | Notes |
|-------------|-----------|-------------|-------|
| `double` (scalar) | `number` | `42` | Direct mapping |
| `complex` (scalar) | `object` | `{ "re": 3.0, "im": 4.0 }` | Rectangular form |
| `matrix` (real) | `array` | `[[1, 2], [3, 4]]` | 2D, row-major |
| `matrix` (complex) | `object` | `{ "real": [[1]], "imag": [[2]] }` | Separate parts |
| `string` | `string` | `"hello"` | UTF-8 |
| `boolean` | `boolean` | `true` / `false` | Direct mapping |
| `list` | `array` | `[1, "two", true]` | Recursive marshalling |
| `struct` | `object` | `{ "field1": 1 }` | Named fields |
| `sparse` | `object` | `{ "rows": [...], "cols": [...], "values": [...] }` | Compressed sparse row |
| `cell` | `array` | `[["a", 1], ["b", 2]]` | Nested array |
| `void` | `null` | `null` | No value |
| `poly` | `object` | `{ "coefficients": [...], "variable": "x" }` | Polynomial |

### 7.5 Error Codes

| Code | Constant | Meaning |
|------|----------|---------|
| `-32700` | `PARSE_ERROR` | Invalid JSON |
| `-32600` | `INVALID_REQUEST` | Not a valid JSON-RPC request |
| `-32601` | `METHOD_NOT_FOUND` | Unknown method |
| `-32602` | `INVALID_PARAMS` | Params don't match spec |
| `-32603` | `INTERNAL_ERROR` | Scilab internal error |
| `-31000` | `SCILAB_EVAL_ERROR` | Evaluation failed (syntax/runtime) |
| `-31001` | `SCILAB_TIMEOUT` | Computation exceeded timeout |
| `-31002` | `SCILAB_BUSY` | Engine busy, request rejected |
| `-31003` | `SCILAB_NOT_RUNNING` | Engine not started |
| `-31004` | `SCILAB_VAR_NOT_FOUND` | Variable doesn't exist |
| `-31005` | `SCILAB_TYPE_ERROR` | Type mismatch in marshalling |

### 7.6 Connection Lifecycle

```
  Tauri App                    Rust Sidecar                  Scilab Process
      │  startSidecar()             │                              │
      │────────────────────────────▶│  spawn("scilab -nw")         │
      │                             │─────────────────────────────▶│
      │                             │  stdout ready                │
      │◀────────────────────────────│◀─────────────────────────────│
      │  request({method:"eval"})   │  stdin.write(json+newline)   │
      │────────────────────────────▶│─────────────────────────────▶│
      │  response({result:...})     │  stdout.read(json+newline)   │
      │◀────────────────────────────│◀─────────────────────────────│
      │  stopSidecar()              │  process.kill(SIGTERM)       │
      │────────────────────────────▶│─────────────────────────────▶│
      │  stopped event              │                              │
      │◀────────────────────────────│                              │
```

---

## 8. Future Services

### AI Engineering Assistant (v0.3)
An in-app AI assistant that helps users write Scilab code, interpret results, and build visualizations through natural language conversation. Runs a local 7B parameter model with optional cloud fallback. Provides inline code suggestions, explains error messages, and generates boilerplate for common engineering workflows like signal processing, control systems, and numerical optimization.

### Cloud Sync (v2.0)
Encrypted cross-device project synchronization. Projects are diffed at the file level and synced incrementally. Authentication uses OAuth 2.0 with major identity providers. Conflict resolution uses last-write-wins with manual merge for simultaneous edits. Requires a Scilab Studio account and encrypted cloud storage backend.

### Real-time Collaboration (v2.0)
Multi-user simultaneous editing of projects using CRDTs for conflict-free merged state. Users see each other's cursors and changes in real time. Requires Cloud Sync as a dependency. Supports role-based access: viewer (read-only), editor (full access), and admin (manage members and permissions).

### Community Marketplace (v0.4)
A public registry where plugin authors publish plugins and users discover, install, rate, and review them. Includes automated security scanning, license compliance checking, and version compatibility verification. Plugins are published via a CLI command and reviewed before listing. Supports both free and paid plugins with optional donation funding.

### Digital Twin Engine (v0.3)
A framework for creating real-time digital twins of physical systems. Connects to live data sources (MQTT, OPC UA, REST APIs) and maps them to Scilab models. Provides a visual configuration interface for defining data pipelines and updating model parameters in real time. Supports replay of historical data for debugging and validation.

### Package Manager (v0.2)
A CLI and GUI tool for managing Scilab toolboxes and libraries. Wraps Scilab's existing `atomsInstall` with a modern interface. Resolves dependency graphs, manages versions, and integrates with the Community Marketplace. Supports both Scilab-native packages and Scilab Studio plugins in a unified dependency resolution.

---

## 9. Architecture Principles

**Rule 1:** Modules cannot depend on each other directly. All communication flows through the event bus or shared state. Direct imports create hidden coupling that breaks testability and replaceability.

**Rule 2:** Every module exposes a public API through the event bus. Modules register handlers for request events and emit broadcast events. No module exports functions or classes for other modules to call.

**Rule 3:** Plugins cannot modify the core platform. Plugins contribute panels, commands, menu items, and visualization types through declared contribution points only.

**Rule 4:** Widgets must implement the common Widget interface: `init`, `render`, `resize`, `destroy`, `toJSON`, `fromJSON`. This ensures consistent behavior and workspace serialization.

**Rule 5:** Scientific computation always goes through the Scilab Integration Layer. No module may spawn its own Scilab process or communicate through any channel other than the Rust sidecar.

**Rule 6:** User data is stored in project workspaces, not global directories. Global storage is reserved for user preferences, plugin installations, and application metadata.

**Rule 7:** All user-facing text must be localizable. Strings are referenced by key, not hardcoded. Translation files load at startup and can be overridden per-user.

**Rule 8:** Configuration follows a three-level hierarchy: global defaults → user overrides → project overrides. Deep merge for objects, replacement for arrays and scalars.

**Rule 9:** Events follow the `domain:action:detail` naming convention. This makes routing, filtering, and debugging predictable.

**Rule 10:** No module may block the UI thread for more than 50ms. Long-running operations must be offloaded to Web Workers, the Rust sidecar, or background threads. The UI thread is reserved for input handling, layout, and paint.

**Rule 11:** Every plugin declares its required permissions in advance. The platform denies any API call that exceeds declared permissions. Permissions cannot be granted at runtime — the user must reinstall the plugin with expanded permissions.

**Rule 12:** The event bus is the only way modules discover each other's existence. No module holds a reference to another module. If a module is removed, its listeners are automatically deregistered. If a module is added, it begins receiving events immediately.

---

## 10. Future Evolution

```
Version 0.1 (Current) — Foundation
├── Project Workspace + Manager
├── GUI Builder (9 components)
├── Visualization Studio (4 chart types)
├── Data Studio (CSV, Excel)
├── Report Generator (PDF, HTML)
└── Learning Center (examples)

Version 0.2 — Extensibility
├── Plugin System
├── Widget Marketplace
├── Lab Creator
├── Xcos Builder
└── Project Templates

Version 0.3 — Intelligence
├── AI Engineering Assistant
├── Digital Twin Framework
├── Parameter Sweep Studio
└── Dashboard Builder

Version 0.4 — Community
├── Community Marketplace
├── Open Engineering Library
├── Research Workspace
└── Experiment Recorder

Version 2.0 — Platform
├── Cloud Deployment
├── Real-time Collaboration
├── Web-based (WASM)
└── Enterprise Features
```

---

## Appendix A: Configuration System

### Three-Level Hierarchy

```
  Level 1: Global Defaults          Level 2: User Overrides         Level 3: Project Overrides
  ─────────────────────────         ───────────────────────         ───────────────────────────
  Location:    Application binary   Location:    ~/.config/.../user.json  Location:    project.json → "settings"
  Purpose:     Out-of-box defaults  Purpose:     Personal prefs     Purpose:     Project-specific
  Modified by: Rarely               Modified by: User via UI        Modified by: User via UI
```

### Global Defaults Schema

```jsonc
{
  "editor": { "fontSize": 14, "fontFamily": "JetBrains Mono, monospace", "tabSize": 2,
              "insertSpaces": true, "wordWrap": "off", "minimap": true, "lineNumbers": true },
  "engine": { "mode": "child-process", "scilabPath": "auto", "timeout": 30000,
              "maxMemory": "2GB", "autoStart": true },
  "visualization": { "renderer": "canvas", "defaultTheme": "dark", "animationDuration": 300,
                     "maxDataPoints": 10000, "antialiasing": true },
  "plugins": { "autoUpdate": true, "sandboxed": true, "maxConcurrent": 4,
               "allowedPermissions": ["fs:read", "engine", "ui"] },
  "ai": { "provider": "local", "model": "scilab-coder-7b", "suggestions": true,
          "maxTokens": 2048, "temperature": 0.7 },
  "data": { "autoDetectTypes": true, "maxPreviewRows": 100, "csvDelimiter": "auto", "encoding": "utf-8" },
  "general": { "language": "en", "theme": "dark", "autoSave": true, "autoSaveInterval": 30000,
               "recentProjectsMax": 20 }
}
```

### Merge Strategy

Deep merge with last-write-wins:

```typescript
function deepMerge<T extends Record<string, any>>(base: T, override: Partial<T>): T {
  const result = { ...base };
  for (const key of Object.keys(override)) {
    const baseVal = result[key];
    const overVal = override[key];
    if (baseVal !== null && typeof baseVal === 'object' && !Array.isArray(baseVal)
        && typeof overVal === 'object' && !Array.isArray(overVal)) {
      result[key] = deepMerge(baseVal, overVal);
    } else if (overVal !== undefined) {
      result[key] = overVal;
    }
  }
  return result;
}
```

**Merge order:** `resolved = deepMerge(deepMerge(globalDefaults, userOverrides), projectOverrides)`

**Rules:** Scalars are replaced entirely. Objects are recursively merged. Arrays are replaced (not concatenated). `undefined` keys do not delete lower-level keys. Resolved config is immutable after project load.

---

## Appendix B: Security Model

### Trust Levels

| Level | Name | Scope | Sandbox |
|-------|------|-------|---------|
| **0** | Core Platform | Built-in modules | None (trusted) |
| **1** | Verified Plugins | Marketplace-vetted | Capability-based sandbox |
| **2** | Community Plugins | User-installed, unvetted | Full sandbox, restricted fs/network |
| **3** | User Scripts | User-authored Scilab | Scilab process isolation |

### Capability Enforcement

```typescript
function enforcePermission(pluginId: string, capability: string): void {
  const manifest = getManifest(pluginId);
  const level = getTrustLevel(pluginId);
  if (!manifest.permissions.includes(capability)) {
    throw new PermissionDeniedError(`Plugin "${pluginId}" attempted "${capability}" without declaration`);
  }
  if (level >= 2) rateLimiter.check(pluginId, capability);
  if (level >= 3) throw new PermissionDeniedError(`User scripts cannot access "${capability}" directly`);
}
```

### Sandbox

| Resource | Mechanism | Config |
|----------|-----------|--------|
| Filesystem | Path whitelist | Only `<project>/.scilab-studio/plugins/<id>/` + declared paths |
| Network | Domain whitelist | DNS pinning, no raw sockets |
| CPU | Execution timeout | 30s default, `abort()` on timeout |
| Memory | RSS monitoring | Polling every 5s, suspended at 128MB |
| File Descriptors | Soft cap | 256 open FDs per plugin |
| Scilab Engine | Eval sandbox | Isolated workspace, no platform variable access |

### Supply Chain

1. Dependencies resolved from marketplace registry only (no npm/git/URL).
2. Installed versions pinned with exact versions in `project.json`.
3. SHA-256 checksums verified against registry on download.
4. Auto-updated plugins re-verified before activation.

---

## Appendix C: Performance Budget

### Timing Constraints

| Metric | Target | Owner |
|--------|--------|-------|
| Cold startup | `< 2s` | Shell (Tauri) |
| Hot restart | `< 500ms` | Shell (Tauri) |
| Module load | `< 500ms` | Plugin System |
| Module unload | `< 200ms` | Plugin System |
| Scilab simple eval | `< 100ms` | Scilab Bridge |
| Scilab matrix eval (1000x1000) | `< 500ms` | Scilab Bridge |
| File open | `< 200ms` | Data Layer |
| Large CSV (100MB) | `< 3s` | Data Layer |
| Chart render (10K points) | `< 50ms` | Visualization |
| Chart render (1M points) | `< 200ms` | Visualization (WebGL) |
| Command palette open | `< 50ms` | UI Layer |

### Rendering Budget (60 FPS)

```
  Frame Budget: 16.67ms per frame

  Input Handling      │  1ms      │ Keyboard, mouse, resize
  Style Recalc        │  1ms      │ CSS computed styles
  Layout (Reflow)     │  2ms      │ Box model, flex/grid
  Paint               │  4ms      │ Rasterization, compositing
  JS Execution        │  5ms      │ Handlers, state, transforms
  Frame Remainder     │  3.67ms   │ Safety margin (GC, JIT)
```

### Memory Constraints

| Context | Limit | Action on Exceed |
|---------|-------|-----------------|
| Application total | 500 MB | `system:memory:warning`, prompt to close panels |
| Single visualization | 100 MB | Downsample, show warning |
| Scilab engine | 2 GB (configurable) | Auto-GC, warn user |
| Per-plugin | 128 MB | Plugin suspended, `plugin:error:memory` |
| File cache | 256 MB | LRU eviction |

### Optimization Strategies

| Strategy | Where | Implementation |
|----------|-------|----------------|
| Lazy loading | Modules, plugins | `import()` on first use |
| Virtual scrolling | Data tables, lists | Render visible rows (+-5 buffer) |
| Web Workers | Heavy computation | Data transforms, AI, reports |
| Canvas pooling | Visualization | Reuse `<canvas>` elements |
| Debounced updates | UI re-renders | 16ms debounce on rapid changes |
| Result caching | Scilab eval | SHA-256 hash, configurable TTL |
| Stream processing | Real-time data | 4096-record chunks |
| Precompiled templates | Reports | Compiled once, reused per render |

---

*This document is the authoritative normative specification for Scilab Studio
system architecture. All module implementations must conform to the schemas,
protocols, and constraints defined herein. Deviations require an Architecture
Decision Record (ADR) approved by the core team.*
