# Security Standards

## Principles

1. **Defense in Depth**: Multiple layers of security.
2. **Least Privilege**: Minimum necessary permissions.
3. **Secure by Default**: Secure options enabled by default.
4. **Fail Securely**: Errors don't expose sensitive data.

## Input Validation

- Validate all user input.
- Sanitize file paths.
- Limit input length.
- Reject unexpected data types.

```typescript
// Good
function validateProjectName(name: string): boolean {
  return /^[a-zA-Z0-9_-]+$/.test(name) && name.length <= 100;
}

// Bad
function validateProjectName(name: string): boolean {
  return name.length > 0; // Accepts anything
}
```

## Plugin Security

- Plugins run in sandboxed contexts.
- Permissions are declared and enforced.
- File system access is restricted to project directory.
- Network access requires explicit permission.
- Plugins cannot modify other plugins.

## File System Security

- Paths are normalized and validated.
- No path traversal (`../`).
- Project root is the boundary.
- Symlinks are resolved and checked.

## Data Security

- No secrets in source code.
- No API keys in client-side code.
- Sensitive data is not logged.
- User data is not transmitted without consent.

## Dependency Security

- Dependencies are audited regularly.
- Known vulnerabilities are patched immediately.
- Dependencies are pinned to specific versions.
- Lock files are committed.

## Error Handling

- Errors don't expose internal details.
- Stack traces are logged, not displayed.
- User-facing errors are descriptive but safe.

## Checklist

- [ ] Input validation on all user inputs.
- [ ] Path traversal prevention.
- [ ] Plugin sandboxing enforced.
- [ ] No secrets in code.
- [ ] Dependencies audited.
- [ ] Error messages are safe.
- [ ] Logging doesn't expose sensitive data.
- [ ] Permissions follow least privilege.
