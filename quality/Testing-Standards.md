# Testing Standards

## Test Pyramid

```
         /  E2E  \
        / Integration \
       /    Unit Tests   \
      ──────────────────────
```

- **Unit tests**: Fast, isolated, many.
- **Integration tests**: Component interaction, moderate.
- **E2E tests**: Full workflow, few.

## Unit Tests

### Framework
- Frontend: Vitest
- Backend: Rust's built-in test framework

### Requirements
- Every public function must have unit tests.
- Test happy path and error paths.
- Test edge cases (empty input, null, boundary values).
- Tests must be deterministic.
- Tests must be independent (no shared state).

### Coverage
| Component | Minimum Coverage |
|-----------|-----------------|
| Core Runtime | 90% |
| Plugin System | 85% |
| Widget Framework | 85% |
| Visualization | 80% |
| Data Pipeline | 85% |
| UI Components | 75% |

### Example
```typescript
describe('Runtime', () => {
  it('should execute Scilab code', async () => {
    const result = await runtime.execute('x = 1 + 1');
    expect(result.variables.x.value).toBe(2);
  });

  it('should handle syntax errors', async () => {
    await expect(runtime.execute('if('))
      .rejects.toThrow('Syntax error');
  });

  it('should timeout on long execution', async () => {
    await expect(
      runtime.execute('while(1) end', { timeout: 100 })
    ).rejects.toThrow('Timeout');
  });
});
```

## Integration Tests

### What to Test
- Plugin loading and activation.
- Widget creation and rendering.
- Data import and transform pipeline.
- Chart creation and export.
- Project save and load.

### Example
```typescript
describe('Plugin System', () => {
  it('should load and activate a plugin', async () => {
    const plugin = await pluginManager.load('./test-plugin');
    expect(plugin.status).toBe('active');
    expect(plugin.commands.length).toBe(2);
  });
});
```

## E2E Tests

### Framework
- Playwright for UI testing.
- Custom harness for Scilab integration.

### What to Test
- Full user workflows (create project, edit, save).
- Plugin installation and usage.
- Chart creation and export.
- Report generation.

## Performance Tests

### Requirements
- All performance benchmarks must pass.
- See Benchmarks section for targets.

### Example
```typescript
describe('Performance', () => {
  it('should open project in < 2 seconds', async () => {
    const start = Date.now();
    await project.open('./large-project');
    expect(Date.now() - start).toBeLessThan(2000);
  });
});
```

## Visual Regression Tests

### What to Test
- Chart rendering matches reference images.
- UI components match design spec.
- Themes apply correctly.

### Framework
- Playwright screenshot comparison.
- Threshold: 0.1% pixel difference.

## Accessibility Tests

### What to Test
- Keyboard navigation works.
- ARIA attributes are present.
- Focus indicators are visible.
- Contrast ratios meet WCAG 2.1 AA.

### Framework
- axe-core integration.
- Manual testing checklist.

## Test Commands

```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run E2E tests
npm run test:e2e

# Run performance tests
npm run test:perf

# Run accessibility tests
npm run test:a11y

# Generate coverage report
npm run test:coverage
```

## Rules

- Tests must pass before merge.
- No flaky tests. Fix or remove.
- Test code follows the same standards as production code.
- Mock external dependencies (Scilab, file system).
- Use factories for test data.
