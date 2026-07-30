# Template Development

Create project templates for common engineering workflows.

## Template Structure

```
my-template/
├── template.json      # Manifest (required)
├── README.md          # Documentation
├── main.sce           # Scilab script
├── data/
│   └── sample.csv     # Sample data
└── gui/
    └── main.gui.json  # GUI definition
```

## Manifest (template.json)

```json
{
  "id": "edu.control-systems",
  "name": "Control Systems Lab",
  "description": "Template for control systems coursework",
  "version": "1.0.0",
  "author": "FOSSEE",
  "license": "GPL-3.0",
  "category": "education",
  "tags": ["control-systems", "lab", "coursework"],
  "scilab_version": ">=7.0",
  "scilab_studio_version": ">=0.1",
  "icon": "template-control",
  "variables": {
    "course_name": {
      "type": "string",
      "default": "Control Systems",
      "description": "Name of the course"
    },
    "student_name": {
      "type": "string",
      "default": "",
      "description": "Student name"
    },
    "experiment_number": {
      "type": "number",
      "default": 1,
      "description": "Experiment number"
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
    },
    {
      "source": "gui/main.gui.json",
      "target": "gui/main.gui.json",
      "template": true
    }
  ],
  "post_create": [
    {
      "command": "studio.open_file",
      "args": { "path": "main.sce" }
    },
    {
      "command": "studio.execute_scilab",
      "args": { "code": "clear; clc;" }
    }
  ]
}
```

## Variables

### Built-in Variables

| Variable | Description |
|----------|-------------|
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{time}}` | Current time (HH:MM) |
| `{{project_name}}` | Name of the new project |
| `{{year}}` | Current year |

### Custom Variables

Define custom variables in `variables`:

```json
{
  "variables": {
    "frequency": {
      "type": "number",
      "default": 60,
      "description": "Signal frequency (Hz)"
    }
  }
}
```

### Variable Types

| Type | UI Control | Validation |
|------|-----------|-----------|
| `string` | Text input | Non-empty |
| `number` | Number input | Min/max |
| `boolean` | Checkbox | — |
| `enum` | Dropdown | Options list |

## Template Files

Files marked as `"template": true` support variable substitution:

```scilab
// main.sce
// {{course_name}} - Experiment {{experiment_number}}
// Student: {{student_name}}
// Date: {{date}}

function result = analyze(data)
    // Your code here
endfunction
```

### Substitution Rules

- Variables are replaced at creation time.
- Unresolved variables are left as-is.
- Variables can appear in file contents and file names.

## Post-Creation Actions

After files are copied, `post_create` actions run:

```json
{
  "post_create": [
    {
      "command": "studio.open_file",
      "args": { "path": "main.sce" }
    },
    {
      "command": "studio.execute_scilab",
      "args": { "code": "disp('Welcome!')" }
    }
  ]
}
```

### Available Commands

| Command | Description |
|---------|-------------|
| `studio.open_file` | Open a file in the editor |
| `studio.execute_scilab` | Run Scilab code |
| `studio.show_message` | Show a notification |
| `studio.open_panel` | Open a specific panel |

## Template Categories

| Category | Description |
|----------|-------------|
| `education` | Coursework and lab assignments |
| `research` | Research workflows |
| `engineering` | Common engineering tasks |
| `blank` | Empty project with minimal structure |

## Publishing

### Local Templates

Place templates in `~/.scilab-studio/templates/`:

```
~/.scilab-studio/templates/
└── my-custom-template/
    ├── template.json
    └── ...
```

### Template Registry

Publish to the Template Registry:

```bash
scilab-studio publish-template ./my-template
```

### Template Marketplace (v0.2+)

Community templates are available in the Template Marketplace.

## Testing

```bash
# Preview template
scilab-studio preview-template ./my-template

# Test variable substitution
scilab-studio test-template ./my-template --var frequency=60

# Validate manifest
scilab-studio validate-template ./my-template
```

## Best Practices

- Provide sensible defaults for all variables.
- Include sample data and documentation.
- Test with different variable values.
- Keep templates focused on one use case.
- Document prerequisites (Scilab packages, etc.).
- Use meaningful file names.
- Include a README explaining the template.
