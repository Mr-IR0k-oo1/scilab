# EDD-003: Module System

## Purpose

The Module System handles discovery, registration, lifecycle, and dependency management for all platform components.

## Architecture

```
┌─────────────────────────────────────────┐
│           Module System                  │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Discovery │  │ Dependency       │   │
│  │ Engine    │  │ Resolver         │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Lifecycle │  │ Isolation        │   │
│  │ Manager   │  │ Context          │   │
│  └───────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

## Module Types

| Type | Description | Example |
|------|-------------|---------|
| `core` | Platform services | Event Bus, Logger |
| `feature` | User-facing modules | GUI Builder, Viz Studio |
| `plugin` | Third-party extensions | Community plugins |
| `widget` | Custom GUI components | Gauge, Chart Widget |
| `theme` | Visual themes | Ocean, Monokai |

## Module Descriptor

```typescript
interface ModuleDescriptor {
  id: string;
  name: string;
  version: string;
  type: ModuleType;
  description: string;
  author: string;
  license: string;
  dependencies: Dependency[];
  provides: ServiceDescriptor[];
  activation: ActivationCondition;
}
```

## Lifecycle

```
Discovery → Registration → Dependency Check → Activation → Running → Deactivation → Cleanup
```

### Discovery
Scan configured directories for module manifests.

### Registration
Validate manifest, register with Module Registry.

### Dependency Check
Resolve all dependencies. Reject if unresolvable.

### Activation
Call module's `onActivate()`. Module begins providing services.

### Running
Module is active and responsive.

### Deactivation
Call module's `onDeactivate()`. Release resources.

### Cleanup
Remove from registry. Release isolation context.

## Dependency Resolution

```typescript
interface Dependency {
  id: string;
  version: string;  // semver range
  optional: boolean;
}
```

**Resolution Algorithm:**
1. Collect all dependencies (recursive).
2. Build dependency graph.
3. Check for cycles (reject if found).
4. Topological sort (activation order).
5. Verify all versions compatible.

**Error Cases:**
- Missing dependency: reject module.
- Circular dependency: reject module.
- Version conflict: reject module.

## Isolation Context

Each module runs in an isolated context:

```typescript
interface IsolationContext {
  readonly moduleId: string;
  eventBus: EventBus;  // Scoped to module
  storage: Storage;    // Namespaced to module
  logger: Logger;      // Tagged with module ID
}
```

**Rules:**
- Module cannot access other modules' storage.
- Module cannot modify the event bus structure.
- Module cannot access the file system outside project.
- Module errors are caught and logged, not propagated.

## Error Handling

- Module activation failure: log error, skip module.
- Module runtime error: catch, log, notify user.
- Module deactivation failure: log warning, force cleanup.
- Dependency resolution failure: reject module, log.

## Performance

- Discovery: < 100ms for 50 modules.
- Registration: < 1ms per module.
- Activation: < 100ms per module.
- Total startup: < 2 seconds for 20 modules.
