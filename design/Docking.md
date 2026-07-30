# Docking

## Panel Docking

Panels dock to the edges of the editor area.

### Dock Positions
| Position | Panel | Default |
|----------|-------|---------|
| Left | File Explorer, Search, Extensions | ✅ |
| Right | Properties, Widget Inspector | ✅ |
| Bottom | Console, Output, Problems | ✅ |
| Center | Editor | ✅ |

## Docking Behavior

### Drop Zones
When dragging a panel tab, drop zones appear:

```
┌──────────┬──────────────────────┬──────────┐
│          │       TOP            │          │
│  LEFT    ├──────────────────────┤  RIGHT   │
│          │       CENTER         │          │
│          ├──────────────────────┤          │
│          │       BOTTOM         │          │
└──────────┴──────────────────────┴──────────┘
```

- Drop zones highlight with accent border.
- Drop zone size: 80px from edge.
- Center drop: splits the editor area.

### Drag Behavior
- Drag the panel tab to undock.
- Drag to a drop zone to re-dock.
- Drag to another panel to tab alongside.
- Drag outside to create a floating window (v0.2+).

## Tab Stripping

Multiple panels can share a tab bar:

```
┌─────────────────────────────────┐
│ [Console] [Output] [Problems]   │
├─────────────────────────────────┤
│                                 │
│         Active View             │
│                                 │
└─────────────────────────────────┘
```

- Tabs are reorderable via drag.
- Middle-click closes a tab.
- Close button on each tab.
- Overflow: scroll with arrows.

## Split Views

The editor area can be split:

```
┌──────────────────┬───────────────┐
│                  │               │
│    Editor 1      │   Editor 2    │
│                  │               │
└──────────────────┴───────────────┘
```

- Split horizontally or vertically.
- Drag the divider to resize.
- Double-click divider to equalize.
- Maximum splits: 4 (v0.1).

## Panel Visibility

| Shortcut | Action |
|----------|--------|
| Ctrl+B | Toggle left sidebar |
| Ctrl+Shift+B | Toggle right sidebar |
| Ctrl+J | Toggle bottom panel |
| Ctrl+1..9 | Switch to panel 1..9 |

## Rules

- Panels remember their dock position.
- Panels can be undocked and re-docked.
- Split ratio persists between sessions.
- Minimum panel size: 150px (sidebar), 100px (bottom).
- Maximum panel size: 400px (sidebar), 400px (bottom).
