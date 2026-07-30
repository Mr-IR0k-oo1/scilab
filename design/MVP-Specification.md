# MVP Specification

## What Ships

| # | Feature | What It Does | Done When |
|---|---------|-------------|-----------|
| 1 | **Workspace** | Main window, file explorer, tabs, status bar | Can open/edit/save files |
| 2 | **GUI Builder** | Drag-and-drop canvas, 9 widgets, property inspector | Can build and preview a GUI |
| 3 | **Visualization** | Line, scatter, bar, heatmap charts | Can render CSV data as charts |
| 4 | **Data Studio** | CSV import, data preview, column stats | Can import and inspect CSV |
| 5 | **Report Generator** | Block editor, PDF/HTML export | Can generate a report with charts |
| 6 | **Scilab Bridge** | Execute Scilab code, capture output | Can run .sce files and see results |
| 7 | **Project System** | Create/open/save projects | Can manage .scstudio projects |

## What's NOT in MVP

- Plugin system (v0.2)
- Widget marketplace (v0.2)
- AI assistant (v0.3)
- Digital twins (v0.3)
- Community marketplace (v0.4)
- Learning center (v0.2)
- Template gallery (v0.2)
- Xcos integration (v0.2)

## Success Test

A user can:
1. Create a new project from a blank template.
2. Write a Scilab script in the editor.
3. Run the script and see output in the console.
4. Import a CSV file.
5. Create a chart from the CSV data.
6. Build a simple GUI with buttons and labels.
7. Generate a PDF report with the chart.
8. Save the project and reopen it.

If all 8 steps work, the MVP is done.

## Timeline

| Week | Deliverable |
|------|-------------|
| 1-2 | Workspace shell, project system, file explorer |
| 3-4 | Code editor, Scilab bridge, console |
| 5-6 | GUI builder canvas, widget palette, property inspector |
| 7-8 | Visualization engine (4 chart types) |
| 9-10 | Data studio (CSV import), report generator |

## Out of Scope for MVP

- Custom widgets
- Plugin SDK
- Template marketplace
- Multi-platform testing (Linux only for MVP)
- Performance optimization
- Accessibility audit
