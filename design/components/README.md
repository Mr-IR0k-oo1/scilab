# Component Definitions

## Button

**States:** Default, Hover, Active, Focused, Disabled
**Sizes:** sm (24px), md (32px), lg (40px)
**Variants:** Primary, Secondary, Ghost, Danger

```
Default:     +--[ Label ]--+
Hover:       +--[ Label ]--+  (lighter bg)
Active:      +--[ Label ]--+  (darker bg)
Focused:     +--[ Label ]--+  (outline)
Disabled:    +--[ Label ]--+  (grayed)
```

**Keyboard:** Tab to focus, Enter/Space to activate.
**Accessibility:** `role="button"`, `aria-label`, focusable.

---

## Card

**States:** Default, Selected, Hover

```
+----------------------------+
| Header                     |
+----------------------------+
|                            |
| Content                    |
|                            |
+----------------------------+
| Footer                     |
+----------------------------+
```

**Usage:** Group related content. Tooltips, settings, plugin listings.

---

## Toolbar

```
+--[Icon]--[Icon]--+--[Icon]--[Icon]--+--[Label]--+
    Group 1            Group 2           Group 3
```

**Rules:** Icon-only buttons. 32px height. Groups separated by 1px dividers.
**Keyboard:** Tab between groups, Enter/Space to activate.

---

## Sidebar

```
+--[Title]--------[Collapse]--+
|                              |
| > Item 1                     |
| > Item 2                     |
|   > Child 1                  |
|   > Child 2                  |
| > Item 3                     |
|                              |
+------------------------------+
```

**States:** Expanded (250px), Collapsed (48px icon rail), Hidden
**Keyboard:** Arrow keys to navigate, Enter to expand/collapse.

---

## Panel

```
+--[Tab1]--[Tab2]--[Tab3]-----+
|                              |
|         Content              |
|                              |
+------------------------------+
```

**States:** Visible, Collapsed, Docked
**Resize:** Drag handle on edges (4px invisible, visible on hover).

---

## Inspector (Property Panel)

```
+--Properties------------------+
|                              |
| > Data                       |
|   Label: [____________]      |
|   Value: [____________]      |
|                              |
| > Layout                     |
|   X: [____________]          |
|   Y: [____________]          |
|   Width: [____________]      |
|   Height: [____________]     |
|                              |
| > Events                     |
|   onClick: [____________]    |
+------------------------------+
```

**Rules:** Grouped by category. Collapsible groups. Live preview on change.

---

## Canvas (GUI Builder)

```
+--[Grid: ON]--[Snap: ON]--[Zoom: 100%]--+
|                                          |
|     [Widget]    [Widget]                 |
|                                          |
|          [Widget]                        |
|                                          |
+------------------------------------------+
```

**Interactions:**
- Click: Select widget
- Shift+Click: Add to selection
- Drag on empty: Rubber band select
- Drag widget: Move
- Drag handle: Resize
- Delete: Remove selected
- Arrow keys: Nudge 1px
- Shift+Arrow: Nudge 10px

---

## Table

```
+--[Col1]---[Col2]---[Col3]---+
|  [val]    [val]    [val]    |
|  [val]    [val]    [val]    |
|  [val]    [val]    [val]    |
+------------------------------+
```

**Features:** Sortable columns, resizable columns, row selection, keyboard navigation.
**Keyboard:** Arrow keys, Enter to select, Space to toggle.

---

## Dialog

```
+--[Title]-------------------[×]--+
|                                   |
|  Message content here.            |
|                                   |
|          [Cancel]  [Confirm]      |
+-----------------------------------+
```

**Behavior:** Focus trapped, Escape closes, backdrop click closes (if not required).
**Sizes:** sm (320px), md (480px), lg (640px).

---

## Graph (Chart Canvas)

```
+--[Title]---------------------------+
|  ^                                  |
|  |    *                             |
|  |   * *                            |
|  |  *   *                           |
|  | *     *                          |
|  +----------->                      |
+-------------------------------------+
```

**Interactions:** Hover (tooltip), Click (select), Scroll (zoom), Drag (pan).
**Export:** PNG, SVG, CSV, PDF.

---

## Tooltip

```
+--[Content]--+
```

**Behavior:** Appears on hover (500ms delay). Follows cursor. Disappears on mouse leave.
**Position:** Auto-positioned to stay within viewport.
