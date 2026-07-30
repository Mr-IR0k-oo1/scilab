# Testing Strategy

## Test Pyramid

```
         /  E2E  \           Few, slow, high confidence
        / Integration \      Some, moderate speed
       /    Unit Tests   \   Many, fast, isolated
      ──────────────────────
```

## Unit Tests

### Scope
- Every public function.
- Every component.
- Every utility.
- Edge cases and error paths.

### Framework
- Vitest for TypeScript/Svelte.
- Rust's built-in `#[test]` for backend.

### Coverage Requirements

| Module | Coverage |
|--------|----------|
| Core Runtime | 90% |
| Plugin System | 85% |
| Widget Framework | 85% |
| Visualization Engine | 80% |
| Data Pipeline | 85% |
| UI Components | 75% |

### Commands
```bash
npm run test:unit          # Run all unit tests
npm run test:unit -- --watch  # Watch mode
npm run test:coverage      # Coverage report
```

## Integration Tests

### Scope
- Plugin loading and activation.
- Widget creation and rendering.
- Data import and transform pipeline.
- Chart creation and export.
- Project save and load.
- Scilab execution.

### Framework
- Vitest with mocked dependencies.
- Custom test harness for Scilab.

### Commands
```bash
npm run test:integration
```

## E2E Tests

### Scope
- Full user workflows.
- Cross-module interactions.
- Installation and upgrade.
- Plugin marketplace.

### Framework
- Playwright for UI testing.

### Commands
```bash
npm run test:e2e
```

## Performance Tests

### Scope
- All benchmarks in Benchmarks.md.
- Memory usage over time.
- CPU usage during rendering.
- Bundle size.

### Framework
- Vitest benchmarks.
- Custom performance harness.

### Commands
```bash
npm run test:perf
```

## Visual Regression Tests

### Scope
- Chart rendering.
- UI component appearance.
- Theme application.
- Responsive layouts.

### Framework
- Playwright screenshot comparison.
- Threshold: 0.1% pixel difference.

### Commands
```bash
npm run test:visual
```

## Accessibility Tests

### Scope
- Keyboard navigation.
- ARIA attributes.
- Focus indicators.
- Contrast ratios.

### Framework
- axe-core integration.
- Manual testing checklist.

### Commands
```bash
npm run test:a11y
```

## Test Data

### Fixtures
- `tests/fixtures/projects/` — Sample projects.
- `tests/fixtures/data/` — Sample data files.
- `tests/fixtures/plugins/` — Test plugins.

### Factories
```typescript
function createTestProject(overrides?: Partial<Project>): Project {
  return {
    name: 'Test Project',
    path: '/tmp/test-project',
    ...overrides
  };
}
```

## Rules

- Tests must pass before merge.
- No flaky tests.
- Test code follows production standards.
- Mock external dependencies.
- Use factories for test data.
