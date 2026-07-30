# File Format Specification

> Detailed specifications for all file formats used by Scilab Studio.

---

## Overview

Scilab Studio uses a set of structured file formats to define projects, plugins, templates, widgets, digital twins, reports, and configuration. All formats use JSON or YAML as the base serialization format, chosen for readability, tooling support, and cross-language compatibility.

---

## Project File Format (.scilab-studio project)

A Scilab Studio project is defined by a `.scilab-studio` directory containing a `project.json` manifest and project content.

### Directory Structure
```
my-project.scilab-studio/
  project.json          # Project manifest
  main.sce              # Entry point Scilab script
  src/                  # Source code
  data/                 # Datasets
  results/              # Output figures, reports
  gui/                  # GUI definitions
  tests/                # Project-specific tests
  .project-config.json  # User-specific overrides (gitignored)
```

### project.json Schema
```json
{
  "formatVersion": "1.0.0",
  "name": "Signal Processing Lab",
  "description": "FIR filter design and analysis",
  "version": "1.0.0",
  "author": "Jane Engineer",
  "license": "GPL-3.0",
  "createdAt": "2026-01-15T10:30:00Z",
  "updatedAt": "2026-01-20T14:22:00Z",
  "entryPoint": "main.sce",
  "modules": [
    { "name": "data-studio", "version": "^1.0.0" },
    { "name": "visualization", "version": "^1.0.0" }
  ],
  "dependencies": [
    { "name": "signal-processing-toolbox", "version": "^2.1.0", "source": "marketplace" }
  ],
  "settings": {
    "scilabVersion": "2024.0",
    "autoSave": true,
    "autoSaveInterval": 300,
    "defaultExportFormat": "pdf"
  },
  "tags": ["signal-processing", "filters", "education"],
  "template": "signal-processing"
}
```

---

## Plugin Manifest Format

Every plugin must include a `plugin.json` manifest file.

### plugin.json Schema
```json
{
  "manifestVersion": "1.0.0",
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "A brief description of what this plugin does.",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://example.com"
  },
  "license": "GPL-3.0",
  "homepage": "https://github.com/example/my-plugin",
  "repository": "https://github.com/example/my-plugin",
  "engines": {
    "scilab-studio": ">=0.1.0"
  },
  "entryPoint": "dist/index.js",
  "icon": "assets/icon.png",
  "categories": ["visualization", "analysis"],
  "tags": ["charts", "plotting"],
  "permissions": [
    "read:project",
    "write:visualization",
    "execute:scilab"
  ],
  "dependencies": {},
  "contributes": {
    "commands": [
      {
        "id": "my-plugin.generateChart",
        "title": "Generate Custom Chart",
        "category": "My Plugin"
      }
    ],
    "views": [
      {
        "id": "my-plugin.panel",
        "title": "My Panel",
        "type": "sidebar",
        "entryPoint": "dist/panel.js"
      }
    ],
    "menuItems": [
      {
        "label": "My Plugin",
        "menu": "tools",
        "command": "my-plugin.generateChart"
      }
    ]
  }
}
```

---

## Template Format

Templates define reusable project scaffolds.

### Directory Structure
```
my-template/
  template.json         # Template manifest
  README.md             # Template documentation
  preview.png           # Preview image (800x600 minimum)
  files/                # Template files (copied into new project)
    main.sce
    data/
    ...
```

### template.json Schema
```json
{
  "formatVersion": "1.0.0",
  "id": "signal-processing",
  "name": "Signal Processing",
  "description": "Template for signal processing projects including filter design and spectral analysis.",
  "version": "1.0.0",
  "author": "Scilab Studio Team",
  "license": "GPL-3.0",
  "category": "engineering",
  "domain": "Signal Processing",
  "difficulty": "intermediate",
  "tags": ["signals", "filters", "FFT", "DSP"],
  "modules": ["data-studio", "visualization"],
  "files": {
    "entryPoint": "main.sce",
    "copy": ["**/*"],
    "exclude": ["preview.png", "README.md"]
  },
  "variables": [
    {
      "name": "projectName",
      "type": "string",
      "prompt": "Enter the project name:",
      "default": "My Signal Processing Project"
    }
  ],
  "preview": "preview.png"
}
```

---

## Widget Definition Format

Widgets are reusable UI components for the GUI builder and marketplace.

### Directory Structure
```
my-widget/
  widget.json           # Widget manifest
  index.js              # Widget implementation
  styles.css            # Default styles
  README.md             # Documentation
  examples/             # Usage examples
```

### widget.json Schema
```json
{
  "formatVersion": "1.0.0",
  "id": "com.example.gauge-widget",
  "name": "Gauge Widget",
  "version": "1.0.0",
  "description": "A circular gauge widget for displaying numeric values.",
  "author": "Author Name",
  "license": "GPL-3.0",
  "category": "indicators",
  "tags": ["gauge", "indicator", "仪表"],
  "thumbnail": "thumbnail.png",
  "entryPoint": "index.js",
  "widgetType": "display",
  "properties": [
    {
      "name": "value",
      "type": "number",
      "default": 0,
      "min": 0,
      "max": 100,
      "description": "Current gauge value"
    },
    {
      "name": "min",
      "type": "number",
      "default": 0,
      "description": "Minimum scale value"
    },
    {
      "name": "max",
      "type": "number",
      "default": 100,
      "description": "Maximum scale value"
    },
    {
      "name": "unit",
      "type": "string",
      "default": "%",
      "description": "Unit label"
    },
    {
      "name": "color",
      "type": "color",
      "default": "#4CAF50",
      "description": "Gauge color"
    }
  ],
  "events": [
    {
      "name": "valueChanged",
      "description": "Fired when the gauge value changes"
    }
  ],
  "methods": [
    {
      "name": "setValue",
      "parameters": [{ "name": "value", "type": "number" }],
      "description": "Set the gauge value"
    }
  ],
  "dependencies": [],
  "compatibility": {
    "scilab-studio": ">=0.1.0",
    "platforms": ["linux", "macos", "windows", "web"]
  }
}
```

---

## Digital Twin Definition Format

Digital twins are defined using YAML for human readability.

### twin.yaml Schema
```yaml
formatVersion: "1.0.0"
id: "dt-wind-turbine-001"
name: "Wind Turbine Digital Twin"
description: "Real-time digital twin of a 2MW wind turbine"
version: "1.0.0"
author: "Research Lab"
license: "GPL-3.0"

# Physical system reference
physicalSystem:
  type: "wind-turbine"
  manufacturer: "Example Corp"
  model: "WT-2000"
  ratedPower: 2000  # kW
  location:
    latitude: 42.3601
    longitude: -71.0589

# Simulation model
simulation:
  engine: "scilab"
  modelFile: "turbine_model.sce"
  parameters:
    rotorDiameter: 80  # meters
    hubHeight: 80      # meters
    cutInSpeed: 3      # m/s
    ratedSpeed: 12     # m/s
    cutOutSpeed: 25    # m/s

# Data connectors
connectors:
  - id: "scada-feed"
    type: "mqtt"
    broker: "mqtt.example.com"
    topic: "turbine/+/data"
    interval: 1000  # ms
  - id: "weather-api"
    type: "rest"
    url: "https://api.weather.example.com/v1/current"
    interval: 60000

# Monitoring dashboards
dashboards:
  - name: "Overview"
    widgets:
      - type: "gauge"
        property: "powerOutput"
        label: "Power Output (kW)"
      - type: "chart"
        property: "windSpeed"
        chartType: "line"
        timeRange: "1h"

# Alerts
alerts:
  - name: "High Vibration"
    condition: "vibration > 5.0"
    severity: "warning"
    notify: ["email", "dashboard"]
  - name: "Temperature Critical"
    condition: "gearboxTemp > 85"
    severity: "critical"
    notify: ["email", "dashboard", "sms"]

# Versioning
metadata:
  createdAt: "2026-01-15T10:30:00Z"
  updatedAt: "2026-06-20T14:00:00Z"
  tags: ["wind-energy", "renewable", "monitoring"]
```

---

## Report Template Format

Report templates define the structure and layout of generated reports.

### report-template.json Schema
```json
{
  "formatVersion": "1.0.0",
  "id": "lab-report-standard",
  "name": "Standard Lab Report",
  "description": "A standard laboratory report template for engineering courses.",
  "version": "1.0.0",
  "pageSettings": {
    "size": "A4",
    "orientation": "portrait",
    "margins": { "top": "2cm", "bottom": "2cm", "left": "2.5cm", "right": "2.5cm" }
  },
  "sections": [
    {
      "id": "title",
      "type": "title",
      "title": "Project Title",
      "subtitle": "Subtitle or course name",
      "author": "{{project.author}}",
      "date": "{{currentDate}}"
    },
    {
      "id": "objective",
      "type": "text",
      "title": "Objective",
      "placeholder": "State the objective of this experiment..."
    },
    {
      "id": "theory",
      "type": "richtext",
      "title": "Theory",
      "placeholder": "Describe the theoretical background..."
    },
    {
      "id": "code",
      "type": "code",
      "title": "Implementation",
      "sourceFile": "main.sce",
      "syntaxHighlight": "scilab"
    },
    {
      "id": "results",
      "type": "figures",
      "title": "Results",
      "figureSource": "results/",
      "layout": "grid",
      "columns": 2
    },
    {
      "id": "data-table",
      "type": "table",
      "title": "Data Summary",
      "datasetId": "latest",
      "maxRows": 20
    },
    {
      "id": "conclusion",
      "type": "text",
      "title": "Conclusion",
      "placeholder": "Summarize findings and conclusions..."
    }
  ],
  "exportFormats": ["pdf", "html", "docx", "latex"],
  "theme": {
    "fontFamily": "serif",
    "headingStyle": "numbered",
    "codeStyle": "monochrome"
  }
}
```

---

## Configuration File Format

Scilab Studio uses JSON for configuration files.

### Global Config (~/.scilab-studio/config.json)
```json
{
  "formatVersion": "1.0.0",
  "general": {
    "language": "en",
    "theme": "dark",
    "autoUpdate": true,
    "telemetry": false
  },
  "editor": {
    "fontSize": 14,
    "fontFamily": "Fira Code",
    "tabSize": 2,
    "lineNumbers": true,
    "wordWrap": true,
    "minimap": false
  },
  "engine": {
    "path": "/usr/local/bin/scilab",
    "version": "2024.0",
    "timeout": 30000,
    "maxSessions": 4
  },
  "marketplace": {
    "registry": "https://marketplace.scilab-studio.org",
    "autoUpdate": true,
    "installPath": "~/.scilab-studio/plugins"
  },
  "proxy": {
    "enabled": false,
    "host": "",
    "port": 0
  }
}
```

---

## Workspace Format

A workspace defines the layout and state of the IDE.

### workspace.json Schema
```json
{
  "formatVersion": "1.0.0",
  "projectId": "proj_abc123",
  "layout": {
    "sidebar": {
      "visible": true,
      "width": 260,
      "activePanel": "explorer"
    },
    "editor": {
      "openTabs": [
        { "file": "main.sce", "line": 42, "column": 0 },
        { "file": "utils.sce", "line": 1, "column": 0 }
      ],
      "splitDirection": "none"
    },
    "panel": {
      "visible": true,
      "height": 200,
      "activeTab": "output"
    },
    "toolbar": {
      "visible": true,
      "customButtons": []
    }
  },
  "moduleStates": {
    "visualization": { "active": true, "pinnedCharts": ["chart_001"] },
    "data-studio": { "active": true, "loadedDatasets": ["ds_001"] }
  },
  "recentFiles": [
    "main.sce",
    "data/input.csv",
    "results/analysis.png"
  ]
}
```

---

## Version Compatibility

All format files include a `formatVersion` field using semantic versioning:

- **Major version bump:** Incompatible schema changes. Migration required.
- **Minor version bump:** New optional fields. Backward-compatible.
- **Patch version bump:** Documentation or clarification changes.

### Compatibility Matrix

| Format | Current Version | Min Supported | Migration Available |
|--------|----------------|---------------|---------------------|
| project.json | 1.0.0 | 1.0.0 | N/A (initial) |
| plugin.json | 1.0.0 | 1.0.0 | N/A (initial) |
| template.json | 1.0.0 | 1.0.0 | N/A (initial) |
| widget.json | 1.0.0 | 1.0.0 | N/A (initial) |
| twin.yaml | 1.0.0 | 1.0.0 | N/A (initial) |
| report-template.json | 1.0.0 | 1.0.0 | N/A (initial) |
| config.json | 1.0.0 | 1.0.0 | N/A (initial) |
| workspace.json | 1.0.0 | 1.0.0 | N/A (initial) |

---

## Migration Guides

Migration guides will be provided when major version bumps require schema changes. Each guide will include:

1. **What changed** — List of schema differences.
2. **Impact** — What breaks and what still works.
3. **Migration steps** — Step-by-step instructions.
4. **Automated tool** — A CLI command to perform the migration: `scilab-studio migrate --format project.json --from 1.0 --to 2.0`.

For the initial release (v1.0), no migration is needed. Migration guides will be added with future major versions.
