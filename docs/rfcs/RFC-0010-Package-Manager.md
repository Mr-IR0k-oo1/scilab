# RFC-0010: Package Manager

| Field | Value |
|-------|-------|
| RFC | 0010 |
| Title | Package Manager |
| Status | Accepted |
| Author | Scilab Studio Team |
| Created | 2025-01-15 |
| Updated | 2025-01-15 |
| Version | 1.0 |

---

## Summary

Defines how plugins, widgets, templates, and themes are discovered, installed, updated, and removed.

## Motivation

The platform needs a unified way to manage extensions. Users should install a plugin, widget, or template with one click, not manually download and extract files.

## Detailed Design

### Package Types

| Type | Extension | Location |
|------|-----------|----------|
| Plugin | `.scplugin` | `~/.scilab-studio/plugins/` |
| Widget | `.scwidget` | `~/.scilab-studio/widgets/` |
| Template | `.sctemplate` | `~/.scilab-studio/templates/` |
| Theme | `.sctheme` | `~/.scilab-studio/themes/` |

### Package Manifest

Every package includes a manifest:

```json
{
  "type": "plugin",
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "A brief description",
  "author": "Author Name",
  "license": "MIT",
  "repository": "https://github.com/example/my-plugin",
  "keywords": ["engineering", "signal-processing"],
  "scilab_studio_version": ">=0.1",
  "dependencies": {},
  "assets": [
    {
      "path": "index.js",
      "type": "javascript"
    }
  ]
}
```

### Package Sources

| Source | Description | v0.1 |
|--------|-------------|------|
| Local | Install from `.scplugin` file | ✅ |
| Registry | Install from central registry | ✅ |
| Git | Install from git repository | ❌ v0.2 |
| Marketplace | Browse and install from UI | ❌ v0.2 |

### Installation Flow

```
User clicks Install
    ↓
Package is downloaded (or copied from local)
    ↓
Manifest is validated
    ↓
Dependencies are resolved
    ↓
Permissions are reviewed
    ↓
Package is extracted to target directory
    ↓
Package is activated
    ↓
Success notification
```

### Dependency Resolution

- Dependencies are declared in the manifest.
- The package manager resolves versions using semver.
- Circular dependencies are rejected.
- Missing dependencies show an error with installation instructions.

### Update Flow

```
Check for updates (on startup or manual)
    ↓
Compare installed vs available versions
    ↓
Show update notifications
    ↓
User clicks Update
    ↓
Download new version
    ↓
Run migration script (if any)
    ↓
Replace old version
    ↓
Restart package
```

### Removal Flow

```
User clicks Remove
    ↓
Confirm removal
    ↓
Call package cleanup hook
    ↓
Remove package files
    ↓
Remove from installed list
    ↓
Success notification
```

### CLI Interface

```bash
# Install from file
scilab-studio install ./my-plugin.scplugin

# Install from registry
scilab-studio install com.example.my-plugin

# List installed
scilab-studio list

# Update all
scilab-studio update

# Remove
scilab-studio remove com.example.my-plugin

# Search
scilab-studio search "signal processing"
```

### Package Registry

The central registry stores package metadata:

```
https://registry.scilab-studio.org/api/v1/packages/
```

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/packages` | List all packages |
| GET | `/packages/:id` | Get package metadata |
| GET | `/packages/:id/versions` | List versions |
| GET | `/packages/:id/versions/:version` | Get specific version |
| POST | `/packages` | Publish package (auth required) |

### Package Validation

Before installation, packages are validated:

1. Manifest schema validation.
2. Required fields present.
3. Version format valid.
4. Dependencies resolvable.
5. No conflicting packages.
6. Scilab Studio version compatibility.

## Alternatives Considered

1. **npm-style**: Full npm compatibility. Too complex for our use case.
2. **Git submodules**: Version control but no UI. Not user-friendly.
3. **No package manager**: Manual installation. Not scalable.

## Security Considerations

- Packages are scanned for known vulnerabilities before installation.
- Packages are sandboxed (see RFC-0008: Extension Permissions).
- Package signatures verify author identity.
- Packages from untrusted sources require explicit user consent.

## Testing Strategy

- Unit tests for manifest parsing and validation.
- Integration tests for install/update/remove flows.
- Performance tests for large package lists (500+ packages).
- Security tests for malicious package detection.

## Rollout

- v0.1: CLI package manager, local installation, basic registry.
- v0.2: Marketplace UI, automatic updates, dependency resolution.
- v0.3: Package signing, vulnerability scanning, community packages.
