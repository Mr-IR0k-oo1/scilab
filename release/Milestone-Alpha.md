# Milestone: Alpha

## Goal

Demonstrate the core platform concept with a polished, working prototype.

## Scope

Deliver **only** these capabilities:

### 1. Core Runtime
- Event Bus
- Workspace Manager
- Project System
- Configuration
- Logging

### 2. Project Workspace
- File explorer with directory tree
- Tab-based editor with open/close/save
- Auto-save
- Status bar
- Command palette

### 3. Visual GUI Builder
- Drag-and-drop canvas
- 9 built-in components:
  - Button
  - Label
  - Text Field
  - Slider
  - Checkbox
  - Dropdown
  - Panel
  - Image
  - Table
- Property inspector
- Code generation
- Preview mode

### 4. Engineering Visualization Engine
- 4 chart types:
  - Line chart
  - Scatter chart
  - Bar chart
  - Heatmap
- Interactive zoom and pan
- Export to PNG, SVG, CSV
- Dark and light themes

### 5. Data Studio
- CSV import with auto-detection
- Excel import
- Data preview table
- Column statistics

### 6. Report Generator
- Block-based editor
- PDF export
- HTML export
- Embedded charts and tables

### 7. Scilab Integration
- JSON-RPC over stdin/stdout
- Process management
- Command execution
- Variable access

### 8. Example Projects
- Signal Processing Lab
- Control Systems Lab
- Data Analysis
- Numerical Methods

## Out of Scope (Future Milestones)

- Plugin system (v0.2)
- Widget Marketplace (v0.2)
- AI Assistant (v0.3)
- Digital Twin Framework (v0.3)
- Community Marketplace (v0.4)
- Learning Center (v0.2)

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Cold start | < 2 seconds |
| Project open | < 1 second |
| Chart render (1k points) | < 16ms |
| CSV import (10 MB) | < 2 seconds |
| All tests pass | 100% |
| Accessibility | WCAG 2.1 AA |
| Platforms | Linux, macOS, Windows |

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Foundation | 2 weeks | Core runtime, project system |
| Workspace | 2 weeks | File explorer, editor, tabs |
| GUI Builder | 3 weeks | Canvas, components, properties |
| Visualization | 2 weeks | 4 chart types, export |
| Data Studio | 2 weeks | CSV/Excel import, preview |
| Report Generator | 2 weeks | Block editor, export |
| Scilab Integration | 2 weeks | JSON-RPC, process management |
| Polish | 2 weeks | Testing, bug fixes, documentation |
| **Total** | **10 weeks** | **Alpha release** |

## What Judges See

A polished application that:
1. Opens a project with one click.
2. Builds a GUI by dragging components.
3. Imports data from CSV.
4. Visualizes data with interactive charts.
5. Generates a report with embedded charts.
6. All in a modern, accessible interface.

That demonstrates the platform concept. The Plugin Marketplace, AI Assistant, and Digital Twin Framework can remain in the roadmap.
