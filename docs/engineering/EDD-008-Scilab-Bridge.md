# EDD-008: Scilab Bridge

## Purpose

The Scilab Bridge manages communication between the frontend and the Scilab runtime process.

## Architecture

```
┌─────────────────────────────────────────┐
│          Scilab Bridge                   │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Process   │  │ JSON-RPC         │   │
│  │ Manager   │  │ Client           │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Command   │  │ Variable         │   │
│  │ Queue     │  │ Cache            │   │
│  └───────────┘  └──────────────────┘   │
│  ┌──────────────────────────────────┐  │
│  │ Version Detector                 │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Process Manager

```typescript
interface ProcessManager {
  start(): Promise<void>;
  stop(): Promise<void>;
  restart(): Promise<void>;
  getState(): ProcessState;
  onStateChange(handler: (state: ProcessState) => void): Disposable;
}
```

**States:**
```
NotRunning → Starting → Ready → Running → Idle → Stopping → NotRunning
```

**Auto-Recovery:**
```
Crash Detected
    ↓
Wait 1 second
    ↓
Restart Process
    ↓
Replay Last Command (if safe)
    ↓
Emit 'runtime:restarted' event
```

## JSON-RPC Client

```typescript
interface JSONRPCClient {
  request(method: string, params: any, timeout?: number): Promise<any>;
  batch(requests: RPCRequest[]): Promise<any[]>;
}
```

**Message Format:**
```json
// Request
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "execute",
  "params": { "code": "x = sin(0:0.1:10)" }
}

// Response
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "output": "",
    "variables": { "x": { "type": "matrix", "rows": 101, "cols": 1 } }
  }
}
```

## Command Queue

```typescript
interface CommandQueue {
  enqueue(command: Command): Promise<Result>;
  cancel(commandId: string): void;
  clear(): void;
  getPending(): Command[];
}
```

**Rules:**
- Sequential execution.
- Maximum queue size: 100.
- Timeout per command: 30s default.
- Cancellation support.

## Variable Cache

```typescript
interface VariableCache {
  get(name: string): Promise<VariableValue>;
  invalidate(name: string): void;
  invalidateAll(): void;
  getDirty(): string[];
}
```

**Cache Strategy:**
- Cache variable values after fetch.
- Invalidate on workspace change.
- Background refresh for frequently accessed variables.

## Version Detector

```typescript
interface VersionDetector {
  detect(): Promise<ScilabVersion>;
  isCompatible(version: string): boolean;
  getCapabilities(): ScilabCapability[];
}
```

## Scilab Interface

```typescript
interface ScilabInterface {
  execute(code: string, options?: ExecuteOptions): Promise<ExecuteResult>;
  evaluate(expression: string): Promise<any>;
  getVariable(name: string): Promise<VariableValue>;
  setVariable(name: string, value: any): Promise<void>;
  listVariables(): Promise<VariableInfo[]>;
  interrupt(): Promise<void>;
  reset(): Promise<void>;
  ping(): Promise<boolean>;
}
```

## Error Handling

- Process crash: auto-restart.
- Command timeout: interrupt and return error.
- Syntax error: return structured error with line/column.
- Queue full: reject new commands with `QueueFull`.

## Performance

- Process startup: < 3 seconds.
- Command latency: < 100ms.
- Variable fetch: < 50ms.
- Auto-recovery: < 2 seconds.
