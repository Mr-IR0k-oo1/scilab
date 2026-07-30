# User Stories — Student

## US-S01: Create My First Project
> I want to create a project in two clicks so I can start working immediately.

**Acceptance Criteria:**
- File → New Project opens a dialog.
- User enters name and selects location.
- `project.json` and directory structure are created.
- Project opens in the workspace.

---

## US-S02: Drag Widgets Instead of Writing GUI Code
> I want to design a GUI by dragging components, not by writing `uicontrol` code.

**Acceptance Criteria:**
- Widget appears on canvas immediately after drag.
- Can resize with handles.
- Can edit properties in the inspector.
- Can save the layout as a JSON file.
- Can generate valid Scilab code from the layout.

---

## US-S03: Import My CSV Data
> I want to import a CSV file and see my data in a table.

**Acceptance Criteria:**
- File → Import Data opens a file picker.
- CSV is parsed with correct column types.
- Data preview shows first rows in a spreadsheet view.
- Column statistics (min, max, mean) are computed.
- Data is available in the Data Studio panel.

---

## US-S04: Create a Chart from My Data
> I want to visualize my data as a chart without writing Scilab plot code.

**Acceptance Criteria:**
- User selects chart type (line, scatter, bar, heatmap).
- User selects data source (imported dataset or Scilab variable).
- Chart renders in the Visualization Studio panel.
- Chart is interactive (tooltips on hover).
- Chart can be exported as PNG.

---

## US-S05: Run My Scilab Script
> I want to write a Scilab script and run it from the editor.

**Acceptance Criteria:**
- User writes code in the editor tab.
- Press F5 or click "Run" to execute.
- Output appears in the console panel.
- Errors are shown inline in the editor.
- Results are available in the variable explorer.

---

## US-S06: Save and Reopen My Work
> I want my project to save automatically so I don't lose work.

**Acceptance Criteria:**
- Auto-save triggers on significant actions.
- Ctrl+S / Cmd+S saves manually.
- Last saved timestamp shown in status bar.
- On reopen, all files, layouts, and settings are restored.

---

## US-S07: Learn Scilab Interactively
> I want to learn Scilab by doing examples, not just reading docs.

**Acceptance Criteria:**
- Learning Center is accessible from Help menu.
- Examples are categorized by topic and difficulty.
- Each example has a description, prerequisites, and "Open Example" button.
- Tutorials guide step-by-step with validation.
- Scilab function reference is searchable.

---

## US-S08: Use a Template to Start
> I want to start from a template so I don't set up everything from scratch.

**Acceptance Criteria:**
- File → New from Template shows available templates.
- Templates are categorized (signal processing, control systems, etc.).
- Selecting a template creates a pre-configured project.
- Template includes example scripts, data, and visualizations.
