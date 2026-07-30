# EDD-010: Command System

## Purpose

The Command System provides a unified mechanism for user actions, undo/redo, keyboard shortcuts, and the command palette.

## Architecture

```
┌─────────────────────────────────────────┐
│          Command System                  │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Command   │  │ History          │   │
│  │ Registry  │  │ Manager          │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Keybinding│  │ Palette          │   │
│  │ Resolver  │  │ Search           │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Command Registry

```typescript
interface CommandRegistry {
  register(command: CommandDescriptor): Disposable;
  get(id: string): CommandDescriptor | null;
  getAll(): CommandDescriptor[];
  execute(id: string, ...args: any[]): Promise<any>;
}
```

**Command Descriptor:**
```typescript
interface CommandDescriptor {
  id: string;
  label: string;
  category: string;
  icon?: string;
  keybinding?: string;
  enabled?: () => boolean;
  execute: (...args: any[]) => Promise<any> | any;
  undo?: (...args: any[]) => Promise<any> | any;
}
```

## History Manager

```typescript
interface HistoryManager {
  push(command: CommandDescriptor, args: any[], result: any): void;
  undo(): Promise<void>;
  redo(): Promise<void>;
  canUndo(): boolean;
  canRedo(): boolean;
  clear(): void;
  getHistory(): HistoryEntry[];
}
```

**Rules:**
- Maximum history: 100 entries.
- Commands without `undo()` are not added to history.
- New command after undo clears redo stack.
- Grouping: related commands can be grouped.

## Keybinding Resolver

```typescript
interface KeybindingResolver {
  resolve(keybinding: string): CommandDescriptor | null;
  register(keybinding: string, commandId: string): void;
  unregister(keybinding: string): void;
  getConflicts(): Conflict[];
}
```

**Resolution Order:**
1. Exact match on keybinding.
2. User keybinding overrides.
3. Platform-specific defaults (Ctrl on Linux/Windows, Cmd on macOS).
4. If conflict: last registered wins.

## Palette Search

```typescript
interface PaletteSearch {
  search(query: string): SearchResult[];
  getRecent(): SearchResult[];
}
```

**Search Algorithm:**
- Fuzzy match on label and id.
- Exact match ranked higher.
- Recent commands shown first when query is empty.
- Categories are searchable.

## Undo/Redo

```
[cmd1, cmd2, cmd3] → undo → [cmd1, cmd2] → undo → [cmd1]
                                                     ↓
                                              redo → [cmd1, cmd2]
```

**Grouping:**
```typescript
interface CommandGroup {
  label: string;
  commands: CommandDescriptor[];
}
```

Multiple related commands execute as a single undo step.

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `command:executed` | `{ commandId, args, result }` | After execution |
| `command:failed` | `{ commandId, args, error }` | After failure |
| `command:undone` | `{ commandId }` | After undo |
| `command:redone` | `{ commandId }` | After redo |

## Error Handling

- Command not found: throw `CommandNotFound`.
- Command execution failure: catch, log, notify user.
- Undo failure: log warning, clear history.
- Keybinding conflict: warn in console.

## Performance

- Command lookup: < 1μs.
- Command execution: varies by command.
- History push: < 1μs.
- Palette search: < 50ms for 1000 commands.
