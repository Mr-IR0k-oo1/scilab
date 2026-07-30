# RFC-0004: Visualization API

| Field | Value |
|-------|-------|
| RFC | 0004 |
| Title | Visualization API |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how charts are created, configured, rendered, and how they interact with Scilab data.

## Motivation

Visualization is a core engineering capability. The API must support both quick plotting and publication-quality output while remaining performant with large datasets.

## Detailed Design

### Chart Creation

```typescript
interface ChartDescriptor {
  type: ChartType;
  data: DataDescriptor;
  options?: ChartOptions;
}

type ChartType =
  | 'line'
  | 'scatter'
  | 'bar'
  | 'heatmap'
  | 'histogram'
  | 'pie'
  | 'surface'
  | 'waterfall'
  | 'bode'
  | 'nyquist'
  | 'root-locus'
  | 'polar'
  | 'contour'
  | 'quiver'
  | 'stem'
  | 'box';
```

### Data Descriptor

```typescript
interface DataDescriptor {
  source: 'scilab' | 'inline' | 'file';
  expression?: string;        // Scilab expression
  file?: string;              // File path
  columns?: string[];         // Column names
  transform?: DataTransform;  // Pre-processing
}
```

### Chart Options

```typescript
interface ChartOptions {
  title?: string;
  xlabel?: string;
  ylabel?: string;
  zlabel?: string;
  legend?: string[];
  grid?: boolean;
  theme?: 'dark' | 'light' | 'system';
  width?: number;
  height?: number;
  dpi?: number;
  colors?: string[];
  animation?: AnimationOptions;
  interaction?: InteractionOptions;
}
```

### Rendering Pipeline

```
Data Source → Expression Evaluation → Data Transform → Chart Render → Canvas Output
```

1. **Data Source**: Data comes from Scilab variable, inline array, or file.
2. **Expression Evaluation**: Scilab expressions are evaluated asynchronously.
3. **Data Transform**: Apply transforms (normalize, filter, aggregate).
4. **Chart Render**: Render to Canvas 2D or WebGL.
5. **Canvas Output**: Display on screen or export to file.

### Interaction Model

| Interaction | Default | Behavior |
|------------|---------|----------|
| Scroll | Zoom | Zoom in/out centered on cursor |
| Drag | Pan | Pan the viewport |
| Click | Select | Select nearest data point |
| Shift+Click | Multi-select | Add to selection |
| Hover | Tooltip | Show data point details |
| Double-click | Reset | Reset zoom and pan |

### Export

```typescript
interface ExportOptions {
  format: 'png' | 'svg' | 'pdf' | 'csv' | 'json';
  width?: number;
  height?: number;
  dpi?: number;
  filename?: string;
}
```

### Theme System

Charts inherit the application theme by default. Custom themes can be applied per chart:

```json
{
  "background": "#1e1e1e",
  "text": "#e0e0e0",
  "grid": "#404040",
  "colors": ["#4a9eff", "#ff6384", "#4caf50"],
  "fonts": { "family": "Inter", "size": 12 }
}
```

### Performance Budgets

| Dataset Size | Render Budget |
|-------------|---------------|
| 1,000 points | < 16ms (60 FPS) |
| 10,000 points | < 100ms |
| 100,000 points | < 500ms (progressive) |
| 1,000,000 points | Downsample to 100k |

### Scilab Integration

Charts can be created directly from Scilab code:

```scilab
// In Scilab script
x = 0:0.1:10;
y = sin(x);
studio.plot(x, y, "title=Sine Wave", "xlabel=Time", "ylabel=Amplitude");
```

## Alternatives Considered

1. **D3.js**: Powerful but heavy. For a desktop app, Canvas is more performant.
2. **Chart.js**: Good for web, but not optimized for engineering data.
3. **Plotly.js**: Feature-rich but very large bundle. Better for web apps.

## Security Considerations

- Chart rendering is confined to the canvas element.
- Export operations use the file system API with user consent.
- Scilab expressions are evaluated in the sandboxed Scilab process.

## Testing Strategy

- Visual regression tests for each chart type.
- Performance tests for large datasets.
- Accessibility tests for chart interactions.
- Export tests for each format.

## Rollout

- v0.1: Line, scatter, bar, heatmap (4 types).
- v0.2: Surface, histogram, pie, bode, nyquist, root-locus (6 types).
- v0.3: Polar, contour, quiver, stem, box (5 types).
