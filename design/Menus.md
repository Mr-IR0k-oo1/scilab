# Menus

## Main Menu

```
File  Edit  View  Run  Project  Plugins  Help
```

- Height: 24px (not visible on macOS — native menu bar).
- Background: `--ss-bg-secondary`.
- Font: `--ss-text-md`.

## Menu Items

```
┌─────────────────────────────────────┐
│ [icon] Label            Ctrl+S  ▶  │
│ [icon] Label            Ctrl+Z     │
│ ─────────────────────────────────── │
│ [icon] Label                       │
│ [icon] Label            Ctrl+N     │
└─────────────────────────────────────┘
```

### Item Properties
| Property | Description |
|----------|-------------|
| Icon | Optional 16×16 icon |
| Label | Text label |
| Shortcut | Keyboard shortcut (right-aligned) |
| Disabled | Grayed out, no interaction |
| Checked | Checkmark indicator |

### Item States
| State | Appearance |
|-------|-----------|
| Default | Text: `--ss-text-primary` |
| Hover | Background: `--ss-bg-hover` |
| Active | Background: `--ss-bg-active` |
| Disabled | Text: `--ss-text-muted` |

## Separator

```
── ── ── ── ── ── ── ── ── ── ── ──
```

- 1px horizontal line.
- Groups related menu items.

## Submenu

```
┌─────────────────────────────────────┐
│ Recent Files                   ▶   │
│ ┌─────────────────────────────────┐ │
│ │ [📄] main.sce           Ctrl+1 │ │
│ │ [📄] analysis.sce       Ctrl+2 │ │
│ │ [📄] data.csv           Ctrl+3 │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

- Opens on hover (delay: 200ms).
- Opens on click.
- Closes when mouse leaves.
- Arrow indicator (▶) on the right.

## Context Menu

```
┌─────────────────────────────────────┐
│ [📄] Open                          │
│ [📋] Copy                Ctrl+C    │
│ [✂️] Cut                 Ctrl+X    │
│ ─────────────────────────────────── │
│ [🗑️] Delete              Del      │
│ [✏️] Rename              F2       │
│ ─────────────────────────────────── │
│ [📁] Open in System Explorer       │
└─────────────────────────────────────┘
```

- Opens on right-click.
- Opens on Shift+F10.
- Items are context-sensitive.
- Position: at cursor or near cursor (if near edge).

## Keyboard Menu

- Alt activates the menu bar.
- Arrow keys navigate.
- Enter selects.
- Escape closes.
- Type-ahead search for item labels.

## Rules

- Consistent menu structure across the application.
- Destructive actions at the bottom, separated by a line.
- Keyboard shortcuts are consistent with VS Code conventions.
- Menus close when clicking outside.
- Maximum menu height: 400px (scrollable).
- Icons are optional but recommended for frequently-used items.
