# SPEC-008 — Scilab Execution

## Purpose

Provide a controlled, observable, and cancellable interface to the Scilab engine. Never let modules execute Scilab directly. All execution goes through the Command Queue.

---

## Command Queue

### Design
- FIFO queue, capacity 256 pending commands.
- One command executes at a time.
- Prevents race conditions, deadlocks, unbounded parallelism.

### Queue States

```
Idle → Running → Waiting → Running → ... → Idle
```

### Priority
- `critical` commands jump to front of queue.
- Normal commands follow FIFO order.

---

## API

| Method | Input | Output | Timeout |
|--------|-------|--------|---------|
| eval(code, options?) | Scilab code string | EvalResult | 60s |
| callFunction(name, args, options?) | Function name + args | Any | 30s |
| getVariable(name) | Variable name | Variable | 5s |
| setVariable(name, value) | Name + value | void | 5s |
| listVariables() | — | VariableInfo[] | 5s |
| abort() | — | void | 5s |
| isConnected() | — | boolean | — |
| getVersion() | — | string | — |
| restart() | — | void | 30s |

### EvalResult

```typescript
interface EvalResult {
  type: string;        // "matrix" | "string" | "void" | etc.
  value: any;          // Marshalled result
  output?: string;     // Captured stdout
  error?: string;      // Scilab error message
  duration: number;    // Execution time (ms)
}
```

---

## Execution Flow

```
1. Module calls engine.eval("code")
2. Validate request (size, timeout)
3. Enqueue command
4. If queue full: reject with "busy" error
5. When command reaches front:
   a. Set status to "busy"
   b. Emit engine:busy(true)
   c. Serialize JSON-RPC request
   d. Write to Scilab stdin
   e. Wait for response (with timeout)
   f. Parse stdout
   g. Unmarshal result
   h. Set status to "idle"
   i. Emit engine:busy(false)
   j. Return result
6. Process next command
```

---

## Variable Marshalling

### Scilab → TypeScript

| Scilab Type | JSON Format | Example |
|-------------|-------------|---------|
| double (scalar) | number | 42 |
| double (matrix) | number[][] | [[1,2],[3,4]] |
| complex | {real, imag} | {real:1, imag:2} |
| string | string | "hello" |
| string (vector) | string[] | ["a","b"] |
| boolean | boolean | true |
| list | array | [1,"two",3.0] |
| struct | object | {key:"value"} |
| void | null | null |

### TypeScript → Scilab

| JSON Type | Scilab Type |
|-----------|-------------|
| number | double |
| number[] | double (row vector) |
| number[][] | double (matrix) |
| string | string |
| string[] | string (vector) |
| boolean | boolean |
| object | struct |
| array | list |

---

## Process Management

### Lifecycle

```
Spawn → Initialize → Ready → Processing → Ready → ... → Shutdown
```

### Initialization Script

```scilab
funcprot(0);
format("v", 20);
// JSON serialization helpers
```

### Restart Policy

| Event | Action |
|-------|--------|
| Normal exit | No restart |
| Crash | Restart after 2s delay |
| 3 crashes in 60s | Stop, show "Reconnect" dialog |
| User request | Restart immediately |

---

## Cancellation

```
1. User clicks Abort (Ctrl+C)
2. engine:abort emitted
3. Sidecar sends SIGINT to Scilab
4. Scilab interrupts computation
5. Command receives cancellation error
6. Queue continues with next command
```

If SIGINT fails within 5s → SIGKILL. Workspace may be inconsistent after abort.

---

## Progress Tracking

Long-running computations can report progress:
- User instruments code with `ss_progress(N, total)` calls.
- Progress events emitted: `engine:progress { percent, message }`.
- UI shows progress bar.

---

## Logging

Last 100 commands kept in memory. All commands persisted to SQLite `command_log` table.

```typescript
interface CommandHistoryEntry {
  id: string;
  code: string;           // Truncated at 1KB
  timestamp: number;
  duration: number;
  status: "success" | "error" | "timeout" | "cancelled" | "crash";
  result?: any;           // Truncated at 1KB
  error?: string;
}
```

---

## Security

- All execution through the Command Queue. No bypass.
- Timeout enforcement prevents infinite loops.
- Code > 1MB rejected.
- Plugins without `engine:eval` can only read variables.
- Scilab runs as child process with no network access.
- Scilab file access limited to project directory.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Queue capacity | 256 |
| Default eval timeout | 60s |
| Default callFunction timeout | 30s |
| Max code size | 1MB |
| Command history (memory) | 100 |
| Max crashes before stop | 3 in 60s |
| Restart delay | 2s |
| Abort timeout (SIGKILL) | 5s |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Scilab not found | Runtime disconnected, features disabled |
| Scilab crashes | Auto-restart (max 3 in 60s) |
| Command timeout | Abort command, return timeout error |
| Queue overflow | Reject new commands with "busy" |
| Invalid JSON-RPC | Parse error, skip malformed output |
| Scilab syntax error | Return error with line/column info |
| Variable not found | Return "Undefined variable" error |

---

## Extension Points

- Custom output parsers.
- Custom variable marshallers.
- Execution middleware (logging, profiling, rate limiting).
- Custom progress tracking strategies.
- Multi-engine support (future).
