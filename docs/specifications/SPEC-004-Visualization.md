# SPEC-004 — Visualization

## Purpose

Provide a charting engine that renders data as interactive visualizations. Every chart type follows a common pipeline: Data → Transformation → Theme → Renderer → Interaction.

---

## Supported Charts

### Line
- **Purpose:** Show trends over continuous data.
- **Input:** Series of (x, y) pairs or single series of y values.
- **Output:** Line(s) connecting data points.
- **Interaction:** Hover tooltips, zoom, pan, point selection.
- **Export:** PNG, SVG, JPEG.
- **Animation:** Line drawing on first render (optional).
- **Data:** Numeric arrays, up to 10 series, up to 100,000 points (downsampled to 2,000 for rendering).
- **Performance:** Render < 1s for 10k points.

### Scatter
- **Purpose:** Show relationships between two variables.
- **Input:** Series of (x, y) pairs with optional size/color encoding.
- **Output:** Points plotted on 2D axes.
- **Interaction:** Hover tooltips, zoom, pan, point selection, lasso select.
- **Export:** PNG, SVG, JPEG.
- **Animation:** Points appear with fade-in (optional).
- **Data:** Numeric arrays, up to 5 series, up to 50,000 points.
- **Performance:** Render < 1s for 10k points.

### Surface
- **Purpose:** Visualize 3D data as a surface plot.
- **Input:** Z matrix with optional X and Y vectors.
- **Output:** 3D surface rendered with WebGL.
- **Interaction:** Rotate (drag), zoom (scroll), hover for coordinates.
- **Export:** PNG, SVG.
- **Animation:** Rotation on first render (optional).
- **Data:** Numeric matrix up to 500×500.
- **Performance:** Render < 2s for 200×200.

### Heatmap
- **Purpose:** Show intensity patterns in matrix data.
- **Input:** Rows × Columns matrix of values.
- **Output:** Colored grid with value-to-color mapping.
- **Interaction:** Hover for cell value, click to select.
- **Export:** PNG, SVG.
- **Animation:** Color fade-in on first render (optional).
- **Data:** Numeric matrix, up to 1000×1000.
- **Performance:** Render < 500ms for 200×200.

### Sankey
- **Purpose:** Show flow and proportions between categories.
- **Input:** Nodes and weighted links.
- **Output:** Flow diagram with proportional widths.
- **Interaction:** Hover to highlight path, click to select node.
- **Export:** PNG, SVG.
- **Animation:** Flow drawing on first render.
- **Data:** Up to 100 nodes, 500 links.
- **Performance:** Render < 1s.

### Network
- **Purpose:** Show relationships and connections between entities.
- **Input:** Nodes and edges with optional weights.
- **Output:** Graph layout with nodes and edges.
- **Interaction:** Drag nodes, zoom, pan, hover for details.
- **Export:** PNG, SVG.
- **Animation:** Force-directed layout settling (optional).
- **Data:** Up to 1,000 nodes, 10,000 edges.
- **Performance:** Render < 2s for 500 nodes.

### Radar
- **Purpose:** Compare multiple variables across categories.
- **Input:** Axes labels and series of values per axis.
- **Output:** Polar chart with filled polygons.
- **Interaction:** Hover for values, toggle series visibility.
- **Export:** PNG, SVG.
- **Animation:** Polygon drawing on first render.
- **Data:** Up to 20 axes, 5 series.
- **Performance:** Render < 500ms.

### Gauge
- **Purpose:** Show a single value within a range.
- **Input:** Value, min, max, unit.
- **Output:** Circular gauge with needle/arc.
- **Interaction:** Hover for exact value.
- **Export:** PNG.
- **Animation:** Needle animation on value change.
- **Data:** Single numeric value.
- **Performance:** Render < 100ms.

### Histogram
- **Purpose:** Show distribution of a dataset.
- **Input:** Array of numeric values.
- **Output:** Bins with bars showing frequency.
- **Interaction:** Hover for bin details, click to select range.
- **Export:** PNG, SVG.
- **Animation:** Bar growth on first render.
- **Data:** Numeric array up to 1,000,000 values.
- **Performance:** Render < 500ms.

### Waterfall
- **Purpose:** Show cumulative effect of sequential values.
- **Input:** Categories and values (positive/negative).
- **Output:** Floating bars showing contribution to total.
- **Interaction:** Hover for values.
- **Export:** PNG, SVG.
- **Animation:** Bars grow from baseline.
- **Data:** Up to 50 categories.
- **Performance:** Render < 500ms.

---

## Common Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| title | string | "" | Chart title |
| subtitle | string | "" | Chart subtitle |
| width | number | auto | Canvas width (px) |
| height | number | auto | Canvas height (px) |
| xAxisLabel | string | "" | X-axis label |
| yAxisLabel | string | "" | Y-axis label |
| showGrid | boolean | true | Show grid lines |
| showLegend | boolean | true | Show legend |
| legendPosition | string | "top" | "top" \| "bottom" \| "left" \| "right" |
| interactive | boolean | true | Enable tooltips, zoom, pan |
| theme | string | "dark" | "dark" \| "light" |
| renderer | string | "webgl" | "canvas2d" \| "webgl" |

---

## Rendering Pipeline

```
Data Input
  │
  ▼
Validate (types, NaN handling)
  │
  ▼
Transform (filter, sort, aggregate — optional)
  │
  ▼
Scale Mapping (data domain → pixel coordinates)
  │
  ▼
Geometry Generation (build shapes)
  │
  ▼
Render (draw to canvas/WebGL)
  │
  ▼
Interact (tooltips, zoom, pan, selection)
```

---

## Export

| Format | Method | Quality |
|--------|--------|---------|
| PNG | Canvas toDataURL / WebGL readPixels | Lossless |
| SVG | Re-render to SVG context | Vector |
| JPEG | Canvas toDataURL('image/jpeg') | Lossy, smaller |

Clipboard: Ctrl+Shift+C (PNG), Ctrl+Shift+D (CSV data).

---

## Performance

| Technique | Description |
|-----------|-------------|
| LTTB Downsampling | Reduce >100k points to ~2,000 while preserving shape |
| WebGL Rendering | GPU-accelerated for large datasets |
| Geometry Caching | Cache computed shapes until data changes |
| Frame Caching | Cache static chart frames |
| Virtual Rendering | Only render visible portion of large charts |

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max series per chart | 10 |
| Max points per series (before downsampling) | 100,000 |
| Rendered points (after downsampling) | 2,000 |
| Max heatmap cells | 1,000,000 |
| Max network nodes | 1,000 |
| Animation duration | 300ms (configurable) |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Empty data | Show "No data" placeholder |
| All NaN/Inf | Show "No valid data" message |
| Single data point | Show point with tooltip (no axes needed) |
| WebGL unavailable | Fall back to Canvas 2D |
| Export fails | Show error, offer retry |

---

## Extension Points

- Custom chart types via Widget SDK.
- Custom color scales.
- Custom tooltip renderers.
- Custom export formats.
- Custom animation curves.
