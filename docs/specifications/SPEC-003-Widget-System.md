# SPEC-003 — Widget System

## Purpose

Provide reusable UI components that extend the GUI Designer and Dashboard Builder. Every widget follows a common interface, ensuring consistent behavior across the platform.

---

## Supported Widgets

### Input
- Button
- Text Field
- Number Input
- Checkbox
- Dropdown
- Slider (v0.2)
- Color Picker (v0.2)

### Display
- Label
- Table
- Image (v0.2)
- Icon

### Visualization
- Gauge
- Line Chart
- Bar Chart
- Scatter Plot
- Heatmap
- Histogram (v0.2)

### Layout
- Panel
- Tab Container (v0.2)
- Toolbar
- Canvas

---

## Widget Lifecycle

```
Create
  │
  ▼
Initialize
  │
  ▼
Render
  │
  ▼
Interact
  │
  ▼
Update
  │
  ▼
Serialize
  │
  ▼
Destroy
```

### State Machine

```
Created → Initialized → Active ↔ Updated → Serialized → Destroyed
                                │
                                ▼
                             Error
```

---

## Widget Interface

Every widget must implement:

```typescript
initialize()
render()
update()
destroy()
serialize()
deserialize()
validate()
```

### Method Contracts

| Method | Input | Output | When Called |
|--------|-------|--------|------------|
| `initialize(config)` | Widget configuration | void | After creation |
| `render()` | — | DOM element or virtual node | On every visual update |
| `update(data)` | New data or properties | void | When bound data changes |
| `destroy()` | — | void | When removed from canvas |
| `serialize()` | — | WidgetState | When saving layout |
| `deserialize(state)` | Saved WidgetState | void | When loading layout |
| `validate()` | — | ValidationResult | Before saving, before export |

---

## Widget Interface Definition

```typescript
interface Widget {
  // Identity
  name: string;
  version: string;
  icon: string;
  category: "input" | "display" | "visualization" | "layout";

  // Sizing
  defaultSize: { width: number; height: number };
  minSize: { width: number; height: number };
  maxSize: { width: number; height: number };
  resizable: boolean;
  aspectRatio: number | null;

  // Properties
  properties: PropertyDefinition[];

  // Events
  events: EventDefinition[];

  // Actions
  actions: ActionDefinition[];

  // Rendering
  renderer: SvelteComponent;

  // Persistence
  serialize(instance: WidgetInstance): WidgetState;
  deserialize(state: WidgetState): WidgetInstance;
}
```

---

## Property Types

| Type | Input Widget | Schema |
|------|-------------|--------|
| string | Text input | `{ type, default, minLength?, maxLength?, placeholder? }` |
| number | Number input / slider | `{ type, default, min?, max?, step? }` |
| boolean | Toggle switch | `{ type, default }` |
| color | Color picker | `{ type, default }` |
| select | Dropdown | `{ type, options: string[], default }` |
| multiselect | Multi-select | `{ type, options: string[], default }` |
| json | Code editor | `{ type, default }` |
| image | File picker | `{ type, default }` |
| font | Font picker | `{ type, default }` |

---

## Data Binding

### Binding Sources

| Source | Syntax | Description |
|--------|--------|-------------|
| Static | (literal value) | Fixed value |
| Engine Variable | `engine:variableName` | Live Scilab variable |
| Data Column | `data:path::column` | Column from imported data |
| Event Payload | `event:type.path` | Value from an event |

### Binding Modes

| Mode | Description |
|------|-------------|
| on-change | Update when source changes |
| on-tick | Update on timer (configurable interval) |
| manual | Only update on explicit trigger |

---

## Events

Widgets can emit events on user interaction:

```typescript
interface EventDefinition {
  name: string;
  label: string;
  payload: Record<string, string>;
}
```

Example: `valueChanged` event with `{ value: number, previousValue: number }`.

---

## Serialization

```typescript
interface WidgetState {
  id: string;
  type: string;
  x: number;
  y: number;
  width: number;
  height: number;
  properties: Record<string, any>;
  bindings: Record<string, DataBinding>;
  locked: boolean;
}
```

---

## Validation

Every widget must validate:
- Required properties are present.
- Property values are within declared ranges.
- Data bindings reference valid sources.
- Size is within min/max constraints.

Validation errors are reported as warnings. The widget is still renderable in a degraded state.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max properties per widget | 20 |
| Max event handlers per widget | 10 |
| Max nesting depth (panels) | 5 |
| Serialization size limit | 10KB per widget instance |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Invalid property value | Clamp to valid range, show warning |
| Data binding source unavailable | Show "disconnected" state |
| Renderer throws | Show error state with details |
| Serialization fails | Use default state, log error |

---

## Extension Points

- Custom property types.
- Custom data binding sources.
- Custom rendering strategies (Canvas 2D, WebGL).
- Custom serialization formats.
