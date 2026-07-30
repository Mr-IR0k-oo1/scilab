# Performance Benchmarks

## Targets

| Metric | Target | How Measured |
|--------|--------|-------------|
| Cold start | < 2 seconds | App launch to ready |
| Warm start | < 500ms | Re-launch after close |
| Project open | < 1 second | Click to project loaded |
| Project save | < 500ms | Click to saved |
| File open | < 200ms | Click to file displayed |
| Panel switch | < 100ms | Click to panel visible |
| Tab switch | < 50ms | Click to tab content |
| Command palette open | < 100ms | Ctrl+P to visible |
| Search results | < 200ms | Typing to results |
| CSV import (10 MB) | < 2 seconds | File selected to data visible |
| CSV import (100 MB) | < 10 seconds | File selected to data visible |
| Excel import (10 MB) | < 3 seconds | File selected to data visible |
| Chart render (1k points) | < 16ms | Data to rendered (60 FPS) |
| Chart render (10k points) | < 100ms | Data to rendered |
| Chart render (100k points) | < 500ms | Data to rendered |
| Chart render (1M points) | < 2 seconds | Data to rendered (progressive) |
| Report generation (10 pages) | < 5 seconds | Click to exported |
| Plugin load | < 500ms | Plugin file to active |
| Plugin activation | < 100ms | Activate to ready |
| Scilab startup | < 3 seconds | Process start to ready |
| Scilab execution | < 100ms | Command to result |
| Widget render (100 widgets) | < 200ms | Data to all rendered |

## Memory Budgets

| Component | Maximum |
|-----------|---------|
| Application (idle) | 150 MB |
| Application (with project) | 300 MB |
| Per open file | 10 MB |
| Per chart (100k points) | 50 MB |
| Per plugin | 20 MB |
| Scilab process | 500 MB |

## Bundle Size Budgets

| Bundle | Maximum (gzipped) |
|--------|-------------------|
| Main bundle | 500 KB |
| Per plugin | 100 KB |
| Per widget | 20 KB |
| Total CSS | 100 KB |

## Measurement

### Frontend
- Chrome DevTools Performance panel.
- Lighthouse scores.
- Custom performance markers.

### Backend
- Rust benchmarks with `cargo bench`.
- Memory profiling with `valgrind` / `leaks`.
- CPU profiling with `perf` / `Instruments`.

### CI
- Performance tests run on every PR.
- Regression detected if metric degrades > 10%.
- Results published to dashboard.

## Rules

- No performance regressions in PRs.
- New features must meet the budget.
- Profile before optimizing.
- Document performance characteristics.
