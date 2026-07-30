# Interaction Patterns

## Selection

### Single Click
Select an item. Deselects all other items.

### Shift+Click
Add to selection (multi-select).

### Drag on Empty Area
Create a selection rectangle. Items inside are selected.

### Click on Empty Area
Deselect all.

## Drag and Drop

### Visual Feedback
- Dragged element follows cursor with 50% opacity.
- Drop target highlights with accent border.
- Invalid drop targets show a "no" cursor.

### Snap
- Grid snap (toggleable, default 10px).
- Alignment guides appear when near other elements' edges.

### Cancel
- Press Escape during drag to cancel.

## Context Menu

### Right-Click
Opens context menu at cursor position. Menu items are context-sensitive.

### Keyboard
Shift+F10 or Menu key opens context menu for focused element.

## Inline Editing

### Double-Click
Enters edit mode for the double-clicked element (file rename, property value, etc.).

### Enter
Confirms edit.

### Escape
Cancels edit, reverts to original value.

## Confirmation Dialogs

### Destructive Actions
Delete, overwrite, and similar actions show a confirmation dialog with:
- Clear description of what will happen.
- "Confirm" button (destructive actions in red).
- "Cancel" button.
- Keyboard: Enter to confirm, Escape to cancel.

## Toast Notifications

### Position
Bottom-right corner.

### Behavior
- Auto-dismiss after duration (5s for info, 10s for error).
- Click to dismiss.
- Stack vertically (max 5 visible).
- Actions available as buttons within the toast.

## Progress Indicators

### Determinate
Show percentage (progress bar) when total is known.

### Indeterminate
Show spinner when total is unknown.

###位置
- Inline: within the component being processed.
- Global: status bar for background operations.
- Modal: for operations that block the UI.

## Search

### Quick Filter
Type to filter visible items (file explorer, variable list, etc.).

### Global Search
Ctrl+P / Cmd+P opens the command palette with search.

### Results
- Highlighted matches.
- Keyboard navigation (arrow keys + Enter).
- Fuzzy matching enabled.
