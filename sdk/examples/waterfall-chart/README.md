# Example: Waterfall Chart

A custom waterfall chart visualization.

## Files

```
waterfall-chart/
├── viz.json
├── index.js
├── renderer.js
└── README.md
```

## viz.json

```json
{
  "id": "com.example.waterfall",
  "name": "Waterfall Chart",
  "version": "1.0.0",
  "description": "A waterfall chart for cumulative data",
  "author": "Scilab Studio Team",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "type": "waterfall",
  "category": "engineering"
}
```

## index.js

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
    negativeColor: { type: 'color', default: '#f44336' }
  },

  dataRequirements: {
    columns: { min: 2, max: 2 },
    types: ['string', 'number']
  },

  render: WaterfallRenderer.render,
  export: WaterfallRenderer.export
};
```

## renderer.js

```javascript
class WaterfallRenderer {
  static render(canvas, data, options, theme) {
    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;

    ctx.clearRect(0, 0, width, height);

    const padding = { top: 40, right: 20, bottom: 60, left: 60 };
    const plotWidth = width - padding.left - padding.right;
    const plotHeight = height - padding.top - padding.bottom;

    const labels = data.columns[0].values;
    const values = data.columns[1].values;

    const cumulative = [];
    let running = 0;
    for (const v of values) {
      cumulative.push(running);
      running += v;
    }

    const maxVal = Math.max(...cumulative.map(Math.abs), ...values.map(Math.abs));
    const scale = plotHeight / (maxVal * 2.5);

    const barWidth = (plotWidth / labels.length) * 0.6;
    const gap = (plotWidth / labels.length) * 0.4;

    for (let i = 0; i < labels.length; i++) {
      const x = padding.left + i * (barWidth + gap) + gap / 2;
      const baseY = padding.top + plotHeight / 2;
      const barHeight = Math.abs(values[i]) * scale;
      const y = values[i] >= 0
        ? baseY - cumulative[i] * scale - barHeight
        : baseY - cumulative[i] * scale;

      ctx.fillStyle = values[i] >= 0
        ? options.positiveColor
        : options.negativeColor;
      ctx.fillRect(x, y, barWidth, barHeight);

      if (options.showValues) {
        ctx.fillStyle = theme.text.primary;
        ctx.font = `${theme.typography.sizes.xs} ${theme.typography.fontFamily}`;
        ctx.textAlign = 'center';
        ctx.fillText(
          String(values[i]),
          x + barWidth / 2,
          values[i] >= 0 ? y - 4 : y + barHeight + 12
        );
      }

      ctx.fillStyle = theme.text.secondary;
      ctx.font = `${theme.typography.sizes.sm} ${theme.typography.fontFamily}`;
      ctx.textAlign = 'center';
      ctx.fillText(labels[i], x + barWidth / 2, height - padding.bottom + 16);
    }

    if (options.title) {
      ctx.fillStyle = theme.text.primary;
      ctx.font = `bold ${theme.typography.sizes.lg} ${theme.typography.fontFamily}`;
      ctx.textAlign = 'center';
      ctx.fillText(options.title, width / 2, 20);
    }
  }

  static export(canvas, data, options, format) {
    if (format === 'png') {
      return canvas.toDataURL('image/png');
    }
    if (format === 'csv') {
      const headers = data.columns.map(c => c.name).join(',');
      const rows = data.columns[0].values.map((_, i) =>
        data.columns.map(c => c.values[i]).join(',')
      );
      return [headers, ...rows].join('\n');
    }
  }
}

module.exports = WaterfallRenderer;
```

## What This Demonstrates

- Visualization manifest structure
- Canvas 2D rendering
- Theme integration
- Export to PNG and CSV
- Data requirements specification
