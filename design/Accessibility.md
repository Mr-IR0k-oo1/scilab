# Accessibility

## Standards

WCAG 2.1 Level AA compliance for all user-facing components.

## Keyboard Navigation

### Focus Management
- All interactive elements are focusable.
- Focus order follows visual layout.
- Focus indicators: 2px solid `--ss-accent` outline.
- Focus trap in modal dialogs.

### Tab Order
```
1. Title bar controls
2. Menu bar
3. Toolbar
4. Left sidebar
5. Editor area
6. Right sidebar
7. Bottom panel
8. Status bar
```

### Keybindings
| Key | Action |
|-----|--------|
| Tab | Next focusable element |
| Shift+Tab | Previous focusable element |
| Enter/Space | Activate focused element |
| Escape | Close dialog/menu, cancel operation |
| Arrow keys | Navigate within groups |
| Home/Start | First item in group |
| End | Last item in group |

## Screen Reader Support

### ARIA Attributes
- All custom components include `role` and `aria-*` attributes.
- Live regions for dynamic content: `aria-live="polite"` (info), `aria-live="assertive"` (errors).
- Labels for all form inputs.
- Descriptions for complex components.

### Semantic HTML
- Use `<button>` for buttons, not `<div>`.
- Use `<input>` for inputs, not custom elements.
- Use `<nav>` for navigation.
- Use `<main>` for primary content.

### Chart Accessibility
- Charts include text summaries.
- Data tables available as alternative.
- Keyboard navigation for data points.

## Color and Contrast

### Contrast Ratios
| Element | Minimum Ratio |
|---------|--------------|
| Normal text | 4.5:1 |
| Large text | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

### Color Independence
- Error states use color + icon (not color alone).
- Status indicators use text + icon.
- Charts use patterns + color.

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- All animations disabled.
- Transitions instant.
- Chart animations disabled.

## High Contrast Mode

- All components work in Windows High Contrast Mode.
- Borders and outlines visible.
- Text readable against all backgrounds.

## Font Scaling

- Respects system font size.
- Minimum font size: 10px.
- Layout does not break at 200% zoom.

## Testing

- Keyboard-only navigation testing.
- Screen reader testing (NVDA, VoiceOver).
- Contrast ratio testing.
- Reduced motion testing.
- High contrast mode testing.
