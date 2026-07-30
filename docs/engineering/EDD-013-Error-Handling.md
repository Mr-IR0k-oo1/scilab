# EDD-013: Error Handling

## Purpose

The Error Handling System ensures the application degrades gracefully instead of crashing.

## Error Taxonomy

| Category | Severity | Recovery |
|----------|----------|----------|
| User Error | Low | Show message, continue |
| Module Error | Medium | Log, disable module, continue |
| Runtime Error | High | Log, attempt recovery |
| System Error | Critical | Log, save state, exit |

## Error Types

```typescript
// User Errors
class ValidationError extends Error {}
class FileNotFoundError extends Error {}
class PermissionDeniedError extends Error {}

// Module Errors
class PluginLoadError extends Error {}
class PluginRuntimeError extends Error {}
class WidgetRenderError extends Error {}

// Runtime Errors
class ScilabCrashError extends Error {}
class ScilabTimeoutError extends Error {}
class ScilabSyntaxError extends Error {}

// System Errors
class StorageCorruptedError extends Error {}
class ConfigInvalidError extends Error {}
class DependencyMissingError extends Error {}
```

## Error Handler

```typescript
interface ErrorHandler {
  handle(error: Error, context: ErrorContext): ErrorAction;
  setFallback(handler: (error: Error) => void): void;
}
```

**Error Context:**
```typescript
interface ErrorContext {
  module?: string;
  component?: string;
  operation?: string;
  data?: any;
}
```

**Error Actions:**
```typescript
type ErrorAction =
  | { type: 'retry'; delay: number }
  | { type: 'fallback'; value: any }
  | { type: 'ignore' }
  | { type: 'disable-module'; moduleId: string }
  | { type: 'notify'; message: string }
  | { type: 'crash'; message: string };
```

## Recovery Strategy

```
Error Occurs
    ↓
Log Error (with context)
    ↓
Classify Severity
    ↓
┌─────────────┬──────────────┬──────────────┐
│ Low         │ Medium       │ High         │
│ ↓           │ ↓            │ ↓            │
│ Show Message│ Disable      │ Attempt      │
│ Continue    │ Module       │ Recovery     │
│             │ Continue     │ ↓            │
│             │              │ If Recovery  │
│             │              │ Fails:       │
│             │              │ Disable &    │
│             │              │ Continue     │
└─────────────┴──────────────┴──────────────┘
```

## Module Failure Isolation

```typescript
function withErrorIsolation<T>(
  moduleId: string,
  fn: () => T,
  fallback: T
): T {
  try {
    return fn();
  } catch (error) {
    logger.error(`Module "${moduleId}" failed`, { error });
    eventBus.emit('module:error', { moduleId, error });
    return fallback;
  }
}
```

**Rules:**
- Module errors don't crash the application.
- Module is disabled after 3 errors in 5 minutes.
- User is notified of module failure.
- Other modules continue running.

## Scilab Error Handling

```typescript
interface ScilabErrorHandler {
  handleSyntaxError(error: ScilabSyntaxError): void;
  handleRuntimeError(error: ScilabRuntimeError): void;
  handleCrash(error: ScilabCrashError): void;
  handleTimeout(error: ScilabTimeoutError): void;
}
```

**Recovery:**
- Syntax error: highlight in editor, show in problems panel.
- Runtime error: show in console, suggest fix.
- Crash: auto-restart, replay last command.
- Timeout: interrupt, show timeout message.

## Error Reporting

```typescript
interface ErrorReporter {
  report(error: Error, context: ErrorContext): void;
  getRecent(count: number): ErrorReport[];
  clear(): void;
}
```

**Report Format:**
```json
{
  "id": "err-001",
  "timestamp": "2025-01-15T10:00:00Z",
  "level": "error",
  "message": "Plugin failed to activate",
  "module": "com.example.my-plugin",
  "stack": "...",
  "context": { "operation": "activate" }
}
```

## User-Facing Errors

| Error | Message |
|-------|---------|
| File not found | "File 'data.csv' not found. Check the path." |
| Permission denied | "No permission to read 'secret.txt'." |
| Scilab not found | "Scilab not found. Install Scilab 7.0+." |
| Plugin failed | "Plugin 'My Plugin' failed to load. Check logs." |
| Timeout | "Operation timed out. Try again or increase timeout." |

## Performance

- Error handling overhead: < 1μs.
- Error logging: < 10μs.
- Error recovery: varies by error type.
