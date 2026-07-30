# Workspace API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.1 |
| Stability | Stable |

---

## Purpose

Manages the workspace UI: tabs, panels, sidebar, status bar, and layout.

## Methods

### workspace.openFile(path: string): Promise\<Tab\>

Opens a file in the editor. Returns the tab descriptor.

```javascript
const tab = await workspace.openFile('main.sce');
console.log(tab.id); // "tab-abc123"
```

### workspace.closeTab(tabId: string): Promise\<void\>

Closes a tab by ID.

```javascript
await workspace.closeTab('tab-abc123');
```

### workspace.getActiveTab(): Tab | null

Returns the currently active tab.

```javascript
const tab = workspace.getActiveTab();
if (tab) {
  console.log(tab.path); // "main.sce"
}
```

### workspace.getOpenTabs(): Tab[]

Returns all open tabs.

```javascript
const tabs = workspace.getOpenTabs();
console.log(tabs.length); // 3
```

### workspace.switchToTab(tabId: string): Promise\<void\>

Switches to a specific tab.

```javascript
await workspace.switchToTab('tab-abc123');
```

### workspace.splitTab(tabId: string, direction: 'horizontal' | 'vertical'): Promise\<void\>

Splits the editor area.

```javascript
await workspace.splitTab('tab-abc123', 'vertical');
```

### workspace.getPanel(panelId: string): Panel | null

Returns a panel descriptor.

```javascript
const panel = workspace.getPanel('explorer');
console.log(panel.visible); // true
```

### workspace.togglePanel(panelId: string): Promise\<void\>

Toggles panel visibility.

```javascript
await workspace.togglePanel('explorer');
```

### workspace.setStatusBar(item: StatusBarItem): void

Updates a status bar item.

```javascript
workspace.setStatusBar({
  id: 'my-plugin.status',
  text: 'Ready',
  position: 'right'
});
```

### workspace.getLayout(): LayoutDescriptor

Returns the current layout state.

```javascript
const layout = workspace.getLayout();
console.log(layout.leftSidebar.visible); // true
console.log(layout.leftSidebar.width); // 250
```

### workspace.setLayout(layout: LayoutDescriptor): Promise\<void\>

Applies a layout configuration.

```javascript
await workspace.setLayout({
  leftSidebar: { visible: true, width: 300 },
  rightSidebar: { visible: false },
  bottomPanel: { visible: true, height: 200 }
});
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `workspace:tabOpened` | `{ tab: Tab }` | A file was opened |
| `workspace:tabClosed` | `{ tabId: string }` | A tab was closed |
| `workspace:tabSwitched` | `{ tab: Tab }` | Active tab changed |
| `workspace:tabModified` | `{ tabId: string, dirty: boolean }` | Tab dirty state changed |
| `workspace:panelToggled` | `{ panelId: string, visible: boolean }` | Panel visibility changed |
| `workspace:layoutChanged` | `{ layout: LayoutDescriptor }` | Layout was modified |

## Examples

### Open and Edit a File

```javascript
// Open file
const tab = await workspace.openFile('data.csv');

// Listen for modifications
workspace.on('workspace:tabModified', (event) => {
  if (event.tabId === tab.id && event.dirty) {
    console.log('File has unsaved changes');
  }
});
```

### Custom Status Bar Item

```javascript
workspace.setStatusBar({
  id: 'my-plugin.progress',
  text: 'Processing...',
  position: 'right',
  priority: 100
});

// Update later
workspace.setStatusBar({
  id: 'my-plugin.progress',
  text: 'Done',
  position: 'right',
  priority: 100
});
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `FileNotFound` | WS-001 | File does not exist |
| `FileAccessDenied` | WS-002 | No permission to read file |
| `TabLimitReached` | WS-003 | Maximum tabs open |
| `InvalidLayout` | WS-004 | Invalid layout configuration |
| `PanelNotFound` | WS-005 | Panel ID does not exist |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
