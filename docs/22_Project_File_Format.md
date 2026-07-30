# 22 — Project File Format

Every Scilab Studio project is a directory with a `project.json` manifest. The official project archive extension is `.scstudio`. This gives the platform its own identity and makes projects portable across machines.

For the Scilab compatibility layer that handles version differences, see [31 — Scilab Compatibility Layer](31_Scilab_Compatibility_Layer.md).

---

## 1. Project Identity

A Scilab Studio project is identified by the presence of `project.json` at its root. The directory name is the project name (case-preserved, no sanitization applied). Projects are portable: copy the directory to another machine and it works.

---

## 2. Directory Structure

```
project-root/
├── project.json                    # Project manifest (required)
├── .scstudio/                      # Platform metadata (hidden)
│   ├── lock                        # Crash recovery lock file
│   ├── emergency/                  # Emergency snapshots
│   │   └── snapshot-<id>.json
│   ├── cache/                      # Temporary cache
│   │   └── thumbnails/
│   └── plugins/                    # Project-local plugin overrides
│       └── <plugin-id>/
│           └── settings.json
├── layouts/                        # Panel layout snapshots
│   ├── default.json
│   ├── coding.json
│   └── analysis.json
├── scripts/                        # Scilab code
│   ├── main.sce
│   ├── functions/
│   │   └── helpers.sci
│   └── utilities/
│       └── processing.sce
├── data/                           # Datasets
│   ├── measurements.csv
│   ├── measurements.csv.meta.json  # Auto-generated metadata
│   └── results/
│       └── output.csv
├── assets/                         # Static resources
│   ├── logo.svg
│   └── screenshots/
├── guis/                           # GUI Builder layouts
│   ├── main_gui.json
│   └── settings_dialog.json
├── visualizations/                 # Saved chart configurations
│   ├── frequency_response.json
│   └── time_series.json
├── reports/                        # Generated reports
│   ├── analysis_v1.pdf
│   ├── summary.html
│   └── templates/
│       └── weekly_report.json
└── plugins/                        # Project-local plugin data
    └── <plugin-id>/
        └── data/
```

### Required Paths

| Path | Created By | Description |
|------|-----------|-------------|
| `project.json` | Platform | Project manifest |
| `.scstudio/` | Platform | Hidden metadata directory |
| `scripts/` | Platform | Default scripts directory |
| `data/` | Platform | Default data directory |
| `layouts/` | Platform | Layout snapshots |

### Optional Paths

| Path | Created By | Description |
|------|-----------|-------------|
| `assets/` | User | Static resources |
| `guis/` | GUI Builder | GUI layout files |
| `visualizations/` | Visualization Studio | Saved chart configs |
| `reports/` | Report Generator | Generated reports |
| `plugins/` | Plugin Manager | Plugin-specific data |

---

## 3. Project Manifest

### 3.1 Schema

```jsonc
{
  "$schema": "https://scilab-studio.dev/schemas/project-v1.json",
  "version": "1.0.0",
  "name": "My Engineering Project",
  "description": "Vibration analysis of rotating machinery",
  "created": "2026-07-27T10:00:00.000Z",
  "modified": "2026-07-27T14:30:00.000Z",
  "author": {
    "name": "Jane Engineer",
    "email": "jane@example.com"
  },
  "scilab_version": "2024.1.0",
  "modules": ["data-import", "visualization-engine", "report-generator"],
  "plugins": [
    {
      "id": "com.example.vibration-analyzer",
      "version": "1.2.0",
      "enabled": true,
      "settings": { "samplingRate": 1000 }
    }
  ],
  "settings": {
    "editor": { "fontSize": 14, "tabSize": 2 },
    "engine": { "timeout": 60000 },
    "visualization": { "renderer": "webgl" }
  },
  "workspace": {
    "layout": "default",
    "panels": {
      "left":   { "visible": true, "width": 250, "activePanel": "file-explorer" },
      "right":  { "visible": true, "width": 300, "activePanel": "inspector" },
      "bottom": { "visible": false, "height": 200, "activePanel": "console" }
    },
    "openTabs": ["scripts/main.sce", "data/measurements.csv"],
    "activeTab": "scripts/main.sce"
  }
}
```

### 3.2 Field Specifications

| Field | Type | Required | Constraint |
|-------|------|----------|------------|
| `$schema` | string | yes | Must be `"https://scilab-studio.dev/schemas/project-v1.json"` |
| `version` | string | yes | Must be `"1.0.0"` |
| `name` | string | yes | 1–128 chars, no `/`, `\`, or null bytes |
| `description` | string | no | 0–1024 chars |
| `created` | string (ISO 8601) | yes | Immutable after creation |
| `modified` | string (ISO 8601) | yes | Must be ≥ `created` |
| `author` | object | no | `{ name?: string, email?: string }` |
| `scilab_version` | string | yes | Semver (e.g., `"2024.1.0"`) |
| `modules` | string[] | yes | Unique, sorted alphabetically |
| `plugins` | object[] | no | Each must have unique `id` |
| `plugins[].id` | string | yes | Reverse-domain (e.g., `"com.example.name"`) |
| `plugins[].version` | string | yes | Semver |
| `plugins[].enabled` | boolean | no | Default `true` |
| `plugins[].settings` | object | no | Arbitrary key-value pairs |
| `settings` | object | no | Project-level overrides (merged with user settings) |
| `workspace` | object | no | Persisted layout state |

### 3.3 Validation Rules

1. `version` must match `^1\.0\.0$`.
2. `created` must be ≤ `modified`.
3. `modules` must not contain duplicates.
4. Each `plugins[].id` must be unique.
5. `workspace.layout` must reference an existing file in `layouts/`.
6. On load, invalid projects cannot be opened until corrected.

---

## 4. Layout Files

Layout snapshots are stored in `layouts/` as JSON files.

```jsonc
{
  "name": "default",
  "description": "Default workspace layout",
  "created": "2026-07-27T10:00:00.000Z",
  "panels": {
    "left":   { "visible": true, "width": 250, "activePanel": "file-explorer" },
    "right":  { "visible": true, "width": 300, "activePanel": "inspector" },
    "bottom": { "visible": false, "height": 200, "activePanel": "console" }
  },
  "editor": {
    "splitDirection": "none",
    "splitRatio": 0.5
  }
}
```

### Built-in Layouts

| Name | Description |
|------|-------------|
| `default` | Left sidebar + editor + right sidebar, bottom hidden |
| `coding` | Left collapsed, editor full width, bottom (console) visible |
| `design` | Left (palette), editor (canvas), right (properties) |
| `analysis` | Left (explorer), editor (data/charts), bottom (variables) |

---

## 5. Data File Metadata

When a data file is imported, a sidecar `.meta.json` is created:

```
data/
├── measurements.csv
└── measurements.csv.meta.json
```

```jsonc
{
  "source": "measurements.csv",
  "imported": "2026-07-27T10:00:00.000Z",
  "format": "csv",
  "encoding": "utf-8",
  "delimiter": ",",
  "rows": 1500,
  "columns": 8,
  "columnTypes": ["string", "double", "double", "double", "string", "double", "double", "boolean"],
  "columnNames": ["timestamp", "temperature", "pressure", "voltage", "status", "frequency", "amplitude", "valid"],
  "hash": "sha256:abc123..."
}
```

---

## 6. File Naming Conventions

| File Type | Extension | Location |
|-----------|-----------|----------|
| Scilab execute | `.sce` | `scripts/` |
| Scilab functions | `.sci` | `scripts/functions/` |
| Scilab data | `.sod` | `data/` |
| GUI layouts | `.json` | `guis/` |
| Chart configs | `.json` | `visualizations/` |
| Report templates | `.json` | `reports/templates/` |
| Generated reports | `<name>_v<N>.<format>` | `reports/` |

---

## 7. Project Archive (`.scstudio`)

Projects can be exported as `.scstudio` archive files for sharing.

### 7.1 Archive Structure

A `.scstudio` file is a ZIP archive containing the project directory, excluding:
- `.scstudio/cache/`
- `.scstudio/emergency/`
- `.scstudio/lock`
- `node_modules/`
- `.git/`
- OS-specific files (`.DS_Store`, `Thumbs.db`)

### 7.2 Archive Manifest

The archive includes a `MANIFEST.json` at its root:

```jsonc
{
  "format": "scstudio",
  "version": "1.0.0",
  "created": "2026-07-27T10:00:00.000Z",
  "project": "My Engineering Project",
  "scilab_version": "2024.1.0",
  "files": [
    { "path": "project.json", "hash": "sha256:...", "size": 1234 },
    { "path": "scripts/main.sce", "hash": "sha256:...", "size": 5678 }
  ]
}
```

### 7.3 Import

To import a `.scstudio` archive:
1. Extract to the target directory.
2. Validate `project.json` and `MANIFEST.json`.
3. Verify file hashes.
4. Register in recent projects.
5. Open the project.

---

## 8. Settings Resolution

Settings are resolved in priority order (highest wins):

```
1. Project settings     (project.json → settings)
2. User settings        (~/.config/scilab-studio/settings.json)
3. Platform defaults    (compiled into binary)
```

Project settings are shallow-merged with user settings. A project setting overrides the user setting for the same key.

---

## 9. Migration and Versioning

### Schema Versioning

The `project.json` schema uses semantic versioning. Current version: `1.0.0`.

- **Patch (1.0.x):** Backward-compatible (new optional fields).
- **Minor (1.x.0):** Additive (new optional sections).
- **Major (x.0.0):** Breaking (field removals, type changes).

### Migration Strategy

When a project is opened with a newer version:
1. Read the `version` field.
2. If older, run migration (add missing fields, rename if needed).
3. Save migrated project (original backed up to `.scstudio/backup/`).
4. Notify user.

### Backward Compatibility

Scilab Studio v1.x always opens v1.0.0 projects. A future v2.0 schema will trigger a read-only warning in v1.x.
