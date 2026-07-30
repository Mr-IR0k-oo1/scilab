# Windows

## Main Window

```
┌─────────────────────────────────────────────────┐
│ Title Bar (32px)                                │
│ [icon] Scilab Studio - Project Name  [—][□][×]  │
├──────────┬──────────────────────┬───────────────┤
│          │                      │               │
│  Left    │     Editor Area      │  Right        │
│  Sidebar │     (flex: 1)        │  Sidebar      │
│  (250px) │                      │  (300px)      │
│          │                      │               │
│          │                      │               │
│          │                      │               │
├──────────┴──────────────────────┴───────────────┤
│ Bottom Panel (200px, collapsible)               │
│ [Console] [Output] [Problems] [Terminal]        │
├─────────────────────────────────────────────────┤
│ Status Bar (24px)                               │
│ main.sce | Ln 42, Col 15 | Scilab 7.0 | ● 2    │
└─────────────────────────────────────────────────┘
```

## Window States

| State | Description |
|-------|-------------|
| Normal | Default size and position |
| Minimized | Hidden from view |
| Maximized | Fills screen |
| Fullscreen | No title bar or status bar |

## Title Bar

- Height: 32px.
- Background: `--ss-bg-secondary`.
- Contains: app icon, project name, window controls.
- Draggable (except on controls).
- Double-click toggles maximize.

## Window Controls

| Control | Action |
|---------|--------|
| Minimize (—) | Minimize window |
| Maximize (□) | Toggle maximize/restore |
| Close (×) | Close window |

## Resize

- Drag window edges to resize.
- Minimum size: 800×600.
- Resize handle: 4px invisible area at edges.

## Rules

- Window remembers size and position between sessions.
- Title bar matches the theme.
- Window controls follow OS conventions.
- No custom title bar on macOS (native traffic lights).
