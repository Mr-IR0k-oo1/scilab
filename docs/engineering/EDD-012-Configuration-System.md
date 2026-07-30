# EDD-012: Configuration System

## Purpose

The Configuration System manages application settings, project settings, and user preferences with cascading priority.

## Architecture

```
┌─────────────────────────────────────────┐
│        Configuration System              │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Config    │  │ Schema           │   │
│  │ Merge     │  │ Validator        │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Watcher   │  │ Default          │   │
│  │           │  │ Provider         │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Configuration Sources

Priority (highest to lowest):

1. **Command-line arguments** — Runtime overrides
2. **Environment variables** — `SCILAB_STUDIO_*`
3. **Project settings** — `.scstudio/project.json`
4. **User settings** — `~/.scilab-studio/settings.json`
5. **Default settings** — Built-in defaults

## Config Merge

```typescript
interface ConfigMerge {
  merge(...sources: ConfigSource[]): Config;
  get<T>(key: string): T;
  set(key: string, value: any, source?: ConfigSource): void;
}
```

**Merge Rules:**
- Objects are deep-merged.
- Arrays are replaced (not concatenated).
- Scalars are overwritten by higher priority.
- `undefined` values are ignored.

## Schema Validator

```typescript
interface SchemaValidator {
  register(schema: ConfigSchema): void;
  validate(config: Config): ValidationResult;
  getSchema(key: string): FieldSchema | null;
}
```

**Schema Format:**
```json
{
  "key": "editor.tabSize",
  "type": "number",
  "default": 2,
  "minimum": 1,
  "maximum": 8,
  "description": "Number of spaces per tab"
}
```

## Config Watcher

```typescript
interface ConfigWatcher {
  onDidChange(key: string, handler: ConfigChangeHandler): Disposable;
  onAnyChange(handler: ConfigChangeHandler): Disposable;
}
```

**Change Events:**
```typescript
interface ConfigChangeEvent {
  key: string;
  oldValue: any;
  newValue: any;
  source: ConfigSource;
}
```

## Default Provider

```typescript
interface DefaultProvider {
  getDefaults(): ConfigSchema[];
  getDefault(key: string): any;
}
```

## Settings Files

### User Settings (`~/.scilab-studio/settings.json`)
```json
{
  "theme": "dark",
  "editor": {
    "tabSize": 2,
    "wordWrap": true,
    "fontSize": 13
  },
  "scilab": {
    "autoStart": true,
    "timeout": 30000
  }
}
```

### Project Settings (`.scstudio/project.json`)
```json
{
  "name": "My Project",
  "scilab_version": ">=7.0",
  "plugins": ["com.example.my-plugin"],
  "settings": {
    "editor.tabSize": 4
  }
}
```

## Error Handling

- Invalid schema: reject config, use defaults.
- Corrupted file: log warning, use defaults.
- Merge conflict: higher priority wins.

## Performance

- Config read: < 1μs (cached).
- Config write: < 10ms.
- Schema validation: < 1ms.
- Change notification: < 5ms.
