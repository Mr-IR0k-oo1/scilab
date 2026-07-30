# EDD-015: Security

## Purpose

The Security System protects against malicious plugins, data leakage, and unauthorized access.

## Threat Model

| Threat | Severity | Mitigation |
|--------|----------|-----------|
| Malicious plugin | High | Sandboxing, permissions |
| Path traversal | Medium | Path validation |
| Code injection | High | Input sanitization |
| Data leakage | Medium | No telemetry, offline-first |
| Dependency vulnerability | Medium | Auditing, pinning |

## Plugin Security

### Sandboxing
- Plugins run in isolated JavaScript contexts.
- No access to Node.js APIs.
- No access to file system outside project.
- No network access (unless permitted).

### Permission System
```typescript
interface PermissionSystem {
  request(pluginId: string, permission: Permission): Promise<boolean>;
  check(pluginId: string, permission: Permission): boolean;
  revoke(pluginId: string, permission: Permission): void;
  getGranted(pluginId: string): Permission[];
}
```

### Code Review
- All published plugins require review.
- Automated scanning for known vulnerabilities.
- Manual review for security-sensitive plugins.

## File System Security

### Path Validation
```typescript
function validatePath(path: string, projectRoot: string): boolean {
  const resolved = path.resolve(path);
  return resolved.startsWith(projectRoot);
}
```

### Rules
- No path traversal (`../`).
- No symlinks outside project.
- No write outside project directory.
- File watcher with rate limiting.

## Input Sanitization

```typescript
interface InputSanitizer {
  sanitizeHTML(input: string): string;
  sanitizePath(input: string): string;
  sanitizeSQL(input: string): string;
  sanitizeRegex(input: string): string;
}
```

## Data Security

### No Telemetry
- No usage data collected.
- No analytics.
- No phone-home.

### Offline-First
- All data stored locally.
- No cloud sync (unless user opts in).
- Network requests only when user initiates.

### Secrets
- No secrets in source code.
- No API keys in client-side code.
- Credentials stored in OS keychain (v0.2+).

## Dependency Security

```typescript
interface DependencyAuditor {
  audit(): VulnerabilityReport[];
  fix(vulnerability: Vulnerability): void;
  getPolicy(): SecurityPolicy;
}
```

**Policy:**
- Dependencies pinned to exact versions.
- Lock files committed.
- Audited weekly.
- Vulnerabilities patched within 48 hours.

## Security Checklist

- [ ] All user input validated.
- [ ] All file paths validated.
- [ ] Plugin sandboxing enforced.
- [ ] Permissions enforced at runtime.
- [ ] No secrets in code.
- [ ] Dependencies audited.
- [ ] No telemetry.
- [ ] Error messages don't expose internals.
- [ ] Logging doesn't include sensitive data.
- [ ] File system access is restricted.

## Incident Response

1. Vulnerability reported.
2. Severity assessed.
3. Fix developed and tested.
4. Release patched version.
5. Users notified.
6. Post-mortem conducted.

## Performance

- Permission check: < 1μs.
- Path validation: < 1μs.
- Input sanitization: < 10μs.
- Dependency audit: < 30 seconds.
