# Dependency Rules

## Layer Architecture

```
Applications
      │
Feature Modules
      │
Platform Services
      │
Core Runtime
      │
Scilab Engine
```

## Rules

### Rule 1: Dependencies Flow Down

```
Applications → Feature Modules → Platform Services → Core Runtime → Scilab Engine
```

**Violation:** A Feature Module importing from another Feature Module.

**Violation:** A Platform Service importing from a Feature Module.

**Violation:** Core Runtime importing from a Platform Service.

### Rule 2: No Circular Dependencies

No module may depend on a module that depends on it.

**Detection:** Build-time analysis rejects circular dependencies.

### Rule 3: Core Runtime Has No Dependencies

The Core Runtime depends only on:
- External libraries (Tauri, Svelte).
- Standard library (Node.js, Rust std).
- No application code.

### Rule 4: Services Communicate Through Events

Services do not call each other directly. All inter-service communication uses the Event Bus.

```typescript
// Wrong: Direct call
const data = dataService.import(file);
vizService.createChart('line', data);

// Right: Event-based
dataService.import(file);
eventBus.emit('data:imported', { file });
// Visualization service listens and creates chart
```

### Rule 5: Applications Are Thin

Applications are thin wrappers that:
- Wire services together.
- Configure the workspace.
- Handle application lifecycle.

Applications do not contain business logic.

## Dependency Matrix

| Layer | Can Depend On |
|-------|--------------|
| Applications | Feature Modules, Platform Services, Core Runtime |
| Feature Modules | Platform Services, Core Runtime |
| Platform Services | Core Runtime |
| Core Runtime | External libraries only |
| Scilab Engine | External (separate process) |

## Enforcement

### Build-Time
- ESLint rule: `no-cross-layer-import`.
- Rust: `cargo-deny` for dependency checking.
- CI: Checks all imports follow the layer rules.

### Runtime
- Module isolation prevents direct access.
- Event Bus mediates all communication.

## Violation Response

1. CI build fails.
2. Developer is notified of violation.
3. Fix: refactor to follow the layer rules.
4. If the violation is justified: document the exception.

## Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Applications                       │
│  Lab Creator │ Dashboard Builder │ Report Studio     │
├─────────────────────────────────────────────────────┤
│                 Feature Modules                      │
│  GUI Builder │ Viz Studio │ Data Studio │ Templates  │
├─────────────────────────────────────────────────────┤
│               Platform Services                      │
│  Visualization │ Widget │ Plugin │ Data │ Scilab     │
│  Report │ Theme │ AI │ Storage │ Logging             │
├─────────────────────────────────────────────────────┤
│                  Core Runtime                        │
│  Event Bus │ Module System │ Config │ Commands       │
├─────────────────────────────────────────────────────┤
│                 Scilab Engine                        │
│  (JSON-RPC over stdin/stdout)                       │
└─────────────────────────────────────────────────────┘
```
