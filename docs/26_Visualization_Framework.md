# 26 — Visualization Framework

Instead of exposing plotting functions, build a visualization engine. Every chart follows the same pipeline:

```
Data
  │
  ▼
Transformation
  │
  ▼
Theme
  │
  ▼
Renderer
  │
  ▼
Interaction
```

For the Visualization Studio feature, see [Feature Modules §2.3](05_Feature_Modules.md).

---

## 1. Rendering Architecture

### 1.1 Renderer Selection

| Backend | Use Case | Trade-offs |
|---------|----------|------------|
| **Canvas 2D** | Small datasets (< 10k points) | Faster initial render, no GPU |
| **WebGL** | Large datasets (> 10k points) | Faster for large data, requires GPU |

Default: WebGL (falls back to Canvas 2D if unavailable). Configurable in settings.

### 1.2 Pipeline

```
Data Input → Validate → Transform → Scale Mapping → Geometry → Render → Interact
```

1. **Data arrives** — from Scilab, imported file, or API.
2. **Validate** — correct types, handle NaN/Inf.
3. **Transform** — filter, sort, aggregate (optional).
4. **Scale mapping** — map data domain to pixel coordinates.
5. **Geometry generation** — build shapes (lines, bars, points, cells).
6. **Render** — draw to Canvas 2D or WebGL context.
7. **Interact** — tooltips, zoom, pan, selection.

---

## 2. Supported Charts (v0.1)

### 2.1 Line

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | ChartData | — | X/Y series |
| `lineWidth` | number | `2` | Stroke width (px) |
| `smooth` | boolean | `false` | Bezier interpolation |
| `showPoints` | boolean | `false` | Draw markers |
| `fillArea` | boolean | `false` | Fill under line |
| `stacked` | boolean | `false` | Stack multiple series |

```typescript
// Simple
{ series: [{ name: "Temp", data: [20, 22, 21, 25] }] }

// Explicit X
{ series: [{ name: "Temp", data: [{ x: 0, y: 20 }, { x: 1, y: 22 }] }] }

// Multiple series
{
  labels: ["Jan", "Feb", "Mar"],
  series: [
    { name: "Temp", data: [20, 22, 21], color: "#ff6384" },
    { name: "Humidity", data: [65, 70, 68], color: "#36a2eb" }
  ]
}
```

### 2.2 Scatter

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `pointSize` | number | `5` | Marker radius |
| `pointShape` | string | `"circle"` | `"circle"` \| `"square"` \| `"triangle"` \| `"cross"` |
| `showLabels` | boolean | `false` | Point labels |
| `colorScale` | string | — | Color by value |

### 2.3 Surface (3D)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | SurfaceData | — | Z matrix with optional X/Y vectors |
| `wireframe` | boolean | `false` | Show wireframe overlay |
| `colormap` | string | `"viridis"` | Color mapping |
| `elevation` | number | `30` | Camera elevation (degrees) |
| `azimuth` | number | `45` | Camera azimuth (degrees) |

```typescript
interface SurfaceData {
  x?: number[];                     // Optional X axis values
  y?: number[];                     // Optional Y axis values
  z: number[][];                    // Z values matrix
}
```

### 2.4 Heatmap

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | HeatmapData | — | Matrix data |
| `colorScale` | string | `"viridis"` | Color mapping |
| `showValues` | boolean | `false` | Show value in cells |
| `interpolate` | boolean | `true` | Smooth transitions |

```typescript
interface HeatmapData {
  rows: string[];
  columns: string[];
  values: number[][];
}
```

Color scales: `"viridis"`, `"plasma"`, `"inferno"`, `"magma"`, `"cividis"`, `"hot"`, `"cool"`, `"rainbow"`.

### 2.5 Sankey

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | SankeyData | — | Nodes and links |
| `nodePadding` | number | `10` | Space between nodes |
| `nodeWidth` | number | `20` | Node width |
| `align` | string | `"justify"` | `"left"` \| `"right"` \| `"center"` \| `"justify"` |

```typescript
interface SankeyData {
  nodes: { name: string; color?: string }[];
  links: { source: number; target: number; value: number; color?: string }[];
}
```

### 2.6 Network

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | NetworkData | — | Nodes and edges |
| `layout` | string | `"force"` | `"force"` \| `"circular"` \| `"tree"` |
| `directed` | boolean | `false` | Show arrows |
| `nodeSize` | number | `5` | Default node radius |

```typescript
interface NetworkData {
  nodes: { id: string; label?: string; size?: number; color?: string }[];
  edges: { source: string; target: string; weight?: number; label?: string }[];
}
```

### 2.7 Radar

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | RadarData | — | Axes and series |
| `filled` | boolean | `true` | Fill area |
| `maxValue` | number | auto | Maximum axis value |

```typescript
interface RadarData {
  axes: string[];
  series: { name: string; data: number[]; color?: string }[];
}
```

### 2.8 Gauge

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `value` | number | — | Current value |
| `min` | number | `0` | Minimum |
| `max` | number | `100` | Maximum |
| `unit` | string | `""` | Unit label |
| `color` | string | `"#4CAF50"` | Arc color |
| `showValue` | boolean | `true` | Display value |

### 2.9 Histogram

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | number[] | — | Values to bin |
| `bins` | number \| "auto" | `"auto"` | Number of bins |
| `binWidth` | number | — | Bin width (overrides bins count) |
| `normalized` | boolean | `false` | Normalize to probability density |
| `showCurve` | boolean | `false` | Overlay KDE curve |

### 2.10 Waterfall

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `data` | WaterfallData | — | Categories and values |
| `showTotal` | boolean | `true` | Show total bar |
| `increasingColor` | string | `"#4CAF50"` | Positive color |
| `decreasingColor` | string | `"#f44336"` | Negative color |
| `totalColor` | string | `"#2196F3"` | Total bar color |

```typescript
interface WaterfallData {
  categories: string[];
  values: number[];
  totals?: boolean[];               // Which bars are totals
}
```

---

## 3. Common Chart Options

```typescript
interface ChartOptions {
  title?: string;
  subtitle?: string;
  width?: number;
  height?: number;
  padding?: { top: number; right: number; bottom: number; left: number };

  // Axes
  xAxisLabel?: string;
  yAxisLabel?: string;
  xAxisMin?: number;
  xAxisMax?: number;
  yAxisMin?: number;
  yAxisMax?: number;
  xLogScale?: boolean;
  yLogScale?: boolean;

  // Grid
  showGrid?: boolean;
  gridColor?: string;
  tickCount?: number;
  tickFormat?: string;

  // Legend
  showLegend?: boolean;
  legendPosition?: "top" | "bottom" | "left" | "right";

  // Interaction
  interactive?: boolean;
  tooltip?: boolean;
  zoom?: boolean;
  pan?: boolean;
  select?: boolean;

  // Theme
  theme?: "dark" | "light" | "system";
  renderer?: "canvas2d" | "webgl";
}
```

---

## 4. Theming

### Dark Theme (default)

```jsonc
{
  "background": "#1e1e1e",
  "text": "#e0e0e0",
  "grid": "#404040",
  "axes": "#606060",
  "series": ["#4a9eff", "#ff6384", "#4caf50", "#ff9800", "#9c27b0", "#00bcd4", "#e91e63", "#8bc34a"]
}
```

### Light Theme

```jsonc
{
  "background": "#ffffff",
  "text": "#333333",
  "grid": "#e0e0e0",
  "axes": "#cccccc",
  "series": ["#2196f3", "#e91e63", "#4caf50", "#ff9800", "#9c27b0", "#00bcd4", "#f44336", "#8bc34a"]
}
```

### Custom Themes

Users can define custom themes in Visualization Studio settings.

---

## 5. Export

| Format | Method | Quality |
|--------|--------|---------|
| PNG | Canvas `toDataURL()` / WebGL readPixels | Lossless |
| SVG | Re-render to SVG context | Vector |
| JPEG | Canvas `toDataURL('image/jpeg')` | Lossy, smaller |

```typescript
interface ExportOptions {
  format: "png" | "svg" | "jpeg";
  width?: number;
  height?: number;
  scale?: number;          // Resolution multiplier (default 2 for retina)
  quality?: number;        // JPEG quality (0–1)
  background?: string;     // Background color
}
```

Clipboard: Ctrl+Shift+C (PNG), Ctrl+Shift+D (CSV data).

---

## 6. Data Binding

Charts can be bound to:
- **Scilab variables** — Live update as computations run.
- **Data imports** — Update when file changes.
- **Event payloads** — Update on event.

Update frequency: `on-change`, `on-tick` (configurable interval), or `manual`.

---

## 7. Performance

### LTTB Downsampling

For datasets > 100,000 points, the renderer uses Largest Triangle Three Buckets to reduce rendered points to ~2,000 while preserving visual shape.

### WebGL Optimization

- Points rendered as GL_POINTS (up to 10M at 60fps).
- Lines as GL_LINE_STRIP.
- Bars as instanced quads.
- Heatmaps as textured quads.

### Caching

- Computed scales cached until data/options change.
- Geometry buffers cached per dataset.
- Static chart frames cached.
