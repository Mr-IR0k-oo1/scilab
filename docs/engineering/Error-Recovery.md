# Error Recovery

## Recovery Strategy

Engineering software should degrade gracefully. Never crash when you can recover.

## Recovery Flow

```
Error Occurs
    ↓
Log Error (with context)
    ↓
Classify Severity
    ↓
┌─────────────────────────────────────────────┐
│ Low (User Error)                            │
│  → Show message                             │
│  → Continue                                 │
├─────────────────────────────────────────────┤
│ Medium (Module Error)                       │
│  → Log error                                │
│  → Disable module                           │
│  → Notify user                              │
│  → Continue                                 │
├─────────────────────────────────────────────┤
│ High (System Error)                         │
│  → Log error                                │
│  → Attempt recovery                         │
│  → If recovery fails:                       │
│    → Save state                             │
│    → Disable affected component             │
│    → Continue with reduced functionality    │
├─────────────────────────────────────────────┤
│ Critical (Fatal Error)                      │
│  → Log error                                │
│  → Save state                               │
│  → Show error dialog                        │
│  → Offer to restart                         │
└─────────────────────────────────────────────┘
```

## Module Failure Isolation

```typescript
function isolateModule<T>(moduleId: string, fn: () => T, fallback: T): T {
  try {
    return fn();
  } catch (error) {
    // Log
    logger.error(`Module "${moduleId}" failed`, { error, moduleId });

    // Disable module
    moduleRegistry.disable(moduleId);

    // Notify user
    ui.showWarning(`Module "${moduleId}" encountered an error and has been disabled.`);

    // Emit event
    eventBus.emit('module:error', { moduleId, error });

    return fallback;
  }
}
```

## Auto-Recovery Rules

| Error | Recovery | Max Retries |
|-------|----------|-------------|
| Scilab crash | Restart process | 3 |
| Plugin crash | Deactivate plugin | 3 |
| File write failure | Retry once | 1 |
| State corruption | Fall back to defaults | 1 |
| Memory pressure | Force garbage collection | 1 |

## Recovery Escalation

```
Attempt 1: Auto-recover (silent)
    ↓ (if fails)
Attempt 2: Auto-recover (notify user)
    ↓ (if fails)
Attempt 3: Disable component (notify user)
    ↓ (if fails)
Attempt 4: Save state, offer restart
```

## State Preservation

Before recovery:

1. Save current workspace state.
2. Save current project state.
3. Save error report.
4. Attempt recovery.

After recovery:

1. Restore workspace state.
2. Restore project state.
3. Verify state integrity.
4. Notify user of recovery status.

## User-Facing Messages

| Error | Message | Action |
|-------|---------|--------|
| Module crash | "Module X encountered an error and has been disabled." | Retry, Ignore |
| Scilab crash | "Scilab crashed. Restarting..." | Wait |
| File write failed | "Could not save file. Check permissions." | Retry, Save As |
| State corrupted | "Project data is corrupted. Using defaults." | Continue |
| Memory pressure | "Running low on memory. Closing unused tabs." | Continue |

## Error Reporting

```typescript
interface ErrorReport {
  id: string;
  timestamp: string;
  level: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  module?: string;
  stack: string;
  context: object;
  recovery: 'auto' | 'manual' | 'none';
  recovered: boolean;
}
```

## Rules

- Never lose user data.
- Always save state before recovery.
- Always log before recovering.
- Always notify the user.
- Never silently fail.
- Always provide a path forward.
