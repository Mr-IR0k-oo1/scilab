# Color System

## Dark Theme (Default)

```css
:root {
  /* Backgrounds */
  --ss-bg-primary: #1e1e1e;
  --ss-bg-secondary: #252526;
  --ss-bg-tertiary: #2d2d2d;
  --ss-bg-hover: #383838;
  --ss-bg-active: #37373d;
  --ss-bg-selected: #04395e;

  /* Text */
  --ss-text-primary: #e0e0e0;
  --ss-text-secondary: #a0a0a0;
  --ss-text-muted: #666666;
  --ss-text-disabled: #555555;

  /* Accent */
  --ss-accent: #4a9eff;
  --ss-accent-hover: #6ab4ff;
  --ss-accent-active: #3d8be0;

  /* Borders */
  --ss-border: #404040;
  --ss-border-strong: #555555;
  --ss-border-subtle: #333333;

  /* Status */
  --ss-error: #f44336;
  --ss-error-bg: rgba(244, 67, 54, 0.1);
  --ss-warning: #ff9800;
  --ss-warning-bg: rgba(255, 152, 0, 0.1);
  --ss-success: #4CAF50;
  --ss-success-bg: rgba(76, 175, 80, 0.1);
  --ss-info: #2196F3;
  --ss-info-bg: rgba(33, 150, 243, 0.1);

  /* Shadows */
  --ss-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --ss-shadow-md: 0 2px 4px rgba(0, 0, 0, 0.4);
  --ss-shadow-lg: 0 4px 8px rgba(0, 0, 0, 0.5);

  /* Radius */
  --ss-radius-sm: 2px;
  --ss-radius-md: 4px;
  --ss-radius-lg: 8px;
  --ss-radius-full: 9999px;
}
```

## Light Theme

```css
:root {
  --ss-bg-primary: #ffffff;
  --ss-bg-secondary: #f5f5f5;
  --ss-bg-tertiary: #e8e8e8;
  --ss-bg-hover: #e0e0e0;
  --ss-bg-active: #d5d5d5;
  --ss-bg-selected: #c8e6ff;

  --ss-text-primary: #333333;
  --ss-text-secondary: #666666;
  --ss-text-muted: #999999;
  --ss-text-disabled: #cccccc;

  --ss-accent: #2196F3;
  --ss-accent-hover: #1976D2;
  --ss-accent-active: #1565C0;

  --ss-border: #e0e0e0;
  --ss-border-strong: #cccccc;
  --ss-border-subtle: #f0f0f0;

  --ss-error: #d32f2f;
  --ss-error-bg: rgba(211, 47, 47, 0.05);
  --ss-warning: #f57c00;
  --ss-warning-bg: rgba(245, 124, 0, 0.05);
  --ss-success: #388e3c;
  --ss-success-bg: rgba(56, 142, 60, 0.05);
  --ss-info: #1976D2;
  --ss-info-bg: rgba(25, 118, 210, 0.05);

  --ss-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.08);
  --ss-shadow-md: 0 2px 4px rgba(0, 0, 0, 0.12);
  --ss-shadow-lg: 0 4px 8px rgba(0, 0, 0, 0.16);
}
```

## Chart Colors

### Dark Theme
```json
["#4a9eff", "#ff6384", "#4caf50", "#ff9800", "#9c27b0", "#00bcd4", "#e91e63", "#8bc34a"]
```

### Light Theme
```json
["#2196f3", "#e91e63", "#4caf50", "#ff9800", "#9c27b0", "#00bcd4", "#f44336", "#8bc34a"]
```

## Usage Rules

- Never hard-code colors. Always use CSS custom properties.
- Status colors (error, warning, success, info) are consistent across the application.
- Accent color is used for interactive elements, focus states, and links.
- Text colors ensure WCAG 2.1 AA contrast ratios.
