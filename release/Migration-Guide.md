# Migration Guide

## v0.1 → v0.2

### Project Files

No changes. Projects created in v0.1 work in v0.2.

### Plugin API

```typescript
// v0.1
context.registerCommand('my-command', handler);

// v0.2
context.registerCommand({
  id: 'my-plugin.my-command',
  label: 'My Command',
  execute: handler
});
```

### Widget API

```typescript
// v0.1
{
  type: 'button',
  label: 'Click',
  onClick: handler
}

// v0.2
{
  type: 'button',
  properties: {
    label: { type: 'string', default: 'Click' }
  },
  events: {
    onClick: { label: 'Clicked' }
  },
  render: (props) => { /* ... */ }
}
```

## v0.2 → v0.3

### Plugin Manifest

```json
// v0.2
{
  "id": "my-plugin",
  "version": "1.0.0"
}

// v0.3
{
  "id": "com.example.my-plugin",
  "version": "1.0.0",
  "permissions": ["scilab.execute"]
}
```

### Event Names

```typescript
// v0.2
context.on('data-imported', handler);

// v0.3
context.on('data:imported', handler);
```

## Migration Steps

1. Read the migration guide for the target version.
2. Update your code according to the changes.
3. Run the migration tool (if available):
   ```bash
   scilab-studio migrate --from 0.2 --to 0.3
   ```
4. Test your plugin/widget.
5. Update the manifest version.

## Deprecation Timeline

| Feature | Deprecated In | Removed In |
|---------|--------------|-----------|
| v0.1 plugin API | v0.2 | v0.4 |
| v0.1 widget API | v0.2 | v0.4 |
| Undocumented events | v0.2 | v0.3 |

## Breaking Change Policy

- Breaking changes require a major version bump.
- Deprecated features are removed after 2 major versions.
- Migration tools are provided when possible.
- Documentation is updated before release.
