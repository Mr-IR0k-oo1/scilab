# Spacing

## Base Unit

4px. All spacing is a multiple of 4.

## Spacing Scale

| Token | Value | Use |
|-------|-------|-----|
| `space-0` | 0px | No spacing |
| `space-1` | 4px | Tight gaps (icon to text) |
| `space-2` | 8px | Small gaps (form fields) |
| `space-3` | 12px | Medium gaps (list items) |
| `space-4` | 16px | Default gap (between sections) |
| `space-5` | 20px | Large gaps (panel padding) |
| `space-6` | 24px | Extra large gaps (page margins) |
| `space-8` | 32px | Section spacing |
| `space-10` | 40px | Page section spacing |
| `space-12` | 48px | Large section spacing |

## Layout Spacing

| Context | Value |
|---------|-------|
| Between form fields | `space-3` (12px) |
| Between sections | `space-6` (24px) |
| Panel padding | `space-4` (16px) |
| Page margin | `space-6` (24px) |
| Dialog padding | `space-5` (20px) |
| Toolbar padding | `space-2` (8px) |
| Status bar padding | `space-2` (8px) |

## Margin/Padding

```css
/* Component padding */
.ss-panel {
  padding: var(--ss-space-4);
}

/* Section spacing */
.ss-section + .ss-section {
  margin-top: var(--ss-space-6);
}

/* Form field spacing */
.ss-form-group + .ss-form-group {
  margin-top: var(--ss-space-3);
}
```

## Rules

- Never use arbitrary pixel values. Always use the spacing scale.
- Consistent spacing creates visual rhythm.
- Tighter spacing for dense UI (data tables).
- Looser spacing for content areas (documentation).
