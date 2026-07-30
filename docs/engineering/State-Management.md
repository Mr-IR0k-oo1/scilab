# State Management

## State Layers

```
Workspace State
      ↓
Project State
      ↓
Module State
      ↓
Widget State
      ↓
Runtime State
```

## Workspace State

**Owner:** Workspace System
**Lifetime:** Application session
**Persistence:** `.scstudio/workspace.json`
**Serialization:** JSON

```typescript
interface WorkspaceState {
  tabs: TabState[];
  panels: Record<string, PanelState>;
  layout: LayoutState;
  commandHistory: HistoryEntry[];
}
```

## Project State

**Owner:** Project System
**Lifetime:** Project session
**Persistence:** `.scstudio/project.json`
**Serialization:** JSON

```typescript
interface ProjectState {
  name: string;
  version: string;
  scilabVersion: string;
  files: FileState[];
  settings: Record<string, any>;
  plugins: string[];
}
```

## Module State

**Owner:** Module System
**Lifetime:** Module lifetime
**Persistence:** Module-specific storage
**Serialization:** Module-defined

```typescript
interface ModuleState {
  moduleId: string;
  status: 'active' | 'inactive' | 'error';
  settings: Record<string, any>;
  data: Record<string, any>;
}
```

## Widget State

**Owner:** Widget Engine
**Lifetime:** Widget instance lifetime
**Persistence:** GUI definition file
**Serialization:** JSON

```typescript
interface WidgetState {
  instanceId: string;
  type: string;
  properties: Record<string, any>;
  bindings: Record<string, string>;
  position: Point;
  size: Size;
  selected: boolean;
}
```

## Runtime State

**Owner:** Scilab Bridge
**Lifetime:** Scilab process lifetime
**Persistence:** None (ephemeral)
**Serialization:** N/A

```typescript
interface RuntimeState {
  status: 'not-running' | 'starting' | 'ready' | 'running' | 'idle';
  version: string;
  variables: Map<string, VariableValue>;
  lastCommand: string | null;
  errorCount: number;
}
```

## State Flow

```
User Action
    ↓
Command System
    ↓
State Update
    ↓
Event Bus Notification
    ↓
UI Re-render
```

## State Persistence

| State | Save Trigger | Load Trigger |
|-------|-------------|-------------|
| Workspace | On close, auto-save | On open |
| Project | Manual save, auto-save | On project open |
| Module | On change | On module activation |
| Widget | On GUI save | On GUI open |
| Runtime | Never | On Scilab start |

## State Serialization

All state is serializable to JSON:

```typescript
interface Serializable {
  serialize(): JSON;
  deserialize(json: JSON): void;
}
```

## State Migration

When state format changes:

1. Detect old format version.
2. Run migration function.
3. Update format version.
4. Save in new format.

## Error Handling

- Corrupted state: fall back to defaults.
- Partial state: recover what's possible.
- Missing state: use defaults.
- Migration failure: keep original, log error.

## Performance

- State read: < 1ms (cached).
- State write: < 10ms.
- State serialization: < 5ms.
- State deserialization: < 5ms.
