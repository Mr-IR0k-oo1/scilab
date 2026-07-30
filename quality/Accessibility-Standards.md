# Accessibility Standards

## Compliance

WCAG 2.1 Level AA for all user-facing features.

## Requirements

### Perceivable

1.1 **Text Alternatives**
- All images have alt text.
- Charts have text summaries.
- Icons have aria-labels.

1.3 **Adaptable**
- Content is readable at 200% zoom.
- Layout does not break at different font sizes.
- Reading order is logical.

1.4 **Distinguishable**
- Text contrast ratio ≥ 4.5:1.
- UI component contrast ratio ≥ 3:1.
- Focus indicators are visible.
- Color is not the only indicator.

### Operable

2.1 **Keyboard Accessible**
- All features operable via keyboard.
- No keyboard traps.
- Keyboard shortcuts are discoverable.

2.4 **Navigable**
- Skip navigation links.
- Descriptive page titles.
- Logical focus order.
- Clear focus indicators.

### Understandable

3.1 **Readable**
- Language is clear and simple.
- Technical terms are explained.
- Consistent terminology.

3.3 **Input Assistance**
- Labels for all form inputs.
- Error messages are descriptive.
- Suggestions for error correction.

### Robust

4.1 **Compatible**
- Valid HTML.
- ARIA attributes used correctly.
- Works with screen readers.

## Testing Checklist

- [ ] Keyboard-only navigation for all features.
- [ ] Screen reader testing (NVDA, VoiceOver, JAWS).
- [ ] Contrast ratio testing for all text.
- [ ] Focus indicator visibility testing.
- [ ] Reduced motion testing.
- [ ] High contrast mode testing.
- [ ] Font scaling testing (200%).
- [ ] Color independence testing.
- [ ] ARIA attribute validation.

## Tools

- axe-core for automated testing.
- Lighthouse for accessibility scoring.
- WAVE for manual testing.
- Screen readers for manual testing.

## Rules

- Accessibility is not optional. Every feature must be accessible.
- Test with real assistive technology.
- Don't rely solely on automated testing.
- Include accessibility in code reviews.
