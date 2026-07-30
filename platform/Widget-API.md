# Widget API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.2 |
| Stability | Stable |

---

## Purpose

Manages widget registration, instantiation, and data binding.

## Methods

### widget.getWidgetType(typeId: string): WidgetType | null

Returns a widget type definition.

```javascript
const type = widget.getWidgetType('button');
console.log(type.properties.length); // 8
```

### widget.getAllWidgetTypes(): WidgetType[]

Returns all registered widget types.

```javascript
const types = widget.getAllWidgetTypes();
console.log(types.map(t => t.type)); // ["button", "label", "slider", ...]
```

### widget.getWidgetTypesByCategory(category: string): WidgetType[]

Returns widget types in a category.

```javascript
const inputWidgets = widget.getWidgetTypesByCategory('input');
```

### widget.createWidget(typeId: string, props?: object): WidgetInstance

Creates a new widget instance.

```javascript
const btn = widget.createWidget('button', {
  label: 'Click Me',
  width: 120,
  height: 40
});
console.log(btn.id); // "widget-abc123"
```

### widget.getWidget(widgetId: string): WidgetInstance | null

Returns a widget instance by ID.

```javascript
const btn = widget.getWidget('widget-abc123');
console.log(btn.getProperty('label')); // "Click Me"
```

### widget.destroyWidget(widgetId: string): void

Destroys a widget instance.

```javascript
widget.destroyWidget('widget-abc123');
```

### widget.setProperty(widgetId: string, name: string, value: any): void

Updates a widget property.

```javascript
widget.setProperty('widget-abc123', 'label', 'New Label');
```

### widget.bindProperty(widgetId: string, name: string, expression: string): void

Binds a widget property to a Scilab expression.

```javascript
widget.bindProperty('widget-abc123', 'value', 'motor_speed');
```

### widget.unbindProperty(widgetId: string, name: string): void

Removes a data binding.

```javascript
widget.unbindProperty('widget-abc123', 'value');
```

### widget.serializeWidget(widgetId: string): WidgetJSON

Serializes a widget to JSON.

```javascript
const json = widget.serializeWidget('widget-abc123');
// { id: "widget-abc123", type: "button", properties: {...} }
```

### widget.deserializeWidget(json: WidgetJSON): WidgetInstance

Creates a widget from JSON.

```javascript
const btn = widget.deserializeWidget({
  id: 'widget-abc123',
  type: 'button',
  properties: { label: 'Click Me' }
});
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `widget:created` | `{ widget: WidgetInstance }` | Widget was created |
| `widget:destroyed` | `{ widgetId: string }` | Widget was destroyed |
| `widget:propertyChanged` | `{ widgetId: string, name: string, value: any }` | Property changed |
| `widget:bindingUpdated` | `{ widgetId: string, name: string, value: any }` | Binding value updated |
| `widget:error` | `{ widgetId: string, error: Error }` | Widget encountered an error |

## Examples

### Create and Bind

```javascript
// Create a slider
const slider = widget.createWidget('slider', {
  min: 0,
  max: 100,
  value: 50
});

// Bind to Scilab variable
widget.bindProperty(slider.id, 'value', 'temperature');

// Listen for changes
widget.on('widget:propertyChanged', (event) => {
  if (event.widgetId === slider.id) {
    console.log(`Temperature: ${event.value}`);
  }
});
```

### Serialize for Persistence

```javascript
const json = widget.serializeWidget(slider.id);
// Save to project file
await project.saveWidget(json);
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `WidgetTypeNotFound` | WD-001 | Widget type does not exist |
| `WidgetNotFound` | WD-002 | Widget instance does not exist |
| `InvalidProperty` | WD-003 | Property name is invalid |
| `InvalidValue` | WD-004 | Property value is invalid |
| `BindingError` | WD-005 | Data binding failed |
| `SerializationError` | WD-006 | Widget serialization failed |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
