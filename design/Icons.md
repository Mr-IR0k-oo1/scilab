# Icons

## System

Scilab Studio uses Lucide icons (MIT license). Icons are SVG-based, rendered inline.

## Sizes

| Size | Dimensions | Use |
|------|-----------|-----|
| `icon-xs` | 12×12 | Inline indicators, badges |
| `icon-sm` | 16×16 | Menu items, tree view, list items |
| `icon-md` | 20×20 | Toolbar buttons, panel tabs |
| `icon-lg` | 24×24 | Sidebar navigation, empty states |
| `icon-xl` | 32×32 | Welcome screen, hero icons |

## Colors

Icons inherit the text color of their parent element.

```css
/* Default */
.ss-icon {
  color: inherit;
}

/* Active/selected */
.ss-icon--active {
  color: var(--ss-accent);
}

/* Disabled */
.ss-icon--disabled {
  color: var(--ss-text-secondary);
  opacity: 0.5;
}
```

## Core Icon Set

### Navigation
`arrow-left`, `arrow-right`, `arrow-up`, `arrow-down`, `chevron-right`, `chevron-down`, `menu`, `external-link`

### Files
`file`, `file-text`, `file-code`, `file-csv`, `file-image`, `folder`, `folder-open`, `save`, `download`, `upload`

### Actions
`plus`, `minus`, `x`, `check`, `search`, `refresh`, `copy`, `clipboard`, `trash-2`, `edit-3`, `pencil`

### Scilab
`play`, `square`, `terminal`, `code`, `variable`, `function`, `calculator`, `sigma`

### Visualization
`bar-chart-2`, `line-chart`, `pie-chart`, `scatter-chart`, `activity`, `trending-up`, `trending-down`

### UI
`settings`, `sliders`, `layers`, `grid`, `maximize-2`, `minimize-2`, `move`, `grip-vertical`, `eye`, `eye-off`

### Status
`alert-circle`, `alert-triangle`, `check-circle`, `x-circle`, `info`, `help-circle`

## Usage

```html
<!-- Inline icon -->
<span class="ss-icon ss-icon-sm">
  <!-- SVG content -->
</span>

<!-- Icon button -->
<button class="ss-icon-button">
  <span class="ss-icon ss-icon-md"><!-- SVG --></span>
</button>

<!-- Icon with text -->
<span class="ss-icon-text">
  <span class="ss-icon ss-icon-sm"><!-- SVG --></span>
  <span>Label</span>
</span>
```

## Rules

- Icons always have text labels in menus and toolbars.
- Exception: compact toolbar buttons (24×24 area).
- No decorative icons. Every icon communicates meaning.
- Consistent stroke width: 1.5px.
- Consistent style: outline (not filled).
