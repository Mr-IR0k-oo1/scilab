# 29 — UI Design System

Almost every hackathon ignores this. Scilab Studio does not. The entire application should feel like one product.

---

## 1. Design Principles

1. **Consistent** — Every screen uses the same spacing, typography, colors, and interaction patterns.
2. **Accessible** — WCAG 2.1 AA compliance. Keyboard navigable. Screen reader friendly.
3. **Responsive** — Adapts to window sizes without breaking.
4. **Dark-first** — Dark theme is the default. Light theme is available.
5. **Minimal chrome** — Content is the focus. UI elements recede until needed.

---

## 2. Spacing

A 4px base grid. All spacing is a multiple of 4.

| Token | Value | Use |
|-------|-------|-----|
| `--ss-space-xs` | 4px | Tight gaps (icon to text) |
| `--ss-space-sm` | 8px | Small gaps (related items) |
| `--ss-space-md` | 16px | Default gap (between sections) |
| `--ss-space-lg` | 24px | Large gaps (major sections) |
| `--ss-space-xl` | 32px | Page margins |
| `--ss-space-2xl` | 48px | Section separators |

### Component Spacing

| Component | Internal Padding | Gap to Neighbors |
|-----------|-----------------|------------------|
| Button | 12px vertical, 16px horizontal | 8px |
| Input field | 8px vertical, 12px horizontal | 8px |
| Card | 16px all sides | 16px |
| Panel section | 16px all sides | 16px between sections |
| Menu item | 8px vertical, 12px horizontal | 0 (stacked) |
| Toolbar | 8px vertical, 12px horizontal | 4px between items |

---

## 3. Typography

### Font Stack

```css
--ss-font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
--ss-font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Type Scale

| Token | Size | Weight | Line Height | Use |
|-------|------|--------|-------------|-----|
| `--ss-text-xs` | 11px | 400 | 16px | Captions, helper text |
| `--ss-text-sm` | 12px | 400 | 16px | Secondary text, labels |
| `--ss-text-base` | 14px | 400 | 20px | Body text, UI labels |
| `--ss-text-md` | 14px | 500 | 20px | Emphasized body text |
| `--ss-text-lg` | 16px | 500 | 24px | Section headers |
| `--ss-text-xl` | 20px | 600 | 28px | Panel titles |
| `--ss-text-2xl` | 24px | 600 | 32px | Page titles |
| `--ss-text-3xl` | 32px | 700 | 40px | Hero text (welcome screen) |

### Code Typography

All code, Scilab scripts, variable names, and file paths use the mono font at `--ss-text-base` (14px).

---

## 4. Icons

### Icon System

Scilab Studio uses a custom icon set based on Lucide icons (MIT licensed). Icons are rendered as SVG inline.

### Icon Sizes

| Size | Dimensions | Use |
|------|-----------|-----|
| `xs` | 12×12 | Inline indicators |
| `sm` | 16×16 | Menu items, tree view |
| `md` | 20×20 | Toolbar buttons, panel tabs |
| `lg` | 24×24 | Sidebar navigation |
| `xl` | 32×32 | Welcome screen, empty states |

### Icon Colors

Icons inherit the text color of their parent. Active/selected icons use `--ss-accent`. Disabled icons use `--ss-text-secondary` at 50% opacity.

---

## 5. Colors

### Dark Theme (default)

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

### Light Theme

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

---

## 6. Component Behavior

### Buttons

| State | Visual |
|-------|--------|
| Default | Border + text color |
| Hover | Background lightens, cursor pointer |
| Active | Background darkens, scale 0.98 |
| Disabled | 50% opacity, cursor not-allowed |
| Loading | Spinner replaces text, disabled |

### Input Fields

| State | Visual |
|-------|--------|
| Default | Border, no background |
| Focus | Border turns accent color, 2px ring |
| Error | Border turns error color, helper text below |
| Disabled | 50% opacity, background matches disabled bg |

### Panels

- Resizable via drag handle (4px wide, invisible until hovered).
- Drag handle turns accent color on hover.
- Collapse button in panel header (chevron icon).
- Panel header: 32px height, font `--ss-text-sm`, weight 500.

### Tables

- Header row: `--ss-bg-tertiary`, font weight 600.
- Alternating rows: `--ss-bg-primary` / `--ss-bg-secondary`.
- Hover row: `--ss-bg-hover`.
- Selected row: `--ss-bg-selected`.
- Sortable columns: click header to sort, arrow icon indicates direction.

---

## 7. Animations

### Duration

| Token | Value | Use |
|-------|-------|-----|
| `--ss-duration-fast` | 100ms | Button press, toggle |
| `--ss-duration-normal` | 200ms | Panel resize, tab switch |
| `--ss-duration-slow` | 300ms | Modal open/close, notification slide |

### Easing

| Token | Value | Use |
|-------|-------|-----|
| `--ss-ease-default` | ease-out | Most transitions |
| `--ss-ease-in` | ease-in | Exiting elements |
| `--ss-ease-in-out` | ease-in-out | Resizing, layout changes |

### Reduced Motion

All animations respect `prefers-reduced-motion: reduce`. When enabled, transitions are instant (0ms).

---

## 8. Layout

### Application Layout

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

### Panel Constraints

| Panel | Min Width | Max Width | Default |
|-------|-----------|-----------|---------|
| Left sidebar | 150px | 400px | 250px |
| Right sidebar | 200px | 500px | 300px |
| Bottom panel | 100px height | 400px height | 200px |

### Breakpoints

| Width | Behavior |
|-------|----------|
| ≥ 1400px | Full layout |
| 1000–1399px | Left sidebar collapses to icons |
| 600–999px | Both sidebars collapse, editor fills width |
| < 600px | Graceful degradation |

---

## 9. Keyboard Shortcuts

### Global

| Shortcut | Action |
|----------|--------|
| Ctrl+S / Cmd+S | Save project |
| Ctrl+Z / Cmd+Z | Undo |
| Ctrl+Shift+Z / Cmd+Shift+Z | Redo |
| Ctrl+P / Cmd+P | Command palette |
| Ctrl+, / Cmd+, | Settings |
| Ctrl+J / Cmd+J | Toggle bottom panel |
| Ctrl+B / Cmd+B | Toggle left sidebar |
| Ctrl+Shift+B / Cmd+Shift+B | Toggle right sidebar |
| Ctrl+Shift+D / Cmd+Shift+D | Debug panel |
| F1 | Help / Learning Center |
| Ctrl+= / Cmd+= | Zoom in |
| Ctrl+- / Cmd+- | Zoom out |
| Ctrl+0 / Cmd+0 | Reset zoom |

### Editor

| Shortcut | Action |
|----------|--------|
| Ctrl+F / Cmd+F | Find |
| Ctrl+H / Cmd+H | Find and replace |
| Ctrl+G / Cmd+G | Go to line |
| Tab | Indent |
| Shift+Tab | Outdent |
| Ctrl+D / Cmd+D | Duplicate line |
| Ctrl+/ / Cmd+/ | Toggle comment |
| Ctrl+Shift+K / Cmd+Shift+K | Delete line |

### Navigation

| Shortcut | Action |
|----------|--------|
| Ctrl+1..9 / Cmd+1..9 | Switch to panel 1..9 |
| Ctrl+Tab | Next tab |
| Ctrl+Shift+Tab | Previous tab |
| Ctrl+W / Cmd+W | Close current tab |

---

## 10. Responsive Rules

### Mobile (< 600px)

- Sidebars are hidden (accessible via hamburger menu).
- Bottom panel overlays content.
- Tab bar scrolls horizontally.
- Property inspector becomes a bottom sheet.

### Tablet (600–999px)

- Left sidebar collapses to icon rail (48px).
- Right sidebar is hidden by default.
- Bottom panel is available.

### Desktop (≥ 1000px)

- Full layout with resizable panels.
- All features available.

---

## 11. Theme System

### Theme Selection

Settings → Appearance → Theme: Dark | Light | System

"System" follows the OS preference (`prefers-color-scheme`).

### Theme Application

1. On theme change, CSS custom properties are updated.
2. All components re-render using the new values.
3. Charts and visualizations update their themes.
4. The theme choice is persisted in user settings.

### Custom Themes (v0.2)

Users can define custom themes by extending the base theme:

```jsonc
{
  "name": "My Theme",
  "extends": "dark",
  "overrides": {
    "--ss-accent": "#ff6384",
    "--ss-bg-primary": "#0a0a0a"
  }
}
```
