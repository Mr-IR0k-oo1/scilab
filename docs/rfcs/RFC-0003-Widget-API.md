# RFC-0003: Widget API

| Field | Value |
|-------|-------|
| RFC | 0003 |
| Title | Widget API |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how widgets are created, registered, rendered, and how they exchange data with Scilab.

## Motivation

Widgets are the building blocks of visual GUIs. A clear, composable widget API enables third-party developers to create custom widgets without understanding the rendering engine internals.

## Detailed Design

### Widget Definition

```typescript
interface WidgetDefinition {
  type: string;
  name: string;
  icon: string;
  category: WidgetCategory;
  version: string;
  properties: PropertyDefinition[];
  events: EventDefinition[];
  render: (props: WidgetProps) => WidgetElement;
}
```

### Widget Instance

```typescript
interface WidgetInstance {
  readonly id: string;
  readonly type: string;
  readonly element: WidgetElement;

  getProperty(name: string): any;
  setProperty(name: string, value: any): void;
  on(event: string, handler: EventHandler): Disposable;
  destroy(): void;
}
```

### Property Definitions

```typescript
interface PropertyDefinition {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'color' | 'enum' | 'expression';
  default: any;
  label: string;
  description: string;
  required?: boolean;
  min?: number;
  max?: number;
  options?: { label: string; value: any }[];
  group?: string;
}
```

### Data Binding

Widgets connect to Scilab variables through data binding expressions:

```json
{
  "property": "value",
  "binding": "my_variable",
  "expression": "sin(2 * pi * freq * t)"
}
```

**Binding lifecycle:**
1. Widget declares binding expressions in its properties.
2. Data Pipeline evaluates expressions via Scilab.
3. Results are pushed to widget instances.
4. Widget re-renders with new data.
5. Changes flow back through `onPropertyChange` events.

### Widget Element

Widgets return a declarative element tree:

```typescript
interface WidgetElement {
  tag: string;
  props: Record<string, any>;
  children: (WidgetElement | string)[];
}
```

Example:

```typescript
function renderButton(props: WidgetProps): WidgetElement {
  return {
    tag: 'button',
    props: {
      class: 'ss-widget ss-widget-button',
      style: { width: props.width, height: props.height },
      onClick: () => props.onAction?.({ type: 'click' })
    },
    children: [props.label || 'Button']
  };
}
```

### Serialization

Widgets serialize to JSON for persistence:

```json
{
  "id": "btn_001",
  "type": "button",
  "properties": {
    "label": "Run Simulation",
    "width": 120,
    "height": 40,
    "color": "#4a9eff"
  },
  "bindings": {
    "enabled": "is_running == false"
  },
  "events": {
    "onClick": "run_simulation()"
  },
  "position": { "x": 100, "y": 200 },
  "size": { "width": 120, "height": 40 }
}
```

### Widget Categories

| Category | Description |
|----------|-------------|
| `input` | Text fields, sliders, checkboxes, dropdowns |
| `display` | Labels, images, tables, indicators |
| `container` | Panels, tabs, split views |
| `chart` | Inline charts and gauges |
| `control` | Buttons, toggles, progress bars |
| `custom` | User-defined widgets |

## Alternatives Considered

1. **React-style JSX**: Familiar but adds build complexity. Chose simpler element API.
2. **Web Components**: Standards-based but heavier runtime. Can be added later.

## Security Considerations

- Widget rendering is sandboxed in the UI thread.
- Data bindings are evaluated in the Scilab process, not the UI.
- Widgets cannot access the file system or network directly.

## Testing Strategy

- Unit tests for widget rendering and property handling.
- Visual regression tests for widget appearance.
- Integration tests for data binding.
- Performance tests for 100+ widgets on screen.

## Rollout

- v0.1: 9 built-in widgets, no custom widget support.
- v0.2: Widget SDK for custom widgets. Widget Marketplace.
