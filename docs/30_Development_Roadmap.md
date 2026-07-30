# 30 — Development Roadmap

Development is split into sprints. Each sprint produces a working increment that can be demonstrated.

---

## Sprint 1 — Platform Foundation

**Goal:** A working shell that can load modules, manage projects, and talk to Scilab.

### Deliverables

| Component | Description |
|-----------|-------------|
| Core Runtime | Startup, shutdown, dependency injection, error handling |
| Event Bus | Fire-and-forget, request/response, priority dispatch |
| Service Registry | Service registration and resolution |
| Workspace Manager | Panel layout, tabs, resize, persistence |
| Scilab Runtime | Process spawn, JSON-RPC, command queue, variable marshalling |
| Project Manager | Create, open, save projects; `project.json` schema |
| File Explorer | Tree view, file operations, watch for changes |
| Storage Layer | SQLite database, file system access, emergency snapshots |

### Acceptance Criteria

- [ ] Application starts, initializes all services, connects to Scilab.
- [ ] User can create a project (name, location → `project.json` + directory structure).
- [ ] User can open a project and see the file tree.
- [ ] User can open files in editor tabs.
- [ ] Layout state persists across sessions.
- [ ] Scilab evaluation works through the command queue.
- [ ] Status bar shows connection status, project name, last saved.

---

## Sprint 2 — GUI Builder

**Goal:** A drag-and-drop GUI designer that generates Scilab code.

### Deliverables

| Component | Description |
|-----------|-------------|
| GUI Builder Module | Canvas, component palette, property inspector |
| Built-in Widgets | Button, Label, Text Field, Number Input, Checkbox, Dropdown, Plot, Table, Panel |
| Widget Runtime | Load, render, serialize, bind data |
| Code Generator | Generate Scilab `uicontrol` code from layout |
| Layout Manager | Save/load GUI layouts as JSON |
| Preview Mode | Render GUI without edit controls |

### Acceptance Criteria

- [ ] User can drag components from palette to canvas.
- [ ] User can select, move, resize, and delete components.
- [ ] Property inspector shows and edits component properties.
- [ ] Grid snapping and alignment guides work.
- [ ] User can save and load GUI layouts.
- [ ] Code generator produces valid Scilab code.
- [ ] Preview mode renders the GUI interactively.

---

## Sprint 3 — Visualization and Data

**Goal:** Import data, create charts, and visualize Scilab results.

### Deliverables

| Component | Description |
|-----------|-------------|
| Visualization Studio | Chart canvas, type selector, property panel |
| Chart Types | Line, Scatter, Bar, Heatmap |
| Data Studio | CSV/Excel import, preview table, column statistics |
| Data Pipeline | Import → Validate → Transform → Export flow |
| Transform Pipeline | Filter, sort, select, rename, aggregate, pivot |
| Export | PNG, SVG, JPEG image export |
| Scilab Integration | Charts bound to Scilab variables, live updates |

### Acceptance Criteria

- [ ] User can import CSV and Excel files.
- [ ] Data preview shows first rows with column types.
- [ ] Column statistics are computed automatically.
- [ ] User can create line, scatter, bar, and heatmap charts.
- [ ] Charts are interactive (tooltips, zoom, pan).
- [ ] Charts can be exported as PNG, SVG, JPEG.
- [ ] Charts can be bound to Scilab variables for live updates.
- [ ] Transform pipelines work (filter, sort, aggregate).

---

## Sprint 4 — Plugins and Marketplace

**Goal:** Extensible platform with a plugin ecosystem.

### Deliverables

| Component | Description |
|-----------|-------------|
| Plugin Runtime | Sandboxed JS execution, lifecycle management |
| Plugin SDK | Manifest schema, context API, permissions |
| Plugin Manager UI | Install, enable, disable, uninstall plugins |
| Widget SDK | Widget definition, property types, data binding |
| Marketplace Client | Browse, search, install plugins/widgets |
| Templates | Project templates for common workflows |
| Learning Center | Built-in examples and tutorials |

### Acceptance Criteria

- [ ] A third-party plugin can be installed and activated.
- [ ] Plugins run in sandboxed contexts with enforced permissions.
- [ ] Plugin health is monitored via heartbeats.
- [ ] Widget definitions are loaded and rendered on the canvas.
- [ ] Marketplace browser shows available plugins with categories.
- [ ] At least 5 built-in example projects are available.
- [ ] At least 3 project templates are available.

---

## Sprint 5 — Reports and Polish

**Goal:** Professional report generation and a polished user experience.

### Deliverables

| Component | Description |
|-----------|-------------|
| Report Generator | Block-based editor, template system |
| Report Blocks | Heading, Paragraph, Chart, Table, Image, Code, Divider, Page Break |
| Report Export | PDF, HTML generation |
| UI Design System | Typography, colors, spacing, animations, keyboard shortcuts |
| Responsive Layout | Breakpoints, panel collapse, mobile adaptation |
| Accessibility | Keyboard navigation, screen reader support, contrast |
| Performance | LTTB downsampling, virtual scrolling, memory budgets |
| Documentation | API reference, developer guide, deployment guide |

### Acceptance Criteria

- [ ] User can create reports with drag-and-drop blocks.
- [ ] Reports can include charts, tables, text, and images.
- [ ] PDF and HTML export work correctly.
- [ ] The UI is visually consistent across all modules.
- [ ] Keyboard shortcuts work everywhere.
- [ ] The application is responsive to window resizing.
- [ ] Performance budgets are met (cold start < 3s, chart render < 1s).
- [ ] All documentation is complete and accurate.

---

## Post-MVP Roadmap

### v0.2 — Extensibility

- Widget Marketplace (community-contributed widgets)
- Xcos Builder (visual block diagram editor)
- Lab Creator (interactive lab builder)
- Additional chart types (3D, Bode, Nyquist, Root Locus)

### v0.3 — Intelligence

- AI Assistant (context-aware coding help)
- Digital Twin Framework (real-time system modeling)
- Parameter Sweep (automated parameter studies)
- Dashboard Builder (real-time monitoring dashboards)

### v0.4 — Community

- Community Marketplace (full plugin ecosystem)
- Open Engineering Library (shared components and templates)
- Research Workspace (collaboration, versioning, reproducibility)

---

## Milestone Summary

| Sprint | Focus | Duration | Key Deliverable |
|--------|-------|----------|-----------------|
| 1 | Platform | 2 weeks | Working shell with Scilab integration |
| 2 | GUI | 2 weeks | Drag-and-drop GUI builder |
| 3 | Data + Viz | 2 weeks | Data import and chart creation |
| 4 | Plugins | 2 weeks | Extensible plugin ecosystem |
| 5 | Reports + Polish | 2 weeks | Professional reports and UX |
| **Total** | | **10 weeks** | **v0.1 release** |
