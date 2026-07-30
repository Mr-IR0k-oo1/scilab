# Scilab Studio — Learning Center Specification

**Version:** 1.0.0
**Status:** Normative
**Last Updated:** 2026-07-27

This document specifies the Learning Center: built-in examples, tutorials, and educational content. For the Learning Center feature overview, see [Feature Modules §2.7](05_Feature_Modules.md).

---

## 1. Purpose

The Learning Center is the onboarding and educational hub of Scilab Studio. It provides:
- Pre-built example projects that demonstrate platform features.
- Step-by-step tutorials for common engineering tasks.
- Scilab language reference integrated with the platform.
- Templates for starting new projects.

---

## 2. Learning Center UI

### 2.1 Layout

```
Learning Center
├── Header
│   ├── Title: "Learning Center"
│   ├── Search bar
│   └── Category filter tabs
├── Content Grid
│   ├── Example cards (thumbnail, title, description, difficulty)
│   └── Tutorial cards (thumbnail, title, progress)
└── Detail Panel (on click)
    ├── Full description
    ├── Prerequisites
    ├── Files included
    ├── "Open Example" / "Start Tutorial" button
    └── Related examples
```

### 2.2 Access

- Menu: Help → Learning Center
- Welcome screen: "Browse Examples" button
- Command palette: "Learning Center: Open"

---

## 3. Content Categories

### 3.1 Categories

| Category | Description |
|----------|-------------|
| **Getting Started** | Platform basics, first project, basic operations |
| **Data Analysis** | CSV import, statistics, data transformation |
| **Visualization** | Chart creation, customization, export |
| **GUI Design** | GUI Builder usage, component properties, event binding |
| **Scilab Basics** | Scilab language fundamentals |
| **Signal Processing** | FFT, filtering, spectral analysis |
| **Control Systems** | Transfer functions, Bode plots, stability |
| **Optimization** | Linear programming, curve fitting |
| **Numerical Methods** | ODE solving, interpolation, integration |
| **Reports** | Report creation, data embedding, export |

### 3.2 Difficulty Levels

| Level | Description |
|-------|-------------|
| **Beginner** | No prior Scilab or engineering knowledge required |
| **Intermediate** | Basic Scilab knowledge assumed |
| **Advanced** | Engineering domain knowledge required |

---

## 4. Example Projects

### 4.1 Example Structure

Each example is a complete Scilab Studio project in `examples/`:

```
examples/
├── getting-started/
│   ├── project.json
│   ├── scripts/
│   │   └── main.sce
│   └── data/
│       └── sample.csv
├── data-analysis/
│   ├── project.json
│   ├── scripts/
│   │   ├── import_data.sce
│   │   └── analyze.sce
│   └── data/
│       └── measurements.csv
└── visualization/
    ├── project.json
    ├── scripts/
    │   └── charts.sce
    └── visualizations/
        └── line_chart.json
```

### 4.2 Example Metadata

Each example includes a `README.md`:

```markdown
# Basic Data Import

## Description
Import a CSV file, view its contents, and compute basic statistics.

## Difficulty
Beginner

## Duration
10 minutes

## What You'll Learn
- How to import CSV data
- How to preview data in the Data Studio
- How to compute column statistics
- How to export data

## Prerequisites
- None

## Files
- `data/measurements.csv` — Sample temperature measurements
- `scripts/main.sce` — Main script with import and analysis code
```

### 4.3 Built-in Examples (v0.1)

| Example | Category | Difficulty | Duration |
|---------|----------|-----------|----------|
| Hello World | Getting Started | Beginner | 5 min |
| First Project | Getting Started | Beginner | 10 min |
| Import CSV | Data Analysis | Beginner | 10 min |
| Data Statistics | Data Analysis | Beginner | 15 min |
| Transform Pipeline | Data Analysis | Intermediate | 20 min |
| Line Chart | Visualization | Beginner | 10 min |
| Multi-Series Chart | Visualization | Intermediate | 15 min |
| Heatmap | Visualization | Intermediate | 15 min |
| Export Charts | Visualization | Beginner | 10 min |
| Basic GUI | GUI Design | Beginner | 15 min |
| GUI with Callbacks | GUI Design | Intermediate | 25 min |
| Signal FFT | Signal Processing | Intermediate | 20 min |
| Bode Plot | Control Systems | Advanced | 25 min |
| ODE Solver | Numerical Methods | Advanced | 30 min |
| Lab Report | Reports | Intermediate | 20 min |

---

## 5. Tutorial System

### 5.1 Tutorial Structure

Tutorials are step-by-step guided experiences within the platform:

```jsonc
{
  "id": "tutorial-first-chart",
  "title": "Create Your First Chart",
  "description": "Learn how to create a line chart from imported data",
  "category": "visualization",
  "difficulty": "beginner",
  "duration": "10 minutes",
  "steps": [
    {
      "id": "step-1",
      "title": "Create a New Project",
      "instruction": "Click File → New Project. Name it 'My First Chart' and choose a location.",
      "action": {
        "type": "command",
        "command": "project:create"
      },
      "validation": {
        "type": "project_exists",
        "name": "My First Chart"
      },
      "hint": "The project name should appear in the title bar when successful."
    },
    {
      "id": "step-2",
      "title": "Import Sample Data",
      "instruction": "In the Data Studio panel, click 'Import Data' and select the provided sample CSV file.",
      "action": {
        "type": "command",
        "command": "data:import"
      },
      "validation": {
        "type": "data_imported"
      },
      "hint": "The data should appear in the Data Studio preview."
    }
  ]
}
```

### 5.2 Tutorial UI

When a tutorial is active:
- A tutorial panel appears at the bottom or right of the screen.
- The current step is highlighted with an instruction.
- A "Check" button validates the step's completion.
- A "Hint" button shows additional guidance.
- A "Skip" button advances to the next step.
- Progress is shown as a bar (e.g., "Step 3 of 8").

### 5.3 Validation Types

| Type | Description |
|------|-------------|
| `project_exists` | A project with the given name exists |
| `file_exists` | A file with the given path exists in the project |
| `data_imported` | A dataset has been imported |
| `chart_created` | A chart has been created |
| `code_executed` | Specific Scilab code was evaluated |
| `command_run` | A specific command was executed |
| `manual` | User clicks "I've done this" (no automated check) |

---

## 6. Scilab Reference

### 6.1 Integrated Help

The Learning Center includes a searchable Scilab function reference:
- Function name, syntax, parameters, return values, examples.
- Linked from the code editor (click a function name to see its reference).
- Searchable via the Learning Center search bar.

### 6.2 Function Categories

| Category | Functions |
|----------|-----------|
| **Basic** | `disp`, `who`, `clear`, `size`, `type`, `exists` |
| **Matrices** | `zeros`, `ones`, `rand`, `eye`, `diag`, `triu`, `tril` |
| **Plotting** | `plot`, `scatter`, `bar`, `histplot`, `title`, `xlabel`, `ylabel`, `legend` |
| **Data** | `csvRead`, `xlsRead`, `savemat`, `loadmat` |
| **Signal** | `fft`, `ifft`, `filter`, `correl`, `psd` |
| **Control** | `tf`, `ss`, `bode`, `nyquist`, `rlocus`, `step`, `impulse` |
| **Optimization** | `linpro`, `fsolve`, `lsq`, `qpsolve` |
| **Numerical** | `ode`, `ode45`, `interp`, `spline`, `intg` |
| **Statistics** | `mean`, `median`, `stdev`, `histc`, `corr`, `reglin` |

---

## 7. Content Management

### 7.1 Bundled Content

All built-in examples and tutorials are bundled with the application in the `examples/` directory. They are read-only and cannot be modified by the user.

### 7.2 User Content

Users can:
- Create their own examples in `~/.scilab-studio/user-examples/`.
- Save tutorials as JSON files in `~/.scilab-studio/user-tutorials/`.
- Import examples from the marketplace or from shared `.scstudio` archives.

### 7.3 Marketplace Content

Additional examples and tutorials are available from the marketplace:
- Community-contributed example projects.
- Professional tutorial series.
- Domain-specific content packs (e.g., "Control Systems Toolkit").

---

## 8. Search

### 8.1 Search Scope

The Learning Center search covers:
- Example titles and descriptions.
- Tutorial titles and step instructions.
- Scilab function names and descriptions.
- File contents within examples.

### 8.2 Search Features

- Fuzzy matching (typo tolerance).
- Category and difficulty filters.
- "Recently opened" quick access.
- "Continue where you left off" for tutorials.
