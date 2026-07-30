# Component Library

## Buttons

### Primary Button
```html
<button class="ss-button ss-button--primary">Save</button>
```
- Background: `--ss-accent`
- Text: white
- Hover: lighten 10%
- Active: darken 5%

### Secondary Button
```html
<button class="ss-button ss-button--secondary">Cancel</button>
```
- Background: transparent
- Border: `--ss-border-strong`
- Text: `--ss-text-primary`

### Ghost Button
```html
<button class="ss-button ss-button--ghost">Close</button>
```
- Background: transparent
- No border
- Text: `--ss-text-secondary`

### Danger Button
```html
<button class="ss-button ss-button--danger">Delete</button>
```
- Background: `--ss-error`
- Text: white

### Button Sizes
| Size | Height | Padding | Font |
|------|--------|---------|------|
| `sm` | 24px | 8px 12px | `text-sm` |
| `md` | 32px | 8px 16px | `text-md` |
| `lg` | 40px | 12px 20px | `text-lg` |

## Inputs

### Text Input
```html
<input class="ss-input" type="text" placeholder="Enter value">
```

### Number Input
```html
<input class="ss-input ss-input--number" type="number" min="0" max="100">
```

### Select
```html
<select class="ss-select">
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

### Checkbox
```html
<label class="ss-checkbox">
  <input type="checkbox">
  <span class="ss-checkbox__mark"></span>
  <span class="ss-checkbox__label">Enable feature</span>
</label>
```

### Radio
```html
<label class="ss-radio">
  <input type="radio" name="group">
  <span class="ss-radio__mark"></span>
  <span class="ss-radio__label">Option 1</span>
</label>
```

## Cards

```html
<div class="ss-card">
  <div class="ss-card__header">Title</div>
  <div class="ss-card__body">Content</div>
  <div class="ss-card__footer">Actions</div>
</div>
```

## Badges

```html
<span class="ss-badge ss-badge--info">Info</span>
<span class="ss-badge ss-badge--success">Success</span>
<span class="ss-badge ss-badge--warning">Warning</span>
<span class="ss-badge ss-badge--error">Error</span>
```

## Tooltips

```html
<div class="ss-tooltip" data-tooltip="This is a tooltip">
  <span>Hover me</span>
</div>
```

## Progress

```html
<div class="ss-progress">
  <div class="ss-progress__bar" style="width: 60%"></div>
</div>
```

## Rules

- All components support both dark and light themes.
- All components are keyboard accessible.
- All components have hover, focus, active, and disabled states.
- Consistent border-radius: `--ss-radius-md` (4px).
- Consistent font sizes: use the type scale.
