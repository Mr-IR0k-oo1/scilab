# 28 — Scilab Runtime

Never let modules execute Scilab directly. Instead:

```
GUI
  │
  ▼
Command Queue
  │
  ▼
Scilab Runtime
  │
  ▼
Execution
  │
  ▼
Result
  │
  ▼
Visualization
```

Benefits: better debugging, logging, security, cancellation, progress tracking.

For the Scilab Compatibility Layer (version abstraction), see [31 — Scilab Compatibility Layer](31_Scilab_Compatibility_Layer.md). For the JSON-RPC protocol, see [System Architecture §7](03_System_Architecture.md).

---

## 1. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Scilab Studio                         │
│                                                         │
│  ┌─────────────┐     ┌──────────────────────────────┐  │
│  │ Any Module   │────►│         Event Bus             │  │
│  │ (GUI, Viz,   │     │                              │  │
│  │  Plugin)     │     └──────────┬───────────────────┘  │
│  └─────────────┘                │                       │
│                                 │ engine:eval            │
│  ┌──────────────────────────────▼─────────────────────┐ │
│  │              Scilab Runtime                         │ │
│  │                                                     │ │
│  │  ┌──────────────┐  ┌──────────────┐               │ │
│  │  │ Command Queue │  │ Result Parser │               │ │
│  │  │ (FIFO, 256)  │  │              │               │ │
│  │  └──────┬───────┘  └──────▲───────┘               │ │
│  │         │                  │                        │ │
│  │  ┌──────▼──────────────────┴───────┐               │ │
│  │  │       Process Manager            │               │ │
│  │  │  (spawn, monitor, restart)       │               │ │
│  │  └──────────────┬──────────────────┘               │ │
│  └─────────────────┼──────────────────────────────────┘ │
│                    │ stdio (JSON-RPC 2.0)               │
│  ┌─────────────────▼──────────────────────────────────┐ │
│  │            Scilab Engine                            │ │
│  │         (external process)                          │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Command Queue

### 2.1 Design

The Command Queue serializes all Scilab operations. No two commands execute simultaneously. This prevents:
- Race conditions in Scilab's global workspace.
- Deadlocks from concurrent eval calls.
- Unbounded parallelism from plugins.

### 2.2 Queue Properties

| Property | Value |
|----------|-------|
| Capacity | 256 pending commands |
| Order | FIFO |
| Timeout (default) | 60,000ms for eval, 30,000ms for callFunction |
| Cancellation | Supported (abort current command) |
| Priority | `critical` commands jump to front |

### 2.3 Queue States

```
         ┌──────────┐
         │          │
    ────►│  Idle    │
         │          │
         └────┬─────┘
              │ command enqueued
              ▼
         ┌──────────┐
         │          │
         │ Running  │◄──────┐
         │          │       │
         └────┬─────┘       │
              │             │
         ┌────▼─────┐       │
         │          │       │ next command
         │ Waiting  │───────┘
         │          │
         └──────────┘
```

---

## 3. API

### 3.1 Core Methods

```typescript
interface ScilabRuntime {
  // Execute code
  eval(code: string, options?: EvalOptions): Promise<EvalResult>;
  callFunction(name: string, args: any[], options?: CallOptions): Promise<any>;

  // Variable access
  getVariable(name: string): Promise<Variable>;
  setVariable(name: string, value: any): Promise<void>;
  listVariables(): Promise<VariableInfo[]>;

  // Control
  abort(): Promise<void>;
  isConnected(): boolean;
  getVersion(): string | null;
  restart(): Promise<void>;

  // History
  getHistory(): CommandHistoryEntry[];
}

interface EvalOptions {
  timeout?: number;                // Override default timeout
  output?: boolean;                // Capture stdout (default true)
  progress?: boolean;              // Track progress (default false)
}

interface EvalResult {
  type: string;                    // "matrix" | "string" | "void" | etc.
  value: any;                      // Marshalled result
  output?: string;                 // Captured stdout
  error?: string;                  // Scilab error message
  duration: number;                // Execution time (ms)
}
```

---

## 4. Execution Flow

### 4.1 eval("x = [1, 2, 3]")

```
1. Module calls engine.eval("x = [1, 2, 3]")
2. Scilab Runtime validates the request
3. Command is enqueued (FIFO)
4. If queue is full: reject with "busy" error
5. When command reaches front of queue:
   a. Set status to "busy"
   b. Emit engine:busy(true)
   c. Serialize JSON-RPC request
   d. Write to Scilab's stdin
   e. Wait for response (with timeout)
   f. Parse Scilab's stdout
   g. Unmarshal result
   h. Set status to "idle"
   i. Emit engine:busy(false)
   j. Return result to caller
6. Next command in queue is processed
```

### 4.2 Error During Execution

```
1. Scilab returns an error response
2. Scilab Runtime logs the error
3. Error is returned to the caller
4. The queue continues processing
5. The Scilab workspace is NOT rolled back
   (Scilab does not support transactional execution)
```

### 4.3 Process Crash During Execution

```
1. Scilab process dies
2. Sidecar detects via read() returning EOF
3. Current command receives a crash error
4. Sidecar waits 2 seconds
5. Sidecar spawns a new Scilab process
6. Sidecar runs initialization script
7. Emit engine:status("reconnected")
8. Queue continues processing remaining commands
9. User is notified: "Scilab engine restarted"
```

---

## 5. Process Management

### 5.1 Lifecycle

```
Spawn
  │
  ▼
Initialize (run init script)
  │
  ▼
Ready (accepting commands)
  │
  ▼
Processing (executing a command)
  │
  ▼
Ready (next command)
  │
  ...
  │
  ▼
Shutdown (SIGTERM → SIGKILL)
```

### 5.2 Initialization Script

After spawning, the Sidecar sends:

```scilab
// Scilab Studio initialization
funcprot(0);

// JSON serialization helpers
function json_str = ss_serialize(value)
    // Handle matrices, strings, structs, lists
endfunction

function value = ss_deserialize(json_str)
    // Parse JSON string to Scilab value
endfunction

// Output formatting
format("v", 20);
```

### 5.3 Restart Policy

| Event | Action |
|-------|--------|
| Process exits normally | No restart needed |
| Process crashes | Restart after 2s delay |
| 3 crashes in 60s | Stop restarting, show "Reconnect" dialog |
| User requests restart | Restart immediately |

---

## 6. Variable Marshalling

### Scilab → TypeScript

| Scilab Type | JSON Wire Format | Example |
|-------------|------------------|---------|
| `double` (scalar) | `number` | `42` |
| `double` (matrix) | `number[][]` | `[[1, 2], [3, 4]]` |
| `complex` | `{ real, imag }` | `{ "real": 1, "imag": 2 }` |
| `string` | `string` | `"hello"` |
| `string` (vector) | `string[]` | `["a", "b", "c"]` |
| `boolean` | `boolean` | `true` |
| `list` | `array` | `[1, "two", 3.0]` |
| `struct` | `object` | `{ "key": "value" }` |
| `void` | `null` | `null` |

### TypeScript → Scilab

| JSON Type | Scilab Type | Notes |
|-----------|-------------|-------|
| `number` | `double` | Scalar |
| `number[]` | `double` (row vector) | 1×N matrix |
| `number[][]` | `double` (matrix) | M×N matrix |
| `string` | `string` | Scalar |
| `string[]` | `string` (vector) | 1×N cell |
| `boolean` | `boolean` | `%t` / `%f` |
| `object` | `struct` | Keys become field names |
| `array` | `list` | Mixed types allowed |

---

## 7. Cancellation

### 7.1 Abort Flow

```
1. User clicks "Abort" (or Ctrl+C)
2. engine:abort event is emitted
3. Scilab Runtime sends abort request to Sidecar
4. Sidecar sends SIGINT to Scilab process
5. Scilab interrupts the current computation
6. Scilab returns an error (interrupted)
7. The command receives a cancellation error
8. The queue continues with the next command
```

### 7.2 Abort Limitations

- Scilab may not respond to SIGINT during certain built-in operations.
- If SIGINT does not work within 5 seconds, SIGKILL is sent.
- The Scilab workspace may be in an inconsistent state after abort.
- The user is notified and offered the option to restart Scilab.

---

## 8. Progress Tracking

For long-running computations, the Scilab Runtime can track progress:

```typescript
// Enable progress tracking
const result = await engine.eval("for i=1:1000; x=i; end", { progress: true });

// Progress events are emitted
engine.on("engine:progress", (event) => {
  updateProgressBar(event.payload.percent);
});
```

Progress is tracked by:
1. Instrumenting Scilab code with progress markers (user adds `ss_progress(N, total)` calls).
2. Monitoring computation time and estimating completion.
3. For known operations (e.g., matrix operations), estimating based on input size.

---

## 9. Logging

Every command is logged:

```typescript
interface CommandHistoryEntry {
  id: string;
  code: string;                    // The Scilab code (truncated at 1KB)
  timestamp: number;
  duration: number;                // ms
  status: "success" | "error" | "timeout" | "cancelled" | "crash";
  result?: any;                    // Serialized result (truncated at 1KB)
  error?: string;
}
```

The last 100 commands are kept in memory. All commands are persisted to the SQLite `command_log` table.

The Debug panel (Ctrl+Shift+D) shows the command history with full details.

---

## 10. Security

### 10.1 Code Execution

- All Scilab code execution goes through the Command Queue.
- No module can bypass the queue to execute code directly.
- The queue enforces timeouts to prevent infinite loops.
- The queue enforces size limits (code > 1MB is rejected).

### 10.2 Variable Access

- Variable access is serialized through the queue.
- Plugins with `engine:eval` permission can execute arbitrary code.
- Plugins without `engine:eval` can only read variables via `getVariable`.

### 10.3 Process Isolation

- Scilab runs as a child process with no network access.
- Scilab's file system access is limited to the project directory (via `chdir`).
- Scilab cannot spawn child processes.
