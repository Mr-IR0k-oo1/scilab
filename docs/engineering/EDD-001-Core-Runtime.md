# EDD-001: Core Runtime

## Purpose

The Core Runtime is the foundation of Scilab Studio. It provides the event bus, module system, configuration, logging, and lifecycle management. Everything else builds on it.

## Architecture

```
┌─────────────────────────────────────────┐
│            Core Runtime                  │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Event Bus │  │ Module Registry  │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Config    │  │ Logger           │   │
│  └───────────┘  └──────────────────┘   │
│  ┌──────────────────────────────────┐  │
│  │ Lifecycle Manager                │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Components

### Event Bus

A publish-subscribe system for inter-module communication.

```typescript
interface EventBus {
  on(event: string, handler: EventHandler): Disposable;
  emit(event: string, data?: any): void;
  off(event: string, handler: EventHandler): void;
}
```

**Guarantees:**
- Event delivery is synchronous within a module.
- Event delivery order is registration order.
- Errors in handlers are caught and logged.
- Handlers can return values (used by some events).

**Event Naming:**
```
module:action
workspace:fileOpened
plugin:activated
runtime:ready
```

### Module Registry

Tracks all loaded modules and their state.

```typescript
interface ModuleRegistry {
  register(module: ModuleDescriptor): void;
  get(id: string): ModuleDescriptor | null;
  getAll(): ModuleDescriptor[];
  getActive(): ModuleDescriptor[];
}
```

**Module States:**
```
Discovered → Registered → Active → Paused → Stopped → Unregistered
```

### Configuration

Manages application and module settings.

```typescript
interface Configuration {
  get<T>(key: string): T | undefined;
  set(key: string, value: any): void;
  onDidChange(key: string, handler: (value: any) => void): Disposable;
}
```

**Configuration Sources (priority order):**
1. Command-line arguments
2. Environment variables
3. Project settings (`.scstudio/project.json`)
4. User settings (`~/.scilab-studio/settings.json`)
5. Default settings

### Logger

Structured logging with levels and categories.

```typescript
interface Logger {
  info(message: string, data?: object): void;
  warn(message: string, data?: object): void;
  error(message: string, data?: object): void;
  debug(message: string, data?: object): void;
}
```

**Log Destinations:**
- Console (stdout)
- File (`~/.scilab-studio/logs/`)
- UI Panel (Log Viewer)

### Lifecycle Manager

Manages application startup and shutdown.

```
Startup:
1. Load configuration
2. Initialize event bus
3. Initialize logger
4. Scan for modules
5. Register modules
6. Activate modules
7. Restore workspace state
8. Ready

Shutdown:
1. Save workspace state
2. Deactivate modules (reverse order)
3. Flush logs
4. Close event bus
5. Exit
```

## Interfaces

```typescript
interface CoreRuntime {
  readonly eventBus: EventBus;
  readonly modules: ModuleRegistry;
  readonly config: Configuration;
  readonly logger: Logger;
  readonly lifecycle: LifecycleManager;

  initialize(): Promise<void>;
  shutdown(): Promise<void>;
  getVersion(): string;
}
```

## Error Handling

- Event bus errors are caught and logged.
- Module activation failures are logged, module is skipped.
- Configuration errors fall back to defaults.
- Logger errors are written to stderr.

## Performance

- Event bus: < 1μs per emit.
- Module registration: < 1ms.
- Configuration read: < 1μs.
- Startup: < 500ms (excluding Scilab).
