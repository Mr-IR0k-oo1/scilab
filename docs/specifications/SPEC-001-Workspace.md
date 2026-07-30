# SPEC-001 — Workspace

## Purpose

Provide the foundational shell that every other module inhabits. The Workspace manages project files, editor layout, panel arrangement, and session state.

---

## Components

### Title Bar
- Application name and project name.
- Window controls (minimize, maximize, close).
- Menu bar trigger on Linux/Windows; native on macOS.

### Menu Bar
- File (New Project, Open Project, Save, Recent, Exit)
- Edit (Undo, Redo, Cut, Copy, Paste, Find, Replace)
- View (Toggle Panels, Zoom, Layouts)
- Project (Settings, Plugins, Templates)
- Scilab (Restart Engine, Abort, Clear Console)
- Help (Docs, Learning Center, About)

### Left Sidebar
- File Explorer (tree view of project directory)
- Panel tabs for registered modules (switchable)
- Resize handle (150–400px range)
- Collapse to icon rail on narrow windows

### Editor Area
- Tab bar with reorderable, closable tabs.
- Each tab hosts one editor component (code, data preview, GUI canvas, chart, report).
- Dirty indicator on unsaved tabs.
- Pin tabs to keep them on the left.

### Right Sidebar
- Property Inspector (context-sensitive for selected element)
- Module-specific panels (chart properties, widget properties)
- Resize handle (200–500px range)
- Collapsible

### Bottom Panel
- Toggle with Ctrl+J / Cmd+J.
- Tabs: Console, Variables, Data Pipeline, Plugin panels.
- Resize handle (100–400px range).
- Hidden by default.

### Status Bar
- Scilab connection status (Connected / Disconnected / Connecting).
- Current project name.
- Cursor position in active editor (line:column).
- Last saved timestamp.

---

## Behavior

### Project Lifecycle
1. **Create:** User provides name, location, optional description. Platform generates `project.json` + directory structure.
2. **Open:** User selects from recent list or filesystem. Previous layout state restored.
3. **Save:** Auto-save on significant actions. Manual save with Ctrl+S / Cmd+S.

### File Operations
- Create file (with template: blank, Scilab script, data file).
- Create folder.
- Rename (with confirmation if referenced elsewhere).
- Delete (with confirmation).
- Move (drag-and-drop within tree).
- Copy path.

### Layout Persistence
- Panel sizes, visibility, and active tabs are saved to `project.json` on close.
- Layout restored on open.
- Users can save named layouts and switch between them.

### Tab Management
- Open: double-click file in explorer, or programmatic.
- Close: close button, middle-click, Ctrl+W / Cmd+W.
- Reorder: drag-and-drop.
- Pin: right-click → Pin (stays on left).
- Switch: Ctrl+Tab / Ctrl+Shift+Tab, or click.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Left sidebar default width | 250px |
| Left sidebar min/max | 150–400px |
| Right sidebar default width | 300px |
| Right sidebar min/max | 200–500px |
| Bottom panel default height | 200px |
| Bottom panel min/max | 100–400px |
| Max open tabs | 50 |
| Auto-save interval | On significant action (debounced 2s) |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Layout file corrupt | Fall back to default layout, notify user |
| Tab component not found | Show placeholder with error message |
| File locked by another process | Show error, offer retry |
| Project directory deleted externally | Show "Project not found" dialog, remove from recents |

---

## Extension Points

- Modules register panels in any sidebar position.
- Modules register tabs in the bottom panel.
- Custom editor components can be registered for specific file types.
- Layout serialization can be extended with new formats.
