# Layout Rules

## Application Layout

```
┌─────────────────────────────────────────────┐
│ Title Bar (32px)                            │
├──────────┬──────────────────────┬───────────┤
│          │                      │           │
│  Left    │     Editor Area      │  Right    │
│  Sidebar │     (flex: 1)        │  Sidebar  │
│  (250px) │                      │  (300px)  │
│          │                      │           │
├──────────┴──────────────────────┴───────────┤
│ Bottom Panel (200px, collapsible)           │
├─────────────────────────────────────────────┤
│ Status Bar (24px)                           │
└─────────────────────────────────────────────┘
```

## Panel Constraints

| Panel | Min | Max | Default |
|-------|-----|-----|---------|
| Left sidebar | 150px | 400px | 250px |
| Right sidebar | 200px | 500px | 300px |
| Bottom panel | 100px | 400px | 200px |
| Title bar | — | — | 32px |
| Status bar | — | — | 24px |

## Resize Behavior

- Drag handle is 4px wide, invisible until hovered.
- Handle turns accent color on hover.
- Double-click handle resets to default size.
- Minimum sizes are enforced. Cannot drag below min.

## Breakpoints

| Width | Behavior |
|-------|----------|
| ≥ 1400px | Full layout |
| 1000–1399px | Left sidebar collapses to icon rail (48px) |
| 600–999px | Both sidebars collapse. Editor fills width. |
| < 600px | Graceful degradation |

## Panel Header

- Height: 32px.
- Font: `--ss-text-sm`, weight 500.
- Contains: title, collapse button, module-specific buttons.
- Background: `--ss-bg-secondary`.

## Tab Bar

- Height: 35px.
- Tabs are reorderable via drag-and-drop.
- Close button on each tab (middle-click also closes).
- Dirty indicator (dot) on unsaved tabs.
- Scrollable when tabs exceed available width.

## Spacing

4px base grid. All spacing is a multiple of 4.

| Token | Value | Use |
|-------|-------|-----|
| xs | 4px | Tight gaps |
| sm | 8px | Small gaps |
| md | 16px | Default gap |
| lg | 24px | Large gaps |
| xl | 32px | Page margins |
