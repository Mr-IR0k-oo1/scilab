# Scilab Studio — Visualization Engine Architecture

## 1. Overview

The Visualization Engine is the rendering backbone of Scilab Studio. It
translates data into interactive charts, graphs, dashboards, and 3D scenes.
The engine supports 30+ chart types out of the box, real-time streaming data,
WebGL-accelerated rendering for large datasets, and a plugin API for custom
visualization types. It integrates tightly with Scilab's plot functions while
providing a modern, hardware-accelerated rendering pipeline.

---

## 2. Engine Architecture

### 2.1 Renderer Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                   RENDERER PIPELINE                               │
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Data     │───▶│ Transform│───▶│  Scale   │───▶│  Layout  │  │
│  │  Ingest   │    │  (clean, │    │  (map    │    │  (axes,  │  │
│  │           │    │   filter,│    │   data to│    │   labels,│  │
│  │  Raw data │    │   aggr.) │    │  pixels) │    │  legends)│  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│                                                        │         │
│                                                        v         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Export   │◀───│ Animate  │◀───│ Interact │◀───│  Render  │  │
│  │  (PNG,   │    │  (trans- │    │  (events,│    │  (draw   │  │
│  │  SVG,    │    │  itions, │    │  tooltips│    │   to     │  │
│  │  PDF)    │    │  easing) │    │  zoom)   │    │  canvas) │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
  Source                Engine                    Output
  ------                ------                    ------

  Scilab variables -+
  CSV/Excel files  -+     +-------------+
  REST APIs        -+---->| Data        |    +--------------+
  MQTT streams     -+     | Processor   |--->| Rendered     |
  Manual input     -+     |             |    | Visualization|
  Digital Twin     -+     | - Parse     |    |              |
                          | - Validate  |    | - Canvas 2D  |
                          | - Transform |    | - WebGL      |
                          | - Sample    |    | - SVG        |
                          | - Aggregate |    | - Export     |
                          +-------------+    +--------------+
                                |
                                v
                          +-------------+
                          | Update      |
                          | Manager     |
                          |             |
                          | - Diff      |
                          | - Batch     |
                          | - Throttle  |
                          | - Debounce  |
                          +-------------+
```

### 2.3 Update Mechanism

```
  Data Change Detected
         |
         v
  +--------------------------+
  |  Diff Engine              |
  |  Compare new vs old data  |
  |  Determine minimal update |
  +----------+---------------+
             |
             v
  +--------------------------+
  |  Update Scheduler         |
  |                           |
  |  Batch updates within     |
  |  same frame (16ms)        |
  |                           |
  |  Priorities:              |
  |  - Immediate: user action |
  |  - High: animation        |
  |  - Normal: data update    |
  |  - Low: background recomp |
  +----------+---------------+
             |
             v
  +--------------------------+
  |  Render                  |
  |  Only re-render dirty    |
  |  regions (damage rect)   |
  +--------------------------+
```

---

## 3. Chart Types

### 3.1 Complete Catalog

| Category | Type | Description | Real-time |
|---|---|---|---|
| **Basic** | Line | XY line plot with markers | Yes |
| | Bar | Vertical/horizontal bars, grouped/stacked | Yes |
| | Scatter | Point plot with size/color encoding | Yes |
| | Area | Filled area under curves | Yes |
| | Pie | Circular proportion chart | No |
| | Donut | Pie with center cutout | No |
| **Statistical** | Histogram | Frequency distribution | Yes |
| | BoxPlot | Quartile distribution | Yes |
| | Violin | Density distribution | No |
| | ErrorBar | Data with error ranges | Yes |
| **Advanced** | Heatmap | Color-mapped 2D grid | Yes |
| | Bubble | Scatter with size dimension | Yes |
| | Radar | Multi-axis comparison | No |
| | Treemap | Hierarchical area chart | No |
| | Sunburst | Radial hierarchy | No |
| | Sankey | Flow/energy diagrams | No |
| **Engineering** | Gauge | Single-value dial | Yes |
| | GaugeLinear | Horizontal bar gauge | Yes |
| | Oscilloscope | Real-time waveform | Yes |
| | Spectrum | Frequency spectrum (FFT) | Yes |
| | Bode | Magnitude/phase plot | No |
| | Nyquist | Complex plane plot | No |
| | Nichols | Gain/phase plot | No |
| | PoleZero | Pole/zero constellation | No |
| | PhasePortrait | 2D phase space | Yes |
| **3D** | Surface | 3D surface plot | Yes |
| | Mesh | Wireframe mesh | Yes |
| | Volume | Volume rendering | No |
| | Contour | 2D contour from 3D data | Yes |
| | Bar3D | 3D bar chart | No |
| | Scatter3D | 3D scatter plot | Yes |
| **Network** | Graph | Node-edge network | No |
| | Chord | Circular flow diagram | No |
| **Geographic** | Map | GeoJSON rendering | No |
| | HeatmapOverlay | Spatial heatmap | Yes |
| **Dashboard** | SingleValue | KPI card | Yes |
| | MultiMetric | Multi-KPI panel | Yes |
| | Sparkline | Inline mini-chart | Yes |

### 3.2 Chart Type Registration

```
  Built-in charts are registered at startup.
  Custom charts are registered via plugin API:

  +---------------------------------------------+
  |  viz.registerChartType({                     |
  |    type: "custom-waterfall",                 |
  |    name: "Waterfall",                        |
  |    category: "Engineering",                  |
  |    icon: "waterfall.svg",                    |
  |                                              |
  |    defaultConfig: {                          |
  |      axes: { x: "category", y: "value" },   |
  |      colors: ["#4CAF50","#F44336","#2196F3"]|
  |      showConnectors: true,                   |
  |    },                                        |
  |                                              |
  |    dataSchema: {                             |
  |      required: ["categories", "values"],     |
  |      optional: ["colors", "connectors"],     |
  |    },                                        |
  |                                              |
  |    render: (ctx, data, config, dims) => {},  |
  |    interactions: { hover: "tooltip" },       |
  |    export: ["PNG", "SVG", "CSV"],            |
  |  });                                         |
  +---------------------------------------------+
```

---

## 4. Data Binding

### 4.1 Binding Model

```
  Data Source ---------> Binding ---------> Visual

  Binding Types:

  +-- Direct Binding -----------------------------------------+
  |  data -> chart                                            |
  |  When data changes, chart re-renders                     |
  +----------------------------------------------------------+

  +-- Computed Binding ---------------------------------------+
  |  data -> transform(fn) -> chart                           |
  |  Transform function applied before rendering             |
  +----------------------------------------------------------+

  +-- Multi-Source Binding -----------------------------------+
  |  data1 -+                                                 |
  |  data2 -+- merge(strategy) -> chart                      |
  |  data3 -+                                                 |
  |  Multiple data sources merged into one view               |
  +----------------------------------------------------------+

  +-- Scilab Variable Binding --------------------------------+
  |  engine.getVariable("x") -> chart                        |
  |  Polled or push-based updates from Scilab                |
  +----------------------------------------------------------+

  +-- Stream Binding -----------------------------------------+
  |  mqtt://topic -> buffer(window=1000) -> chart            |
  |  Sliding window over streaming data                       |
  +----------------------------------------------------------+
```

### 4.2 Binding API

```javascript
const chart = viz.createChart({
  type: "line",
  container: "#chart-container",

  // Direct data
  data: {
    x: [0, 1, 2, 3, 4],
    y: [0, 1, 4, 9, 16],
  },

  // Or bind to a data source
  bind: {
    source: "scilab:variable:x",
    poll: 100,
    transform: (data) => ({ x: data.t, y: data.y }),
  },

  // Or bind to a stream
  stream: {
    url: "mqtt://broker/sensor/temperature",
    buffer: 500,
    decode: "json",
    field: "value",
  },

  config: {
    title: "Temperature Over Time",
    xLabel: "Time (s)",
    yLabel: "Temperature (C)",
    grid: true,
    legend: true,
  },
});

chart.bind({ source: "dataframe:simulation_results",
             columns: ["time", "position"] });
chart.unbind();
```

---

## 5. Interactive Features

### 5.1 Interaction Map

```
+-- Zoom -------------------------------------------------------+
|  - Scroll wheel: zoom in/out at cursor                       |
|  - Pinch gesture: zoom (touch devices)                       |
|  - Zoom range: configurable min/max                          |
|  - Zoom reset: double-click or Ctrl+0                        |
|  - Axis-specific: lock one axis, zoom other                  |
+--------------------------------------------------------------+

+-- Pan --------------------------------------------------------+
|  - Click + drag: pan view                                    |
|  - Arrow keys: pan by fixed step                             |
|  - Momentum: continues after release                         |
+--------------------------------------------------------------+

+-- Hover ------------------------------------------------------+
|  - Tooltip: show data point values on hover                  |
|  - Crosshair: follow cursor across axes                      |
|  - Highlight: emphasize hovered series                       |
|  - Nearest point: snap to closest data point                 |
+--------------------------------------------------------------+

+-- Selection --------------------------------------------------+
|  - Click: select single data point                           |
|  - Shift+click: multi-select                                 |
|  - Box select: rubber-band area selection                    |
|  - Lasso select: freeform selection (2D scatter)             |
|  - Select events emitted for downstream processing           |
+--------------------------------------------------------------+

+-- Animation --------------------------------------------------+
|  - Transition: smooth data updates                           |
|  - Enter/exit: elements appear/disappear with animation      |
|  - Easing: linear, ease-in, ease-out, elastic, bounce       |
|  - Duration: configurable per element or globally            |
|  - Stagger: animate elements sequentially with delay         |
+--------------------------------------------------------------+

+-- Tooltip System ----------------------------------------------+
|  Positioning: auto, fixed, cursor, follow                    |
|  Content: template strings, custom render functions          |
|  Styling: inherits chart theme, customizable                 |
|  Trigger: hover, click, or manual                            |
+--------------------------------------------------------------+
```

### 5.2 Event API

```javascript
chart.on("zoom", (range) => {
  console.log("Zoomed to:", range);
});

chart.on("select", (points) => {
  engine.setVariable("selected", points);
});

chart.on("hover", (point) => {
  highlightRelatedData(point);
});

chart.on("click", (point, event) => {
  showContextMenu(point, event);
});

chart.on("brush", (region) => {
  filterData(region);
});
```

---

## 6. Real-Time Updates

### 6.1 Streaming Architecture

```
  Data Sources            Buffer              Renderer
  -------------           ------              --------

  MQTT --------+        +----------+        +--------------+
               +------->|  Ring    |------->|  Chart       |
  WebSocket ---+        |  Buffer  |        |  Renderer    |
                        |          |        |              |
  USB/Serial --+        |  window: |        |  Throttle:   |
               |        |  N points|        |  60 FPS max  |
  Scilab ------+        |          |        |              |
               +------->|  down-   |        |  Only dirty  |
  File Watch --+        |  sample: |        |  regions     |
               |        |  auto    |        |  re-rendered |
  Timer --------+       +----------+        +--------------+

  Update Strategies:
  +---------------------------------------------------+
  |  Strategy          | When to Use                  |
  |  ----------        | ----------                  |
  |  Replace           | New data replaces old       |
  |  Append            | Add new points, trim old    |
  |  Merge             | Update existing in-place    |
  |  Replace+Scroll    | Replace with auto-scroll    |
  +---------------------------------------------------+
```

### 6.2 Oscilloscope Mode

```json
{
  "type": "oscilloscope",
  "channels": [
    { "name": "CH1", "color": "#00FF00", "source": "mqtt://ch1" },
    { "name": "CH2", "color": "#FF6600", "source": "mqtt://ch2" }
  ],
  "timeWindow": 10,
  "sampleRate": 10000,
  "triggerLevel": 0,
  "triggerEdge": "rising",
  "persistence": 0.5,
  "gridStyle": "engineering",
  "cursors": "both"
}
```

**Oscilloscope features:**
- Multi-channel overlay with configurable colors
- Adjustable time base (ms/div to s/div)
- Trigger holdoff and edge selection
- FFT analysis view toggle
- Measurement cursors (dt, dV, frequency, RMS)
- Export to CSV for offline analysis

### 6.3 Frame Budget Management

```
  Real-time data arrives at 10kHz
  Display updates at 60 FPS (16.67ms)

  +---------------------------------------------------+
  |  Data arrives: 10,000 samples/second              |
  |                                                    |
  |  Buffer strategy:                                 |
  |  +----------------------------------------------+|
  |  |  Raw:  [1,2,3,4,5,6,7,8,9,10,...]           ||
  |  |  | Downsample (LTTB algorithm)               ||
  |  |  v                                           ||
  |  |  Display: [1, 3.5, 5.2, 7.8, ...]           ||
  |  |  (reduced to display resolution ~1920 pts)   ||
  |  +----------------------------------------------+|
  |                                                    |
  |  Render pipeline per frame:                       |
  |  [Input] -> [Downsample] -> [Transform] -> [Draw] |
  |    0ms       1ms            2ms          8ms      |
  |  Total: ~11ms (within 16.67ms budget)            |
  +---------------------------------------------------+
```

---

## 7. Custom Visualization API

### 7.1 Creating a Custom Chart Type

```typescript
import { ChartType, RenderContext } from "@scilab-studio/viz-api";

export const WaterfallChart: ChartType = {
  type: "waterfall",
  name: "Waterfall",
  category: "Engineering",
  icon: "waterfall",

  dataSchema: {
    required: { labels: "string[]", values: "number[]" },
    optional: { colors: "string[]", connectors: "boolean" },
  },

  defaults: {
    width: 600,
    height: 400,
    padding: { top: 40, right: 40, bottom: 60, left: 80 },
    axes: {
      x: { label: "", rotation: 0 },
      y: { label: "Value", grid: true },
    },
    colors: {
      increase: "#4CAF50",
      decrease: "#F44336",
      total: "#2196F3",
      connector: "#999999",
    },
    animation: { duration: 300, easing: "ease-out" },
  },

  render(ctx: RenderContext) {
    const { canvas, data, config, scales } = ctx;
    const context = canvas.getContext("2d");

    // Calculate cumulative values
    let cumulative = 0;
    const segments = data.values.map((v, i) => {
      const start = cumulative;
      cumulative += v;
      return { index: i, start, end: cumulative, value: v };
    });

    // Draw each bar
    segments.forEach((seg) => {
      const color = seg.value >= 0
        ? config.colors.increase
        : config.colors.decrease;
      const x = scales.x(seg.index);
      const yTop = scales.y(Math.max(seg.start, seg.end));
      const yBot = scales.y(Math.min(seg.start, seg.end));
      context.fillStyle = color;
      context.fillRect(x, yTop, scales.x.bandwidth(), yBot - yTop);
    });

    // Draw connector lines
    if (config.connectors !== false) {
      context.strokeStyle = config.colors.connector;
      context.setLineDash([4, 4]);
      segments.forEach((seg, i) => {
        if (i < segments.length - 1) {
          const x1 = scales.x(seg.index) + scales.x.bandwidth();
          const y1 = scales.y(seg.end);
          const x2 = scales.x(seg.index + 1);
          context.beginPath();
          context.moveTo(x1, y1);
          context.lineTo(x2, y1);
          context.stroke();
        }
      });
      context.setLineDash([]);
    }
  },
};
```

### 7.2 Render Context Interface

```typescript
interface RenderContext {
  canvas: HTMLCanvasElement;
  width: number;
  height: number;
  data: ChartData;
  config: ChartConfig;
  scales: {
    x: any;  // d3-like scale
    y: any;
    color: any;
    size: any;
  };
  theme: ThemeDefinition;
  interaction: InteractionState;
  animation: AnimationState;
}
```

---

## 8. Export Formats

### 8.1 Format Support

| Format | Charts | 3D | Interactive | Vector | Quality |
|---|---|---|---|---|---|
| PNG | Yes | Yes | No | No | Raster (configurable DPI) |
| SVG | Yes | No | Partial | Yes | Infinite scale |
| PDF | Yes | Yes | No | Yes | Print quality |
| HTML | Yes | Yes | Yes | N/A | Fully interactive |
| CSV | Yes (data) | No | No | No | Raw data |
| JSON | Yes (config) | No | No | No | Full state |
| WebP | Yes | Yes | No | No | Smaller than PNG |

### 8.2 Export API

```javascript
// Export as PNG with custom DPI
const pngBlob = await chart.export("png", {
  scale: 3,              // 3x resolution for print
  background: "#ffffff", // Override transparent background
  padding: 20,
});

// Export as interactive HTML
const htmlString = await chart.export("html", {
  includeData: true,     // Embed data in HTML
  title: "My Chart",
  theme: "dark",
});

// Export as SVG for editing in Illustrator/Inkscape
const svgString = await chart.export("svg", {
  fonts: "embed",        // Embed fonts in SVG
  simplify: true,        // Optimize path data
});

// Export chart data as CSV
const csvString = await chart.export("csv", {
  delimiter: ",",
  headers: true,
  precision: 4,
});
```

---

## 9. Performance Optimization

### 9.1 Large Dataset Strategies

| Strategy | Threshold | Description |
|---|---|---|
| **LTTB Downsampling** | >10K points | Largest Triangle Three Buckets preserves shape |
| **Canvas Batching** | All | Batch draw calls to minimize state changes |
| **Virtual Rendering** | >50K points | Only render visible data points |
| **WebGL Renderer** | >100K points | GPU-accelerated point/line rendering |
| **Level of Detail** | Zoom-dependent | Simplify geometry at low zoom levels |
| **Offscreen Canvas** | All | Render in worker, transfer bitmap |
| **Damage Region** | All | Only repaint changed areas |

### 9.2 WebGL Renderer

```
  +-----------------------------------------------------------+
  |  WebGL Renderer (for large datasets)                       |
  |                                                             |
  |  CPU Path (default):                                        |
  |  Data -> JS Processing -> Canvas 2D API -> Display          |
  |                                                             |
  |  GPU Path (>100K points):                                   |
  |  Data -> Buffer Upload -> Vertex Shader -> Fragment Shader  |
  |        -> Framebuffer -> Display                             |
  |                                                             |
  |  WebGL Advantages:                                          |
  |  - Hardware-accelerated point rendering                     |
  |  - Efficient line rendering with anti-aliasing              |
  |  - Supports millions of data points                         |
  |  - Smooth zoom/pan via GPU transforms                       |
  |  - Shared GPU memory for multiple charts                    |
  +-----------------------------------------------------------+
```

### 9.3 Memory Management

```
  +-----------------------------------------------------------+
  |  Memory Strategy                                           |
  |                                                             |
  |  Per chart budget: 50 MB (configurable)                    |
  |                                                             |
  |  Breakdown:                                                 |
  |  - Data buffers:     30 MB (raw + processed)               |
  |  - Canvas buffers:   10 MB (front + back)                  |
  |  - Interaction state: 5 MB (selections, hover)            |
  |  - Animation state:   5 MB (tweens, transitions)          |
  |                                                             |
  |  Eviction policy (LRU):                                    |
  |  - When budget exceeded, least-recently-used chart          |
  |    data is evicted from memory                              |
  |  - Evicted data can be reloaded from source                 |
  |  - User notified when eviction occurs                       |
  +-----------------------------------------------------------+
```

---

## 10. Theme System

### 10.1 Chart Theme Structure

```json
{
  "name": "Engineering Dark",
  "chart": {
    "background": "#1a1a2e",
    "border": "#333366",
    "padding": 40
  },
  "axes": {
    "line": "#666688",
    "tick": "#888899",
    "label": "#ccccdd",
    "title": "#ffffff",
    "grid": "#333355",
    "gridLineDash": [4, 4]
  },
  "series": {
    "palette": [
      "#00d4ff", "#ff6b6b", "#51cf66", "#ffd43b",
      "#cc5de8", "#ff922b", "#20c997", "#748ffc"
    ],
    "lineWidth": 2,
    "pointRadius": 3,
    "areaOpacity": 0.3
  },
  "tooltip": {
    "background": "rgba(26, 26, 46, 0.95)",
    "text": "#ffffff",
    "border": "#333366",
    "shadow": "0 4px 12px rgba(0,0,0,0.3)"
  },
  "legend": {
    "text": "#ccccdd",
    "itemSpacing": 12
  },
  "annotation": {
    "line": "#ff6b6b",
    "text": "#ff6b6b",
    "background": "rgba(255,107,107,0.1)"
  }
}
```

### 10.2 Built-in Chart Themes

| Theme | Background | Palette Style | Use Case |
|---|---|---|---|
| Dark | #1a1a2e | Neon/bright | Default, low-light |
| Light | #ffffff | Muted/professional | Print, bright rooms |
| Engineering | #0d1117 | High contrast | Instrument panels |
| Scilab Classic | #f0f0f0 | Scilab defaults | Compatibility |
| Solarized Dark | #002b36 | Solarized | Eye comfort |
| Solarized Light | #fdf6e3 | Solarized | Eye comfort |
| High Contrast | #000000 | White/yellow | Accessibility |

---

## 11. Integration with Scilab Plot Functions

### 11.1 Mapping Table

| Scilab Function | Studio Chart Type | Notes |
|---|---|---|
| `plot()` / `plot2d()` | Line | Direct mapping |
| `plot3d()` / `plot3d1()` | Surface / Mesh | 3D rendering |
| `bar()` | Bar | Customizable bar chart |
| `histplot()` | Histogram | Frequency distribution |
| `scatter()` / `plot2d` with flags | Scatter | Point cloud |
| `contour()` / `contour2D` | Contour | Level curves |
| `mesh()` | Mesh | Wireframe surface |
| `champ()` | Vector Field | Arrows on 2D grid |
| `grayplot()` | Heatmap | Color-mapped grid |
| `hist3d()` | Bar3D | 3D histogram |
| `polarplot()` | Radar/Polar | Radial coordinates |
| `semilogx()` / `semilogy()` | Line (log scale) | Log axes |
| `loglog()` | Line (log-log) | Both axes log |

### 11.2 Automatic Conversion

```scilab
// Scilab script
x = linspace(0, 2*%pi, 100);
y = sin(x);
plot(x, y);
title("Sine Wave");
xlabel("Time");
ylabel("Amplitude");
```

The visualization engine captures Scilab's plot commands and renders them
through its own pipeline, adding interactivity (zoom, pan, tooltip) that
native Scilab graphics lack:

```
  Scilab plot() call
       |
       v
  +------------------+
  | Plot Interceptor |  Captures plot commands via graphics hooks
  +--------+---------+
           |
           v
  +------------------+
  | Config Builder   |  Translates Scilab plot config to chart config
  +--------+---------+
           |
           v
  +------------------+
  | Viz Engine       |  Renders with full interactivity
  | (Canvas/WebGL)   |
  +------------------+
```

---

## 12. 3D Visualization

### 12.1 3D Rendering Pipeline

```
+-----------------------------------------------------------+
|  3D Rendering Pipeline                                     |
|                                                             |
|  +-----------+    +-----------+    +-----------+           |
|  | Mesh Data |--->| Transform |--->| Clip &   |           |
|  | (vertices,|    | (model,   |    | Cull     |           |
|  |  normals, |    |  view,    |    | (frustum)|           |
|  |  indices) |    |  project) |    |           |           |
|  +-----------+    +-----------+    +-----+-----+           |
|                                          |                  |
|                                          v                  |
|  +-----------+    +-----------+    +-----------+           |
|  | Display   |<---| Lighting |<---| Rasterize |           |
|  |           |    | (Phong,  |    | (fill,    |           |
|  |           |    |  flat)   |    |  shade)   |           |
|  +-----------+    +-----------+    +-----------+           |
+-----------------------------------------------------------+
```

### 12.2 3D Features

| Feature | Description |
|---|---|
| Surface rendering | Shaded surfaces with configurable lighting |
| Wireframe mode | Mesh overlay or standalone wireframe |
| Volume rendering | Ray-casting for 3D scalar fields |
| Isosurface extraction | Marching cubes for threshold surfaces |
| Camera controls | Orbit, pan, zoom, reset |
| Cross-section | Clip planes along any axis |
| Color mapping | 20+ colormaps (viridis, magma, jet, etc.) |
| Multiple views | Split screen with linked cameras |

### 12.3 Scilab 3D Integration

```scilab
// Scilab 3D plot captured by visualization engine
[X, Y] = meshgrid(-3:0.1:3, -3:0.1:3);
Z = sin(sqrt(X.^2 + Y.^2));
plot3d(X, Y, Z);
// Rendered through WebGL with:
// - Orbit camera controls
// - Mouse wheel zoom
// - Real-time rotation
// - Exportable as PNG/SVG/PDF
```

---

## 13. Engineering-Specific Visualizations

### 13.1 Built-in Engineering Types

| Visualization | Description | Data Format |
|---|---|---|
| **Power Flow Diagram** | Sankey diagram for energy flow | Node + flow values |
| **Single Line Diagram** | Electrical system topology | Components + connections |
| **P&ID Diagram** | Piping and instrumentation | Symbols + connections |
| **Bode Plot** | Frequency response (magnitude + phase) | freq[], mag[], phase[] |
| **Nyquist Plot** | Complex frequency response | real[], imag[] |
| **Pole-Zero Map** | System stability visualization | poles[], zeros[] |
| **Phase Portrait** | Dynamic system behavior | x[], y[], dx[], dy[] |
| **Spectrogram** | Time-frequency analysis | time[], freq[], power[][] |
| **GIS Overlay** | Geographic data on maps | GeoJSON + data layers |
| **Trend Lines** | Historical data over time | timestamp[], values[] |
| **Alarm Summary** | Active alarms table | alarm_id, priority, time |
| **Gauge Panel** | Multi-instrument dashboard | value, min, max per gauge |

### 13.2 Power Flow Diagram Example

```javascript
viz.createChart({
  type: "sankey",
  data: {
    nodes: [
      { id: "grid", label: "Grid Input", value: 500 },
      { id: "transformer", label: "Transformer", value: 480 },
      { id: "bus1", label: "Bus 1", value: 200 },
      { id: "bus2", label: "Bus 2", value: 180 },
      { id: "bus3", label: "Bus 3", value: 100 },
      { id: "load1", label: "Motor Load", value: 150 },
      { id: "load2", label: "HVAC", value: 120 },
      { id: "loss", label: "Losses", value: 20 },
    ],
    links: [
      { source: "grid", target: "transformer", value: 500 },
      { source: "transformer", target: "bus1", value: 200 },
      { source: "transformer", target: "bus2", value: 180 },
      { source: "transformer", target: "bus3", value: 100 },
      { source: "transformer", target: "loss", value: 20 },
      { source: "bus1", target: "load1", value: 150 },
      { source: "bus2", target: "load2", value: 120 },
    ],
  },
  config: {
    title: "Campus Power Flow",
    nodeColor: "#2196F3",
    linkColor: "source",
    units: "kW",
  },
});
```

### 13.3 Dashboard Composition

```
  +-----------------------------------------------------------+
  |  Engineering Dashboard                                      |
  |                                                             |
  |  +------------------+  +------------------+               |
  |  | SingleValue      |  | Gauge            |               |
  |  | "Total Load"     |  | "Voltage"        |               |
  |  | 1,247 kW        |  | [   480 V   ]    |               |
  |  +------------------+  +------------------+               |
  |                                                             |
  |  +------------------------------------------+              |
  |  | Oscilloscope                              |              |
  |  | ~~~~CH1~~~~~~CH2~~~~                      |              |
  |  | ~~~~~~~~~~~~~~~~~~~~~~~                   |              |
  |  +------------------------------------------+              |
  |                                                             |
  |  +------------------+  +------------------+               |
  |  | Trend Line       |  | Alarm Table      |               |
  |  | (24h history)    |  | [3 active]       |               |
  |  |                  |  | CRITICAL: P-201  |               |
  |  |  /\  /\          |  | WARNING: T-105   |               |
  |  | /  \/  \         |  | INFO: F-301      |               |
  |  +------------------+  +------------------+               |
  +-----------------------------------------------------------+
```

---

*This document defines the visualization engine architecture for Scilab Studio.
All chart types, rendering pipelines, and data binding must conform to these
specifications.*
