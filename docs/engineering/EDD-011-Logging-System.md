# EDD-011: Logging System

## Purpose

The Logging System provides structured, leveled logging for debugging, auditing, and diagnostics.

## Architecture

```
┌─────────────────────────────────────────┐
│          Logging System                  │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Logger    │  │ Transport        │   │
│  │ Factory   │  │ Manager          │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Log       │  │ Filter           │   │
│  │ Buffer    │  │ Engine           │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Log Levels

| Level | Value | Use |
|-------|-------|-----|
| `trace` | 0 | Verbose debugging |
| `debug` | 1 | Debug information |
| `info` | 2 | General information |
| `warn` | 3 | Warnings |
| `error` | 4 | Errors |

## Logger

```typescript
interface Logger {
  trace(message: string, data?: object): void;
  debug(message: string, data?: object): void;
  info(message: string, data?: object): void;
  warn(message: string, data?: object): void;
  error(message: string, data?: object): void;
  group(label: string): void;
  groupEnd(): void;
  time(label: string): void;
  timeEnd(label: string): void;
}
```

## Log Entry

```typescript
interface LogEntry {
  level: LogLevel;
  message: string;
  data?: object;
  timestamp: string;
  source: string;
  module?: string;
}
```

## Transports

| Transport | Destination | Format |
|-----------|-------------|--------|
| Console | stdout | Human-readable |
| File | `~/.scilab-studio/logs/` | JSON lines |
| UI Panel | Log Viewer panel | Formatted |

```typescript
interface Transport {
  write(entry: LogEntry): void;
  flush(): void;
  close(): void;
}
```

## Filter Engine

```typescript
interface FilterEngine {
  setLevel(level: LogLevel): void;
  addFilter(filter: LogFilter): void;
  removeFilter(filterId: string): void;
  shouldLog(entry: LogEntry): boolean;
}
```

**Filters:**
- By level (minimum level).
- By source (specific module).
- By pattern (regex match).

## Log Buffer

```typescript
interface LogBuffer {
  push(entry: LogEntry): void;
  getRecent(count: number): LogEntry[];
  search(query: string): LogEntry[];
  clear(): void;
}
```

**Buffer Size:** 10,000 entries (circular).

## Logger Factory

```typescript
interface LoggerFactory {
  create(source: string, module?: string): Logger;
  setLevel(level: LogLevel): void;
  setOutput(handler: (entry: LogEntry) => void): Disposable;
}
```

## Error Handling

- Transport failure: fall back to console.
- Buffer overflow: drop oldest entries.
- Logger creation failure: return no-op logger.

## Performance

- Log entry creation: < 1μs.
- Log entry delivery: < 5μs.
- Buffer search: < 10ms for 10k entries.
- File write: async, non-blocking.
