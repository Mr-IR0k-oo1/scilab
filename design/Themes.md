# Themes

## Overview

Scilab Studio supports three theme modes:

| Mode | Description |
|------|-------------|
| Dark | Default. VS Code-inspired. |
| Light | Clean, high-contrast. |
| System | Follows OS preference. |

## Theme Structure

A theme defines colors, typography, spacing, and component styles.

```json
{
  "name": "Dark",
  "type": "dark",
  "colors": { /* ... */ },
  "typography": { /* ... */ },
  "spacing": { /* ... */ },
  "components": { /* ... */ }
}
```

## Color Tokens

### Backgrounds
| Token | Dark | Light |
|-------|------|-------|
| `--ss-bg-primary` | #1e1e1e | #ffffff |
| `--ss-bg-secondary` | #252526 | #f5f5f5 |
| `--ss-bg-tertiary` | #2d2d2d | #e8e8e8 |
| `--ss-bg-hover` | #383838 | #e0e0e0 |
| `--ss-bg-active` | #37373d | #d5d5d5 |
| `--ss-bg-selected` | #04395e | #c8e6ff |

### Text
| Token | Dark | Light |
|-------|------|-------|
| `--ss-text-primary` | #e0e0e0 | #333333 |
| `--ss-text-secondary` | #a0a0a0 | #666666 |
| `--ss-text-muted` | #666666 | #999999 |

### Accent
| Token | Dark | Light |
|-------|------|-------|
| `--ss-accent` | #4a9eff | #2196f3 |
| `--ss-accent-hover` | #6ab4ff | #1976d2 |

### Status
| Token | Dark | Light |
|-------|------|-------|
| `--ss-error` | #f44336 | #d32f2f |
| `--ss-warning` | #ff9800 | #f57c00 |
| `--ss-success` | #4caf50 | #388e3c |
| `--ss-info` | #2196f3 | #1976d2 |

### Borders
| Token | Dark | Light |
|-------|------|-------|
| `--ss-border` | #404040 | #e0e0e0 |
| `--ss-border-strong` | #555555 | #cccccc |

## Custom Themes

Users can create custom themes:

```json
{
  "name": "Ocean",
  "extends": "Dark",
  "colors": {
    "accent": "#00bcd4",
    "bg-primary": "#0d1117",
    "bg-secondary": "#161b22"
  }
}
```

### Inheritance
1. Start with base theme (Dark or Light).
2. Override specified properties.
3. Missing properties fall back to base.

## Chart Theme

Charts inherit theme colors:

```json
{
  "chart": {
    "colors": ["#4a9eff", "#ff6384", "#4caf50", "#ff9800"],
    "background": "transparent",
    "grid": "#404040",
    "text": "#a0a0a0"
  }
}
```

## Accessibility

- All themes meet WCAG 2.1 AA contrast ratios.
- High contrast mode available for all themes.
- Focus indicators visible in all themes.

## Rules

- Never hard-code colors. Always use CSS custom properties.
- Test all features in both dark and light themes.
- Chart colors must be readable in both themes.
- Custom themes are validated before application.
