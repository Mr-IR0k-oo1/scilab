# 21 — Component Specification

Every major component in Scilab Studio gets a formal specification. Each specification defines the component's responsibilities, public API, internal state, events, dependencies, failure modes, and extension points.

For the runtime architecture that wires these components together, see [20 — Technical Architecture](20_Technical_Architecture.md).

---

## 1. Core Runtime

### Responsibilities
- Orchestrate application startup and shutdown.
- Own the Service Registry and wire dependency injection.
- Route fatal errors to the error boundary.
- Manage application-level lifecycle events.

### Public API

```typescript
interface CoreRuntime {
  start(): Promise<void>;
  stop(): Promise<void>;
  getService<T>(name: string): T;
  registerService(name: string, service: any): void;
  on(event: string, handler: Function): Subscription;
  emit(event: string, payload: any): void;
}
```

### Internal State
- `services: Map<string, any>` — Registered service instances.
- `phase: "booting" | "running" | "shutting-down" | "stopped"` — Current lifecycle phase.
- `errorBoundary: ErrorBoundary` — Catches and categorizes unhandled errors.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `app:starting` | Emitted | `{ version, platform }` |
| `app:ready` | Emitted | `{}` |
| `app:shutting-down` | Emitted | `{ reason }` |
| `app:error` | Emitted | `ErrorPayload` |

### Dependencies
- None (this is the root component).

### Failure Modes
- **SQLite initialization fails:** Application cannot start. Show error dialog with recovery options (retry, delete database, exit).
- **Scilab not found:** Application starts in degraded mode. Engine features disabled. Notification shown.
- **Settings file corrupt:** Use defaults. Notify user. Offer to reset settings.

### Extension Points
- Services can be registered by any component during startup.
- The error boundary can be extended with custom handlers.

---

## 2. Module Loader

### Responsibilities
- Scan directories for module manifests.
- Parse and validate manifests against the schema.
- Resolve the dependency graph.
- Detect circular dependencies.
- Produce a sorted activation order.
- Activate and deactivate modules in the correct order.

### Public API

```typescript
interface ModuleLoader {
  scan(): Promise<ModuleManifest[]>;
  resolve(modules: ModuleManifest[]): ActivationOrder;
  activate(moduleId: string, context: ModuleContext): Promise<void>;
  deactivate(moduleId: string): Promise<void>;
  getActive(): string[];
  getModule(id: string): LoadedModule | null;
}
```

### Internal State
- `manifests: Map<string, ModuleManifest>` — Discovered manifests.
- `active: Map<string, LoadedModule>` — Currently active modules.
- `activationOrder: string[]` — Sorted by dependency resolution.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `module:discovered` | Emitted | `{ id, manifest }` |
| `module:activated` | Emitted | `{ id }` |
| `module:deactivated` | Emitted | `{ id }` |
| `module:error` | Emitted | `{ id, error }` |
| `module:circular-dependency` | Emitted | `{ cycle: string[] }` |

### Dependencies
- Core Runtime (for service access).
- Storage Layer (for scanning directories).

### Failure Modes
- **Circular dependency detected:** Fatal. The involved modules are not activated. User is notified which modules are affected.
- **Module activation fails:** That module is skipped. Dependent modules enter degraded mode. Other modules continue.
- **Manifest schema invalid:** Module is skipped with a validation error notification.
- **Missing dependency:** Module enters `pending` state. If dependency is never resolved, module is marked `failed`.

### Extension Points
- New manifest fields can be added without breaking existing loaders.
- Custom validation rules can be registered.
- Activation order can be overridden per-module via manifest `activationPriority` field.

---

## 3. Event Bus

### Responsibilities
- Route events from emitters to subscribers.
- Support fire-and-forget broadcast and request/response RPC.
- Enforce event priority ordering.
- Log all events for debugging.
- Handle subscriber errors without crashing the emitter.

### Public API

```typescript
interface EventBus {
  emit(type: string, payload: any, options?: EmitOptions): string;
  request(type: string, payload: any, options?: RequestOptions): Promise<any>;
  on(type: string, handler: EventHandler): Subscription;
  once(type: string, handler: EventHandler): Subscription;
  off(subscription: Subscription): void;
  handle(type: string, handler: RpcHandlerFn): Subscription;
}
```

### Internal State
- `subscribers: Map<string, EventHandler[]>` — Active subscriptions by event type.
- `queue: EventBusEvent[]` — Pending events (bounded to 10,000).
- `rpcHandlers: Map<string, RpcHandlerFn>` — Registered RPC handlers.
- `eventLog: EventLogEntry[]` — Recent events for debugging (circular buffer, last 1,000).

### Events
The Event Bus does not emit events about itself (to avoid infinite recursion). It logs internally.

### Dependencies
- Core Runtime (for initialization).
- Storage Layer (for event logging).

### Failure Modes
- **Subscriber throws:** Error is caught, logged, and the next subscriber is called. The emitter is not affected.
- **RPC handler throws:** Caller receives an error response. Other handlers for the same type are not affected.
- **RPC request times out:** Caller receives a timeout error after the configured duration.
- **Queue overflow (>10,000):** Low-priority events are dropped. A `system:backpressure` warning is emitted.

### Extension Points
- Custom dispatch strategies (e.g., request coalescing, debouncing).
- Middleware pipeline for event transformation.
- Event replay for testing.

---

## 4. Service Registry

### Responsibilities
- Maintain a global map of named service interfaces to implementations.
- Support lazy initialization (services created on first access).
- Validate that required services exist before module activation.

### Public API

```typescript
interface ServiceRegistry {
  register(name: string, service: any, options?: RegisterOptions): void;
  get<T>(name: string): T;
  has(name: string): boolean;
  unregister(name: string): void;
  list(): string[];
}
```

### Internal State
- `services: Map<string, { instance: any, factory?: Function, lazy: boolean }>` — Registered services.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `service:registered` | Emitted | `{ name }` |
| `service:unregistered` | Emitted | `{ name }` |

### Dependencies
- None (standalone utility).

### Failure Modes
- **Service not found:** Throws `ServiceNotFoundError`. Caller must handle.
- **Service initialization fails:** Throws during `get()`. Caller receives the error.

### Extension Points
- Service decorators (logging, caching, retry).
- Service health checks.

---

## 5. Workspace Manager

### Responsibilities
- Manage the physical layout of the application: panels, tabs, split views.
- Persist layout state to `project.json` on close.
- Restore layout state from `project.json` on open.
- Handle panel resize, collapse, expand, reorder.
- Manage tab lifecycle (open, close, activate, reorder, pin).

### Public API

```typescript
interface WorkspaceManager {
  // Layout
  getLayout(): LayoutState;
  setLayout(layout: LayoutState): void;
  saveLayout(name: string): Promise<void>;
  loadLayout(name: string): Promise<void>;
  listLayouts(): Promise<string[]>;

  // Panels
  openPanel(panelId: string, position: PanelPosition): void;
  closePanel(panelId: string): void;
  resizePanel(position: PanelPosition, width: number): void;
  collapsePanel(position: PanelPosition): void;
  expandPanel(position: PanelPosition): void;

  // Tabs
  openTab(config: TabConfig): string;
  closeTab(tabId: string): void;
  activateTab(tabId: string): void;
  reorderTab(tabId: string, newIndex: number): void;
  pinTab(tabId: string): void;
  unpinTab(tabId: string): void;
  getOpenTabs(): Tab[];
  getActiveTab(): Tab | null;
}
```

### Internal State
- `layout: LayoutState` — Current panel sizes, positions, and visibility.
- `tabs: Tab[]` — Open tabs in order.
- `activeTabId: string | null` — Currently active tab.
- `savedLayouts: Map<string, LayoutState>` — User-saved layout snapshots.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `workspace:layout_changed` | Emitted | `LayoutState` |
| `workspace:panel:opened` | Emitted | `{ panelId, position }` |
| `workspace:panel:closed` | Emitted | `{ panelId }` |
| `workspace:tab:opened` | Emitted | `Tab` |
| `workspace:tab:closed` | Emitted | `{ tabId }` |
| `workspace:tab:activated` | Emitted | `{ tabId }` |

### Dependencies
- Core Runtime (for service access).
- Storage Layer (for persisting layout).
- Event Bus (for event routing).

### Failure Modes
- **Layout file corrupt:** Fall back to default layout. Notify user.
- **Tab component not found:** Show placeholder panel with error message.
- **Panel limit exceeded:** Reject new panel. Show notification.

### Extension Points
- Custom panel types can be registered.
- Layout serialization can be extended with new formats.
- Panel positions can be extended (e.g., floating panels).

---

## 6. Plugin Runtime

### Responsibilities
- Host third-party plugins in sandboxed JavaScript contexts.
- Enforce plugin permissions.
- Manage plugin lifecycle (install, activate, suspend, deactivate, uninstall).
- Provide the Plugin Context API to each plugin.
- Monitor plugin health via heartbeats.
- Handle plugin errors without crashing the host.

### Public API

```typescript
interface PluginRuntime {
  install(manifest: PluginManifest, files: Uint8Array): Promise<void>;
  uninstall(pluginId: string): Promise<void>;
  activate(pluginId: string): Promise<void>;
  deactivate(pluginId: string): Promise<void>;
  suspend(pluginId: string): Promise<void>;
  resume(pluginId: string): Promise<void>;
  getPlugin(id: string): PluginInstance | null;
  listPlugins(): PluginInstance[];
  isEnabled(id: string): boolean;
}
```

### Internal State
- `plugins: Map<string, PluginInstance>` — Loaded plugins.
- `sandbox: V8Isolate` — Sandboxed JavaScript execution context.
- `heartbeatTimer: Interval` — Periodic health check (30s).
- `pluginSettings: Map<string, any>` — Per-plugin settings.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `plugin:installed` | Emitted | `{ id, manifest }` |
| `plugin:activated` | Emitted | `{ id }` |
| `plugin:deactivated` | Emitted | `{ id }` |
| `plugin:suspended` | Emitted | `{ id }` |
| `plugin:error` | Emitted | `{ id, error }` |
| `plugin:heartbeat-miss` | Emitted | `{ id, count }` |

### Dependencies
- Core Runtime (for Service Registry access).
- Event Bus (for event routing).
- Storage Layer (for plugin file storage).
- Module Loader (for dependency resolution).

### Failure Modes
- **Plugin activation fails:** Plugin is marked `failed`. Dependent plugins are notified. User sees error notification.
- **Plugin throws at runtime:** Error is caught. Plugin is suspended. Other plugins continue.
- **3 missed heartbeats:** Plugin is automatically suspended. User is notified.
- **Permission violation:** Operation is blocked. Plugin is notified. Logged as security event.
- **Memory limit exceeded:** Plugin is suspended. Memory usage is logged.

### Extension Points
- Custom sandbox implementations (e.g., Worker-based isolation).
- Plugin packaging formats.
- Health check strategies.

---

## 7. Widget Runtime

### Responsibilities
- Load widget definitions from the widget directory.
- Bridge between widget property definitions and the Svelte rendering system.
- Manage widget data binding (static values, Scilab variables, event payloads).
- Handle widget resize, selection, and interaction events.
- Serialize widget state for persistence.

### Public API

```typescript
interface WidgetRuntime {
  load(widgetId: string): Promise<WidgetDefinition>;
  unload(widgetId: string): void;
  list(): WidgetDefinition[];
  render(widget: WidgetInstance): SvelteComponent;
  serialize(widget: WidgetInstance): WidgetState;
  deserialize(state: WidgetState): WidgetInstance;
  bindData(widgetId: string, propertyName: string, binding: DataBinding): void;
}
```

### Internal State
- `definitions: Map<string, WidgetDefinition>` — Loaded widget schemas.
- `instances: Map<string, WidgetInstance>` — Active widget instances on canvases.
- `bindings: Map<string, DataBinding>` — Active data bindings.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `widget:loaded` | Emitted | `{ id, definition }` |
| `widget:property:changed` | Emitted | `{ instanceId, property, value }` |
| `widget:data:updated` | Emitted | `{ instanceId, data }` |
| `widget:action:fired` | Emitted | `{ instanceId, action, payload }` |

### Dependencies
- Core Runtime.
- Event Bus.
- Scilab Runtime (for live data binding).

### Failure Modes
- **Widget definition invalid:** Widget is skipped. Logged as warning.
- **Data binding source unavailable:** Widget enters "disconnected" state. Shows placeholder.
- **Rendering fails:** Widget shows error state with details.

### Extension Points
- Custom property types.
- Custom data binding sources.
- Custom rendering strategies (e.g., Canvas 2D, WebGL).

---

## 8. Scilab Runtime

### Responsibilities
- Maintain a command queue for serialized Scilab execution.
- Translate typed TypeScript requests to JSON-RPC 2.0.
- Manage Scilab process lifecycle (start, monitor, restart, stop).
- Parse Scilab output and marshal variables between TypeScript and Scilab types.
- Enforce execution timeouts.
- Provide cancellation support.
- Track execution progress for long-running computations.

### Public API

```typescript
interface ScilabRuntime {
  eval(code: string, options?: EvalOptions): Promise<EvalResult>;
  callFunction(name: string, args: any[], options?: CallOptions): Promise<any>;
  getVariable(name: string): Promise<Variable>;
  setVariable(name: string, value: any): Promise<void>;
  listVariables(): Promise<VariableInfo[]>;
  abort(): Promise<void>;
  isConnected(): boolean;
  getVersion(): string | null;
}
```

### Internal State
- `commandQueue: CommandQueue` — FIFO queue for pending commands.
- `process: ChildProcess | null` — Scilab process handle.
- `status: "disconnected" | "connecting" | "connected" | "busy"` — Connection state.
- `variableCache: Map<string, Variable>` — Cached variable values.
- `history: CommandHistoryEntry[]` — Last 100 commands for debugging.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `engine:connected` | Emitted | `{ version }` |
| `engine:disconnected` | Emitted | `{ reason }` |
| `engine:busy` | Emitted | `{ busy }` |
| `engine:result` | Emitted | `EvalResult` |
| `engine:stdout` | Emitted | `{ line }` |
| `engine:stderr` | Emitted | `{ line }` |
| `engine:variable:changed` | Emitted | `{ name, type, value }` |
| `engine:progress` | Emitted | `{ percent, message }` |

### Dependencies
- Core Runtime.
- Event Bus.
- Sidecar Process (stdio transport).

### Failure Modes
- **Scilab process crashes:** Auto-restart (max 3 in 60s). User notified.
- **Command timeout:** Command is aborted. Caller receives timeout error.
- **Queue overflow (256 pending):** New commands rejected with "busy" error.
- **Scilab not found:** Runtime enters `disconnected` state. All eval operations fail with descriptive error.

### Extension Points
- Custom output parsers.
- Custom variable marshallers.
- Execution middleware (logging, profiling, rate limiting).

---

## 9. Storage Layer

### Responsibilities
- Provide SQLite database access with connection pooling.
- Manage file system operations within the project directory.
- Handle file watching for external changes.
- Maintain a thumbnail cache.
- Provide emergency snapshot storage for crash recovery.
- Enforce file-level locking for concurrent access.

### Public API

```typescript
interface StorageLayer {
  // Database
  query<T>(sql: string, params?: any[]): Promise<T[]>;
  execute(sql: string, params?: any[]): Promise<void>;

  // File system
  readFile(path: string): Promise<Uint8Array>;
  writeFile(path: string, content: Uint8Array | string): Promise<void>;
  listDir(path: string): Promise<FileEntry[]>;
  createDir(path: string): Promise<void>;
  delete(path: string): Promise<void>;
  rename(oldPath: string, newPath: string): Promise<void>;
  exists(path: string): Promise<boolean>;
  stat(path: string): Promise<FileStat>;

  // File watching
  watch(path: string, callback: FileWatcherCallback): FileWatcher;
  unwatch(watcher: FileWatcher): void;

  // Cache
  cacheGet(key: string): Promise<Uint8Array | null>;
  cacheSet(key: string, value: Uint8Array, ttl?: number): Promise<void>;
  cacheClear(): Promise<void>;

  // Emergency
  saveEmergencySnapshot(data: any): Promise<string>;
  getEmergencySnapshots(): Promise<EmergencySnapshot[]>;
  clearEmergencySnapshot(id: string): Promise<void>;
}
```

### Internal State
- `db: SqlitePool` — Connection pool (default 5 connections).
- `watchers: Map<string, FileWatcher>` — Active file watchers.
- `locks: Map<string, Lock>` — Advisory file locks.

### Events
| Event | Direction | Payload |
|-------|-----------|---------|
| `fs:changed` | Emitted | `{ path, type }` |
| `fs:lock:acquired` | Emitted | `{ path, owner }` |
| `fs:lock:released` | Emitted | `{ path }` |

### Dependencies
- Core Runtime.

### Failure Modes
- **Disk full:** Write operations fail. Application switches to read-only mode. User notified.
- **SQLite corruption:** Attempt recovery from WAL. If failed, offer to recreate database.
- **File locked:** Wait up to 5s, then fail with "file locked by another process" error.
- **Permission denied:** Show OS-level permission error with guidance.

### Extension Points
- Custom database backends (e.g., PostgreSQL for collaboration).
- Custom cache strategies (e.g., LRU, TTL, size-based).
- Custom file watchers (e.g., network file systems).
