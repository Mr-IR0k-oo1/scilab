# UI/UX Guidelines

> Design principles, standards, and patterns for Scilab Studio's user interface.

---

## Design Principles

### 1. Clarity
Every element should communicate its purpose without ambiguity. Labels are descriptive. Actions have visible outcomes. The user should never wonder "what just happened?"

### 2. Consistency
Similar elements look and behave similarly across all modules. A button in the Visualization module behaves like a button in the Data Studio. Design tokens, spacing, and typography are shared globally.

### 3. Efficiency
Minimize the number of clicks and navigations to complete common tasks. Provide keyboard shortcuts for power users. Use progressive disclosure to keep the interface uncluttered while keeping advanced options accessible.

### 4. Accessibility
The interface must be usable by people with diverse abilities. Follow WCAG 2.1 AA standards. Ensure keyboard navigability, screen reader support, sufficient color contrast, and alternative text for all visual elements.

---

## Color System

### Brand Colors
```css
--color-primary:        #2563EB;  /* Blue 600 — primary actions */
--color-primary-hover:  #1D4ED8;  /* Blue 700 — hover state */
--color-primary-light:  #DBEAFE;  /* Blue 100 — backgrounds */
```

### Neutral Colors
```css
--color-bg-primary:     #FFFFFF;  /* Main background */
--color-bg-secondary:   #F9FAFB;  /* Sidebar, panels */
--color-bg-tertiary:    #F3F4F6;  /* Cards, elevated surfaces */
--color-border:         #E5E7EB;  /* Default borders */
--color-border-strong:  #D1D5DB;  /* Emphasized borders */
--color-text-primary:   #111827;  /* Primary text */
--color-text-secondary: #6B7280;  /* Secondary text */
--color-text-muted:     #9CA3AF;  /* Disabled, placeholder */
```

### Semantic Colors
```css
--color-success:        #059669;  /* Green 600 — success states */
--color-success-bg:     #D1FAE5;  /* Green 100 — success backgrounds */
--color-warning:        #D97706;  /* Amber 600 — warning states */
--color-warning-bg:     #FEF3C7;  /* Amber 100 — warning backgrounds */
--color-error:          #DC2626;  /* Red 600 — error states */
--color-error-bg:       #FEE2E2;  /* Red 100 — error backgrounds */
--color-info:           #2563EB;  /* Blue 600 — informational */
--color-info-bg:        #DBEAFE;  /* Blue 100 — info backgrounds */
```

### Chart Palette
```css
--chart-color-1: #2563EB;  /* Blue */
--chart-color-2: #059669;  /* Green */
--chart-color-3: #D97706;  /* Amber */
--chart-color-4: #DC2626;  /* Red */
--chart-color-5: #7C3AED;  /* Purple */
--chart-color-6: #0891B2;  /* Cyan */
--chart-color-7: #BE185D;  /* Pink */
--chart-color-8: #65A30D;  /* Lime */
```

---

## Typography

### Font Stack
```css
--font-sans:  'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono:  'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace;
```

### Type Scale

| Name | Size | Weight | Line Height | Usage |
|------|------|--------|-------------|-------|
| Display | 30px | 700 | 1.2 | Page titles, hero text |
| H1 | 24px | 600 | 1.3 | Section headings |
| H2 | 20px | 600 | 1.4 | Subsection headings |
| H3 | 16px | 600 | 1.5 | Card titles, group labels |
| Body | 14px | 400 | 1.5 | Default text |
| Body Small | 13px | 400 | 1.5 | Secondary text, captions |
| Caption | 12px | 400 | 1.4 | Labels, metadata, timestamps |
| Code | 13px | 400 | 1.6 | Code blocks, inline code |

---

## Spacing and Layout

### Spacing Scale
All spacing uses a 4px base grid:

| Token | Value | Usage |
|-------|-------|-------|
| `--space-0` | 0px | No spacing |
| `--space-1` | 4px | Tight spacing (icon gaps) |
| `--space-2` | 8px | Compact spacing (form fields) |
| `--space-3` | 12px | Default spacing (between elements) |
| `--space-4` | 16px | Comfortable spacing (sections) |
| `--space-5` | 20px | Generous spacing (card padding) |
| `--space-6` | 24px | Section spacing |
| `--space-8` | 32px | Large section spacing |
| `--space-10` | 40px | Page-level spacing |
| `--space-12` | 48px | Major section breaks |

### Layout Grid

```
┌─────────────────────────────────────────────┐
│  Toolbar (48px height)                      │
├──────┬──────────────────────────┬───────────┤
│      │                          │           │
│ Side │      Main Content        │  Properties│
│ bar  │                          │  Panel    │
│260px │      (flexible)          │  280px    │
│      │                          │           │
├──────┴──────────────────────────┴───────────┤
│  Bottom Panel (200px, collapsible)          │
│  (Output, Terminal, Problems)               │
└─────────────────────────────────────────────┘
```

### Breakpoints (for web mode)

| Name | Width | Usage |
|------|-------|-------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Small desktop |
| `xl` | 1280px | Standard desktop |
| `2xl` | 1536px | Large desktop |

---

## Component Library Standards

### Buttons

| Variant | Usage | Appearance |
|---------|-------|------------|
| Primary | Main action (Save, Create, Run) | Filled blue, white text |
| Secondary | Alternate action (Cancel, Close) | Outlined, blue text |
| Danger | Destructive action (Delete, Remove) | Filled red, white text |
| Ghost | Tertiary action, toolbar buttons | Transparent, subtle hover |
| Icon | Compact actions (settings, expand) | Icon only, ghost style |

### Size Variants

| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| Small | 28px | 8px 12px | 12px |
| Medium | 36px | 10px 16px | 14px |
| Large | 44px | 12px 20px | 16px |

### Form Controls

**Text Input:**
- Height: 36px
- Border: 1px solid `--color-border`
- Border radius: 6px
- Focus ring: 2px solid `--color-primary` with 2px offset
- Placeholder color: `--color-text-muted`

**Select / Dropdown:**
- Same styling as text input
- Custom arrow icon on the right
- Dropdown menu: elevation shadow, border radius 8px

**Checkbox / Radio:**
- 16px × 16px
- Custom styled (hidden native input)
- Focus ring for keyboard navigation

**Toggle:**
- 40px × 20px track
- 16px × 16px thumb (with 2px offset for padding)
- Animated transition: 200ms ease

---

## Iconography

### Icon Set
Use the project's custom icon set based on Lucide icons (MIT licensed).

### Icon Sizes

| Size | Dimensions | Usage |
|------|-----------|-------|
| `xs` | 12×12 | Inline badges, indicators |
| `sm` | 16×16 | Compact UI, table rows |
| `md` | 20×20 | Default for buttons, menus |
| `lg` | 24×24 | Standalone icons, navigation |
| `xl` | 32×32 | Feature icons, empty states |

### Icon Guidelines
- Use a consistent stroke width (1.5px for `md` and `lg`).
- Prefer outline/filled variants consistently within a context.
- Icons in buttons should be accompanied by text labels when possible.
- Decorative icons must have `aria-hidden="true"`.
- Functional icons must have `aria-label` or an associated tooltip.

---

## Responsive Design

### Desktop (Primary)
The full three-column layout (sidebar, content, properties panel) is the default experience for desktop users.

### Web Mode Adaptations

| Breakpoint | Adaptation |
|-----------|------------|
| < 1024px | Properties panel collapses to a slide-out drawer |
| < 768px | Sidebar collapses to icons only (48px) |
| < 640px | Sidebar hidden behind hamburger menu |

### Resizable Panels
All panels (sidebar, bottom panel, properties panel) can be resized by dragging their borders. Minimum widths/heights are enforced to maintain usability.

---

## Accessibility (WCAG 2.1 AA Compliance)

### Color Contrast
- Normal text: minimum 4.5:1 contrast ratio.
- Large text (18px+ bold, 24px+ normal): minimum 3:1 contrast ratio.
- UI components and graphical objects: minimum 3:1 contrast ratio.

### Keyboard Navigation
- All interactive elements are reachable via Tab key.
- Focus order follows visual layout (left-to-right, top-to-bottom).
- Focus ring is always visible on keyboard navigation.
- Escape closes modals and menus.
- Arrow keys navigate within menus, tabs, and lists.

### Screen Reader Support
- All images and icons have appropriate alt text or `aria-label`.
- Form fields have associated labels.
- Dynamic content changes are announced via `aria-live` regions.
- Landmark regions (`nav`, `main`, `aside`) are properly used.
- ARIA roles are applied to custom widgets.

### Motion
- Respect `prefers-reduced-motion` media query.
- Disable animations when the user has this preference enabled.
- Never use animation as the sole means of conveying information.

---

## Dark Mode Support

### Theme Switching
The application supports light and dark themes, switchable via:
- Settings > Appearance > Theme
- System preference detection
- Keyboard shortcut (Ctrl+Shift+T)

### Dark Mode Colors
```css
[data-theme="dark"] {
  --color-bg-primary:     #0F172A;  /* Slate 900 */
  --color-bg-secondary:   #1E293B;  /* Slate 800 */
  --color-bg-tertiary:    #334155;  /* Slate 700 */
  --color-border:         #475569;  /* Slate 600 */
  --color-text-primary:   #F8FAFC;  /* Slate 50 */
  --color-text-secondary: #94A3B8;  /* Slate 400 */
  --color-text-muted:     #64748B;  /* Slate 500 */
}
```

### Guidelines
- All colors must be defined as CSS custom properties (not hardcoded).
- Test every screen in both light and dark mode.
- Charts must have a dark-mode variant with appropriate contrast.
- Code editor themes switch automatically with the application theme.

---

## Animation and Transitions

### Duration

| Type | Duration | Usage |
|------|----------|-------|
| Micro | 100ms | Button hover, focus ring |
| Small | 200ms | Toggle, checkbox, dropdown open |
| Medium | 300ms | Panel slide, modal appear |
| Large | 500ms | Page transition, data load |

### Easing

| Name | Value | Usage |
|------|-------|-------|
| Default | `ease-in-out` | Most transitions |
| Enter | `ease-out` | Elements entering the viewport |
| Exit | `ease-in` | Elements leaving the viewport |
| Bounce | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful micro-interactions |

### Guidelines
- Use transitions sparingly — only when they provide spatial or state feedback.
- Avoid animating layout properties (width, height, position) — use `transform` and `opacity` instead.
- Never block user interaction during animations.
- Provide instant feedback for all user actions (optimistic updates where appropriate).

---

## Error States and Loading States

### Loading States

**Skeleton Screens:**
Use skeleton placeholders instead of spinners for content loading. Skeletons mirror the shape of the expected content.

**Spinner:**
Use a spinner for actions taking an indeterminate amount of time (e.g., executing code). Show a progress indicator when the duration is estimable.

**Progress Bar:**
Use for operations with known progress (file import, export, download). Display percentage and estimated time remaining.

### Error States

**Inline Errors:**
Display below the relevant form field or near the failed operation.

**Error Toast:**
For non-critical errors that don't block the workflow. Include a description and optional "Retry" action.

**Full-page Error:**
For critical failures (engine crash, network failure). Include an error illustration, description, and recovery action.

**Error Boundary:**
React error boundaries catch rendering errors and display a fallback UI with the option to reload the affected component.

---

## Navigation Patterns

### Primary Navigation
The sidebar provides primary navigation between modules:
- Icon + label for expanded sidebar.
- Icon only for collapsed sidebar.
- Active module is highlighted.
- Drag to reorder modules.

### Secondary Navigation
Tabs within a module provide secondary navigation:
- Horizontal tab bar at the top of the content area.
- Scrollable when tabs overflow.
- Active tab has an underline indicator.

### Breadcrumbs
For deep navigation hierarchies (file explorer, settings):
```
Project > src > main.sce
```

### Command Palette
Ctrl+Shift+P (Cmd+Shift+P on macOS) opens a command palette for quick access to any action:
- Fuzzy search across all commands.
- Recently used commands are prioritized.
- Keyboard-driven navigation.

---

## Dialog and Modal Patterns

### Confirmation Dialog
For destructive actions (delete, remove, overwrite):
```
┌─────────────────────────────────────┐
│  Delete Project?                    │
│                                     │
│  This will permanently delete       │
│  "My Project" and all its files.    │
│  This action cannot be undone.      │
│                                     │
│        [Cancel]     [Delete]        │
└─────────────────────────────────────┘
```
- The destructive action uses the Danger button variant.
- The destructive action is placed on the right (for LTR layouts).

### Modal Dialog
For focused tasks that require user input:
- Maximum width: 640px
- Backdrop: semi-transparent overlay
- Close on Escape key
- Close on backdrop click (optional, configurable)
- Focus trapped within the modal

### Slide-out Panel
For less critical interactions (settings, properties):
- Slides in from the right
- Width: 320–480px
- Can be resized
- Does not block the main content entirely

---

## Form Design

### Layout
- Use a single-column layout for forms.
- Group related fields with section headers.
- Use horizontal layout only for compact inline forms (search bars).

### Labels
- Labels are placed above inputs (not to the left).
- Labels are always visible (not as placeholders).
- Use sentence case ("Email address" not "Email Address").

### Validation
- Validate on blur for most fields (not on every keystroke).
- Show inline error messages below the field.
- Error messages are specific and actionable ("Password must be at least 8 characters" not "Invalid input").
- Disable submit buttons until required fields are valid.

### Help Text
- Place helper text below the input, above the error message.
- Use `--color-text-muted` for helper text.

---

## Data Visualization Standards

### Chart Defaults

| Property | Value |
|----------|-------|
| Background | Transparent |
| Grid lines | `#E5E7EB` (light) / `#475569` (dark) |
| Axis lines | `#9CA3AF` |
| Font | Inter, 12px |
| Tooltip | Dark background, white text, 8px rounded |

### Chart Types and When to Use

| Chart Type | Use For | Avoid When |
|------------|---------|------------|
| Line | Trends over time | Categories |
| Bar | Comparing categories | Continuous data |
| Scatter | Correlations, distributions | Simple comparisons |
| Histogram | Frequency distributions | Small datasets |
| Pie | Proportions (max 6 slices) | Many categories |
| Heatmap | Matrix data, density | Sparse data |
| Box Plot | Statistical distributions | Single values |
| Surface | 3D function visualization | Simple 2D data |

### Responsive Charts
- Charts resize with their container.
- Axes labels hide when space is insufficient.
- Tooltips show full information on hover/touch.

### Accessibility in Charts
- All charts have a text-based data summary alternative.
- Color is never the only differentiator — use patterns or labels too.
- Charts have `role="img"` with `aria-label` describing the data.
