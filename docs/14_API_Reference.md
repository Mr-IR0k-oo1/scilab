# API Reference

> Scilab Studio API Reference — versioned, consistent, and designed for extensibility.

---

## Overview

Scilab Studio is built with an API-first design philosophy. Every feature exposed through the GUI is also accessible through a programmatic API. This ensures that:

- **Plugins and modules** can extend the platform without special-casing.
- **Automation and scripting** are first-class citizens.
- **Third-party integrations** can interact with Scilab Studio reliably.
- **Testing** can exercise the same code paths as user interactions.

All APIs are versioned, documented with examples, and covered by automated tests.

---

## API Design Principles

### RESTful conventions
All HTTP-based APIs follow REST conventions: proper HTTP methods, resource-oriented URLs, and standard status codes.

### Consistent response format
Every API returns a standard envelope:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "metadata": {
    "version": "v1",
    "timestamp": "2026-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

### Versioning
All APIs are versioned via URL path prefix (`/v1/`, `/v2/`). Breaking changes require a new major version. Deprecation notices are provided at least one minor version before removal.

### Documentation
Every endpoint includes request/response schemas, example calls, and error codes. Documentation is auto-generated from OpenAPI specs.

---

## Core APIs

### Project API

Manage projects throughout their lifecycle.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/projects` | Create a new project |
| `GET` | `/v1/projects` | List all projects |
| `GET` | `/v1/projects/:id` | Get project details |
| `PUT` | `/v1/projects/:id` | Update project metadata |
| `DELETE` | `/v1/projects/:id` | Delete a project |
| `POST` | `/v1/projects/:id/open` | Open a project |
| `POST` | `/v1/projects/:id/save` | Save a project |
| `POST` | `/v1/projects/:id/export` | Export a project |
| `GET` | `/v1/projects/:id/files` | List project files |
| `GET` | `/v1/projects/:id/settings` | Get project settings |
| `PUT` | `/v1/projects/:id/settings` | Update project settings |

**Example — Create a project:**
```json
POST /v1/projects
{
  "name": "Signal Processing Lab",
  "template": "signal-processing",
  "description": "FIR filter design and analysis",
  "location": "/home/user/projects/signal-lab"
}

Response:
{
  "success": true,
  "data": {
    "id": "proj_abc123",
    "name": "Signal Processing Lab",
    "path": "/home/user/projects/signal-lab",
    "createdAt": "2026-01-15T10:30:00Z",
    "modules": ["core", "data-studio", "visualization"]
  }
}
```

---

### Module API

Register, activate, and manage platform modules.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/modules` | List all modules |
| `GET` | `/v1/modules/:name` | Get module details |
| `POST` | `/v1/modules/:name/activate` | Activate a module |
| `POST` | `/v1/modules/:name/deactivate` | Deactivate a module |
| `GET` | `/v1/modules/:name/config` | Get module configuration |
| `PUT` | `/v1/modules/:name/config` | Update module configuration |
| `POST` | `/v1/modules/:name/message` | Send a message to a module |
| `GET` | `/v1/modules/:name/events` | Subscribe to module events (SSE) |

**Example — Activate a module:**
```json
POST /v1/modules/visualization/activate

Response:
{
  "success": true,
  "data": {
    "name": "visualization",
    "status": "active",
    "version": "1.2.0",
    "loadedAt": "2026-01-15T10:30:01Z"
  }
}
```

---

### Plugin API

Manage plugin lifecycle and extensions.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/plugins` | List installed plugins |
| `POST` | `/v1/plugins` | Install a plugin |
| `DELETE` | `/v1/plugins/:id` | Uninstall a plugin |
| `POST` | `/v1/plugins/:id/enable` | Enable a plugin |
| `POST` | `/v1/plugins/:id/disable` | Disable a plugin |
| `GET` | `/v1/plugins/:id/manifest` | Get plugin manifest |
| `POST` | `/v1/plugins/:id/update` | Update a plugin |

**Plugin Lifecycle Hooks:**
```
onInstall → onActivate → onDeactivate → onUninstall
```

**Example — Install a plugin:**
```json
POST /v1/plugins
{
  "source": "marketplace",
  "packageId": "plugin-thermal-analysis",
  "version": "2.0.0"
}

Response:
{
  "success": true,
  "data": {
    "id": "plug_xyz789",
    "name": "Thermal Analysis",
    "version": "2.0.0",
    "status": "installed",
    "permissions": ["read:project", "write:visualization", "execute:scilab"]
  }
}
```

---

### Visualization API

Create, update, and export charts and visualizations.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/visualizations` | Create a new chart |
| `GET` | `/v1/visualizations` | List all charts in current project |
| `GET` | `/v1/visualizations/:id` | Get chart details |
| `PUT` | `/v1/visualizations/:id` | Update chart configuration |
| `DELETE` | `/v1/visualizations/:id` | Delete a chart |
| `POST` | `/v1/visualizations/:id/export` | Export chart (PNG, SVG, PDF) |
| `POST` | `/v1/visualizations/:id/data` | Update chart data |
| `GET` | `/v1/visualizations/:id/image` | Get chart as image |

**Supported chart types:** `line`, `bar`, `scatter`, `histogram`, `pie`, `surface`, `mesh`, `contour`, `box`, `heatmap`, `bode`, `nyquist`, `root-locus`

**Example — Create a line chart:**
```json
POST /v1/visualizations
{
  "type": "line",
  "title": "Step Response",
  "data": {
    "x": [0, 0.1, 0.2, 0.3, 0.4, 0.5],
    "y": [0, 0.25, 0.63, 0.86, 0.95, 0.98]
  },
  "options": {
    "xLabel": "Time (s)",
    "yLabel": "Amplitude",
    "grid": true,
    "legend": ["System Output"]
  }
}
```

---

### Data API

Import, query, and transform data.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/data/import` | Import data from file |
| `GET` | `/v1/data/datasets` | List all datasets |
| `GET` | `/v1/data/datasets/:id` | Get dataset details |
| `GET` | `/v1/data/datasets/:id/preview` | Preview dataset (first N rows) |
| `GET` | `/v1/data/datasets/:id/schema` | Get dataset schema |
| `POST` | `/v1/data/datasets/:id/transform` | Apply transformation |
| `DELETE` | `/v1/data/datasets/:id` | Delete a dataset |
| `POST` | `/v1/data/query` | Query data with filters |
| `POST` | `/v1/data/merge` | Merge multiple datasets |

**Example — Import CSV:**
```json
POST /v1/data/import
Content-Type: multipart/form-data

file: experiment_results.csv
options: {
  "delimiter": ",",
  "hasHeader": true,
  "inferTypes": true
}

Response:
{
  "success": true,
  "data": {
    "id": "ds_def456",
    "name": "experiment_results",
    "rows": 1000,
    "columns": 12,
    "schema": [
      { "name": "timestamp", "type": "datetime" },
      { "name": "temperature", "type": "float" },
      { "name": "pressure", "type": "float" }
    ]
  }
}
```

---

### Engine API

Execute Scilab code and manage computation sessions.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/engine/execute` | Execute Scilab code |
| `POST` | `/v1/engine/execute/batch` | Execute multiple code blocks |
| `GET` | `/v1/engine/sessions` | List active sessions |
| `POST` | `/v1/engine/sessions` | Create a new session |
| `DELETE` | `/v1/engine/sessions/:id` | Terminate a session |
| `GET` | `/v1/engine/sessions/:id/variables` | List session variables |
| `POST` | `/v1/engine/sessions/:id/variables` | Set a session variable |
| `GET` | `/v1/engine/status` | Get engine status |
| `POST` | `/v1/engine/reset` | Reset engine state |

**Example — Execute Scilab code:**
```json
POST /v1/engine/execute
{
  "code": "s = tf('s'); G = 1/(s^2 + 2*s + 1); step(G)",
  "sessionId": "sess_abc123",
  "captureOutput": true
}

Response:
{
  "success": true,
  "data": {
    "output": "",
    "figures": ["fig_001"],
    "variables": {
      "G": { "type": "transfer_function", "dimensions": [1, 1] }
    },
    "executionTime": 0.23
  }
}
```

---

### Report API

Generate and export reports.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/reports` | Create a new report |
| `GET` | `/v1/reports` | List reports |
| `GET` | `/v1/reports/:id` | Get report details |
| `PUT` | `/v1/reports/:id` | Update report content |
| `DELETE` | `/v1/reports/:id` | Delete a report |
| `POST` | `/v1/reports/:id/generate` | Generate report |
| `GET` | `/v1/reports/:id/download` | Download generated report |
| `GET` | `/v1/reports/templates` | List report templates |

**Example — Generate a PDF report:**
```json
POST /v1/reports/rpt_abc123/generate
{
  "format": "pdf",
  "sections": [
    { "type": "title", "text": "Lab Report: Filter Design" },
    { "type": "code", "source": "main.sce" },
    { "type": "figure", "ref": "fig_001" },
    { "type": "table", "datasetId": "ds_def456" },
    { "type": "text", "content": "The filter meets the specification." }
  ]
}

Response:
{
  "success": true,
  "data": {
    "reportId": "rpt_abc123",
    "status": "generated",
    "downloadUrl": "/v1/reports/rpt_abc123/download",
    "size": 245760
  }
}
```

---

### Marketplace API

Publish, download, and rate packages.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/marketplace/packages` | Search packages |
| `GET` | `/v1/marketplace/packages/:id` | Get package details |
| `POST` | `/v1/marketplace/packages/:id/install` | Install a package |
| `DELETE` | `/v1/marketplace/packages/:id/uninstall` | Uninstall a package |
| `POST` | `/v1/marketplace/packages/:id/rate` | Rate a package |
| `POST` | `/v1/marketplace/packages/:id/review` | Write a review |
| `POST` | `/v1/marketplace/publish` | Publish a package |
| `GET` | `/v1/marketplace/categories` | List categories |
| `GET` | `/v1/marketplace/featured` | Get featured packages |

---

## Authentication and Authorization

### API Keys
API keys are used for programmatic access. Keys can be generated from the Settings > API panel.

```bash
curl -H "Authorization: Bearer scilab_sk_xxxxx" /v1/projects
```

### OAuth 2.0
Marketplace operations use OAuth 2.0 for user authentication.

### Permissions
Each API endpoint requires specific permissions:

| Permission | Scope |
|------------|-------|
| `read:project` | Read project files and metadata |
| `write:project` | Create and modify projects |
| `execute:scilab` | Execute Scilab code |
| `read:marketplace` | Browse the marketplace |
| `write:marketplace` | Publish packages |
| `admin` | Administrative operations |

---

## Rate Limiting

| Tier | Requests per Minute | Requests per Hour |
|------|--------------------:|-------------------:|
| Free | 60 | 1,000 |
| Pro | 300 | 10,000 |
| Enterprise | Custom | Custom |

Rate limit headers are included in every response:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642262400
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The 'name' field is required.",
    "details": [
      { "field": "name", "issue": "required" }
    ]
  },
  "metadata": {
    "requestId": "req_abc123"
  }
}
```

**Standard Error Codes:**
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `NOT_FOUND` | 404 | Resource does not exist |
| `VALIDATION_ERROR` | 400 | Invalid request parameters |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMITED` | 429 | Too many requests |
| `ENGINE_ERROR` | 500 | Scilab engine error |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Versioning Strategy

- **Major version** (`/v1/`, `/v2/`): Breaking changes (removed endpoints, changed schemas).
- **Minor version** (header): New features, backward-compatible.
- **Patch version** (header): Bug fixes, backward-compatible.

Deprecation notices are provided via:
- `Deprecation` response header.
- `Sunset` header with the date the endpoint will be removed.
- Changelog entries.

---

## SDK and Client Libraries

Official client libraries are available for:

| Language | Package | Status |
|----------|---------|--------|
| TypeScript/JavaScript | `@scilab-studio/sdk` | Available |
| Python | `scilab-studio-sdk` | Planned |
| MATLAB | `scilab_studio_sdk` | Planned |
| Julia | `ScilabStudio.jl` | Community |

---

## Example API Calls

### Complete workflow — Create project, import data, visualize:

```bash
# 1. Create a project
curl -X POST http://localhost:3000/v1/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Analysis", "template": "control-systems"}'

# 2. Import data
curl -X POST http://localhost:3000/v1/data/import \
  -F "file=@sensor_data.csv"

# 3. Execute Scilab analysis
curl -X POST http://localhost:3000/v1/engine/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "load(data); bode(data)"}'

# 4. Generate a report
curl -X POST http://localhost:3000/v1/reports \
  -H "Content-Type: application/json" \
  -d '{"name": "Analysis Report", "format": "pdf"}'
```
