# RFC-0008: Extension Permissions

| Field | Value |
|-------|-------|
| RFC | 0008 |
| Title | Extension Permissions |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines the security model for plugins and widgets.

## Motivation

Plugins can execute arbitrary code. A permission system protects users from malicious or buggy plugins by requiring explicit consent for sensitive operations.

## Detailed Design

### Permission Model

Permissions are declared in the plugin manifest and granted by the user at install time.

```json
{
  "permissions": [
    "scilab.execute",
    "storage.read",
    "ui.panel"
  ]
}
```

### Permission Categories

| Category | Permissions | Risk |
|----------|-------------|------|
| **Scilab** | `scilab.execute`, `scilab.read`, `scilab.write` | Medium — can run arbitrary code |
| **Storage** | `storage.read`, `storage.write` | Low — scoped to plugin's own storage |
| **UI** | `ui.panel`, `ui.menu`, `ui.statusbar`, `ui.dialog` | Low — visual only |
| **File** | `file.read`, `file.write` | High — access to project files |
| **Network** | `network` | High — can send data externally |

### Permission Flow

```
Plugin declares permissions in manifest
    ↓
User reviews permissions during installation
    ↓
User grants/denies each permission
    ↓
Plugin is installed with granted permissions
    ↓
Runtime checks enforce permissions
```

### Runtime Enforcement

```typescript
// In plugin context
function checkPermission(permission: string): void {
  if (!grantedPermissions.includes(permission)) {
    throw new PermissionDeniedError(
      `Plugin "${pluginId}" requires "${permission}" permission`
    );
  }
}
```

### Permission Dialog

When installing a plugin, the user sees:

```
┌─────────────────────────────────────────┐
│ Install Plugin: My Plugin               │
│                                         │
│ This plugin requests:                   │
│                                         │
│ ✅ Scilab Execute     [Required]        │
│    Run Scilab commands                  │
│                                         │
│ ☐ File Read           [Optional]        │
│    Read project files                   │
│                                         │
│ ☐ Network             [Optional]        │
│    Make network requests                │
│                                         │
│ [Install]  [Cancel]                     │
└─────────────────────────────────────────┘
```

- Required permissions are checked by default and cannot be denied.
- Optional permissions can be granted or denied.
- Denied permissions cause runtime errors when accessed.

### Permission Revocation

Users can revoke permissions after installation:

1. Open Plugin Manager.
2. Select the plugin.
3. Open Permissions panel.
4. Toggle permissions.
5. Plugin is restarted with new permissions.

### Elevated Permissions

Some operations require elevated permissions:

- File write outside project directory: Requires user confirmation dialog.
- Network access to external URLs: Requires user confirmation dialog.
- Scilab execution of destructive commands (`clear`, `quit`): Requires confirmation.

## Alternatives Considered

1. **No permissions**: Simpler but dangerous. A malicious plugin can do anything.
2. **OS-level sandboxing**: Stronger but complex and platform-specific.
3. **Code review**: Manual review of all plugins. Not scalable.

## Security Considerations

- Permissions are enforced at runtime, not just at install time.
- Permission checks are fast (< 1μs overhead per call).
- Denied permission attempts are logged for security auditing.
- Plugins cannot escalate their own permissions.

## Testing Strategy

- Unit tests for permission checking logic.
- Integration tests for permission enforcement.
- Security tests for permission bypass attempts.
- UI tests for permission dialogs.

## Rollout

- v0.1: Permissions declared but not enforced (development mode).
- v0.2: Full permission enforcement, Plugin Marketplace requires review.
