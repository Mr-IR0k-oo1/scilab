# Scilab Studio v0.1 — MVP Specification

**Document Version:** 1.0  
**Date:** 2026-07-27  
**Status:** Authoritative  
**Project:** Scilab Studio  
**Release Target:** v0.1.0

---

## Table of Contents

1. [Overview](#1-overview)
2. [MVP Feature List](#2-mvp-feature-list)
3. [Project File Format](#3-project-file-format-v01)
4. [Directory Structure](#4-directory-structure-v01)
5. [Technical Constraints](#5-technical-constraints)
6. [Definition of Done](#6-definition-of-done)
7. [Explicit Exclusions](#7-explicit-exclusions-what-v01-does-not-include)
8. [Testing Requirements](#8-testing-requirements)
9. [Documentation Requirements](#9-documentation-requirements)
10. [Appendix](#appendix)

---

## 1. Overview

Scilab Studio v0.1 is the first production release of an open-source engineering development platform built around Scilab. It is NOT a prototype, demo, or proof of concept. It must feel like a real, polished product from the moment the user installs it.

### 1.1 Product Identity

- **Name:** Scilab Studio
- **Version:** 0.1.0
- **License:** Open-source (license TBD before release)
- **Target Users:** Engineers, students, educators, researchers who use Scilab
- **Platform:** Desktop application (Linux, macOS, Windows)

### 1.2 Core Value Proposition

Scilab Studio provides a unified, modern development environment for Scilab that replaces the need to juggle separate tools for project management, GUI design, data visualization, data import, and report generation. Everything works together in one application.

### 1.3 What v0.1 Delivers

v0.1 ships with exactly **6 modules** plus a Learning Center:

| Module | Purpose |
|--------|---------|
| Project Workspace | File management, editor layout, Scilab connection |
| Project Manager | Create, open, configure projects |
| Visual GUI Builder | Drag-and-drop GUI design for Scilab |
| Visualization Studio | Create charts (Line, Scatter, Bar, Heatmap) |
| Data Studio | Import CSV/Excel, preview, statistics |
| Report Generator | Build PDF/HTML reports with embedded charts and tables |
| Learning Center | Browse and open example projects |

### 1.4 Non-Negotiable Requirements

1. **Cross-platform:** Must install and run on Linux (Ubuntu 20.04+, Fedora 36+), macOS (12+), and Windows (10+).
2. **No network dependency:** Every core feature must work completely offline.
3. **Local storage only:** All data stays on the user's machine. No cloud, no accounts, no telemetry.
4. **Scilab 7.0+ required:** The application communicates with Scilab via a Rust sidecar using stdin/stdout JSON-RPC.
5. **Real product feel:** The UI must be responsive, consistent, and polished. No "developer UI" or placeholder layouts.

---

## 2. MVP Feature List

### Module 1: Project Workspace

The Project Workspace is the foundational module. It provides the shell that all other modules inhabit.

**In scope:**

- **Create new project:** User provides a name, location, and optional description. The system generates `project.json` and the standard directory structure (see Section 4).
- **Open existing project:** User selects a project from a recent projects list or browses the filesystem. The workspace restores the previous layout state from `project.json`.
- **Save project:** Auto-save on every significant action (file creation, property change, layout change). Manual save via Ctrl+S / Cmd+S.
- **File explorer panel:** Tree view in the left sidebar showing all project files and folders. Expand/collapse, right-click context menu for file operations.
- **File operations:** Create new file (with template: blank, Scilab script, data file), create new folder, rename (with confirmation if referenced elsewhere), delete (with confirmation), move (drag-and-drop within tree).
- **Tab-based editor area:** Center panel with tabbed interface. Each open file gets a tab. Tabs reorderable. Close button on each tab.
- **Status bar:** Bottom bar showing Scilab connection status (Connected / Disconnected / Connecting), current project name, line/column in active editor, last saved timestamp.
- **Panel layout:** Left sidebar (default 250px, resizable 150–400px), center editor (fills remaining), right sidebar (default 300px, resizable 200–500px, collapsible), bottom panel (default hidden, toggle Ctrl+J / Cmd+J, height 100–400px).

**Out of scope:** Git integration (v0.2+), multi-window (v0.3+), cloud sync, collaboration, remote file access.

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| WS-01 | User can create a new project with name and location |
| WS-02 | `project.json` is created with correct schema |
| WS-03 | Directory structure matches Section 4 |
| WS-04 | File explorer shows correct tree structure |
| WS-05 | User can create, rename, and delete files and folders |
| WS-06 | Layout state persists across sessions |
| WS-07 | Scilab connection status visible in status bar |
| WS-08 | Panels resizable within specified ranges |
| WS-09 | Auto-save triggers on significant actions |

---

### Module 2: Project Manager

The Project Manager handles project lifecycle operations and configuration.

**In scope:**

- **New Project dialog:** Fields — Project Name (required), Location (required, folder picker), Description (optional), Template (dropdown, v0.1 only "Blank"). Validation — no `\/:*?"<>|` in name, writable location, no name conflict.
- **Open Project dialog:** Recent Projects list (last 10, sorted by last modified, shows name/location/date), File Browser (standard filesystem navigation to select `project.json`), Quick Open shortcut (Ctrl+Shift+O / Cmd+Shift+O).
- **Project Settings panel:** Scilab Version (display detected, read-only), Scilab Path (manual override), Module Toggles (enable/disable, all default enabled), Theme (Dark default / Light toggle). All saved to `project.json` under `settings`.
- **Project Metadata:** Stored in `project.json` — name, description, creation date, modification date, Scilab version, active modules, workspace layout, settings.

**Out of scope:** Project templates beyond "Blank" (v0.2), project import/export (v0.2), project archiving (v0.3), project duplication (v0.2), multi-project workspace (v0.3+).

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| PM-01 | New Project dialog validates all inputs (invalid names, unwritable locations) |
| PM-02 | `project.json` written with all required fields |
| PM-03 | Recent projects list shows last 10, sorted by last modified |
| PM-04 | File browser opens to system default location |
| PM-05 | Project settings persisted to `project.json` |
| PM-06 | Theme toggle applies immediately |
| PM-07 | Module toggles hide/show module UI elements |

---

### Module 3: Visual GUI Builder

The Visual GUI Builder allows users to design Scilab GUI layouts visually, without writing code.

**In scope:**

- **Canvas:** Grid-based with visible grid lines (toggleable), grid snapping (10px default, configurable), pan (middle-click or Space+drag), zoom (Ctrl+scroll / Cmd+scroll, 25%–400%), configurable size (default 800x600px).
- **Component palette (9 types):** Button, Label, Text Field, Number Input, Checkbox, Dropdown (editable options), Plot Container (placeholder for charts), Table (configurable rows/columns), Panel (grouping container).
- **Component operations:** Drag from palette to create, click to select (blue outline), drag to move, 8 resize handles (corners + midpoints), Delete key to remove, Ctrl+D / Cmd+D to duplicate, Shift+click for multi-select, marquee selection, right-click context menu (Delete, Bring to Front, Send to Back), alignment toolbar (left/center/right/top/middle/bottom).
- **Property panel:** Right sidebar with common props (ID, X, Y, Width, Height, Visible, Enabled) and type-specific props:
  - Button: Text, Font Size, Background Color, Text Color, OnClick (command string)
  - Label: Text, Font Size, Text Color, Alignment
  - Text Field: Placeholder, Default Value, Max Length, OnChange
  - Number Input: Min, Max, Step, Default Value, OnChange
  - Checkbox: Label, Default Checked, OnChange
  - Dropdown: Options (comma-separated), Default Index, OnChange
  - Plot Container: Chart Reference (dropdown of saved charts), Aspect Ratio
  - Table: Rows, Columns, Data Source (manual or file reference)
  - Panel: Border Style, Background Color, Children (nested components)
- **Preview mode:** Toggle via Play button or F5. Renders GUI as end user sees it. Components interactive (buttons clickable, text fields editable). Close with Escape or Stop button. Runs Scilab in background.
- **Persistence:** Save layout as `.json` in `layouts/`. Load from `.json`. Auto-save current layout state to project.
- **Code generation:** Generate Scilab `.sce` file from layout. Uses native Scilab GUI functions (`uicontrol`, `uimenu`, etc.). Code human-readable and editable. Regenerate button updates code from layout changes.

**Out of scope:** Custom widget creation (v0.2), responsive layouts (v0.3), animations (v0.3), multi-page GUIs (v0.2), event binding editor (code only, v0.2), undo/redo (v0.2), component templates (v0.2).

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| GB-01 | All 9 component types can be dragged onto canvas |
| GB-02 | Components can be selected, moved, resized |
| GB-03 | Grid snapping works at 10px intervals |
| GB-04 | Property panel shows correct properties for each type |
| GB-05 | Property edits apply to component in real-time |
| GB-06 | Preview mode renders functional, interactive GUI |
| GB-07 | Layout saves and loads correctly (round-trip) |
| GB-08 | Generated Scilab code is syntactically valid |
| GB-09 | Generated code can be executed by Scilab 7.0+ |
| GB-10 | Multi-select and delete work correctly |

---

### Module 4: Visualization Studio

The Visualization Studio creates charts from data with customization and export.

**In scope:**

- **Chart types (4):**
  - **Line:** X/Y points connected by lines. Multiple series. Line style (solid/dashed/dotted), width, color.
  - **Scatter:** X/Y points as markers. Multiple series. Marker shape (circle/square/triangle/diamond), size, color.
  - **Bar:** Vertical bars. Grouped and stacked modes. Bar width, colors per series.
  - **Heatmap:** 2D matrix as color grid. Color maps (viridis/plasma/jet/grayscale), row/column labels.
- **Data input:** From project datasets (`data/` directory), manual entry (small table editor), clipboard paste (tab-delimited).
- **Customization:** Title (text, font size, bold/italic), X/Y axis labels, axis ranges (auto or manual min/max), legend (show/hide, position: top/bottom/left/right), per-series color picker, background color, grid lines (show/hide, style).
- **Interactivity:** Zoom (mouse wheel or drag-select), Pan (middle-click or Ctrl+drag), Hover tooltip (data point values), Reset view button.
- **Export:** PNG (configurable 72–300 DPI), SVG (vector), PDF (vector, configurable page size A4/Letter).
- **Chart panel:** Sidebar listing saved charts. Double-click to open. Right-click: rename, delete, duplicate, export. Charts saved as `.json` in `charts/` directory.

**Out of scope:** 3D plots (v0.2), Sankey/network graphs (v0.3), gauges/meters (v0.3), real-time charts (v0.3), dashboards (v0.2), engineering plots — Bode/Nyquist/root locus (v0.2), histograms (v0.2), box plots (v0.2), pie charts (v0.2).

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| VS-01 | Line chart renders correctly from X/Y data |
| VS-02 | Scatter chart renders correctly |
| VS-03 | Bar chart renders correctly (grouped and stacked) |
| VS-04 | Heatmap renders correctly from matrix data |
| VS-05 | Chart renders in < 500ms for 10,000 data points |
| VS-06 | Zoom/pan responds within 50ms |
| VS-07 | Hover tooltip displays correct data values |
| VS-08 | PNG/SVG/PDF exports produce valid files |
| VS-09 | Charts load from saved `.json` files |
| VS-10 | Multiple series render with distinct colors |

---

### Module 5: Data Studio

The Data Studio imports, previews, and summarizes tabular data.

**In scope:**

- **CSV Import:** Auto-detect delimiter (comma, tab, semicolon, pipe), auto-detect header row, auto-detect column types (string, integer, float, date), encoding detection (UTF-8, Latin-1, ASCII), manual override for delimiter/header/encoding, preview first 20 rows before confirming.
- **Excel Import:** Read `.xlsx` and `.xls`. Sheet selection for multi-sheet workbooks. Header and type detection (same as CSV). Preview first 20 rows.
- **Data Preview Table:** First 100 rows. Column headers with type indicators (`abc`, `123`, `1.23`, date). Sortable columns. Virtual scrolling for large datasets. Row count at bottom.
- **Column Statistics:** Numeric — min, max, mean, median, standard deviation, null count, unique count. String — min/max length, most common value, null count, unique count. Date — min date, max date, range, null count. Mini histogram showing distribution.
- **Data Summary Panel:** Total rows/columns, memory estimate, column type breakdown, missing values summary.
- **Export:** CSV (configurable delimiter and encoding), column statistics as CSV.

**Out of scope:** SQLite/PostgreSQL import (v0.2+), MAT files (v0.2), IoT/streaming (v0.3), data transformation — filter/pivot/aggregate/join (v0.2), data visualization from Data Studio (use Visualization Studio), data cleaning (v0.2), formula/column creation (v0.2).

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| DS-01 | CSV with comma delimiter imports correctly |
| DS-02 | CSV with tab delimiter imports correctly |
| DS-03 | CSV with semicolon delimiter imports correctly |
| DS-04 | Excel .xlsx file imports correctly |
| DS-05 | Excel .xls file imports correctly |
| DS-06 | Multi-sheet workbook prompts for sheet selection |
| DS-07 | Column types detected with 95%+ accuracy |
| DS-08 | Preview shows first 100 rows |
| DS-09 | Column statistics are mathematically correct |
| DS-10 | 100MB+ CSV loads without crashing (with progress indicator) |
| DS-11 | Export produces valid CSV (re-importable) |
| DS-12 | Empty CSV handled gracefully (error message, no crash) |

---

### Module 6: Report Generator

The Report Generator creates formatted reports with embedded content from other modules.

**In scope:**

- **Templates (2):** Lab Report (title page, abstract, methods, results, conclusion — serif font, formal layout), Technical Brief (title, summary, findings, charts/tables, recommendations — sans-serif, compact).
- **Auto-population:** Title (from project name, editable), Date (current, editable), Project name (from `project.json`, read-only), Author (user-configurable in settings).
- **Content embedding:** Charts (dropdown from saved charts in project), data tables (dropdown from imported datasets), custom text blocks (bold, italic, headings — no images in v0.1), section breaks.
- **Report editor:** WYSIWYG-ish view showing structure. Drag to reorder sections. Add/remove sections. Edit text inline. Insert chart/table at cursor.
- **Export:** PDF (formatted, page breaks, headers, footers), HTML (self-contained single file, inline CSS). Both include title, date, project name, all sections.
- **Storage:** Reports saved as `.json` in `reports/`. Generated PDF/HTML saved alongside.

**Out of scope:** LaTeX equations (v0.2), bibliography/citations (v0.3), custom themes (v0.2), batch generation (v0.3), DOCX export (v0.3), code with syntax highlighting (v0.2), image embedding (v0.2), table of contents (v0.2), page number customization (v0.2).

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| RG-01 | User can select Lab Report template |
| RG-02 | User can select Technical Brief template |
| RG-03 | Auto-populated fields show correct values |
| RG-04 | Chart from Visualization Studio embeds correctly |
| RG-05 | Data table from Data Studio embeds correctly |
| RG-06 | PDF export is properly formatted with page breaks |
| RG-07 | HTML export renders correctly in Chrome/Firefox |
| RG-08 | Report generation completes in < 10 seconds |
| RG-09 | Report can be saved and reloaded |
| RG-10 | Custom text supports bold and italic |

---

### Module 7: Learning Center

**In scope:**

- **Example projects list:** 5–10 pre-built examples with name, brief description, difficulty (Beginner/Intermediate/Advanced), module tags.
- **Open example:** Copies to user workspace (default `~/ScilabStudio/Examples/`) and opens as regular project.
- **Basic search:** Text search across names and descriptions. Real-time filtering as user types.
- **Bundled examples (minimum 5):**
  1. Hello Scilab — Basic script execution, project structure (Beginner)
  2. Data Explorer — Import CSV, view statistics (Beginner)
  3. Chart Maker — Create all 4 chart types (Beginner)
  4. GUI Designer — Build a simple calculator GUI (Intermediate)
  5. Lab Report — Import data, create charts, generate PDF report (Intermediate)

**Out of scope:** Spoken Tutorial integration (v0.2), learning paths (v0.3), progress tracking (v0.3), guided walkthroughs (v0.2), video playback (v0.3), community examples (v0.3).

**Acceptance criteria:**

| ID | Criterion |
|----|-----------|
| LC-01 | At least 5 example projects bundled |
| LC-02 | Examples are complete and runnable |
| LC-03 | Search filters by name and description |
| LC-04 | Opening an example copies it to user workspace |
| LC-05 | Copied example is a valid project with `project.json` |
| LC-06 | Examples cover all 6 modules |

---

## 3. Project File Format (v0.1)

Every project is defined by a `project.json` at the root. This is the single source of truth.

```json
{
  "version": "0.1.0",
  "name": "Signal Analysis Lab",
  "description": "Analysis of frequency response data from oscilloscope measurements",
  "created": "2026-07-27T10:00:00Z",
  "modified": "2026-07-27T14:30:00Z",
  "scilab_version": "7.0.0",
  "modules": ["workspace", "gui-builder", "viz-studio", "data-studio", "report-gen"],
  "plugins": [],
  "settings": {
    "scilab_path": "",
    "theme": "dark"
  },
  "workspace": {
    "layout": {
      "left_panel": { "visible": true, "width": 250, "active_tab": "files" },
      "right_panel": { "visible": true, "width": 300, "active_tab": "properties" },
      "bottom_panel": { "visible": false, "height": 200 }
    }
  },
  "recent_charts": ["charts/frequency_response.json"],
  "recent_data": ["data/oscilloscope_capture.csv"]
}
```

**Required fields:** `version`, `name`, `created`, `modified`, `scilab_version`, `modules`, `settings`.  
**Validation:** `version` must be `"0.1.0"`. `name` max 100 chars, pattern `[^\\/:*?"<>|]+`. `scilab_version` >= `"7.0.0"`. `theme` enum `["dark", "light"]`. Panel widths within ranges (left: 150–400, right: 200–500, bottom: 100–400). `plugins` array must be empty in v0.1.

---

## 4. Directory Structure (v0.1)

```
project/
├── project.json              # Project configuration (required)
├── layouts/                  # GUI Builder layout files (.json)
│   └── calculator.json
├── scripts/                  # Scilab scripts (.sce, .sci)
│   └── main.sce
├── data/                     # Imported datasets (.csv, .xlsx, .xls)
│   ├── measurements.csv
│   └── results.xlsx
├── charts/                   # Chart definitions (.json)
│   └── line_chart_01.json
├── assets/                   # Images, icons, static resources
│   └── logo.png
├── reports/                  # Report definitions and exports
│   ├── lab_report.json       # Report definition
│   ├── lab_report.pdf        # Generated PDF
│   └── lab_report.html       # Generated HTML
└── .scilab-studio/           # Internal metadata (auto-managed)
    ├── recent-files.json
    └── chart-cache/
```

**Rules:**
- All directories created on project initialization.
- `.scilab-studio/` is hidden (dot-prefixed), do not modify.
- File names within `layouts/`, `charts/`, `reports/` must be unique.
- No `\/:*?"<>|` in file names. Max path length 260 chars (Windows).

---

## 5. Technical Constraints

| Requirement | Specification |
|-------------|--------------|
| **Scilab** | Version 7.0.0+. Installed on PATH or configured via `scilab_path`. |
| **OS** | Linux (Ubuntu 20.04+, Fedora 36+, Debian 11+), macOS (12+), Windows (10 1903+) |
| **RAM** | Minimum 4 GB, recommended 8 GB |
| **Disk** | Minimum 1 GB free (application + dependencies) |
| **Display** | Minimum 1280x720. 1920x1080 recommended. |
| **Python** | NOT required (removed as a dependency) |
| **Network** | NOT required (all features offline, no telemetry) |

**Technology stack:**

| Layer | Technology |
|-------|-----------|
| Shell | Tauri 2.x (Rust backend + webview frontend) |
| Frontend | TypeScript + Svelte 5 |
| Backend | Rust (Tauri commands for file I/O, Scilab communication, PDF) |
| Scilab Bridge | Rust sidecar — stdin/stdout JSON-RPC 2.0 |
| Database | SQLite via rusqlite (metadata only: recent projects, search index, preferences) |
| Filesystem | Direct I/O (all project data as flat files) |
| Excel | calamine (Rust crate) |
| CSV | csv (Rust crate) with auto-delimiter detection |
| Charts | HTML Canvas API in frontend |

**Scilab Bridge protocol:** Launches Scilab as subprocess (`scilab -nogui -nosplash -nw`). JSON-RPC 2.0 over stdin/stdout. Methods: `scilab.execute` (run command), `scilab.execute_file` (run .sce), `scilab.get_variable` / `scilab.set_variable` (workspace access), `scilab.get_version`, `scilab.ping`. Crash handling: auto-restart + user notification. Command timeout: 30s default, max 300s. Max message: 10 MB.

**Performance targets:**

| Operation | Target |
|-----------|--------|
| Cold start | < 3 seconds |
| Project open (< 100 files) | < 2 seconds |
| Chart render (10k points) | < 500 ms |
| Chart render (100k points) | < 2 seconds |
| Zoom/pan response | < 50 ms |
| CSV import (100 MB) | < 30 seconds |
| PDF generation (10 pages) | < 10 seconds |
| File explorer refresh (< 1000 files) | < 500 ms |
| Search results | < 100 ms |

---

## 6. Definition of Done

v0.1 is **DONE** when ALL of the following are met:

**Functional:**
1. Installable on Linux (.AppImage + .deb), macOS (.dmg), Windows (.msi)
2. User can create a project and see valid `project.json` + directory structure
3. User can drag GUI components, edit properties, preview, generate valid Scilab code
4. User can import CSV (any delimiter) and Excel, preview data, view column statistics
5. User can create a line chart from imported data, customize, zoom/pan, hover
6. User can create a report, embed chart, export properly formatted PDF
7. User can browse and open example projects from Learning Center

**Quality:**
8. All modules > 80% test coverage (unit + integration)
9. README covers installation on all 3 platforms; user guides for all modules; developer guide complete
10. Zero critical bugs preventing any of the 7 functional requirements
11. No data loss from normal operations; auto-save never writes partial data

**Release artifacts:**
12. Linux: AppImage + .deb
13. macOS: .dmg (signed if possible, unsigned acceptable)
14. Windows: .msi installer
15. Tagged GitHub release with CHANGELOG.md

---

## 7. Explicit Exclusions (What v0.1 Does NOT Include)

The following are definitively excluded. No exceptions.

**Excluded modules:** AI Engineering Assistant, Digital Twin Framework, Parameter Sweep Studio, Experiment Recorder, Interactive Laboratory Creator, Widget Marketplace, Community Marketplace, Open Engineering Library, Open Digital Twin Library, Xcos Builder, Engineering Dashboard Builder, Research Workspace.

**Excluded features:** Git integration, multi-window, cloud sync, multi-language support (i18n), custom widget creation, responsive layouts, undo/redo in GUI Builder, event binding editor, 3D plots, Bode/Nyquist/root locus plots, real-time updating charts, dashboard layouts, data transformation (filter/pivot/aggregate/join), SQL database connections, MAT file import, LaTeX equations, DOCX export, custom report themes, Spoken Tutorial integration, learning paths, progress tracking, plugin system (v0.2), project templates beyond Blank (v0.2), project import/export (v0.2).

---

## 8. Testing Requirements

**Test pyramid:** 60% unit, 30% integration, 10% E2E.

**Unit tests — Rust backend:** Scilab Bridge RPC methods (mock subprocess), CSV parser (delimiter/type/encoding detection), Excel reader, PDF generator, file I/O, `project.json` validation, search indexing.

**Unit tests — Svelte frontend:** Component property panels (all 9 types), chart rendering functions, file explorer tree, property editor inputs, layout persistence.

**Integration tests:** Scilab Bridge (launch + execute + verify output), file operations pipeline (create → verify → read → verify in UI), data import pipeline (import → preview → statistics → export), chart pipeline (load data → create → render → export → verify), report pipeline (create → embed chart → export PDF → verify content).

**E2E tests (automated):** (1) Project creation: launch → new project → verify structure. (2) GUI builder: open → drag 3 components → edit properties → preview. (3) Data import: import CSV → verify preview → verify statistics. (4) Chart creation: load data → create line chart → verify render → zoom. (5) Report export: create report → embed chart → export PDF → verify. (6) Learning Center: browse → search → open example → verify loads.

**Performance tests:** Chart render 10k (< 500ms), 100k (< 2s). CSV import 100MB (< 30s). PDF generation 10-page (< 10s). Cold start (< 3s). Idle memory (< 200MB). Active memory (< 500MB).

**Platform matrix:** All tests pass on Ubuntu 22.04, macOS 13+, Windows 10+. Platform-specific issues documented in release notes.

---

## 9. Documentation Requirements

**README.md** (repository root): Project name + one-line description, 3+ screenshots, system requirements, installation instructions (Linux/macOS/Windows), quick start (5 steps), links to docs, license, contributing guidelines, issue tracker link.

**User guides** (`docs/guides/`): One per module — `project-workspace.md`, `project-manager.md`, `gui-builder.md`, `visualization-studio.md`, `data-studio.md`, `report-generator.md`, `learning-center.md`. Each covers: module overview, step-by-step instructions for common tasks, screenshots, troubleshooting, keyboard shortcuts reference.

**Developer guide** (`docs/DEVELOPER.md`): Prerequisites (Rust, Node.js, Tauri CLI, Scilab), dev setup, architecture overview (Tauri shell, frontend, Scilab Bridge, filesystem), project structure, Scilab Bridge protocol docs, contributing workflow (fork → branch → PR → review → merge), code style (Rust: rustfmt + clippy, TS: prettier + eslint), test instructions.

**API reference** (`docs/API_Reference.md`): Placeholder for v0.2 plugin API — plugin manifest format (draft), available hooks (draft), example plugin skeleton.

---

## Appendix

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-07-27 | Initial MVP — 6 modules + Learning Center |

### Glossary

| Term | Definition |
|------|-----------|
| **Scilab Bridge** | Rust sidecar communicating with Scilab via stdin/stdout JSON-RPC |
| **Layout** | GUI Builder design file (`.json`) defining components and properties |
| **Chart** | Visualization Studio visualization definition (`.json`) |
| **Report** | Report Generator document definition (`.json`) |
| **Module** | A distinct feature area (e.g., GUI Builder, Data Studio) |

### Open Questions (Resolve Before Development)

1. License: MIT, Apache 2.0, or GPL?
2. Code signing for macOS/Windows — feasible for v0.1?
3. Scilab auto-detection method per platform?
4. Chart rendering: Rust library (plotters) for export vs pure Canvas API?
5. PDF generation: `print-pdf`, `wkhtmltopdf` bindings, or custom?
6. Examples: pre-generated data or generate on first run?
7. Theme depth: colors only, or also spacing/typography?

---

*End of Scilab Studio v0.1 MVP Specification*
