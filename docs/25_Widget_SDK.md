# 25 — Widget SDK

Widgets follow a common interface. Every widget behaves consistently because it implements the same contract.

For the Widget Runtime component specification, see [21 — Component Specification §7](21_Component_Specification.md). For the GUI Builder that uses widgets, see [28 — Scilab Runtime](28_Scilab_Runtime.md).

---

## 1. Widget Interface

Every widget exposes:

```
Widget
├── Name
├── Version
├── Icon
├── Properties
├── Events
├── Renderer
├── Serializer
└── Actions
```

### 1.1 Interface Definition

```typescript
interface WidgetDefinition {
  // Identity
  name: string;                    // Display name
  version: string;                 // Semver
  icon: string;                    // Icon identifier or path
  category: "input" | "display" | "visualization" | "layout";

  // Sizing
  defaultSize: { width: number; height: number };
  minSize: { width: number; height: number };
  maxSize: { width: number; height: number };
  resizable: boolean;
  aspectRatio: number | null;      // null = free, 1 = square, 16/9 = widescreen

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

## 2. Properties

### 2.1 Property Types

| Type | Input Widget | Schema |
|------|-------------|--------|
| `string` | Text input | `{ type, default, minLength?, maxLength?, placeholder? }` |
| `number` | Number input / slider | `{ type, default, min?, max?, step? }` |
| `boolean` | Toggle switch | `{ type, default }` |
| `color` | Color picker | `{ type, default }` |
| `select` | Dropdown | `{ type, options: string[], default }` |
| `multiselect` | Multi-select | `{ type, options: string[], default }` |
| `json` | Code editor | `{ type, default }` |
| `image` | File picker | `{ type, default }` |
| `font` | Font picker | `{ type, default }` |

### 2.2 Property Definition

```typescript
interface PropertyDefinition {
  name: string;                    // Unique within the widget
  type: string;                    // One of the types above
  label: string;                   // Display label in property inspector
  default: any;                    // Default value
  required?: boolean;              // Default false
  binding?: "data" | "event" | "static";  // How the property can be bound
  description?: string;            // Tooltip text
  group?: string;                  // Grouping in property inspector
  visible?: (instance: WidgetInstance) => boolean;  // Conditional visibility
}
```

### 2.3 Property Inspector

When a widget is selected on the canvas, the Property Inspector shows:
- Layout properties (position, size).
- Style properties (colors, fonts, borders).
- Widget-specific properties (from the definition).
- Event bindings.
- Data bindings.

All changes are applied immediately (no Apply button). Undo/redo is supported.

---

## 3. Events

Widgets can emit events when the user interacts with them.

```typescript
interface EventDefinition {
  name: string;                    // Event identifier
  label: string;                   // Display name
  payload: Record<string, string>; // Payload schema (name → type)
  description?: string;
}
```

### Example

```jsonc
{
  "name": "valueChanged",
  "label": "Value Changed",
  "payload": { "value": "number", "previousValue": "number" },
  "description": "Fired when the widget value changes"
}
```

Events are published to the Event Bus and can be subscribed to by any module or plugin.

---

## 4. Actions

Widgets can expose actions that other modules can invoke.

```typescript
interface ActionDefinition {
  name: string;                    // Action identifier
  label: string;                   // Display name
  icon?: string;                   // Icon for toolbar
  parameters?: ParameterDef[];     // Action parameters
  description?: string;
}
```

### Example

```jsonc
{
  "name": "exportData",
  "label": "Export Data",
  "icon": "download",
  "parameters": [
    { "name": "format", "type": "select", "options": ["csv", "json"], "default": "csv" }
  ]
}
```

---

## 5. Data Binding

### 5.1 Binding Sources

| Source | Syntax | Description |
|--------|--------|-------------|
| Static | (literal value) | Fixed value from properties |
| Engine Variable | `engine:variableName` | Live Scilab variable |
| Data Column | `data:path::column` | Column from imported data |
| Event Payload | `event:type.path` | Value from an event |
| Computed | `expression` | JavaScript expression |

### 5.2 Binding Configuration

```typescript
interface DataBinding {
  source: string;                  // Binding source identifier
  path: string;                    // Path within the source
  updateMode: "on-change" | "on-tick" | "manual";
  interval?: number;               // For "on-tick" mode (ms)
  transform?: string;              // Optional transform expression
}
```

### 5.3 Widget-Specific Data Inputs

Widgets declare what data they accept:

```jsonc
{
  "dataBinding": {
    "inputs": [
      { "name": "value", "type": "number", "label": "Value", "required": true },
      { "name": "label", "type": "string", "label": "Label", "required": false }
    ],
    "outputs": [
      { "name": "onSelect", "type": "event", "label": "Selection Event" }
    ]
  }
}
```

---

## 6. Renderer

The renderer is a Svelte component that receives properties and emits events.

```svelte
<script>
  import { createEventDispatcher } from 'svelte';

  export let value = 50;
  export let min = 0;
  export let max = 100;
  export let color = '#4CAF50';
  export let label = 'Gauge';

  const dispatch = createEventDispatcher();

  $: percentage = ((value - min) / (max - min)) * 100;

  function handleClick() {
    dispatch('valueChanged', { value: value + 1 });
  }
</script>

<div class="widget" style="--color: {color}">
  <div class="gauge-ring" style="--percent: {percentage}%"></div>
  <span class="value">{value}</span>
  <span class="label">{label}</span>
</div>

<style>
  .widget { position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .value { font-size: 1.5em; font-weight: bold; }
  .label { font-size: 0.9em; opacity: 0.7; }
</style>
```

---

## 7. Serialization

Every widget must implement serialize/deserialize for persistence.

```typescript
interface WidgetState {
  id: string;                      // Instance ID
  type: string;                    // Widget type identifier
  x: number;                       // Position
  y: number;
  width: number;                   // Size
  height: number;
  properties: Record<string, any>; // Property values
  bindings: Record<string, DataBinding>;  // Data bindings
  locked: boolean;                 // Locked on canvas
}
```

### Example

```jsonc
{
  "id": "widget_abc123",
  "type": "gauge",
  "x": 20,
  "y": 50,
  "width": 200,
  "height": 200,
  "properties": {
    "value": 75,
    "min": 0,
    "max": 100,
    "color": "#4CAF50",
    "label": "Temperature"
  },
  "bindings": {
    "value": {
      "source": "engine:variableName",
      "path": "temperature",
      "updateMode": "on-change"
    }
  },
  "locked": false
}
```

---

## 8. Lifecycle Callbacks

| Callback | When | Purpose |
|----------|------|---------|
| `onMount()` | Added to canvas | Initialize, set up subscriptions |
| `onPropertyChange(key, value)` | Property updated | React to configuration changes |
| `onDataUpdate(data)` | Bound data changed | Process new data |
| `onDestroy()` | Removed from canvas | Clean up subscriptions |
| `onResize(width, height)` | Resized on canvas | Adjust layout |
| `onSelect()` | Selected on canvas | Show resize handles, property inspector |
| `onDeselect()` | Deselected | Hide handles |

---

## 9. Built-in Widgets (v0.1)

| Widget | Type | Description |
|--------|------|-------------|
| `button` | Input | Clickable button with label |
| `label` | Display | Text label |
| `textfield` | Input | Text input field |
| `numberinput` | Input | Numeric input with spinners |
| `checkbox` | Input | Boolean toggle |
| `dropdown` | Input | Selection dropdown |
| `plot` | Visualization | Embedded Scilab plot container |
| `table` | Display | Data table |
| `panel` | Layout | Container for grouping children |

---

## 10. Theming

Widgets inherit the platform theme via CSS custom properties:

```css
:root {
  --ss-bg-primary: #1e1e1e;
  --ss-bg-secondary: #2d2d2d;
  --ss-text-primary: #e0e0e0;
  --ss-text-secondary: #a0a0a0;
  --ss-accent: #4a9eff;
  --ss-accent-hover: #6ab4ff;
  --ss-border: #404040;
  --ss-error: #f44336;
  --ss-success: #4CAF50;
  --ss-warning: #ff9800;
  --ss-info: #2196F3;
  --ss-radius: 4px;
  --ss-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}
```

Widgets must use these variables, not hard-coded colors.

---

## 11. Accessibility Requirements

- Keyboard operable (Tab to focus, Enter/Space to activate).
- `role` and `aria-*` attributes for screen readers.
- WCAG 2.1 AA contrast ratios.
- Not relying solely on color to convey information.
- Supporting high-contrast mode.

---

## 12. Packaging

### Local Development

Place widget directory in `~/.scilab-studio/widgets-dev/`.

### Publishing

```bash
scilab-studio widget publish my-widget/
```

1. Validate manifest.
2. Compile Svelte component.
3. Create `.scwidget` archive (ZIP).
4. Upload to marketplace.

### Installation

From marketplace, local file, or CLI. Installed to `~/.scilab-studio/widgets/<widget-id>/`.
