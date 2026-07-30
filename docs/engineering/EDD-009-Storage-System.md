# EDD-009: Storage System

## Purpose

The Storage System manages persistent data: settings, project data, plugin data, and user preferences.

## Architecture

```
┌─────────────────────────────────────────┐
│          Storage System                  │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Key-Value │  │ File             │   │
│  │ Store     │  │ System           │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Schema    │  │ Migration        │   │
│  │ Manager   │  │ Engine           │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Storage Layers

| Layer | Location | Purpose |
|-------|----------|---------|
| Global | `~/.scilab-studio/` | App settings, plugins |
| Project | `.scstudio/` | Project data, layout |
| Plugin | `plugins/{id}/` | Plugin-specific data |
| Session | Memory only | Temporary data |

## Key-Value Store

```typescript
interface KeyValueStore {
  get<T>(key: string): Promise<T | undefined>;
  set<T>(key: string, value: T): Promise<void>;
  delete(key: string): Promise<void>;
  has(key: string): Promise<boolean>;
  keys(pattern?: string): Promise<string[]>;
  clear(): Promise<void>;
}
```

**Implementation:**
- SQLite database for structured data.
- JSON files for simple settings.
- Memory cache for hot data.

## File System Interface

```typescript
interface FileSystem {
  readFile(path: string): Promise<Buffer>;
  writeFile(path: string, data: Buffer): Promise<void>;
  exists(path: string): Promise<boolean>;
  stat(path: string): Promise<FileStat>;
  list(dir: string): Promise<FileEntry[]>;
  watch(path: string, handler: FileChangeHandler): Disposable;
}
```

**Rules:**
- All paths are relative to project root.
- No path traversal (`../`).
- Symlinks are resolved and checked.
- File watcher with rate limiting.

## Schema Manager

```typescript
interface SchemaManager {
  getSchema(version: string): Schema;
  validate(data: any, schema: Schema): ValidationResult;
  migrate(data: any, fromVersion: string, toVersion: string): any;
}
```

**Schema Format:**
```json
{
  "version": "1.0",
  "fields": {
    "name": { "type": "string", "required": true },
    "version": { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" }
  }
}
```

## Migration Engine

```typescript
interface MigrationEngine {
  register(migration: Migration): void;
  migrate(data: any, fromVersion: string, toVersion: string): any;
  getAvailableVersions(): string[];
}
```

**Migration Format:**
```typescript
interface Migration {
  from: string;
  to: string;
  up: (data: any) => any;
  down: (data: any) => any;
}
```

## Data Types

### Project Settings
```json
{
  "name": "My Project",
  "version": "1.0.0",
  "scilab_version": ">=7.0",
  "plugins": [],
  "settings": {}
}
```

### User Settings
```json
{
  "theme": "dark",
  "font_size": 13,
  "auto_save": true,
  "auto_save_delay": 1000,
  "editor": {
    "tab_size": 2,
    "word_wrap": true
  }
}
```

### Plugin Storage
```json
{
  "lastRun": "2025-01-15T10:00:00Z",
  "runCount": 42,
  "settings": {}
}
```

## Error Handling

- Corrupted data: attempt recovery, fall back to defaults.
- Schema validation failure: reject data, log error.
- Migration failure: abort, log, keep original data.
- File system error: retry once, then fail.

## Performance

- KV read: < 1ms (cached), < 10ms (disk).
- KV write: < 10ms.
- File read: < 50ms (10MB file).
- File write: < 100ms (10MB file).
- Schema validation: < 1ms.

## Persistence

- Settings: immediate write.
- Project data: on save (manual or auto-save).
- Plugin data: on change (debounced 1s).
- Session data: lost on close.
