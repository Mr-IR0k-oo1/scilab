# Runtime API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.1 |
| Stability | Stable |

---

## Purpose

Manages the Scilab runtime process: execution, variable access, and lifecycle.

## Methods

### runtime.getStatus(): RuntimeStatus

Returns the current runtime status.

```javascript
const status = runtime.getStatus();
console.log(status.state); // "ready"
console.log(status.scilabVersion); // "7.0.0"
```

### runtime.execute(code: string, options?: ExecuteOptions): Promise\<ExecuteResult\>

Executes Scilab code.

```javascript
const result = await runtime.execute('x = sin(0:0.1:10)');
console.log(result.output); // ""
console.log(result.variables); // { x: { type: "matrix", rows: 101, cols: 1 } }
```

### runtime.evaluate(expression: string): Promise\<any\>

Evaluates a Scilab expression and returns the result.

```javascript
const value = await runtime.evaluate('sin(%pi/2)');
console.log(value); // 1
```

### runtime.getVariable(name: string): Promise\<VariableValue\>

Gets a variable from the Scilab workspace.

```javascript
const x = await runtime.getVariable('x');
console.log(x.type); // "matrix"
console.log(x.rows); // 101
```

### runtime.setVariable(name: string, value: any): Promise\<void\>

Sets a variable in the Scilab workspace.

```javascript
await runtime.setVariable('frequency', 60);
```

### runtime.listVariables(): Promise\<VariableInfo[]\>

Lists all workspace variables.

```javascript
const vars = await runtime.listVariables();
vars.forEach(v => console.log(`${v.name}: ${v.type}`));
```

### runtime.interrupt(): Promise\<void\>

Interrupts the current execution.

```javascript
await runtime.interrupt();
```

### runtime.reset(): Promise\<void\>

Resets the Scilab workspace (clears all variables).

```javascript
await runtime.reset();
```

### runtime.restart(): Promise\<void\>

Restarts the Scilab process.

```javascript
await runtime.restart();
```

### runtime.getVersion(): Promise\<string\>

Returns the Scilab version.

```javascript
const version = await runtime.getVersion();
console.log(version); // "7.0.0"
```

### runtime.ping(): Promise\<boolean\>

Checks if the runtime is responsive.

```javascript
const alive = await runtime.ping();
console.log(alive); // true
```

### runtime.onOutput(handler: (text: string) => void): Disposable

Subscribes to Scilab stdout output.

```javascript
const disposable = runtime.onOutput((text) => {
  console.log('Scilab:', text);
});

// Later
disposable.dispose();
```

### runtime.onError(handler: (error: string) => void): Disposable

Subscribes to Scilab stderr output.

```javascript
const disposable = runtime.onError((error) => {
  console.error('Scilab error:', error);
});
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `runtime:starting` | `{ pid: number }` | Runtime process is starting |
| `runtime:ready` | `{ version: string }` | Runtime is ready |
| `runtime:busy` | `{ commandId: string }` | Runtime is executing |
| `runtime:idle` | `{ commandId: string }` | Runtime finished executing |
| `runtime:output` | `{ text: string }` | Stdout output |
| `runtime:error` | `{ text: string }` | Stderr output |
| `runtime:crashed` | `{ error: Error }` | Runtime process crashed |
| `runtime:restarted` | `{ pid: number }` | Runtime was restarted |
| `runtime:variablesChanged` | `{ variables: string[] }` | Variables were modified |

## Examples

### Execute and Process Results

```javascript
// Run a calculation
const result = await runtime.execute(`
  t = 0:0.01:1;
  y = sin(2 * %pi * 5 * t);
  [t, y]
`);

// The result contains the output and variables
console.log(result.variables);
// { t: { type: "matrix", rows: 101, cols: 1 }, y: { type: "matrix", rows: 101, cols: 1 } }
```

### Stream Output

```javascript
runtime.onOutput((text) => {
  // Append to console panel
  consolePanel.append(text);
});

await runtime.execute('disp("Hello from Scilab")');
// "Hello from Scilab" appears in console
```

### Handle Crashes

```javascript
runtime.on('runtime:crashed', async (event) => {
  console.error('Scilab crashed:', event.error);

  // Auto-restart
  await runtime.restart();

  // Re-run last command
  await runtime.execute(lastCommand);
});
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `RuntimeNotReady` | RT-001 | Runtime is not ready |
| `ExecutionTimeout` | RT-002 | Command timed out |
| `SyntaxError` | RT-003 | Scilab syntax error |
| `RuntimeError` | RT-004 | Scilab runtime error |
| `VariableNotFound` | RT-005 | Variable does not exist |
| `TypeMismatch` | RT-006 | Variable type mismatch |
| `ProcessCrashed` | RT-007 | Scilab process crashed |
| `QueueFull` | RT-008 | Command queue is full |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
