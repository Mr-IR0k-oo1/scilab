# Deprecation Policy

## Principles

1. **Predictable**: Deprecations are announced in advance.
2. **Gradual**: Deprecated features work for at least 2 major versions.
3. **Documented**: All deprecations are documented with alternatives.
4. **Tooling**: Migration tools are provided when possible.

## Deprecation Process

### 1. Announce
- Add deprecation notice to documentation.
- Add console warning when deprecated feature is used.
- Create issue tracking removal.

### 2. Warn
- Log warnings when deprecated features are used.
- Include migration instructions in warnings.
- Track usage of deprecated features.

### 3. Remove
- Remove deprecated feature after 2 major versions.
- Update documentation.
- Provide migration tool (if possible).

## Deprecation Notice Format

```
[DEPRECATED] Feature "X" is deprecated since v0.2 and will be removed in v0.4.
Use "Y" instead. See migration guide: https://docs.scilab-studio.org/migration
```

## Console Warning

```typescript
function deprecated(oldFn: string, newFn: string) {
  console.warn(
    `[DEPRECATED] "${oldFn}" is deprecated. Use "${newFn}" instead.`
  );
}
```

## Documentation Format

```markdown
!!! warning "Deprecated"
    This feature is deprecated since v0.2 and will be removed in v0.4.
    
    Use [New Feature](new-feature.md) instead.
    
    See [Migration Guide](../release/Migration-Guide.md) for details.
```

## Tracked Deprecations

| Feature | Deprecated In | Removed In | Replacement |
|---------|--------------|-----------|-------------|
| v0.1 plugin API | v0.2 | v0.4 | v0.2 plugin API |
| v0.1 widget API | v0.2 | v0.4 | v0.2 widget API |

## Rules

- No surprise removals. Always announce first.
- Provide clear migration paths.
- Track deprecation usage.
- Don't deprecate in patch versions.
- Don't remove in minor versions.
