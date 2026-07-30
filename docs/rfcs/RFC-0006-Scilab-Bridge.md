# RFC-0006: Scilab Bridge

| Field | Value |
|-------|-------|
| RFC | 0006 |
| Title | Scilab Bridge |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how the application communicates with the Scilab runtime process.

## Motivation

Scilab is the numerical engine. All computation flows through it. The bridge must be reliable, fast, and handle process lifecycle cleanly.

## Detailed Design

### Process Lifecycle

```
Not Running → Starting → Ready → Running → Idle → Stopping → Not Running
```

| State | Description |
|-------|-------------|
| Not Running | No Scilab process exists |
| Starting | Process spawned, waiting for ready signal |
| Ready | Process initialized, accepting commands |
| Running | Actively executing a command |
| Idle | Waiting for next command |
| Stopping | Shutdown in progress |

### Communication Protocol

JSON-RPC 2.0 over stdin/stdout.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "execute",
  "params": {
    "code": "x = sin(0:0.1:10)",
    "timeout": 30000
  }
}
```

**Success Response:**
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "output": "",
    "variables": {
      "x": { "type": "matrix", "rows": 101, "cols": 1 }
    }
  }
}
```

**Error Response:**
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "error": {
    "code": -1,
    "message": "Syntax error",
    "data": {
      "line": 1,
      "column": 5
    }
  }
}
```

### Methods

| Method | Description | Params | Result |
|--------|-------------|--------|--------|
| `execute` | Execute Scilab code | `code`, `timeout` | `output`, `variables` |
| `evaluate` | Evaluate expression and return value | `expression`, `timeout` | `value` |
| `getVariable` | Get a variable from workspace | `name` | `value` |
| `setVariable` | Set a variable in workspace | `name`, `value` | `success` |
| `listVariables` | List workspace variables | — | `variables[]` |
| `getVariableInfo` | Get variable type/size | `name` | `info` |
| `interrupt` | Interrupt current execution | — | `success` |
| `reset` | Reset Scilab workspace | — | `success` |
| `getVersion` | Get Scilab version | — | `version` |
| `ping` | Check if process is alive | — | `pong` |

### Error Codes

| Code | Meaning |
|------|---------|
| -1 | Syntax error |
| -2 | Runtime error |
| -3 | Variable not found |
| -4 | Type mismatch |
| -5 | Timeout exceeded |
| -6 | Execution interrupted |
| -7 | Process not ready |
| -8 | Invalid parameters |

### Auto-Recovery

If the Scilab process crashes:
1. The bridge detects the broken pipe.
2. It waits 1 second, then restarts the process.
3. It replays the last command (if safe).
4. It emits a `runtime:restarted` event.

### Version Detection

On startup, the bridge runs `getVersion` and stores the result. APIs that depend on Scilab version check this before calling version-specific functions.

### Command Queue

Commands are queued and executed sequentially. Maximum queue size: 100. If the queue is full, new commands are rejected with `-7`.

### Timeout

Every command has a configurable timeout (default: 30s). If the command doesn't complete in time, it is interrupted and the caller receives `-5`.

## Alternatives Considered

1. **TCP socket**: More flexible but adds network overhead. stdio is simpler for local process.
2. **Shared memory**: Fastest but complex and platform-specific.
3. **D-Bus**: Linux-only. Not cross-platform.

## Security Considerations

- Scilab process runs with the same user permissions as the application.
- No network access from the Scilab process (unless explicitly enabled).
- Command timeout prevents runaway computations from blocking the UI.

## Testing Strategy

- Unit tests for JSON-RPC message serialization.
- Integration tests for each method.
- Failure tests for process crash and recovery.
- Performance tests for command throughput (1000 commands/second).

## Rollout

- v0.1: Basic execute, evaluate, getVariable, listVariables, ping.
- v0.2: Full method set, auto-recovery, version detection.
