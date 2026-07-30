# EDD-004: Plugin Runtime

## Purpose

The Plugin Runtime manages third-party plugin loading, sandboxing, and lifecycle.

## Architecture

```
┌─────────────────────────────────────────┐
│          Plugin Runtime                  │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Plugin    │  │ Sandbox          │   │
│  │ Loader    │  │ Manager          │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Permission│  │ Plugin           │   │
│  │ Enforcer  │  │ Storage          │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Plugin Loading

```typescript
interface PluginLoader {
  load(manifestPath: string): Promise<PluginContext>;
  unload(pluginId: string): Promise<void>;
  reload(pluginId: string): Promise<void>;
}
```

**Loading Process:**
1. Read and validate `plugin.json`.
2. Check permissions.
3. Create sandbox context.
4. Load entry point (`index.js`).
5. Call `onActivate(context)`.
6. Register provided services.

## Sandbox

Plugins run in isolated JavaScript contexts:

```typescript
interface Sandbox {
  readonly pluginId: string;
  readonly permissions: Permission[];

  // Limited APIs
  eventBus: ScopedEventBus;
  storage: ScopedStorage;
  logger: TaggedLogger;
  ui: ScopedUI;

  // Restricted
  fileSystem: RestrictedFS;
  network: RestrictedNetwork;
}
```

**Restrictions:**
- No Node.js APIs.
- No `process` object.
- No `require()` for core modules.
- No file system outside project (unless permitted).
- No network (unless permitted).

## Permission Enforcement

```typescript
function checkPermission(sandbox: Sandbox, permission: Permission): void {
  if (!sandbox.permissions.includes(permission)) {
    throw new PermissionDeniedError(
      `Plugin "${sandbox.pluginId}" requires "${permission}"`
    );
  }
}
```

**Permission Checks:**
- At API call time (runtime enforcement).
- Not just at load time.

## Plugin Storage

```typescript
interface ScopedStorage {
  get(key: string): Promise<any>;
  set(key: string, value: any): Promise<void>;
  delete(key: string): Promise<void>;
  keys(): Promise<string[]>;
}
```

Storage is namespaced: `plugins/{pluginId}/storage/`.

## Plugin Communication

Plugins communicate through the event bus:

```typescript
// Plugin A emits
context.emit('data:imported', { file: 'data.csv' });

// Plugin B listens
context.on('data:imported', (data) => {
  // Process data
});
```

**Rules:**
- Plugins cannot call each other directly.
- All communication through events.
- Events are logged for debugging.

## Error Handling

- Plugin load failure: log, skip plugin.
- Plugin runtime error: catch, log, show in plugin panel.
- Plugin crash: deactivate, log, notify user.
- Repeated crashes (3 in 5 minutes): auto-deactivate.

## Recovery

```
Plugin Error
    ↓
Log Error
    ↓
Show in Plugin Panel
    ↓
Attempt Recovery (restart context)
    ↓
If Recovery Fails: Deactivate Plugin
    ↓
Notify User
```

## Performance

- Plugin load: < 500ms.
- Plugin activation: < 100ms.
- Permission check: < 1μs.
- Event delivery: < 5μs.
