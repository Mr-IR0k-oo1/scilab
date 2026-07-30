# 23 — Event System

Never allow modules to directly call each other. Everything communicates through events. The Event Bus is the central nervous system of Scilab Studio.

For the Event Bus component specification, see [21 — Component Specification §3](21_Component_Specification.md). For the runtime architecture, see [20 — Technical Architecture](20_Technical_Architecture.md).

---

## 1. Communication Pattern

```
Module A                    Event Bus                    Module B
   │                            │                            │
   ├── emit("data:imported") ──►│                            │
   │                            ├── notify subscriber ──────►│
   │                            │                            │
   │                            │◄── handle("data:imported") │
   │                            │                            │
   ├── request("engine:eval") ─►│                            │
   │                            ├── route to handler ───────►│
   │                            │◄── return result ──────────│
   │◄── receive result ─────────│                            │
```

Modules never hold references to each other. They emit events and subscribe to events. The Event Bus handles routing, prioritization, and error isolation.

---

## 2. Event Lifecycle

Every event follows this lifecycle:

```
1. Creation
   ├── Emitter creates event with type, payload, source
   ├── Event gets unique ID (uuid)
   ├── Timestamp is set
   └── Priority is assigned

2. Enqueue
   ├── Event enters the dispatch queue
   ├── Queue is bounded (10,000 events max)
   └── If full: low-priority events are dropped

3. Dispatch
   ├── Events are dispatched in priority order
   ├── For each subscriber:
   │   ├── Handler is called with the event
   │   ├── If handler throws: error is caught, logged, next handler called
   │   └── Handler is NOT removed on error
   └── Dispatch is complete when all subscribers have been called

4. Completion
   ├── Event is logged to the event log (circular buffer, last 1,000)
   ├── For RPC: response is sent back to the caller
   └── Event is discarded (no reference retained)
```

---

## 3. Event Types

### 3.1 Fire-and-Forget (Broadcast)

A module emits an event. Any number of subscribers receive it. No return value.

```typescript
// Emitting
eventBus.emit("project:file:created", { path: "scripts/main.sce" });

// Subscribing
eventBus.on("project:file:created", (event) => {
  console.log(`New file: ${event.payload.path}`);
});
```

### 3.2 Request/Response (RPC)

A module sends a request to a named handler. Exactly one handler processes it and returns a response.

```typescript
// Requesting
const result = await eventBus.request("engine:eval", {
  code: "x = [1, 2, 3]"
});

// Handling
eventBus.handle("engine:eval", async (request) => {
  return await scilabBridge.eval(request.payload.code);
});
```

### 3.3 Wildcard Subscriptions

```typescript
// Listen to all engine events
eventBus.on("engine:*", (event) => { /* ... */ });

// Listen to all events (debugging)
eventBus.onAny((event) => { /* ... */ });
```

Wildcard subscribers are called after exact-match subscribers.

---

## 4. Event Payload

Every event carries:

```typescript
interface EventBusEvent {
  id: string;            // Unique identifier (uuid)
  type: string;          // Event type (e.g., "engine:eval")
  source: string;        // Emitter identifier (module/plugin ID)
  timestamp: number;     // Unix timestamp (ms)
  payload: any;          // Event-specific data
  priority: "low" | "normal" | "high" | "critical";
}
```

RPC requests add:

```typescript
interface RpcRequest extends EventBusEvent {
  timeout: number;       // Max wait for response (ms), default 5000
}
```

RPC responses add:

```typescript
interface RpcResponse {
  id: string;            // Correlates to request id
  payload: any;          // Response data
  error?: {
    code: number;
    message: string;
    data?: any;
  };
}
```

---

## 5. Priority

Events are dispatched in priority order:

| Priority | Dispatch | Use Case |
|----------|----------|----------|
| `critical` | Immediate (synchronous) | System shutdown, fatal error |
| `high` | Next microtask | User action responses |
| `normal` | Scheduled (batched) | Standard module communication |
| `low` | Deferred (idle callback) | Debug logs, background sync |

Within the same priority, events are dispatched in FIFO order.

---

## 6. Async Handling

### 6.1 Subscriber Execution

- Subscribers can be sync or async.
- Async subscribers are awaited in parallel within a priority group.
- If an async subscriber takes longer than the event's timeout (for RPC), it is abandoned and an error is logged.

### 6.2 RPC Timeout

- Default timeout: 5000ms.
- If the handler does not respond within the timeout, the caller receives a timeout error.
- The handler continues running but its result is discarded.

### 6.3 Queue Management

- The dispatch queue is bounded to 10,000 events.
- When the queue is full:
  - `critical` events are always dispatched.
  - `high` events are dispatched if queue < 9,000.
  - `normal` events are dispatched if queue < 5,000.
  - `low` events are dropped.
- A `system:backpressure` event is emitted when events are dropped.

---

## 7. Error Propagation

### 7.1 Subscriber Errors

If a subscriber throws:
1. The error is caught by the Event Bus.
2. It is logged with the event type, subscriber ID, and stack trace.
3. The next subscriber for the same event is called.
4. The emitter is NOT affected.
5. The error is NOT propagated to other subscribers.

### 7.2 RPC Handler Errors

If an RPC handler throws:
1. The error is caught by the Event Bus.
2. An error response is sent to the caller with code `-32000`.
3. The caller receives the error as a rejected promise.
4. Other RPC handlers for the same type are NOT affected.

### 7.3 Emitter Errors

If an emitter's code throws during `emit()`:
1. The error is caught by the Event Bus.
2. The event is NOT dispatched.
3. The error is logged.
4. The emitter can catch this via a try/catch around `emit()`.

---

## 8. Event Catalog

### System Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `system:ready` | Core → All | `{ version }` |
| `system:shutdown` | Core → All | `{ reason }` |
| `system:error` | Any → All | `ErrorPayload` |
| `system:notification` | Any → All | `NotificationPayload` |
| `system:backpressure` | Core → All | `{ queueSize, dropped }` |

### Engine Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `engine:eval` | Renderer → Core | `{ code, timeout? }` |
| `engine:result` | Core → Renderer | `{ type, value, output? }` |
| `engine:stdout` | Core → Renderer | `{ line }` |
| `engine:stderr` | Core → Renderer | `{ line }` |
| `engine:status` | Core → Renderer | `{ status }` |
| `engine:variable:changed` | Core → Renderer | `{ name, type, value }` |
| `engine:abort` | Renderer → Core | `{}` |

### Project Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `project:create` | Renderer → Core | `{ name, path, description? }` |
| `project:created` | Core → Renderer | `{ project }` |
| `project:open` | Renderer → Core | `{ path }` |
| `project:opened` | Core → Renderer | `{ project }` |
| `project:save` | Renderer → Core | `{}` |
| `project:saved` | Core → Renderer | `{ timestamp }` |
| `project:file:created` | Core → All | `{ path }` |
| `project:file:deleted` | Core → All | `{ path }` |
| `project:file:renamed` | Core → All | `{ oldPath, newPath }` |
| `project:file:modified` | Core → All | `{ path }` |

### Plugin Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `plugin:install` | Renderer → Core | `{ id, version? }` |
| `plugin:installed` | Core → All | `{ plugin }` |
| `plugin:uninstall` | Renderer → Core | `{ id }` |
| `plugin:uninstalled` | Core → All | `{ id }` |
| `plugin:enable` | Renderer → Core | `{ id }` |
| `plugin:disable` | Renderer → Core | `{ id }` |
| `plugin:error` | Core → All | `{ pluginId, error }` |
| `plugin:activated` | Core → All | `{ pluginId }` |
| `plugin:deactivated` | Core → All | `{ pluginId }` |

### Data Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `data:import` | Renderer → Core | `{ file, options }` |
| `data:imported` | Core → All | `{ data, metadata }` |
| `data:export` | Renderer → Core | `{ data, file, format }` |
| `data:exported` | Core → All | `{ file }` |
| `data:transform` | Renderer → Core | `{ pipeline }` |
| `data:transformed` | Core → Renderer | `{ data }` |

### Visualization Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `viz:create` | Renderer → Core | `{ type, data, options }` |
| `viz:created` | Core → All | `{ chartId }` |
| `viz:update` | Renderer → Core | `{ chartId, data }` |
| `viz:export` | Renderer → Core | `{ chartId, format }` |
| `viz:exported` | Core → All | `{ chartId, file }` |

### Report Events

| Event | Direction | Payload |
|-------|-----------|---------|
| `report:create` | Renderer → Core | `{ definition }` |
| `report:created` | Core → All | `{ reportId }` |
| `report:generate` | Renderer → Core | `{ reportId, format }` |
| `report:generated` | Core → All | `{ reportId, file }` |

---

## 9. Event Tracing

All events are logged to the SQLite `events` table:

```sql
CREATE TABLE events (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  source TEXT,
  timestamp INTEGER NOT NULL,
  payload TEXT,              -- JSON, truncated at 10KB
  dispatch_duration_ms INTEGER,
  subscriber_count INTEGER,
  errors INTEGER DEFAULT 0
);
```

The Debug panel (Ctrl+Shift+D) shows a live feed of all events with filtering by type, source, and time range.

---

## 10. Cross-Process Events

The Renderer and Core processes each have their own Event Bus instance. Cross-process events are routed through Tauri IPC:

```
Renderer Event Bus ←→ Tauri IPC ←→ Core Event Bus
```

The IPC layer subscribes to relevant events on both sides and forwards them. This is transparent to modules — they emit and subscribe as if there were a single bus.
