# Visualization API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.1 |
| Stability | Stable |

---

## Purpose

Creates, configures, and exports charts.

## Methods

### viz.createChart(type: string, data: DataDescriptor, options?: ChartOptions): Promise\<Chart\>

Creates a new chart.

```javascript
const chart = await viz.createChart('line', {
  source: 'scilab',
  expression: 't = 0:0.1:10; y = sin(t); [t, y]'
}, {
  title: 'Sine Wave',
  xlabel: 'Time',
  ylabel: 'Amplitude'
});
```

### viz.getChart(chartId: string): Chart | null

Returns a chart by ID.

```javascript
const chart = viz.getChart('chart-abc123');
console.log(chart.type); // "line"
```

### viz.updateChart(chartId: string, options: Partial\<ChartOptions\>): Promise\<void\>

Updates chart options.

```javascript
await viz.updateChart('chart-abc123', {
  title: 'Updated Title',
  grid: true
});
```

### viz.updateChartData(chartId: string, data: DataDescriptor): Promise\<void\>

Updates chart data.

```javascript
await viz.updateChartData('chart-abc123', {
  source: 'scilab',
  expression: 'y2 = cos(t); [t, y2]'
});
```

### viz.destroyChart(chartId: string): void

Destroys a chart.

```javascript
viz.destroyChart('chart-abc123');
```

### viz.exportChart(chartId: string, options: ExportOptions): Promise\<Blob\>

Exports a chart to a file format.

```javascript
const png = await viz.exportChart('chart-abc123', {
  format: 'png',
  width: 800,
  height: 600,
  dpi: 150
});
```

### viz.getSupportedTypes(): string[]

Returns all supported chart types.

```javascript
const types = viz.getSupportedTypes();
console.log(types); // ["line", "scatter", "bar", "heatmap", ...]
```

### viz.setTheme(themeId: string): void

Sets the chart theme.

```javascript
viz.setTheme('dark');
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `viz:chartCreated` | `{ chart: Chart }` | Chart was created |
| `viz:chartUpdated` | `{ chart: Chart }` | Chart was updated |
| `viz:chartDestroyed` | `{ chartId: string }` | Chart was destroyed |
| `viz:chartError` | `{ chartId: string, error: Error }` | Chart encountered an error |
| `viz:chartClicked` | `{ chartId: string, point: DataPoint }` | Data point was clicked |
| `viz:chartHovered` | `{ chartId: string, point: DataPoint }` | Data point was hovered |

## Examples

### Create and Export

```javascript
// Create chart
const chart = await viz.createChart('scatter', {
  source: 'inline',
  columns: [
    { name: 'x', values: [1, 2, 3, 4, 5] },
    { name: 'y', values: [2, 4, 5, 4, 5] }
  ]
}, {
  title: 'Scatter Plot',
  xlabel: 'X',
  ylabel: 'Y'
});

// Export as PNG
const blob = await viz.exportChart(chart.id, { format: 'png' });
```

### Interactive Chart

```javascript
const chart = await viz.createChart('line', {
  source: 'scilab',
  expression: 'x = 0:0.1:10; y = sin(x); [x, y]'
});

// Listen for interactions
viz.on('viz:chartClicked', (event) => {
  if (event.chartId === chart.id) {
    console.log(`Clicked: ${event.point.x}, ${event.point.y}`);
  }
});
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `ChartNotFound` | VZ-001 | Chart ID does not exist |
| `InvalidChartType` | VZ-002 | Chart type is not supported |
| `InvalidData` | VZ-003 | Data format is invalid |
| `RenderError` | VZ-004 | Chart rendering failed |
| `ExportError` | VZ-005 | Chart export failed |
| `ScilabError` | VZ-006 | Scilab expression evaluation failed |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
