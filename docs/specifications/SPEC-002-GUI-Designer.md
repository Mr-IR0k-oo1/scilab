# SPEC-002 — GUI Designer

## Purpose

Provide a drag-and-drop interface designer that generates Scilab GUI code. Users design visually; the platform produces the corresponding `uicontrol` + `figure` code.

---

## Components

### Toolbar
Contains tools for canvas interaction:
- Selection Tool (pointer, default)
- Button
- Label
- Text Field
- Number Input
- Checkbox
- Dropdown
- Plot Container
- Table
- Panel
- Image (v0.2)
- Slider (v0.2)
- Tab Container (v0.2)

### Canvas
The design surface where components are placed.

**Supports:**
- Drag (move components by clicking and dragging)
- Resize (8 handles per component: corners + midpoints)
- Multi-select (Shift+click or drag selection rectangle)
- Alignment guides (snap to other components' edges/centers)
- Snap Grid (toggle with Ctrl+G / Cmd+G, default 10px)
- Undo / Redo (Ctrl+Z / Ctrl+Shift+Z)
- Zoom (Ctrl+scroll, or Ctrl+= / Ctrl+-)
- Preview mode (toggle with Ctrl+P / Cmd+P — renders without edit controls)

### Inspector
Context-sensitive property editor for the selected component.

**Tabs:**
- Properties — Component-specific settings (text, value, options, etc.)
- Layout — Position (x, y), size (width, height), lock aspect ratio
- Appearance — Colors, fonts, borders, padding, alignment
- Events — Event bindings (click, change, keypress → Scilab function)
- Bindings — Data bindings (link property to Scilab variable or dataset)

### Code Panel
Shows the generated Scilab code in real-time. Read-only. Updates as the canvas changes.

---

## Component Specification

### Button
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| text | string | "Button" | Label text |
| fontSize | number | 12 | Font size (pt) |
| fontColor | string | "#000000" | Text color |
| backgroundColor | string | "#e0e0e0" | Background color |
| borderColor | string | "#999999" | Border color |
| borderWidth | number | 1 | Border width (px) |
| borderRadius | number | 4 | Corner radius (px) |
| enabled | boolean | true | Interactive or disabled |
| tooltip | string | "" | Hover tooltip |

### Label
| Property | Type | Default |
|----------|------|---------|
| text | string | "Label" |
| fontSize | number | 12 |
| fontColor | string | "#000000" |
| fontFamily | string | "sans-serif" |
| textAlign | string | "left" |
| wordWrap | boolean | true |

### Text Field
| Property | Type | Default |
|----------|------|---------|
| placeholder | string | "Enter text..." |
| defaultValue | string | "" |
| maxLength | number | 0 (unlimited) |
| readOnly | boolean | false |
| password | boolean | false |

### Number Input
| Property | Type | Default |
|----------|------|---------|
| defaultValue | number | 0 |
| min | number | -Infinity |
| max | number | Infinity |
| step | number | 1 |
| decimals | number | 0 |

### Checkbox
| Property | Type | Default |
|----------|------|---------|
| label | string | "Option" |
| checked | boolean | false |

### Dropdown
| Property | Type | Default |
|----------|------|---------|
| options | string[] | ["Option 1", "Option 2"] |
| selectedIndex | number | 0 |
| multiSelect | boolean | false |

### Plot Container
| Property | Type | Default |
|----------|------|---------|
| plotType | string | "line" |
| autoRefresh | boolean | true |
| title | string | "" |

### Table
| Property | Type | Default |
|----------|------|---------|
| dataSource | string | "" |
| headers | string[] | [] |
| showHeader | boolean | true |
| showGrid | boolean | true |
| selectable | boolean | false |
| maxHeight | number | 300 |

### Panel
| Property | Type | Default |
|----------|------|---------|
| backgroundColor | string | "transparent" |
| borderColor | string | "#cccccc" |
| borderWidth | number | 1 |
| borderRadius | number | 4 |
| padding | number | 8 |
| title | string | "" |
| children | Component[] | [] |

---

## Code Generation

Generates Scilab code using `uicontrol` and `figure`:

```scilab
function main_gui()
    fig = figure("position", [100, 100, 800, 600], ...
                  "figure_name", "Main GUI");
    uicontrol(fig, "style", "pushbutton", ...
              "string", "Plot Data", ...
              "position", [20, 480, 120, 40], ...
              "callback", "plot_callback");
endfunction
```

### Generation Options
- `includeHeader` — Add generation comment (default true)
- `functionName` — Generated function name (default: layout name)
- `useCallback` — Generate callback stubs (default true)
- `compactOutput` — Minimize whitespace (default false)

---

## Behavior

### Canvas Interaction
1. User drags a component from the Toolbar to the Canvas.
2. Component appears at drop position, snapped to grid.
3. Component is automatically selected.
4. Inspector shows the component's properties.
5. User edits properties; changes apply immediately.
6. Code Panel updates in real-time.

### Preview Mode
- Toggle with Ctrl+P / Cmd+P.
- Canvas renders the GUI without edit controls.
- Components are interactive (buttons click, inputs type).
- Callbacks are stubbed (console.log equivalent).
- Exit preview with Escape.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Canvas default size | 800 × 600 |
| Grid size | 10px (toggleable) |
| Min component size | 20 × 20 |
| Max components per layout | 500 |
| Undo history depth | 100 actions |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Invalid component position | Clamp to canvas bounds |
| Circular nesting (panel in panel in ...) | Max depth: 5 levels |
| Generated code exceeds Scilab limits | Warning, suggest splitting |
| Layout file corrupt | Show error, offer to reload last saved |

---

## Extension Points

- Custom component types via Widget SDK.
- Custom code generators (HTML, LaTeX).
- Export to Scilab function library.
- Import from existing Scilab GUI code.
