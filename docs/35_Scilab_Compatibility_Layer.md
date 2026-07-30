# Scilab Studio — Scilab Compatibility Layer

**Version:** 1.0.0
**Status:** Normative
**Last Updated:** 2026-07-27

This document specifies the Scilab Compatibility Layer: how Scilab Studio communicates with the Scilab engine, manages its lifecycle, and handles version differences. For the JSON-RPC protocol, see [System Architecture §7](03_System_Architecture.md). For the Sidecar architecture, see [Technical Architecture §1](20_Technical_Architecture.md).

---

## 1. Scilab Discovery

### 1.1 Search Order

The Sidecar locates the Scilab binary in this priority order:

1. **Environment variable:** `SCILAB_PATH` (highest priority).
2. **User setting:** `~/.config/scilab-studio/settings.json → engine.path`.
3. **Platform defaults:**
   | Platform | Default Paths |
   |----------|---------------|
   | Linux | `/usr/bin/scilab`, `/usr/local/bin/scilab`, `/opt/scilab/bin/scilab` |
   | macOS | `/Applications/Scilab.app/Contents/MacOS/bin/scilab` |
   | Windows | `C:\Program Files\Scilab\bin\scilab.exe`, `C:\Program Files (x86)\Scilab\bin\scilab.exe` |
4. **PATH lookup:** Search the system PATH for `scilab`.
5. **Not found:** Show the Scilab Setup Dialog. Block engine features until configured.

### 1.2 Version Detection

After locating the binary, the Sidecar queries the version:

```bash
scilab --version --noexec
```

Expected output format: `Scilab version "2024.1.0"`

The Sidecar parses this and stores:
- Major version (e.g., 2024)
- Minor version (e.g., 1)
- Patch version (e.g., 0)
- Full version string

### 1.3 Version Compatibility

| Scilab Version | Status | Notes |
|----------------|--------|-------|
| 7.0.x | Supported | Basic features only |
| 2023.x | Supported | Full feature set |
| 2024.x | Fully Supported | Recommended |
| 2025.x+ | Forward-compatible | New features may not work |

If the detected version is incompatible (< 7.0), the platform shows a warning and disables engine features.

---

## 2. Process Lifecycle

### 2.1 Startup

```
Sidecar starts
  ├── Locate Scilab binary
  ├── Validate binary exists and is executable
  ├── Spawn Scilab process:
  │     scilab --noexec --noatoms --nogui
  │     (headless mode, no GUI, no atoms)
  ├── Attach stdin/stdout pipes
  ├── Wait for ready signal (first prompt)
  ├── Send initialization:
  │     // Disable GUI elements
  │     // Set working directory to project root
  │     // Load any project-specific .sce files
  └── Emit engine:status("connected")
```

### 2.2 Steady State

During normal operation:
- The Sidecar reads stdout from Scilab line-by-line.
- Complete JSON-RPC messages are assembled from lines.
- Incoming requests from the Core Process are serialized and written to Scilab's stdin.
- The Sidecar monitors Scilab's process status (alive/dead/busy).

### 2.3 Shutdown

```
Sidecar receives stop signal
  ├── Send SIGTERM to Scilab process
  ├── Wait up to 5 seconds for graceful exit
  ├── If still running: send SIGKILL
  ├── Close stdin/stdout pipes
  └── Emit engine:status("disconnected")
```

### 2.4 Crash Recovery

If the Scilab process dies unexpectedly:
1. The Sidecar detects the process exit (read returns EOF).
2. It emits `engine:status("disconnected")`.
3. It waits 2 seconds before restarting.
4. It spawns a new Scilab process (steps from §2.1).
5. It restores the working directory and loads any cached state.
6. It emits `engine:status("connected")`.
7. It notifies the user: "Scilab engine restarted due to unexpected shutdown."

Maximum retries: 3 in 60 seconds. If retries are exhausted, the platform shows a "Reconnect" dialog with manual retry and "Change Scilab Path" options.

---

## 3. JSON-RPC Protocol

### 3.1 Message Format

All messages are newline-delimited JSON over stdin/stdout. Encoding: UTF-8.

**Request:**
```jsonc
{ "jsonrpc": "2.0", "id": "req_a1b2c3", "method": "eval", "params": { "code": "x = [1, 2, 3]" } }
```

**Success response:**
```jsonc
{ "jsonrpc": "2.0", "id": "req_a1b2c3", "result": { "type": "matrix", "value": [[1, 2, 3]] } }
```

**Error response:**
```jsonc
{ "jsonrpc": "2.0", "id": "req_a1b2c3", "error": { "code": -32603, "message": "Evaluation failed", "data": { "scilabError": "Undefined variable: y" } } }
```

### 3.2 Methods

| Method | Params | Result | Timeout | Description |
|--------|--------|--------|---------|-------------|
| `eval` | `{ code, timeout? }` | `{ type, value, output? }` | 60s default | Execute Scilab code |
| `getVariable` | `{ name }` | `{ type, value }` | 5s | Get variable value |
| `setVariable` | `{ name, type, value }` | `{ success }` | 5s | Set variable value |
| `callFunction` | `{ name, args, timeout? }` | `{ type, value }` | 30s default | Call Scilab function |
| `getWorkingDirectory` | `{}` | `{ path }` | 5s | Get CWD |
| `setWorkingDirectory` | `{ path }` | `{ success }` | 5s | Set CWD |
| `getVariableNames` | `{}` | `{ names }` | 5s | List all variables |
| `isBusy` | `{}` | `{ busy }` | 1s | Check if computing |
| `abort` | `{}` | `{ success }` | 5s | Abort computation |
| `getVersion` | `{}` | `{ version, fullVersion }` | 5s | Get Scilab version |

### 3.3 Variable Marshalling

| Scilab Type | JSON Wire Format | Example |
|-------------|------------------|---------|
| `double` (scalar) | `number` | `42` |
| `double` (matrix) | `number[][]` | `[[1, 2], [3, 4]]` |
| `complex` (scalar) | `{ real, imag }` | `{ "real": 1, "imag": 2 }` |
| `complex` (matrix) | `{ real[][], imag[][] }` | `{ "real": [[1]], "imag": [[2]] }` |
| `string` | `string` | `"hello"` |
| `string` (vector) | `string[]` | `["a", "b", "c"]` |
| `boolean` | `boolean` | `true` |
| `list` | `array` | `[1, "two", 3.0]` |
| `struct` | `object` | `{ "key": "value" }` |
| `void` (no return) | `null` | `null` |

### 3.4 Error Codes

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid request | Not a valid JSON-RPC request |
| -32601 | Method not found | Unknown method name |
| -32602 | Invalid params | Invalid method parameters |
| -32603 | Internal error | Scilab evaluation failed |
| -32000 | Plugin error | Plugin-level error |
| -32001 | Timeout | Request timed out |
| -32002 | Aborted | Computation was aborted by user |
| -32003 | Engine busy | Engine is busy with another computation |

---

## 4. Initialization

### 4.1 Engine Setup

After connecting, the Sidecar sends initialization code to Scilab:

```scilab
// Scilab Studio initialization
// Disable GUI elements
// Set format for JSON output
funcprot(0);  // Disable function protection warnings

// Define helper functions for JSON serialization
function json_str = ss_serialize(value)
    // Serialize a Scilab value to JSON-compatible string
    // (Implementation handles matrices, strings, structs, lists)
endfunction

function value = ss_deserialize(json_str)
    // Deserialize a JSON string to Scilab value
endfunction

// Set up output formatting
format("v", 20);  // 20 digits of precision
```

### 4.2 Project Loading

When a project is opened, the Sidecar loads project-specific initialization:

```scilab
// Set working directory
chdir('/path/to/project');

// Load project scripts (if configured)
exec('scripts/init.sce', -1);
```

---

## 5. Timeout Handling

### 5.1 Default Timeouts

| Operation | Default Timeout | Configurable |
|-----------|----------------|-------------|
| `eval` | 60 seconds | Yes (per request) |
| `callFunction` | 30 seconds | Yes (per request) |
| `getVariable` | 5 seconds | No |
| `setVariable` | 5 seconds | No |
| `abort` | 5 seconds | No |
| Connection ready | 30 seconds | No |

### 5.2 Timeout Behavior

When a request times out:
1. The Sidecar sends an `abort` command to Scilab.
2. It waits up to 5 seconds for Scilab to respond to the abort.
3. If Scilab does not respond, the Sidecar kills the process and restarts.
4. The caller receives a timeout error response.

### 5.3 Long-Running Computations

For computations expected to exceed 60 seconds:
- The caller can specify a custom timeout: `{ "code": "...", "timeout": 300000 }` (5 minutes).
- The Sidecar monitors the process and allows it to continue.
- The `isBusy` method can be polled to check if the computation is still running.
- The user can manually abort at any time.

---

## 6. Output Parsing

### 6.1 Stdout Handling

Scilab's stdout is parsed line-by-line. The Sidecar looks for:

1. **JSON-RPC responses:** Lines that are valid JSON objects with `jsonrpc`, `id`, and either `result` or `error`.
2. **Debug output:** Lines prefixed with `[SS_DEBUG]` are captured and forwarded to the debug console.
3. **Warnings:** Lines containing `Warning:` are captured and forwarded as warnings.
4. **Errors:** Lines containing `Error` are captured and forwarded as errors.
5. **Regular output:** All other lines are forwarded to the console panel as stdout.

### 6.2 Stderr Handling

Scilab's stderr is captured and forwarded to the console panel as errors. Stderr output does not affect the JSON-RPC communication.

### 6.3 Binary Output

If Scilab produces binary output (e.g., from `display()`), the Sidecar captures it and encodes it as base64 in the JSON-RPC result.

---

## 7. State Management

### 7.1 Variable Caching

The Sidecar maintains a lightweight cache of Scilab variables:
- On `eval`, if the result is a variable assignment, the cache is updated.
- On `getVariable`, the cache is checked first (faster than IPC).
- On `setVariable`, the cache is updated after Scilab confirms.
- Cache is invalidated on engine restart.

### 7.2 Working Directory

The Sidecar tracks the current working directory and restores it after restart. The directory is set from the project root when a project is opened.

### 7.3 History

The Sidecar maintains a history of the last 100 eval commands for:
- Command history in the console panel.
- Undo/redo support in the code editor.
- Debugging and replay.
