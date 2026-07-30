# Toolbars

## Main Toolbar

```
┌─────────────────────────────────────────────────┐
│ [New] [Open] [Save] | [Undo] [Redo] | [Run] ▶  │
└─────────────────────────────────────────────────┘
```

- Height: 32px.
- Background: `--ss-bg-secondary`.
- Border bottom: 1px `--ss-border`.
- Buttons: icon-only (20×20 icon, 32×32 button area).
- Separator: 1px vertical line between groups.

## Toolbar Button States

| State | Appearance |
|-------|-----------|
| Default | Icon color: `--ss-text-secondary` |
| Hover | Icon color: `--ss-text-primary`, background: `--ss-bg-hover` |
| Active | Icon color: `--ss-accent`, background: `--ss-bg-active` |
| Disabled | Icon color: `--ss-text-muted`, no interaction |

## Toolbar Button with Label

```
┌──────────┐
│ [▶] Run  │
└──────────┘
```

- Icon + text label.
- Used for primary actions.
- Height: 32px.

## Toolbar Separator

```css
.ss-toolbar__separator {
  width: 1px;
  height: 16px;
  background: var(--ss-border);
  margin: 0 4px;
}
```

## Toolbar Group

```html
<div class="ss-toolbar__group">
  <!-- buttons -->
</div>
```

- Groups related buttons.
- Separated by separators from other groups.

## Context Toolbar

Appears when a specific element is selected:

```
┌─────────────────────────────────────────────────┐
│ Button Properties: [Label:_________] [Color: ▼] │
└─────────────────────────────────────────────────┘
```

- Height: 32px.
- Background: `--ss-bg-tertiary`.
- Shows properties of the selected element.

## Rules

- Icon-only buttons in toolbars (no text unless primary action).
- Consistent button size: 32×32.
- Consistent icon size: 20×20.
- Keyboard accessible: Tab to navigate, Enter/Space to activate.
- Tooltip on hover (delay: 500ms).
- No more than 15 buttons per toolbar section.
