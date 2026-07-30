# Visualization Development

Create custom chart types for the Visualization Engine.

## Visualization Structure

```
my-chart/
├── viz.json           # Manifest (required)
├── index.js           # Entry point (required)
├── renderer.js        # Rendering logic
├── styles.css         # Optional styles
├── README.md          # Documentation
└── test/
    └── index.test.js  # Tests
```

## Manifest (viz.json)

```json
{
  "id": "com.example.waterfall",
  "name": "Waterfall Chart",
  "version": "1.0.0",
  "description": "A waterfall chart for cumulative data",
  "author": "Author Name",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "type": "waterfall",
  "category": "engineering",
  "tags": ["waterfall", "cumulative", "engineering"]
}
```

## Entry Point

```javascript
const WaterfallRenderer = require('./renderer');

module.exports = {
  type: 'waterfall',
  name: 'Waterfall Chart',
  icon: 'chart-waterfall',
  category: 'engineering',
  version: '1.0.0',

  options: {
    title: { type: 'string', default: '' },
    xlabel: { type: 'string', default: '' },
    ylabel: { type: 'string', default: '' },
    grid: { type: 'boolean', default: true },
    showValues: { type: 'boolean', default: true },
    positiveColor: { type: 'color', default: '#4CAF50' },
    negativeColor: { type: 'color', default: '#f44336' },
    connectorColor: { type: 'color', default: '#666666' }
  },

  dataRequirements: {
    columns: { min: 2, max: 2 },
    types: ['number', 'number']
  },

  render: WaterfallRenderer.render,
  export: WaterfallRenderer.export
};
```

## Renderer

```javascript
// renderer.js
class WaterfallRenderer {
  static render(canvas, data, options, theme) {
    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    // Clear
    ctx.clearRect(0, 0, width, height);

    // Calculate layout
    const padding = { top: 40, right: 20, bottom: 60, left: 60 };
    const plotWidth = width - padding.left - padding.right;
    const plotHeight = height - padding.top - padding.bottom;

    // Extract data
    const labels = data.columns[0].values;
    const values = data.columns[1].values;

    // Calculate cumulative
    const cumulative = [];
    let running = 0;
    for (const v of values) {
      cumulative.push(running);
      running += v;
    }

    // Draw bars
    const barWidth = plotWidth / labels.length * 0.6;
    const gap = plotWidth / labels.length * 0.4;

    for (let i = 0; i < labels.length; i++) {
      const x = padding.left + i * (barWidth + gap) + gap / 2;
      const yStart = padding.top + this.scaleY(cumulative[i], values, plotHeight);
      const yEnd = padding.top + this.scaleY(cumulative[i] + values[i], values, plotHeight);
      const barHeight = yEnd - yStart;

      // Draw bar
      ctx.fillStyle = values[i] >= 0
        ? options.positiveColor
        : options.negativeColor;
      ctx.fillRect(x, Math.min(yStart, yEnd), barWidth, Math.abs(barHeight));

      // Draw connector
      if (i < labels.length - 1) {
        ctx.strokeStyle = options.connectorColor;
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(x + barWidth, yEnd);
        ctx.lineTo(x + barWidth + gap, yEnd);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // Draw label
      ctx.fillStyle = theme.text.primary;
      ctx.font = `${theme.typography.sizes.sm} ${theme.typography.fontFamily}`;
      ctx.textAlign = 'center';
      ctx.fillText(labels[i], x + barWidth / 2, height - padding.bottom + 20);
    }

    // Draw axes
    this.drawAxes(ctx, padding, plotWidth, plotHeight, theme);

    // Draw title
    if (options.title) {
      ctx.fillStyle = theme.text.primary;
      ctx.font = `bold ${theme.typography.sizes.lg} ${theme.typography.fontFamily}`;
      ctx.textAlign = 'center';
      ctx.fillText(options.title, width / 2, 20);
    }
  }

  static scaleY(value, values, plotHeight) {
    const max = Math.max(...values.map(Math.abs));
    return plotHeight / 2 - (value / (max * 2)) * plotHeight;
  }

  static drawAxes(ctx, padding, plotWidth, plotHeight, theme) {
    ctx.strokeStyle = theme.border;
    ctx.lineWidth = 1;

    // X axis
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top + plotHeight);
    ctx.lineTo(padding.left + plotWidth, padding.top + plotHeight);
    ctx.stroke();

    // Y axis
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top);
    ctx.lineTo(padding.left, padding.top + plotHeight);
    ctx.stroke();
  }

  static export(canvas, data, options, format) {
    if (format === 'png') {
      return canvas.toDataURL('image/png');
    }
    if (format === 'svg') {
      // Convert canvas to SVG
      return this.canvasToSVG(canvas);
    }
    if (format === 'csv') {
      return this.dataToCSV(data);
    }
  }
}

module.exports = WaterfallRenderer;
```

## Data Flow

```
Data Source → Expression Evaluation → Data Transform → Chart Render → Canvas Output
```

1. **Data Source**: Scilab variable, inline data, or file.
2. **Expression Evaluation**: Scilab expressions evaluated asynchronously.
3. **Data Transform**: Normalize, filter, aggregate.
4. **Chart Render**: Call your render function.
5. **Canvas Output**: Display or export.

## Theme Integration

The renderer receives the current theme:

```javascript
render(canvas, data, options, theme) {
  // theme.colors.background.primary
  // theme.colors.text.primary
  // theme.typography.fontFamily
  // theme.spacing.md
  // etc.
}
```

Use theme values for consistent appearance across themes.

## Performance

| Dataset Size | Target |
|-------------|--------|
| 1,000 points | < 16ms |
| 10,000 points | < 100ms |
| 100,000 points | < 500ms (progressive) |

Optimization strategies:
- Use requestAnimationFrame for animations.
- Batch canvas operations.
- Use offscreen canvas for complex calculations.
- Downsample large datasets.

## Testing

```bash
# Visual regression tests
scilab-studio test --visual

# Performance tests
scilab-studio test --perf

# Accessibility tests
scilab-studio test --a11y
```

## Best Practices

- Handle empty datasets gracefully.
- Support both dark and light themes.
- Use theme colors, not hard-coded values.
- Make charts interactive (hover, click, zoom).
- Export to multiple formats (PNG, SVG, CSV).
- Document data requirements clearly.
