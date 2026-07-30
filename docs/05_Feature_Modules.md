# Scilab Studio — Feature Modules

**Version:** 1.0.0
**Status:** Normative
**Last Updated:** 2026-07-27

This document describes the user-facing feature modules in Scilab Studio. For platform infrastructure (Event Bus, Plugin Manager, Scilab Integration Layer, etc.), see [Platform Architecture](04_Platform_Architecture.md).

---

## 1. Module Overview

Feature modules provide the user-facing capabilities of Scilab Studio. Each module is an independent plugin that integrates with the platform through the Event Bus and Plugin Manager. Modules can be installed, updated, or removed independently. They depend on platform services for infrastructure — rendering, persistence, communication — and on each other for cross-cutting features like embedding charts in reports. This separation keeps modules focused on user workflows while the platform handles plumbing.

### Module Lifecycle

Each module follows a defined lifecycle managed by the Plugin Manager:

1. **Discovery** — The module is registered in the plugin manifest (bundled or installed from marketplace).
2. **Activation** — The module registers its panels, menus, commands, and event subscriptions with the Workspace Manager and Event Bus.
3. **Running** — The module responds to user actions and events, renders its UI, and exposes its APIs.
4. **Deactivation** — The module unregisters its contributions, releases resources, and persists any unsaved state.
5. **Removal** — The module's installed files are deleted; its data in the project directory is preserved unless the user explicitly opts to remove it.

Modules declare their dependencies on platform services and on other feature modules. The Plugin Manager resolves dependency order at activation time and prevents circular dependencies. If a dependency is unavailable, the module enters a degraded state and notifies the user which features are unavailable.

### Version Roadmap

| Module | v0.1 | v0.2 | v0.3 | v0.4 |
|--------|------|------|------|------|
| GUI Builder | ✅ 9 components | +Text Area, Image, Tabs, Slider | | |
| Visualization Studio | ✅ 4 chart types | +3D, Bode, Nyquist, Root Locus | +Sankey, Network, Gauges | |
| Data Studio | ✅ CSV, Excel | +SQLite, +Transform pipeline | +PostgreSQL, MAT, Streaming | |
| Report Generator | ✅ PDF, HTML | +LaTeX, +Batch | +DOCX, +Code | |
| Learning Center | ✅ Examples | +Tutorials | +Paths, +Progress | |
| Widget Marketplace | | ✅ | | |
| Lab Creator | | ✅ | | |
| Xcos Builder | | ✅ | | |
| Project Templates | | ✅ | | |
| Dashboard Builder | | | ✅ | |
| AI Assistant | | | ✅ | |
| Digital Twin Framework | | | ✅ | |
| Parameter Sweep | | | ✅ | |
| Experiment Recorder | | | ✅ | |
| Community Marketplace | | | | ✅ |
| Open Engineering Library | | | | ✅ |
| Research Workspace | | | | ✅ |

---

## 2. Version 0.1 Modules (Full Specification)

---

### 2.1 GUI Builder

**Purpose:** Drag-and-drop interface designer that generates Scilab GUI code.

**Scope (v0.1):**
- Drag-and-drop canvas with grid snapping and alignment guides
- Component palette: Button, Label, Text Field, Number Input, Checkbox, Dropdown, Plot Container, Table, Panel
- Property panel (edit selected component: text, size, color, position)
- Preview mode (render the GUI in a new window)
- Save/load layout as `.json` file
- Generate Scilab GUI code from layout

**Out of Scope:**
- Custom widget creation (v0.2 Widget Marketplace)
- Responsive layout (v0.2)
- Animation/transitions (v0.2)
- Multi-page GUIs (v0.2)
- Visual event binding editor (use code for now)
- Text Area, Image Viewer, Tab Container, Slider (v0.2)

**Architecture:**
- Components: `GuiBuilder.svelte`, `Canvas.svelte`, `ComponentPalette.svelte`, `PropertyPanel.svelte`, `PreviewWindow.svelte`, `CodeGenerator.ts`
- APIs: `createLayout()`, `addComponent(type, position)`, `updateProperty(id, prop, value)`, `generateCode(layout)`, `saveLayout()`, `loadLayout()`
- Consumes: Workspace Manager (panel registration), Event Bus (`project:opened`)

**Data Model:**
- Layout file format:
```json
{
  "id": "layout-uuid",
  "name": "My GUI",
  "created": "2026-07-27T10:00:00Z",
  "modified": "2026-07-27T10:00:00Z",
  "canvas": { "width": 800, "height": 600, "background": "#ffffff" },
  "components": [
    {
      "id": "comp-1",
      "type": "button",
      "x": 100, "y": 50, "width": 120, "height": 40,
      "properties": { "text": "Calculate", "fontSize": 14, "color": "#000000", "backgroundColor": "#4CAF50" }
    }
  ]
}
```
- Stored in `layouts/` directory

**Acceptance Criteria:**
1. User can drag 9 component types from palette onto canvas and see them rendered.
2. User can select, move, and resize components on the canvas with snap-to-grid.
3. User can edit component properties (text, font size, color, position) in the property panel and see changes reflected immediately.
4. User can preview the GUI in a separate window that renders the layout.
5. User can save a layout and reload it later with all components preserved.

**Dependencies:** Workspace Manager, Event Bus, Configuration System

---

### 2.2 Visualization Studio

**Purpose:** Create interactive engineering charts from data.

**Scope (v0.1):**
- 4 chart types: Line, Scatter, Bar, Heatmap
- Data input: from imported datasets or manual entry
- Chart customization: title, axis labels, colors, legend, grid
- Interactive: zoom, pan, hover tooltip with data values
- Export: PNG, SVG, PDF
- Chart panel (sidebar listing available charts)

**Out of Scope:**
- 3D surface/mesh plots (v0.2)
- Engineering-specific plots: Bode, Nyquist, Root Locus, Polar (v0.2)
- Sankey diagrams, network graphs (v0.3)
- Gauges, meters, oscilloscopes (v0.3)
- Real-time updating charts (v0.3)
- Dashboard-style multi-panel layouts (v0.3 Dashboard Builder)

**Architecture:**
- Components: `VizStudio.svelte`, `ChartCanvas.svelte`, `ChartConfigurator.svelte`, `ChartExporter.ts`, `renderers/Line.ts`, `renderers/Scatter.ts`, `renderers/Bar.ts`, `renderers/Heatmap.ts`
- APIs: `createChart(type, data, config)`, `updateChart(id, config)`, `exportChart(id, format)`, `getChartList()`
- Consumes: Data Studio (`data:loaded` events), Event Bus

**Data Model:**
- Chart configuration stored in project metadata
- Chart exports saved to `reports/` directory

**Acceptance Criteria:**
1. User can create all 4 chart types from a dataset.
2. Charts render in under 500ms for datasets up to 10,000 points.
3. Zoom, pan, and hover tooltip work smoothly.
4. Export produces valid PNG, SVG, and PDF files.
5. Charts can be embedded in GUI Builder layouts via Plot Container component.

**Dependencies:** Data Studio (for data input), Visualization Engine (rendering infrastructure), Event Bus

---

### 2.3 Data Studio

**Purpose:** Import, preview, and manage engineering datasets.

**Scope (v0.1):**
- Import CSV (auto-detect delimiter, headers, types)
- Import Excel (.xlsx, .xls)
- Data preview table (first 100 rows with pagination)
- Column statistics (min, max, mean, nulls, type)
- Data summary panel
- Export data as CSV

**Out of Scope:**
- SQLite import (v0.2)
- PostgreSQL connection (v0.3)
- MAT file import (v0.3)
- IoT/streaming data (v0.3)
- Data transformation pipeline (filter, pivot, aggregate) (v0.2)
- Direct data visualization (use Visualization Studio)

**Architecture:**
- Components: `DataStudio.svelte`, `ImportDialog.svelte`, `DataPreview.svelte`, `ColumnStats.svelte`, `DataSummary.svelte`
- APIs: `importFile(path, format)`, `getPreview(datasetId)`, `getStatistics(datasetId)`, `exportCSV(datasetId, path)`
- Consumes: Project Manager (`project:opened`), Event Bus

**Data Model:**
- Datasets stored in `data/` directory
- Metadata in SQLite: `datasets` table (id, project_id, name, file_path, format, row_count, column_count, columns_json, imported_at)

**Acceptance Criteria:**
1. CSV import correctly handles commas, tabs, and semicolons as delimiters.
2. Excel import reads both .xlsx and .xls formats.
3. Data preview shows correct data types (numbers, strings, dates).
4. Column statistics are accurate for numeric and categorical columns.
5. Large files (100MB+) show a progress indicator and do not crash the application.

**Dependencies:** File System Service, Event Bus, Configuration System

---

### 2.4 Report Generator

**Purpose:** Export professional reports as PDF and HTML with embedded charts and data.

**Scope (v0.1):**
- Report template selection (Lab Report, Technical Brief)
- Auto-populate: title, date, project name, author
- Embed charts from Visualization Studio
- Embed data tables from Data Studio
- Export as PDF (via print-to-PDF or HTML-to-PDF)
- Export as HTML

**Out of Scope:**
- LaTeX equation rendering (v0.2)
- Bibliography/citations (v0.2)
- Custom themes (v0.2)
- Batch generation (v0.2)
- DOCX export (v0.3)
- Code inclusion (v0.2)

**Architecture:**
- Components: `ReportGenerator.svelte`, `TemplateSelector.svelte`, `ReportPreview.svelte`, `ReportExporter.ts`
- APIs: `selectTemplate(templateId)`, `embedChart(chartId)`, `embedTable(datasetId)`, `generateReport(format)`, `getTemplates()`
- Consumes: Visualization Studio (chart references), Data Studio (dataset references), Event Bus

**Data Model:**
- Report templates stored in `templates/` directory (bundled with app)
- Generated reports saved to `reports/` directory
- Report configuration stored in project metadata

**Acceptance Criteria:**
1. User can select a template and see a preview of the report.
2. Report correctly embeds charts from Visualization Studio.
3. Report correctly embeds data tables from Data Studio.
4. PDF export produces a properly formatted document.
5. HTML export is viewable in any modern browser.

**Dependencies:** Visualization Studio (chart embedding), Data Studio (table embedding), File System Service, Event Bus

---

### 2.5 Learning Center

**Purpose:** Browse and open example projects to learn Scilab Studio workflows.

**Scope (v0.1):**
- Example projects list (5-10 pre-built examples covering different domains)
- Open example project (copies to user's workspace)
- Basic search across examples by name and description

**Out of Scope:**
- Spoken Tutorial video integration (v0.2)
- Guided walkthroughs (v0.2)
- Learning paths and progress tracking (v0.3)
- Skill assessment (v0.3)
- Multi-language support (v0.3)

**Architecture:**
- Components: `LearningCenter.svelte`, `ExampleList.svelte`, `ExampleDetail.svelte`, `SearchBar.svelte`
- APIs: `getExamples()`, `getExample(id)`, `openExample(id)`, `searchExamples(query)`
- Consumes: Project Manager (to create project from example), Event Bus

**Data Model:**
- Examples bundled with the application in `resources/examples/`
- Each example: `example.json` (metadata) + project files

**Acceptance Criteria:**
1. At least 5 example projects are bundled and visible in the Learning Center.
2. User can search examples by name and see filtered results.
3. User can open an example and have it copied to their workspace as a new project.
4. Examples are complete, runnable projects (not stubs).

**Dependencies:** Project Manager (project creation), Event Bus

---

## 3. Module Dependency Graph (v0.1)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ GUI Builder │     │Viz Studio   │     │Data Studio  │
│             │     │             │     │             │
│ embeds ─────│────▶│ charts from │◀────│ data to     │
│             │     │             │     │ chart       │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Event Bus  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐    │    ┌───────▼──────┐
       │Report Gen   │    │    │Learning      │
       │             │    │    │Center        │
       │ embeds ─────│────┘    │              │
       │ charts +    │         │ opens ──────▶│ Project
       │ tables      │         │ examples     │ Manager
       └─────────────┘         └──────────────┘
```

### Dependency Narratives

The dependency graph reveals three tiers of module interaction:

- **Data producers** (Data Studio, Visualization Studio) generate artifacts — datasets and charts — that other modules consume. Data Studio is the primary data entry point; Visualization Studio consumes its output to produce charts.
- **Data consumers** (GUI Builder, Report Generator) embed artifacts produced by other modules. GUI Builder embeds Plot Containers that render Visualization Studio charts. Report Generator embeds both charts and data tables into exportable documents.
- **Orchestrators** (Learning Center) drive the Project Manager to create new projects from templates, triggering the full module chain.

All inter-module communication flows through the Event Bus. No module holds a direct reference to another module's components or APIs. This loose coupling allows any module to be disabled without breaking others — the Report Generator simply will not find charts to embed if Visualization Studio is inactive.

---

## 4. Module Communication (v0.1)

Each module communicates exclusively through the Event Bus. Below are the events each module emits and consumes. Event payloads are documented in the [Platform Architecture](04_Platform_Architecture.md) Event Bus section.

### Event Naming Convention

Events follow the pattern `{module}:{entity}:{action}`:
- `gui:layout:created` — GUI Builder created a layout
- `viz:chart:exported` — Visualization Studio exported a chart
- `data:loaded` — Data Studio finished importing a dataset

### Per-Module Events

**GUI Builder**
- Emits: `gui:layout:created`, `gui:layout:saved`, `gui:layout:loaded`, `gui:code:generated`
- Consumes: `project:opened`, `project:saved`

**Visualization Studio**
- Emits: `viz:chart:created`, `viz:chart:exported`, `viz:chart:updated`
- Consumes: `data:loaded`, `project:opened`

**Data Studio**
- Emits: `data:loaded`, `data:preview`, `data:exported`, `data:statistics`
- Consumes: `project:opened`, `project:saved`

**Report Generator**
- Emits: `report:generated`, `report:exported`
- Consumes: `viz:chart:created`, `data:loaded`, `project:opened`

**Learning Center**
- Emits: `example:opened`
- Consumes: `project:created`

### Cross-Module Data Flow Example

A typical user workflow illustrates the event chain:

1. User imports a CSV in **Data Studio** → emits `data:loaded` with dataset ID.
2. **Visualization Studio** receives `data:loaded`, makes dataset available in chart data picker.
3. User creates a line chart in **Visualization Studio** → emits `viz:chart:created` with chart ID.
4. **Report Generator** receives `viz:chart:created`, makes chart available in embed picker.
5. User embeds the chart and dataset table in a report, then exports as PDF → emits `report:exported`.

At no point does Data Studio know that Visualization Studio exists. The Event Bus decouples producers from consumers entirely.

---

## 5. Future Modules (Brief Descriptions)

### Widget Marketplace (v0.2)

**Purpose:** A curated library of custom GUI widgets contributed by the community and the core team.

**Planned Version:** v0.2

**Key Capability:** Users browse, install, and use third-party widgets in their GUI layouts. Widgets are sandboxed plugins that follow the same component contract as built-in GUI Builder components, but live outside the core codebase.

**Planned Dependencies:** GUI Builder, Plugin Manager

### Interactive Lab Creator (v0.2)

**Purpose:** Auto-generate complete interactive lab exercises from structured input.

**Planned Version:** v0.2

**Key Capability:** Instructors define objectives, theory, simulation code, and assessment questions — the Lab Creator assembles them into a publishable lab package with embedded GUI, interactive plots, and auto-graded evaluation. Integrates with Scilab's execution engine for live student interaction.

**Planned Dependencies:** GUI Builder, Visualization Studio, Scilab Integration Layer

### Xcos Builder (v0.2)

**Purpose:** A visual block-diagram editor for building and running Xcos simulations.

**Planned Version:** v0.2

**Key Capability:** Drag-and-drop block placement, connection wiring, and simulation execution — all within Scilab Studio rather than the standalone Xcos application. Saves diagrams as `.xcos` files and runs them through the Scilab Integration Layer.

**Planned Dependencies:** Scilab Integration Layer, Visualization Studio

### Project Templates (v0.2)

**Purpose:** Pre-built project scaffolds for common engineering workflows.

**Planned Version:** v0.2

**Key Capability:** One-click project creation from templates like "Control System Analysis," "Signal Processing Lab," "Thermal Simulation," or "Data Import & Visualization." Each template comes with folder structure, starter scripts, example data, and configured modules.

**Planned Dependencies:** Project Manager, File System Service

### Dashboard Builder (v0.3)

**Purpose:** Compose multi-panel monitoring dashboards from live charts, gauges, and data feeds.

**Planned Version:** v0.3

**Key Capability:** A freeform canvas where users tile multiple Visualization Studio charts, custom gauges, data tables, and parameter readouts into a single real-time dashboard view. Supports refresh intervals and live data bindings.

**Planned Dependencies:** Visualization Studio, Data Studio, State Management

### AI Engineering Assistant (v0.3)

**Purpose:** Natural-language assistant that helps users write Scilab code, debug errors, and understand results.

**Planned Version:** v0.3

**Key Capability:** Chat-based interface that generates Scilab scripts from descriptions, explains error messages, suggests optimizations, and can reference the user's current project context (open files, loaded datasets, active charts) for relevant suggestions.

**Planned Dependencies:** Scilab Integration Layer, Project Manager, State Management

### Digital Twin Framework (v0.3)

**Purpose:** Build and run live digital-twin simulations that sync with real-world data.

**Planned Version:** v0.3

**Key Capability:** Define a physical system model in Scilab/Xcos, connect it to real-time or recorded sensor data, and run state estimation or predictive simulations. The framework handles data ingestion, model synchronization, and result visualization in a unified dashboard.

**Planned Dependencies:** Scilab Integration Layer, Data Studio, Visualization Studio, Dashboard Builder

### Parameter Sweep Studio (v0.3)

**Purpose:** Systematically vary simulation parameters and analyze the result space.

**Planned Version:** v0.3

**Key Capability:** Define parameter ranges and sweep strategies (grid, random, Latin Hypercube), run batch Scilab simulations, and visualize sensitivity, Pareto fronts, and distribution of outcomes. Stores sweep results in SQLite for post-analysis.

**Planned Dependencies:** Scilab Integration Layer, Visualization Studio, Data Studio

### Experiment Recorder (v0.3)

**Purpose:** Record, annotate, and replay engineering computation sessions.

**Planned Version:** v0.3

**Key Capability:** Captures every command, GUI interaction, and result during a session with timestamps and user annotations. Sessions can be replayed step-by-step, exported as reproducible reports, or shared with collaborators.

**Planned Dependencies:** Event Bus, Report Generator, Project Manager

### Community Marketplace (v0.4)

**Purpose:** A public marketplace for sharing and discovering community-built extensions.

**Planned Version:** v0.4

**Key Capability:** Extends the Widget Marketplace with user reviews, ratings, version history, and dependency resolution. Community members publish widgets, templates, example projects, and plugins for others to install with one click.

**Planned Dependencies:** Widget Marketplace, Plugin Manager, Project Manager

### Open Engineering Library (v0.4)

**Purpose:** A searchable library of open-source Scilab functions, scripts, and toolboxes.

**Planned Version:** v0.4

**Key Capability:** Aggregates vetted Scilab code from FOSSEE, ATOMS, and community contributions into a unified, indexed library. Users search by domain, function name, or problem type, and install code directly into their project.

**Planned Dependencies:** Scilab Integration Layer, Plugin Manager

### Research Workspace (v0.4)

**Purpose:** Collaborative environment for multi-user engineering research projects.

**Planned Version:** v0.4

**Key Capability:** Shared project spaces with real-time co-editing of scripts, data, and visualizations. Includes version control integration, experiment comparison tools, and a publication-ready report pipeline that pulls from the full module ecosystem.

**Planned Dependencies:** Project Manager, Event Bus, State Management, Report Generator

---

## 6. Module Ecosystem Summary

The 17 modules in Scilab Studio are organized into four delivery waves:

| Wave | Modules | Focus |
|------|---------|-------|
| **v0.1** | GUI Builder, Visualization Studio, Data Studio, Report Generator, Learning Center | Core authoring and data workflows |
| **v0.2** | Widget Marketplace, Lab Creator, Xcos Builder, Project Templates | Extensibility and simulation tooling |
| **v0.3** | Dashboard Builder, AI Assistant, Digital Twin, Parameter Sweep, Experiment Recorder | Advanced analysis and intelligence |
| **v0.4** | Community Marketplace, Open Engineering Library, Research Workspace | Collaboration and ecosystem |

The dependency direction is strictly forward: v0.1 modules depend only on platform services. v0.2 modules may depend on v0.1 modules. v0.3 modules may depend on v0.1 and v0.2 modules. v0.4 modules may depend on any earlier module. No backward dependencies are permitted — a v0.1 module must never depend on a v0.2+ module.

This constraint ensures that the core platform remains stable and independently usable even when advanced modules are not installed.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-27 | Core Team | Initial version — v0.1 full spec, future modules brief |
