# Engineering Workspace and Project System Specification

**Document Status:** Production Normative Specification  
**Phase:** 3 — Engineering Workspace and Project System  

---

## 1. System Architecture

The Project System transforms raw file storage into a structured, reproducible engineering project environment.

```
React Frontend (Presentation / Store)
      │
      ▼ REST API (/api/v1/projects/{project_id}/...)
FastAPI Routes (app/api/routes/projects.py)
      │
      ├───────────────────────┬────────────────────────┬───────────────────────┐
      ▼                       ▼                        ▼                       ▼
 Project Manifest       File Security           Dataset Manager         Scilab Runtime
  (project.json)      (Path Traversal Guard)   (CSV/JSON Metadata)      (Phase 2 Service)
      │                       │                        │                       │
      └───────────────────────┴───────────┬────────────┴───────────────────────┘
                                          ▼
                              SQLAlchemy 2.0 Database
                       (Project, Experiment, ExecutionRecord, Dataset)
```

---

## 2. Directory Structure & Manifest (`project.json`)

Standard project directory layout:

```text
MyProject/
├── project.json
├── scripts/
│   └── main.sce
├── datasets/
├── assets/
├── experiments/
├── outputs/
└── reports/
```

### Manifest Schema (`project.json`)
```json
{
  "schema_version": 1,
  "id": "c1f7a29e-4b92-491b-8254-0b1a03975549",
  "name": "Solar Analysis",
  "description": "Solar panel efficiency computations",
  "version": "0.1.0",
  "created_at": "2026-08-10T14:15:00+00:00",
  "updated_at": "2026-08-10T14:15:00+00:00"
}
```

- **Portability:** Contains zero absolute machine-specific file paths. All internal script and dataset references are recorded relative to the project root.

---

## 3. Experiment & Execution History Model

### 3.1 Experiment Model
Represents a reproducible engineering computation.
- **Fields:** `id`, `project_id`, `name`, `description`, `script_path`, `status`, `last_execution_id`, `created_at`, `updated_at`.

### 3.2 Execution Record
Maintains execution history:
- **Fields:** `id`, `project_id`, `experiment_id`, `script_path`, `execution_id`, `status`, `started_at`, `finished_at`, `duration_ms`, `exit_code`, `stdout`, `stderr`.

---

## 4. File Operations & Path Traversal Security

- **Allowed Extensions:** Scripts restricted to `.sce` and `.sci`. Datasets restricted to `.csv`, `.json`, `.txt`.
- **Security Protections:**
  - Rejects `..` path traversal sequences.
  - Rejects target paths escaping project root boundary.
  - Validates real paths against symlink escapes.
- All returned paths are normalized relative to project root.

---

## 5. API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/projects/{id}/tree` | GET | Returns recursive project directory tree |
| `/api/v1/projects/{id}/files` | POST | Creates file or folder |
| `/api/v1/projects/{id}/files/{path}` | GET | Reads project file content |
| `/api/v1/projects/{id}/files/{path}` | PUT | Updates file content |
| `/api/v1/projects/{id}/files/{path}` | DELETE | Deletes file or folder |
| `/api/v1/projects/{id}/datasets` | POST | Uploads dataset file |
| `/api/v1/projects/{id}/datasets` | GET | Lists datasets metadata |
| `/api/v1/projects/{id}/datasets/{dataset_id}` | DELETE | Deletes dataset record |
| `/api/v1/projects/{id}/experiments` | POST | Creates new experiment |
| `/api/v1/projects/{id}/experiments` | GET | Lists project experiments |
| `/api/v1/projects/{id}/experiments/{exp_id}` | GET | Gets experiment details |
| `/api/v1/projects/{id}/experiments/{exp_id}/run` | POST | Runs experiment via Scilab Runtime |
| `/api/v1/projects/{id}/executions` | GET | Lists project execution history |
| `/api/v1/projects/{id}/executions/{exec_id}` | GET | Gets specific execution record |
