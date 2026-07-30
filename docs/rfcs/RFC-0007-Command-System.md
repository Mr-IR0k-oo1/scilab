# RFC-0007: Command System

| Field | Value |
|-------|-------|
| RFC | 0007 |
| Title | Command System |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how user actions are dispatched, executed, and recorded.

## Motivation

A unified command system enables undo/redo, keyboard shortcut mapping, menu integration, and command palette search — all from a single source of truth.

## Detailed Design

### Command Definition

```typescript
interface Command {
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

### Command Registration

```typescript
// In plugin activation
context.registerCommand({
  id: 'myPlugin.doSomething',
  label: 'Do Something',
  category: 'My Plugin',
  keybinding: 'Ctrl+Shift+D',
  execute: async (args) => {
    // Do the thing
  },
  undo: async (args) => {
    // Undo the thing
  }
});
```

### Command Palette

The command palette (Ctrl+P) searches across all registered commands:

- Fuzzy match on label and id.
- Show keyboard shortcut if bound.
- Show enabled/disabled state.
- Group by category.

### Undo/Redo

Commands that modify state should implement `undo()`. The command system maintains a history stack:

```
[cmd1, cmd2, cmd3] → undo → [cmd1, cmd2] → undo → [cmd1]
```

**Rules:**
- Maximum history: 100 commands.
- Commands without `undo()` are not added to history.
- New command after undo clears the redo stack.
- Grouping: Multiple related commands can be grouped into a single undo step.

### Keyboard Shortcut Resolution

```
1. Check command.keybinding for exact match.
2. Check user keybinding overrides.
3. Check platform-specific defaults (Ctrl on Linux/Windows, Cmd on macOS).
4. If conflict, last registered wins (with warning in console).
```

### Command Events

| Event | Payload | Description |
|-------|---------|-------------|
| `command:executed` | `{ commandId, args, result }` | After successful execution |
| `command:failed` | `{ commandId, args, error }` | After failed execution |
| `command:undone` | `{ commandId }` | After undo |

## Alternatives Considered

1. **Direct function calls**: Simpler but no undo, no command palette, no discoverability.
2. **Redux-style actions**: More structured but heavier for a desktop app.

## Security Considerations

- Commands are registered with a namespace (plugin id) to prevent conflicts.
- Sensitive commands (file delete, Scilab reset) require confirmation dialogs.
- Command history is stored in memory, not persisted to disk.

## Testing Strategy

- Unit tests for command registration and execution.
- Integration tests for undo/redo stack.
- UI tests for command palette search.
- Performance tests for 1000+ registered commands.

## Rollout

- v0.1: Core commands (file operations, editor actions, Scilab execution).
- v0.2: Plugin commands, full undo/redo.
