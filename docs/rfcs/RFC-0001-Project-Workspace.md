# RFC-0001: Project Workspace

| Field | Value |
|-------|-------|
| RFC | 0001 |
| Title | Project Workspace |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how Scilab Studio manages project files, directories, tabs, and the workspace UI.

## Motivation

Users need a predictable, fast way to navigate project files, edit multiple files simultaneously, and manage their workspace layout. The workspace is the primary surface of the application — everything else builds on it.

## Detailed Design

### Project Structure

A Scilab Studio project is a directory with a `.scstudio/project.json` file.

```
my-project/
├── .scstudio/
│   └── project.json
├── main.sce
├── utils/
│   └── helpers.sce
├── data/
│   └── measurements.csv
└── gui/
    └── main.gui.json
```

### project.json Schema

```json
{
  "name": "My Project",
  "version": "1.0.0",
  "created": "2025-01-15T10:00:00Z",
  "modified": "2025-01-15T10:00:00Z",
  "scilab_version": ">=7.0",
  "plugins": [],
  "settings": {},
  "templates": []
}
```

### File Explorer

The file explorer shows the project directory tree.

**Behavior:**
- Root is the project directory. Cannot navigate above it.
- Hidden files (dotfiles) are hidden by default. Toggle via settings.
- File icons are determined by extension.
- Right-click context menu: New File, New Folder, Rename, Delete, Open in System Explorer.
- Drag-and-drop files to reorder or move.
- Watch for external file system changes and refresh automatically.

**Sorting:**
- Folders first, then files alphabetically.
- No custom sorting in v0.1.

### Tab System

Tabs represent open files in the editor area.

**Behavior:**
- Click a file in the explorer to open it in a new tab.
- If the file is already open, switch to its tab.
- Tabs are reorderable via drag-and-drop.
- Middle-click closes a tab.
- Close button (×) on each tab.
- Dirty indicator (●) on tabs with unsaved changes.
- Tab overflow: horizontal scroll with scroll buttons.

**Tab Groups (v0.2+):**
- Split horizontally or vertically.
- Drag tabs between groups.
- Each group has independent scroll position.

### Status Bar

The status bar shows:

| Position | Content |
|----------|---------|
| Left | Current file path |
| Left | Line:Column of cursor |
| Right | Scilab version |
| Right | Plugin count |
| Right | Connection status |

### Command Palette

Ctrl+P / Cmd+P opens the command palette.

**Behavior:**
- Fuzzy search across files, commands, and settings.
- Arrow keys to navigate, Enter to select.
- Escape to close.
- Recent files shown first when empty.

### Auto-Save

- Auto-save is enabled by default with a 1-second debounce.
- Can be disabled in settings.
- Auto-save does not trigger Scilab execution.

## Alternatives Considered

1. **Monaco Editor integration**: More features but heavier. Chose simpler custom editor for v0.1.
2. **No project system**: Just open files. But projects provide context for Scilab execution and plugin configuration.

## Security Considerations

- Project files are read from the local file system only.
- No remote file access in v0.1.
- File watcher has rate limiting to prevent resource exhaustion.

## Testing Strategy

- Unit tests for project.json parsing.
- Integration tests for file explorer operations.
- Performance tests for large directories (1000+ files).
- UI tests for tab management.

## Rollout

Ships in v0.1 as the foundation of the application.
