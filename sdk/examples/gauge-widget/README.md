# Example: Gauge Widget

A custom gauge widget for the GUI Builder.

## Files

```
gauge-widget/
├── widget.json
├── index.js
├── styles.css
└── README.md
```

## widget.json

```json
{
  "id": "com.example.gauge",
  "name": "Gauge",
  "version": "1.0.0",
  "description": "A circular gauge widget",
  "author": "Scilab Studio Team",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "icon": "gauge",
  "category": "display"
}
```

## index.js

```javascript
module.exports = {
  type: 'gauge',
  name: 'Gauge',
  icon: 'gauge',
  category: 'display',
  version: '1.0.0',

  properties: [
    {
      name: 'value',
      type: 'number',
      default: 50,
      label: 'Value',
      min: 0,
      max: 100,
      group: 'Data'
    },
    {
      name: 'min',
      type: 'number',
      default: 0,
      label: 'Minimum',
      group: 'Range'
    },
    {
      name: 'max',
      type: 'number',
      default: 100,
      label: 'Maximum',
      group: 'Range'
    },
    {
      name: 'color',
      type: 'color',
      default: '#4a9eff',
      label: 'Color',
      group: 'Appearance'
    },
    {
      name: 'label',
      type: 'string',
      default: 'Speed',
      label: 'Label',
      group: 'Appearance'
    }
  ],

  events: [
    {
      name: 'onChange',
      label: 'Value Changed',
      payload: { value: 'number' }
    }
  ],

  render(props) {
    const percent = ((props.value - props.min) / (props.max - props.min)) * 100;
    const angle = (percent / 100) * 270 - 135;

    return {
      tag: 'div',
      props: {
        class: 'ss-widget ss-widget-gauge',
        style: {
          width: '100%',
          height: '150px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        }
      },
      children: [
        {
          tag: 'svg',
          props: {
            viewBox: '0 0 100 80',
            style: { width: '100%', maxWidth: '120px' }
          },
          children: [
            // Background arc
            {
              tag: 'path',
              props: {
                d: 'M 15 65 A 35 35 0 1 1 85 65',
                fill: 'none',
                stroke: 'var(--ss-border)',
                'stroke-width': '6',
                'stroke-linecap': 'round'
              }
            },
            // Value arc
            {
              tag: 'path',
              props: {
                d: 'M 15 65 A 35 35 0 1 1 85 65',
                fill: 'none',
                stroke: props.color,
                'stroke-width': '6',
                'stroke-linecap': 'round',
                'stroke-dasharray': `${percent * 1.76} 176`
              }
            },
            // Value text
            {
              tag: 'text',
              props: {
                x: '50',
                y: '55',
                'text-anchor': 'middle',
                class: 'gauge-value'
              },
              children: [String(props.value)]
            }
          ]
        },
        // Label
        {
          tag: 'div',
          props: {
            class: 'gauge-label'
          },
          children: [props.label]
        }
      ]
    };
  }
};
```

## styles.css

```css
.ss-widget-gauge .gauge-value {
  font-size: 18px;
  font-weight: 600;
  fill: var(--ss-text-primary);
}

.ss-widget-gauge .gauge-label {
  font-size: 12px;
  color: var(--ss-text-secondary);
  margin-top: 4px;
}
```

## Usage

1. Copy to `~/.scilab-studio/widgets/gauge-widget/`
2. Restart Scilab Studio
3. Open GUI Builder
4. Find "Gauge" in the Display category
5. Drag onto canvas

## What This Demonstrates

- Widget manifest structure
- Property definitions with groups
- Event definitions
- SVG-based rendering
- Theme integration
- CSS styling
