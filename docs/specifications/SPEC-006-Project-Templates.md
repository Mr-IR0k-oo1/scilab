# SPEC-006 — Project Templates

## Purpose

Provide pre-configured project structures for common engineering workflows, so users start with a working project instead of an empty directory.

---

## Template Types

### Built-in Templates

| Template | Description | Modules |
|----------|-------------|---------|
| blank | Empty project with standard directory structure | workspace |
| signal-processing | FFT, filtering, spectral analysis | workspace, visualization |
| control-systems | Transfer functions, Bode plots, root locus | workspace, visualization |
| data-analysis | CSV import, statistics, transforms | workspace, data |
| gui-design | GUI Builder with example components | workspace, gui-builder |
| lab-report | Report template with standard sections | workspace, report |
| parameter-sweep | Multi-run analysis with comparison charts | workspace, visualization, data |
| optimization | Curve fitting, linear programming | workspace, visualization |
| simulation | ODE solving with time-series plots | workspace, visualization |
| education | Student-friendly with guided examples | workspace, learning |

### User Templates

Users can save any project as a template:
1. File → Save As Template.
2. Provide name, description, category.
3. Template saved to `~/.scilab-studio/templates/`.

### Marketplace Templates

Additional templates available from the marketplace, organized by discipline and difficulty.

---

## Template Structure

```
template/
├── template.json          # Template manifest
├── project.json           # Pre-configured project manifest
├── scripts/
│   └── main.sce           # Starter script
├── data/
│   └── sample.csv         # Example data
├── guis/
│   └── main_gui.json      # Pre-built GUI layout
├── visualizations/
│   └── overview.json      # Pre-configured charts
├── reports/
│   └── templates/
│       └── report.json    # Report template
└── README.md              # Template documentation
```

---

## Template Manifest

```jsonc
{
  "id": "signal-processing",
  "name": "Signal Processing",
  "description": "FFT, filtering, and spectral analysis workflows",
  "category": "engineering",
  "difficulty": "intermediate",
  "author": "Scilab Studio Team",
  "version": "1.0.0",
  "thumbnail": "thumbnail.png",
  "modules": ["visualization-engine"],
  "tags": ["signal", "fft", "filter", "spectrum"],
  "files": {
    "scripts/main.sce": "Main analysis script",
    "data/sample.wav": "Example audio signal",
    "visualizations/spectrum.json": "Pre-configured spectrum chart"
  }
}
```

---

## Template Lifecycle

```
Browse (Learning Center or Marketplace)
  │
  ▼
Select Template
  │
  ▼
Configure (name, location, Scilab version)
  │
  ▼
Create Project (copy template files, generate project.json)
  │
  ▼
Open Project
```

---

## Behavior

### Creating from Template
1. User selects a template from the Learning Center or File → New from Template.
2. Dialog asks for project name and location.
3. Platform copies template files to the new project directory.
4. Platform generates `project.json` with the template's module list and settings.
5. Platform opens the new project.

### Saving as Template
1. User opens an existing project.
2. File → Save As Template.
3. Dialog asks for template name, description, category.
4. Platform creates a template archive from the current project.
5. Template is saved to `~/.scilab-studio/templates/`.
6. Template appears in the Learning Center under "My Templates".

### Updating Templates
- Built-in templates are updated with platform releases.
- User templates are not auto-updated.
- Marketplace templates can be updated via the Plugin Manager.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max template size | 10MB |
| Max files per template | 100 |
| Template name length | 1–64 chars |
| Custom templates location | ~/.scilab-studio/templates/ |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Template files corrupt | Show error, offer to re-download |
| Template requires missing module | Show warning, install module or skip |
| Disk full during creation | Show error, clean up partial project |
| Template version mismatch | Use anyway, show compatibility warning |

---

## Extension Points

- Custom template categories.
- Template composition (combine multiple templates).
- Template versioning and migration.
- Template sharing via marketplace.
