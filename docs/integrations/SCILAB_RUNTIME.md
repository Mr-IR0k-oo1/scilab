# Scilab Runtime Integration Architecture

**Document Status:** Production Normative Specification  
**Phase:** 2 — Scilab Runtime Integration  

---

## 1. System Architecture

The Scilab Runtime Integration orchestrates external computation processes without blocking the FastAPI event loop or cluttering presentation logic in the React frontend.

```
React Frontend (presentation)
      │
      ▼ REST API / WebSocket (/ws/scilab)
FastAPI Routes (app/api/routes/scilab.py)
      │
      ▼
Scilab Service (app/services/scilab_service.py)
      │
      ├───────────────────────┬───────────────────────┐
      ▼                       ▼                       ▼
Session Manager         Scilab Executor         Event Bus
(session.py)            (executor.py)        (scilab_events.py)
      │                       │
      └───────────┬───────────┘
                  ▼
          Process Manager
      (process_manager.py)
                  │
                  ▼ asyncio.subprocess
          Scilab Engine CLI
```

---

## 2. Detection System

The detection system automatically scans the host environment across operating systems:

- **Windows:** Searches `SCILAB_EXECUTABLE` env var, PATH, and `C:\Program Files\scilab-*\bin\scilab-cli.exe`.
- **Linux:** Searches `SCILAB_EXECUTABLE`, PATH, `/usr/bin/scilab-cli`, and `/usr/local/bin/scilab-cli`.
- **macOS:** Searches `SCILAB_EXECUTABLE`, PATH, and `/Applications/Scilab-*.app/Contents/bin/scilab-cli`.

Priority sequence:
1. Environment Variable (`SCILAB_EXECUTABLE`)
2. Application Configuration (`scilab_config.executable`)
3. System `PATH` (`shutil.which('scilab-cli')`)
4. Platform Common Install Locations

---

## 3. Process & Session Lifecycle

### 3.1 Process Manager
Uses non-blocking `asyncio.create_subprocess_exec` without `shell=True`. Arguments are supplied strictly as array lists to prevent argument injection attacks.

### 3.2 Session State Machine
Thread-safe state transitions:
`CREATED` → `STARTING` → `RUNNING` ⇄ `EXECUTING` → `STOPPING` → `STOPPED` (or `FAILED`)

Invalid state transitions (e.g. executing before startup or after shutdown) raise `ScilabSessionStateError`.

---

## 4. Execution Flow, Timeouts & Security

### 4.1 Execution Flow
1. API handler receives command or script execution request.
2. `ScilabService` validates request permissions and session availability.
3. `ScilabExecutor` sends command/script string to process stdin.
4. Output lines are captured non-blocking and streamed to WebSocket clients and published to `EventBus`.
5. Result is returned as structured Pydantic model (`ExecutionResultResponse`).

### 4.2 Timeout Behavior
- Configured via `SCILAB_TIMEOUT` (default: 30s) or request override.
- Sequence on timeout:
  1. Mark execution status as `TIMED_OUT`.
  2. Attempt graceful process termination (`SIGTERM`).
  3. If un-terminated after fallback interval, force kill (`SIGKILL`).
  4. Record failure and return cleanly without orphan processes or server crash.

### 4.3 Output Limits
- Configured via `SCILAB_MAX_OUTPUT_SIZE` (default: 1 MB).
- Output exceeding the limit is safely truncated with marker `... [OUTPUT TRUNCATED DUE TO SIZE LIMIT]`.

### 4.4 Script Security & Path Traversal Prevention
- Script path must exist and be a valid file.
- File extension must be `.sci` or `.sce`.
- Path traversal sequences (`..`) are strictly prohibited and raise `ScilabSecurityException`.
- Paths must reside inside approved workspace/project boundaries.

---

## 5. API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/scilab/status` | GET | Returns detection status and session state |
| `/api/v1/scilab/start` | POST | Starts the Scilab process session |
| `/api/v1/scilab/stop` | POST | Gracefully stops the session |
| `/api/v1/scilab/restart` | POST | Restarts the Scilab process |
| `/api/v1/scilab/execute` | POST | Executes inline Scilab code |
| `/api/v1/scilab/execute-script` | POST | Executes validated script file |
| `/api/v1/scilab/executions/{id}` | GET | Returns execution status by ID |
| `/api/v1/scilab/executions/{id}/cancel` | POST | Cancels running execution |
| `/ws/scilab` | WebSocket | Real-time JSON message streaming |

---

## 6. Testing & Observability

- Pytest integration suite located at `backend/tests/integrations/scilab/`.
- All tests use mocked process primitives so CI pipeline passes 100% cleanly without requiring local Scilab installation.
