# Scilab Studio Template Authoring Guide

**Schema Version:** 1  

---

## 1. Directory Structure

Create a directory under `templates/engineering/<category>/<template_id>/`:

```text
templates/engineering/control_systems/control.pid_basic/
├── template.json
├── scripts/
│   └── main.sce
├── datasets/
├── layouts/
└── docs/
    └── README.md
```

## 2. `template.json` Manifest Example
```json
{
  "schema_version": 1,
  "id": "control.pid_basic",
  "name": "PID Control System Demonstration",
  "version": "1.0.0",
  "category": "control_systems",
  "description": "Simulates closed-loop step response.",
  "difficulty": "intermediate",
  "scilab_version": ">=6.0.0",
  "entry_experiment": "scripts/main.sce",
  "parameters": [
    {
      "name": "kp",
      "label": "Proportional Gain",
      "type": "number",
      "default": 1.0,
      "minimum": 0.0,
      "maximum": 50.0,
      "step": 0.1
    }
  ]
}
```
