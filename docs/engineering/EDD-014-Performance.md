# EDD-014: Performance

## Purpose

The Performance System monitors, measures, and enforces performance budgets across the application.

## Budgets

### Startup
| Metric | Budget |
|--------|--------|
| Cold start | < 2 seconds |
| Warm start | < 500ms |
| Module activation (all) | < 2 seconds |
| Scilab startup | < 3 seconds |

### UI
| Metric | Budget |
|--------|--------|
| Panel switch | < 100ms |
| Tab switch | < 50ms |
| Command palette | < 100ms |
| Search results | < 200ms |
| Property update | < 5ms |

### Data
| Metric | Budget |
|--------|--------|
| CSV import (10 MB) | < 2 seconds |
| CSV import (100 MB) | < 10 seconds |
| Excel import (10 MB) | < 3 seconds |

### Visualization
| Metric | Budget |
|--------|--------|
| Chart render (1k points) | < 16ms |
| Chart render (10k points) | < 100ms |
| Chart render (100k points) | < 500ms |
| Chart render (1M points) | < 2 seconds |

### Memory
| Component | Budget |
|-----------|--------|
| Application (idle) | 150 MB |
| Application (with project) | 300 MB |
| Per open file | 10 MB |
| Per chart (100k points) | 50 MB |
| Per plugin | 20 MB |
| Scilab process | 500 MB |

## Performance Monitor

```typescript
interface PerformanceMonitor {
  mark(name: string): void;
  measure(name: string, startMark: string, endMark: string): number;
  getMetrics(): MetricReport[];
  onBudgetExceeded(handler: BudgetExceededHandler): Disposable;
}
```

## Metric Report

```typescript
interface MetricReport {
  name: string;
  value: number;
  unit: string;
  budget: number;
  status: 'ok' | 'warning' | 'exceeded';
  timestamp: string;
}
```

## Profiling

### Frontend
- Chrome DevTools Performance panel.
- Custom performance markers in code.
- Lighthouse scores.

### Backend
- Rust benchmarks with `cargo bench`.
- Memory profiling with `valgrind` / `leaks`.
- CPU profiling with `perf` / `Instruments`.

## Regression Detection

```typescript
interface RegressionDetector {
  baseline: MetricReport[];
  current: MetricReport[];
  threshold: number;  // 10% degradation

  detect(): Regression[];
}
```

**On CI:**
- Performance tests run on every PR.
- Regression detected if metric degrades > 10%.
- PR is blocked if regression detected.

## Optimization Strategies

### Lazy Loading
- Modules loaded on demand.
- Widgets loaded when first used.
- Charts rendered when visible.

### Caching
- File system cache for project files.
- Variable cache for Scilab data.
- Render cache for charts.

### Debouncing
- Auto-save debounced (1 second).
- Config changes debounced (100ms).
- Search input debounced (200ms).

### Progressive Rendering
- Large datasets downsampled first.
- Full resolution renders in background.
- Loading indicators shown.

## Performance Testing

```bash
# Run performance tests
npm run test:perf

# Generate performance report
npm run test:perf -- --report

# Compare against baseline
npm run test:perf -- --compare
```

## Rules

- No performance regressions in PRs.
- New features must meet the budget.
- Profile before optimizing.
- Document performance characteristics.
- Use performance markers for critical paths.
