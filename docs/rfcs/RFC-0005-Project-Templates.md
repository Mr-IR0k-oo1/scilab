# RFC-0005: Project Templates

| Field | Value |
|-------|-------|
| RFC | 0005 |
| Title | Project Templates |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how project templates are defined, discovered, instantiated, and shared.

## Motivation

Templates reduce setup time for common engineering workflows. A student starting a lab assignment should select a template and begin working immediately, not spend time creating directory structures and boilerplate files.

## Detailed Design

### Template Structure

A template is a directory with a `template.json` manifest:

```
templates/
└── signal-processing-lab/
    ├── template.json
    ├── README.md
    ├── main.sce
    ├── data/
    │   └── sample.csv
    └── gui/
        └── main.gui.json
```

### template.json

```json
{
  "id": "edu.signal-processing-lab",
  "name": "Signal Processing Lab",
  "description": "Template for signal processing coursework",
  "version": "1.0.0",
  "author": "FOSSEE",
  "license": "GPL-3.0",
  "category": "education",
  "tags": ["signal-processing", "lab", "coursework"],
  "scilab_version": ">=7.0",
  "scilab_studio_version": ">=0.1",
  "variables": {
    "course_name": {
      "type": "string",
      "default": "Signal Processing",
      "description": "Name of the course"
    },
    "student_name": {
      "type": "string",
      "default": "",
      "description": "Student name"
    }
  },
  "files": [
    {
      "source": "main.sce",
      "target": "main.sce",
      "template": true
    },
    {
      "source": "data/sample.csv",
      "target": "data/sample.csv",
      "template": false
    }
  ],
  "post_create": [
    {
      "command": "studio.open_file",
      "args": { "path": "main.sce" }
    }
  ]
}
```

### Template Variables

Templates support variable substitution in files marked as `"template": true`:

```scilab
// main.sce
// {{course_name}} - {{student_name}}
// Created: {{date}}

function result = analyze(data)
    // Your code here
endfunction
```

**Built-in variables:**
| Variable | Description |
|----------|-------------|
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{time}}` | Current time (HH:MM) |
| `{{project_name}}` | Name of the new project |
| `{{student_name}}` | Student name (from template config) |

### Template Discovery

Templates are loaded from:

1. **Built-in**: Shipped with Scilab Studio in `resources/templates/`.
2. **User**: `~/.scilab-studio/templates/`.
3. **Project**: Templates defined in the current project.
4. **Marketplace**: Downloaded from the Template Marketplace (v0.2+).

### Template Instantiation

1. User selects a template from the New Project dialog.
2. User fills in template variables (if any).
3. Template files are copied to the new project directory.
4. Variable substitution is applied to template files.
5. `post_create` actions are executed.
6. New project opens in the workspace.

### Template Categories

| Category | Description |
|----------|-------------|
| `education` | Coursework and lab assignments |
| `research` | Research workflows |
| `engineering` | Common engineering tasks |
| `blank` | Empty project with minimal structure |

## Alternatives Considered

1. **Git-based templates**: Clone repos as templates. Adds dependency on git. Can be added later.
2. **No templates**: Users create projects from scratch. Wastes time on boilerplate.

## Security Considerations

- Template files are copied locally. No runtime dependencies.
- `post_create` actions are limited to platform commands (no arbitrary code execution).
- User templates are loaded from trusted directories only.

## Testing Strategy

- Unit tests for template parsing and variable substitution.
- Integration tests for template instantiation.
- UI tests for the New Project dialog.

## Rollout

- v0.1: 5 built-in templates (Signal Processing, Control Systems, Data Analysis, Numerical Methods, Blank).
- v0.2: User templates, Template Marketplace.
- v0.3: Template sharing and community templates.
