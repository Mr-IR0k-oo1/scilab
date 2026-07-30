# RFC-0009: Theme System

| Field | Value |
|-------|-------|
| RFC | 0009 |
| Title | Theme System |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how themes are defined, applied, and extended.

## Motivation

A consistent visual language is essential for a professional application. The theme system ensures all components share the same colors, typography, and spacing.

## Detailed Design

### Theme Structure

```json
{
  "name": "Dark",
  "type": "dark",
  "colors": {
    "background": {
      "primary": "#1e1e1e",
      "secondary": "#252526",
      "tertiary": "#2d2d2d"
    },
    "text": {
      "primary": "#e0e0e0",
      "secondary": "#a0a0a0",
      "muted": "#666666"
    },
    "accent": "#4a9eff",
    "border": "#404040",
    "status": {
      "error": "#f44336",
      "warning": "#ff9800",
      "success": "#4CAF50",
      "info": "#2196F3"
    }
  },
  "typography": {
    "fontFamily": "Inter, system-ui, sans-serif",
    "sizes": {
      "xs": "11px",
      "sm": "12px",
      "md": "13px",
      "lg": "14px",
      "xl": "16px"
    },
    "weights": {
      "normal": 400,
      "medium": 500,
      "semibold": 600
    }
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "radius": {
    "sm": "2px",
    "md": "4px",
    "lg": "8px"
  },
  "shadows": {
    "sm": "0 1px 2px rgba(0,0,0,0.3)",
    "md": "0 2px 4px rgba(0,0,0,0.4)",
    "lg": "0 4px 8px rgba(0,0,0,0.5)"
  }
}
```

### Built-in Themes

| Theme | Type | Description |
|-------|------|-------------|
| Dark | dark | Default theme, VS Code-inspired |
| Light | light | Clean, high-contrast |
| System | — | Follows OS preference |

### Theme Application

Themes are applied via CSS custom properties:

```css
:root {
  --ss-bg-primary: var(--theme-background-primary);
  --ss-text-primary: var(--theme-text-primary);
  --ss-accent: var(--theme-accent);
  /* ... */
}
```

### Custom Themes

Users can create custom themes:

```json
{
  "name": "My Theme",
  "extends": "Dark",
  "colors": {
    "accent": "#ff6384"
  }
}
```

Theme inheritance:
1. Start with base theme (Dark or Light).
2. Override specified properties.
3. Merge with platform defaults for missing properties.

### Theme Marketplace (v0.3+)

Community themes can be shared through the Theme Marketplace:

- Theme manifest includes preview images.
- Themes are reviewed before publication.
- Users can fork and modify published themes.

### Chart Theme Integration

Charts inherit theme colors automatically:

```typescript
const chartColors = [
  theme.colors.accent,
  theme.colors.status.error,
  theme.colors.status.success,
  theme.colors.status.warning,
  // ... more colors from theme
];
```

### High Contrast Mode

All themes support high contrast mode:

- Text contrast ratio ≥ 4.5:1 for normal text.
- Text contrast ratio ≥ 3:1 for large text.
- Focus indicators use 2px solid accent color.
- Borders are more visible.

## Alternatives Considered

1. **Hard-coded colors**: Simpler but no customization.
2. **CSS-in-JS**: Runtime overhead. Chose CSS custom properties.
3. **SCSS variables**: Build-time only. Chose runtime CSS properties.

## Security Considerations

- Custom themes are loaded from local files only.
- Theme files are JSON, not executable code.
- Theme validation prevents injection of malicious CSS.

## Testing Strategy

- Visual regression tests for each built-in theme.
- Accessibility tests for contrast ratios.
- UI tests for theme switching.
- Performance tests for theme application (should be < 100ms).

## Rollout

- v0.1: Dark and Light themes.
- v0.2: System theme, custom themes.
- v0.3: Theme Marketplace.
