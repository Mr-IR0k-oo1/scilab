# Python Backend with Dual Deployment

**Date:** 2026-08-03
**Status:** Approved

## Context

The desktop app's backend is currently implemented as Tauri Rust command handlers in
`apps/desktop/src-tauri/src/` (scilab process management, filesystem/project operations,
chart CRUD, widget definitions). The frontend talks to them via
`@tauri-apps/api/core.invoke()`. The landing site (`frontend/`) is static and has no backend.

The team wants a Python backend that both the Tauri desktop app and a web deployment can
talk to, with full feature parity to the current Rust command surface, and the Rust command
handlers removed.

## Goals

- Replace the Rust command handlers with a FastAPI backend written in Python.
- Serve both the Tauri desktop shell and a plain web deployment of the same Next.js app.
- Full parity with every current Rust command: scilab, filesystem, projects, charts, widgets.
- Frontend talks to Python over HTTP in both desktop and web modes; no `invoke()` calls
  remain in app code.
- Tauri becomes a minimal launcher: create window, spawn Python backend, kill on exit.

## Non-Goals

- Bundling a self-contained Python runtime (sidecar). The desktop app requires Python 3.10+
  on the machine and spawns the system Python.
- Replacing the Scilab subprocess approach with Scilab's socket protocol.
- Changing the landing site (`frontend/`); it stays static.
- Adding authentication/authorization to the backend in this pass.

## Architecture

### Repository layout

New `backend/` directory at the repo root, outside the npm workspaces:

```
backend/
  pyproject.toml            # fastapi, uvicorn, pydantic
  fossee_backend/
    __init__.py
    main.py                 # FastAPI app + CORS + /api/health
    config.py               # port, FOSSEE_PROJECTS_DIR resolution
    models.py               # shared pydantic response models
    scilab.py               # asyncio subprocess actor for scilab-cli
    filesystem.py           # fs + project CRUD (port of fs.rs)
    charts.py               # in-memory chart state (port of visualization.rs)
    widgets.py              # widget type defs + instance state (port of widgets.rs)
    routers/
      __init__.py
      scilab.py
      fs.py
      projects.py
      charts.py
      widgets.py
```

### Backend runtime

- FastAPI + uvicorn, dependencies declared in `backend/pyproject.toml`.
- Listens on `127.0.0.1:8747` by default; override with `FOSSEE_BACKEND_PORT`.
- CORS: allow `http://localhost:1420`, `tauri://localhost`, and any origins in
  `FOSSEE_CORS_ORIGINS` (comma-separated, for web deployment).
- `GET /api/health` returns `{ "status": "ok" }`.

### Project directory resolution

`FOSSEE_PROJECTS_DIR` env var wins; otherwise fall back to `<Documents>/FOSSEE`
(`~/Documents/FOSSEE` on Linux/macOS, the user's Documents folder on Windows), matching
the current Rust `get_fossee_dir` behavior.

### Scilab execution

Port the Rust actor to asyncio:

- One persistent `scilab-cli --nw --noecho` subprocess per backend run, spawned lazily on
  `POST /api/scilab/start`.
- Piped stdin/stdout; code is written followed by the `__SCILAB_END__` delimiter line;
  stdout is read until the marker is seen.
- A single asyncio lock serializes writes to the child, matching the "no concurrent
  writes" guarantee of the Rust actor.
- `POST /api/scilab/execute` returns `{ "output": str, "variables": object, "error": str|null, "success": bool }`.
- On crash detection (`child.try_wait()` equivalent), the next execute returns
  "Scilab is not running" and the process is reaped.

### Endpoint surface

Every current Rust command maps to a REST endpoint:

| Area | Rust command(s) | Python endpoint(s) |
|---|---|---|
| Scilab | `start_scilab` | `POST /api/scilab/start` |
| | `stop_scilab` | `POST /api/scilab/stop` |
| | `execute_code` | `POST /api/scilab/execute` |
| | `scilab_status` | `GET /api/scilab/status` |
| FS | `read_text_file` | `GET /api/fs/file?path=` |
| | `write_text_file` | `PUT /api/fs/file` |
| | `list_directory` | `GET /api/fs/list?path=` |
| | `create_directory` | `POST /api/fs/dir` |
| | `remove_file` | `DELETE /api/fs/file?path=` |
| | `remove_directory` | `DELETE /api/fs/dir?path=` |
| | `file_exists` | `GET /api/fs/exists?path=` |
| | `path_info` | `GET /api/fs/info?path=` |
| | `rename_path` | `POST /api/fs/rename` |
| Projects | `get_project_dir` | `GET /api/projects/dir` |
| | `create_project` | `POST /api/projects` |
| | `list_projects` | `GET /api/projects` |
| | `update_project_metadata` | `PATCH /api/projects/{name}` |
| | `delete_project` | `DELETE /api/projects/{name}` |
| Charts | `viz_create_chart` | `POST /api/charts` |
| | `viz_get_chart` | `GET /api/charts/{id}` |
| | `viz_update_chart` | `PATCH /api/charts/{id}` |
| | `viz_update_chart_data` | `PUT /api/charts/{id}/data` |
| | `viz_destroy_chart` | `DELETE /api/charts/{id}` |
| | `viz_export_chart` | `GET /api/charts/{id}/export?format=` |
| | `viz_get_supported_types` | `GET /api/charts/types` |
| Widgets | `widget_get_widget_type` | `GET /api/widgets/types/{id}` |
| | `widget_get_all_widget_types` | `GET /api/widgets/types` |
| | `widget_get_widget_types_by_category` | `GET /api/widgets/types/category/{category}` |
| | `widget_create_widget` | `POST /api/widgets` |
| | `widget_get_widget` | `GET /api/widgets/{id}` |
| | `widget_destroy_widget` | `DELETE /api/widgets/{id}` |
| | `widget_set_property` | `PATCH /api/widgets/{id}/property` |
| | `widget_bind_property` | `POST /api/widgets/{id}/bind` |
| | `widget_unbind_property` | `POST /api/widgets/{id}/unbind` |
| | `widget_serialize_widget` | `GET /api/widgets/{id}/serialize` |
| | `widget_deserialize_widget` | `POST /api/widgets/deserialize` |

Response shapes mirror the Rust `*Result` structs (field names kept identical so the
frontend client can be a thin rename).

## Frontend changes

### Transport

- New `apps/desktop/src/lib/api.ts`: a fetch-based client exposing an `ApiTransport`
  interface with a single `request(method, path, body)` method. Ships a `FetchTransport`
  implementation. This keeps an invoke-based transport possible later without touching
  callers.
- Base URL: `NEXT_PUBLIC_API_URL` env var, default `http://127.0.0.1:8747`.

### Rewritten modules (same public signatures)

- `apps/desktop/src/lib/scilab.ts` — `startScilab`, `stopScilab`, `executeScilabCode`,
  `getScilabStatus`, `syncScilabStatus` now call the Python endpoints.
- `apps/desktop/src/lib/fs.ts` — all file/project helpers now call the Python endpoints.
- `packages/runtime/src/scilab-bridge.ts` — same rewrite to fetch-based; drop
  `@tauri-apps/api/core` import.

Callers (`Shell.tsx`, `Sidebar.tsx`, `ScriptEditor.tsx`, `EcosystemShell.tsx`,
`WorkspaceManager.tsx`, modules) are unchanged because signatures stay the same.

### Backend health in the UI

- Add `backendStatus: 'online' | 'offline'` to the store and a `syncBackendStatus()`
  helper that polls `GET /api/health` on an interval.
- Surface status in `StatusBar.tsx` (and reuse the existing pattern used for scilab
  status polling in `Shell.tsx`).

## Tauri changes

- Delete `apps/desktop/src-tauri/src/scilab.rs`, `fs.rs`, `visualization.rs`, `widgets.rs`.
- Rewrite `apps/desktop/src-tauri/src/main.rs` as a minimal launcher:
  - Create the app window (unchanged Tauri setup).
  - On startup, spawn `python3 -m uvicorn fossee_backend.main:app --host 127.0.0.1 --port 8747`
    with cwd pointing at `backend/`, and set `FOSSEE_PROJECTS_DIR` so the backend uses the
    desktop project location.
  - Pipe the Python process stdout/stderr to the Tauri log.
  - Kill the Python child on app exit (RunEvent::Exit / window destroyed).
- Remove `tauri-plugin-shell` and any other now-unused plugins/dependencies from
  `Cargo.toml` and `tauri.conf.json` if nothing else uses them.
- Frontend talks to Python over HTTP even inside the desktop app.

## Web deployment

- The same Next.js app is served as a normal web app.
- `NEXT_PUBLIC_API_URL` points at the hosted FastAPI backend.
- `FOSSEE_CORS_ORIGINS` and `FOSSEE_PROJECTS_DIR` are set in the hosting environment.
- The landing site (`frontend/`) is unchanged.

## Error handling

- All backend routes return JSON errors with appropriate HTTP status codes
  (400 for validation, 404 for missing chart/widget/project, 500 for process/fs failures),
  with a `detail` string mirroring the previous Rust error strings where practical.
- The frontend `FetchTransport` throws on non-2xx responses so existing `try/catch`
  paths in callers keep working.

## Testing

- Backend unit tests (pytest) for: scilab actor start/execute/stop/status,
  filesystem CRUD + project lifecycle (using a temp `FOSSEE_PROJECTS_DIR`),
  charts CRUD, widgets type/instance lifecycle.
- Frontend: typecheck + existing build remain green; manual smoke test of the
  scilab console, file tree, and project creation against the Python backend.
- Rust side: `cargo check` passes for the minimal launcher.

## Out of scope (future)

- Bundling Python as a Tauri sidecar for end-user distribution.
- Scilab socket protocol / JSON-RPC sidecar.
- AuthN/AuthZ on the backend.
- Landing site backend integration.
