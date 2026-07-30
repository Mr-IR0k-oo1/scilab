# EDD-002: Workspace System

## Purpose

The Workspace System manages the visual layout: tabs, panels, sidebar, and editor area.

## Architecture

```
┌─────────────────────────────────────────┐
│           Workspace System               │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Tab       │  │ Panel            │   │
│  │ Manager   │  │ Manager          │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Layout    │  │ Status Bar       │   │
│  │ Engine    │  │ Manager          │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Components

### Tab Manager

Manages open files and their editor state.

```typescript
interface TabManager {
  open(file: FileDescriptor): Tab;
  close(tabId: string): void;
  getActive(): Tab | null;
  getAll(): Tab[];
  switchTo(tabId: string): void;
  reorder(tabIds: string[]): void;
  split(tabId: string, direction: 'horizontal' | 'vertical'): void;
}
```

**Tab Lifecycle:**
```
Created → Active → Inactive → Closed
```

**Tab State:**
```typescript
interface Tab {
  id: string;
  file: FileDescriptor;
  editor: EditorState;
  dirty: boolean;
  viewColumn: number;
}
```

### Panel Manager

Manages sidebar and bottom panels.

```typescript
interface PanelManager {
  register(panel: PanelDescriptor): void;
  show(panelId: string): void;
  hide(panelId: string): void;
  toggle(panelId: string): void;
  isVisible(panelId: string): boolean;
  getActive(location: PanelLocation): PanelDescriptor | null;
}
```

**Panel Locations:**
```typescript
type PanelLocation = 'left' | 'right' | 'bottom';
```

### Layout Engine

Manages panel sizes, positions, and persistence.

```typescript
interface LayoutEngine {
  getLayout(): LayoutState;
  setLayout(state: LayoutState): void;
  reset(): void;
  save(): void;
  restore(): void;
}
```

**Layout State:**
```typescript
interface LayoutState {
  leftSidebar: { visible: boolean; width: number };
  rightSidebar: { visible: boolean; width: number };
  bottomPanel: { visible: boolean; height: number };
  editorSplits: SplitState[];
}
```

### Status Bar Manager

Manages status bar items.

```typescript
interface StatusBarManager {
  setItem(item: StatusBarItem): void;
  removeItem(itemId: string): void;
  getItems(): StatusBarItem[];
}
```

## State Persistence

Workspace state is saved to `.scstudio/workspace.json`:

```json
{
  "tabs": [
    { "file": "main.sce", "active": true },
    { "file": "utils.sce", "active": false }
  ],
  "panels": {
    "explorer": { "visible": true, "width": 250 },
    "console": { "visible": true, "height": 200 }
  },
  "editor": {
    "splits": [
      { "tabs": ["main.sce"], "size": 0.6 },
      { "tabs": ["utils.sce"], "size": 0.4 }
    ]
  }
}
```

## Error Handling

- Invalid layout state: fall back to defaults.
- Corrupted workspace state: create fresh state.
- Panel crash: log error, keep panel in error state.

## Performance

- Tab switch: < 50ms.
- Panel toggle: < 100ms.
- Layout restore: < 200ms.
