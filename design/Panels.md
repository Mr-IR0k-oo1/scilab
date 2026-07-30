# Panels

## Panel Types

| Type | Position | Default Size | Resize |
|------|----------|-------------|--------|
| Left Sidebar | Left | 250px | Yes (150–400px) |
| Right Sidebar | Right | 300px | Yes (200–500px) |
| Bottom Panel | Bottom | 200px | Yes (100–400px) |
| Editor Area | Center | flex: 1 | No (fills space) |

## Panel Header

```
┌─────────────────────────────────┐
│ [Icon] Panel Title     [—][×]  │
├─────────────────────────────────┤
│                                 │
│         Panel Content           │
│                                 │
└─────────────────────────────────┘
```

- Height: 32px.
- Background: `--ss-bg-secondary`.
- Contains: icon, title, collapse button, close button.
- Font: `--ss-text-sm`, weight 500.

## Panel Content

- Background: `--ss-bg-primary`.
- Overflow: auto (scrollable).
- Padding: `--ss-space-2` (8px).

## Panel Tabs

When a panel has multiple views:

```
┌─────────────────────────────────┐
│ [Console] [Output] [Problems]   │
├─────────────────────────────────┤
│                                 │
│         Active View             │
│                                 │
└─────────────────────────────────┘
```

- Tab height: 32px.
- Active tab: accent border bottom.
- Inactive tab: transparent border.

## Resize Handles

- Width: 4px (invisible until hovered).
- Hover color: `--ss-accent`.
- Cursor: `col-resize` (vertical), `row-resize` (horizontal).
- Double-click: reset to default size.

## Collapse Animation

- Duration: 200ms.
- Easing: ease-out.
- Panel slides out, content area expands.
- Collapse button rotates 180°.

## Rules

- Panels remember their size between sessions.
- Panels can be collapsed but not removed (v0.1).
- Panel content is independent of other panels.
- Panels refresh their content when activated.
