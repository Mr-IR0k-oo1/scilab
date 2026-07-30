# Logging API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.1 |
| Stability | Stable |

---

## Purpose

Structured logging for debugging, auditing, and diagnostics.

## Methods

### logger.info(message: string, data?: object): void

Logs an informational message.

```javascript
logger.info('Plugin activated', { pluginId: 'com.example.my-plugin' });
```

### logger.warn(message: string, data?: object): void

Logs a warning.

```javascript
logger.warn('Scilab version mismatch', {
  expected: '>=7.0',
  actual: '6.0.0'
});
```

### logger.error(message: string, data?: object): void

Logs an error.

```javascript
logger.error('Failed to execute command', {
  command: 'analyze',
  error: 'Variable not found'
});
```

### logger.debug(message: string, data?: object): void

Logs a debug message.

```javascript
logger.debug('Event dispatched', {
  event: 'data:imported',
  source: 'csv'
});
```

### logger.trace(message: string, data?: object): void

Logs a trace message (verbose).

```javascript
logger.trace('Widget render cycle', {
  widgetId: 'widget-abc',
  duration: '12ms'
});
```

### logger.group(label: string): void

Starts a log group.

```javascript
logger.group('Import Process');
logger.info('Reading CSV');
logger.info('Parsing data');
logger.groupEnd();
```

### logger.groupEnd(): void

Ends the current log group.

```javascript
logger.groupEnd();
```

### logger.time(label: string): void

Starts a timer.

```javascript
logger.time('render');
// ... work ...
logger.timeEnd('render'); // "render: 45ms"
```

### logger.timeEnd(label: string): void

Ends a timer and logs the duration.

```javascript
logger.timeEnd('render');
```

### logger.setOutput(handler: (entry: LogEntry) => void): Disposable

Routes log output to a custom handler.

```javascript
const disposable = logger.setOutput((entry) => {
  // Send to custom panel
  logPanel.appendEntry(entry);
});
```

## Log Levels

| Level | Value | Description |
|-------|-------|-------------|
| `trace` | 0 | Verbose debugging |
| `debug` | 1 | Debug information |
| `info` | 2 | General information |
| `warn` | 3 | Warnings |
| `error` | 4 | Errors |

### Setting Log Level

```javascript
logger.setLevel('debug');
// trace messages are now hidden
```

## Log Entry

```typescript
interface LogEntry {
  level: 'trace' | 'debug' | 'info' | 'warn' | 'error';
  message: string;
  data?: object;
  timestamp: string;
  source: string;
}
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `log:entry` | `{ entry: LogEntry }` | A log entry was created |
| `log:levelChanged` | `{ level: string }` | Log level changed |

## Examples

### Plugin Logging

```javascript
// In plugin activation
const log = context.getLogger();

log.info('Plugin activated');
log.debug('Registered 3 commands');
log.debug('Registered 1 panel');

// During execution
try {
  const result = await context.executeScilab(code);
  log.info('Scilab execution completed', { duration: result.duration });
} catch (error) {
  log.error('Scilab execution failed', { error: error.message });
}
```

### Performance Logging

```javascript
logger.time('data-import');
const data = await importCSV(file);
logger.timeEnd('data-import'); // "data-import: 1234ms"

logger.time('chart-render');
await viz.createChart('line', data);
logger.timeEnd('chart-render'); // "chart-render: 45ms"
```

### Custom Log Handler

```javascript
// Route logs to a file
const fs = require('fs');
const logStream = fs.createWriteStream('scilab-studio.log');

logger.setOutput((entry) => {
  const line = `[${entry.timestamp}] ${entry.level.toUpperCase()}: ${entry.message}\n`;
  logStream.write(line);
});
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `InvalidLevel` | LG-001 | Invalid log level |
| `LogQuotaExceeded` | LG-002 | Log buffer full |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
