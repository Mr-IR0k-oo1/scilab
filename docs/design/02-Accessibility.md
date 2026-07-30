# Accessibility Guidelines

## Standards

WCAG 2.1 Level AA compliance for all user-facing components.

## Keyboard Navigation

- All interactive elements are focusable and operable via keyboard.
- Tab order follows visual layout (left-to-right, top-to-bottom).
- Focus indicators are visible (2px solid accent color outline).
- Escape closes modals and overlays.
- Arrow keys navigate within lists, trees, and menus.
- Tab/Shift+Tab moves between focus groups.

## Screen Reader Support

- All components use semantic HTML where possible.
- Custom components include `role` and `aria-*` attributes.
- Charts include text summaries (e.g., "Line chart showing temperature over 24 hours").
- Notifications use `aria-live="polite"` for non-urgent, `aria-live="assertive"` for errors.
- Form inputs have associated labels.

## Color and Contrast

- All text meets WCAG 2.1 AA contrast ratio (4.5:1 for normal text, 3:1 for large text).
- Error states use color + icon (not color alone).
- Interactive elements have visible focus states.

## Reduced Motion

- All animations respect `prefers-reduced-motion: reduce`.
- When enabled, transitions are instant (0ms).
- Chart animations are disabled.

## High Contrast Mode

- All components work in Windows High Contrast Mode.
- Borders and outlines are visible.
- Text remains readable against all backgrounds.

## Font Scaling

- UI respects system font size settings.
- Minimum font size: 11px.
- Layout does not break at 200% zoom.
