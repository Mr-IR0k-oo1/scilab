# Widget Development

Widgets are visual components for the GUI Builder. Users drag widgets onto a canvas to create engineering interfaces.

## Widget Structure

```
my-widget/
├── widget.json       # Manifest (required)
├── index.js          # Entry point (required)
├── styles.css        # Optional styles
├── README.md         # Documentation
└── test/
    └── index.test.js # Tests
```

## Manifest (widget.json)

```json
{
  "id": "com.example.gauge",
  "name": "Gauge",
  "version": "1.0.0",
  "description": "A circular gauge widget",
  "author": "Author Name",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "icon": "gauge",
  "category": "display",
  "tags": ["gauge", "indicator", "display"]
}
```

## Entry Point

```javascript
module.exports = {
  type: 'gauge',
  name: 'Gauge',
  icon: 'gauge',
  category: 'display',
  version: '1.0.0',

  properties: [
    // Property definitions
  ],

  events: [
    // Event definitions
  ],

  render(props) {
    // Return widget element tree
  }
};
```

## Property Definitions

```javascript
properties: [
  {
    name: 'value',
    type: 'number',
    default: 50,
    label: 'Value',
    description: 'Current gauge value',
    min: 0,
    max: 100,
    group: 'Data'
  },
  {
    name: 'min',
    type: 'number',
    default: 0,
    label: 'Minimum',
    description: 'Minimum value',
    group: 'Range'
  },
  {
    name: 'max',
    type: 'number',
    default: 100,
    label: 'Maximum',
    description: 'Maximum value',
    group: 'Range'
  },
  {
    name: 'color',
    type: 'color',
    default: '#4a9eff',
    label: 'Color',
    description: 'Gauge fill color',
    group: 'Appearance'
  },
  {
    name: 'label',
    type: 'string',
    default: 'Speed',
    label: 'Label',
    description: 'Gauge label text',
    group: 'Appearance'
  },
  {
    name: 'showValue',
    type: 'boolean',
    default: true,
    label: 'Show Value',
    description: 'Display the numeric value',
    group: 'Appearance'
  },
  {
    name: 'style',
    type: 'enum',
    default: 'arc',
    label: 'Style',
    description: 'Visual style',
    options: [
      { label: 'Arc', value: 'arc' },
      { label: 'Circle', value: 'circle' },
      { label: 'Semi-circle', value: 'semi' }
    ],
    group: 'Appearance'
  }
]
```

## Property Types

| Type | Description | UI Control |
|------|-------------|-----------|
| `string` | Text value | Text input |
| `number` | Numeric value | Number input |
| `boolean` | True/false | Checkbox |
| `color` | Color value | Color picker |
| `enum` | Discrete options | Dropdown |
| `expression` | Scilab expression | Expression editor |
| `file` | File path | File picker |

## Event Definitions

```javascript
events: [
  {
    name: 'onChange',
    label: 'Value Changed',
    description: 'Fired when the gauge value changes',
    payload: {
      value: 'number',
      previousValue: 'number'
    }
  },
  {
    name: 'onClick',
    label: 'Clicked',
    description: 'Fired when the gauge is clicked'
  }
]
```

## Rendering

Widgets return a declarative element tree:

```javascript
render(props) {
  const percent = ((props.value - props.min) / (props.max - props.min)) * 100;

  return {
    tag: 'div',
    props: {
      class: 'ss-widget ss-widget-gauge',
      style: {
        width: props.width || '100%',
        height: props.height || '150px'
      }
    },
    children: [
      // Background arc
      {
        tag: 'svg',
        props: {
          viewBox: '0 0 100 60',
          class: 'gauge-svg'
        },
        children: [
          {
            tag: 'path',
            props: {
              d: 'M 10 50 A 40 40 0 0 1 90 50',
              fill: 'none',
              stroke: 'var(--ss-border)',
              'stroke-width': '8'
            }
          },
          {
            tag: 'path',
            props: {
              d: 'M 10 50 A 40 40 0 0 1 90 50',
              fill: 'none',
              stroke: props.color,
              'stroke-width': '8',
              'stroke-dasharray': `${percent * 1.26} 126`,
              'stroke-linecap': 'round'
            }
          }
        ]
      },
      // Value display
      props.showValue ? {
        tag: 'text',
        props: {
          x: '50',
          y: '45',
          'text-anchor': 'middle',
          class: 'gauge-value'
        },
        children: [`${props.value}`]
      } : null,
      // Label
      {
        tag: 'text',
        props: {
          x: '50',
          y: '58',
          'text-anchor': 'middle',
          class: 'gauge-label'
        },
        children: [props.label]
      }
    ].filter(Boolean)
  };
}
```

## Data Binding

Widgets connect to Scilab variables through data binding:

```json
{
  "id": "gauge_001",
  "type": "gauge",
  "properties": {
    "value": 50
  },
  "bindings": {
    "value": "motor_speed"
  }
}
```

The `bindings` object maps widget properties to Scilab variable names or expressions.

## Serialization

Widgets serialize to JSON for persistence:

```json
{
  "id": "gauge_001",
  "type": "gauge",
  "properties": {
    "value": 50,
    "min": 0,
    "max": 100,
    "color": "#4a9eff",
    "label": "Speed",
    "showValue": true,
    "style": "arc"
  },
  "bindings": {
    "value": "motor_speed"
  },
  "position": { "x": 100, "y": 200 },
  "size": { "width": 200, "height": 150 }
}
```

## Testing

```bash
# Preview in Scilab Studio
scilab-studio preview

# Run unit tests
scilab-studio test

# Run visual tests
scilab-studio test --visual
```

## Best Practices

- Keep properties simple. Complex state should be computed.
- Use CSS classes, not inline styles. Themes override classes.
- Handle missing data gracefully. Show placeholders.
- Support both dark and light themes.
- Document all properties and events.
- Provide sensible defaults for all properties.
- Keep render functions pure. No side effects.
