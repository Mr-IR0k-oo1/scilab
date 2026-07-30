# Design Principles

## 1. Consistent
Every screen uses the same spacing, typography, colors, and interaction patterns. A user who learns one part of the application can navigate any other part.

## 2. Accessible
WCAG 2.1 AA compliance. Keyboard navigable. Screen reader friendly. High contrast mode. Reduced motion support. No feature is inaccessible.

## 3. Responsive
Adapts to window sizes without breaking. Panels collapse gracefully. Content remains readable at all sizes. Not a mobile app, but handles small windows well.

## 4. Dark-first
Dark theme is the default. Light theme is available. System theme follows OS preference. Charts and visualizations look good in both themes.

## 5. Minimal chrome
Content is the focus. UI elements recede until needed. No unnecessary decoration. No developer UI. The application feels like a product, not a prototype.

## 6. Predictable
Consistent placement of controls. Consistent behavior of similar elements. Consistent keyboard shortcuts across modules. No surprises.

## 8. Forgiving
Undo/redo everywhere. Confirmation dialogs for destructive actions. Auto-save prevents data loss. Crash recovery preserves work. Errors are recoverable.

## 9. Fast
Meet performance budgets. Cold start < 3s. Panel switch < 100ms. Chart render < 1s. Never make the user wait without feedback.

## 10. Educational
Prioritize learning use cases. Guided workflows. Progressive disclosure. The Learning Center and templates are first-class features, not afterthoughts.
