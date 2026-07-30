# EDD-005: Widget Engine

## Purpose

The Widget Engine manages widget creation, rendering, data binding, and serialization.

## Architecture

```
┌─────────────────────────────────────────┐
│          Widget Engine                   │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Widget    │  │ Renderer         │   │
│  │ Registry  │  │ Pipeline         │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Data      │  │ Serializer       │   │
│  │ Binder    │  │                  │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Widget Lifecycle

```
Registration → Instantiation → Rendering → Data Binding → Destruction
```

### Registration

Widget types are registered at startup:

```typescript
interface WidgetRegistry {
  register(definition: WidgetDefinition): void;
  get(type: string): WidgetDefinition | null;
  getAll(): WidgetDefinition[];
  getByCategory(category: string): WidgetDefinition[];
}
```

### Instantiation

```typescript
interface WidgetInstance {
  readonly id: string;
  readonly type: string;
  properties: Record<string, any>;
  bindings: Record<string, string>;
  position: Point;
  size: Size;
}
```

### Rendering

Widget elements are rendered to the canvas:

```typescript
interface WidgetRenderer {
  render(instance: WidgetInstance, context: RenderContext): WidgetElement;
  update(instance: WidgetInstance, changes: PropertyChanges): void;
  destroy(instance: WidgetInstance): void;
}
```

**Render Pipeline:**
```
Instance → Resolve Properties → Apply Bindings → Generate Element → DOM Update
```

### Data Binding

Widgets connect to Scilab variables:

```typescript
interface DataBinder {
  bind(instanceId: string, property: string, expression: string): void;
  unbind(instanceId: string, property: string): void;
  updateValue(instanceId: string, property: string, value: any): void;
}
```

**Binding Flow:**
1. Widget declares binding expression.
2. Binder sends expression to Scilab.
3. Scilab evaluates and returns value.
4. Binder updates widget property.
5. Widget re-renders.

### Serialization

Widgets persist to JSON:

```typescript
interface WidgetSerializer {
  serialize(instance: WidgetInstance): WidgetJSON;
  deserialize(json: WidgetJSON): WidgetInstance;
}
```

**Serialization Format:**
```json
{
  "id": "widget-001",
  "type": "button",
  "properties": {
    "label": "Run",
    "width": 120,
    "height": 40
  },
  "bindings": {
    "enabled": "is_running == false"
  },
  "position": { "x": 100, "y": 200 },
  "size": { "width": 120, "height": 40 }
}
```

## Canvas Rendering

Widgets render on an HTML5 Canvas:

```typescript
interface CanvasRenderer {
  clear(): void;
  drawElement(element: WidgetElement): void;
  hitTest(point: Point): WidgetInstance | null;
  getSelected(): WidgetInstance[];
  select(instance: WidgetInstance): void;
  deselectAll(): void;
}
```

**Hit Testing:**
- Point-in-rect for basic shapes.
- SVG path testing for complex shapes.
- Z-order: last drawn = top.

## Error Handling

- Invalid widget type: show error placeholder.
- Render failure: catch, log, show error state.
- Binding failure: show stale value, log warning.
- Serialization failure: log, skip widget.

## Performance

- Widget render: < 5ms per widget.
- 100 widgets on canvas: < 200ms.
- Hit test: < 1ms.
- Data binding update: < 10ms.
