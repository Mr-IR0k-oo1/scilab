# Compatibility Policy

## Scilab Compatibility

| Version | Supported |
|---------|-----------|
| Scilab 7.0+ | ✅ |
| Scilab 6.x | ❌ |
| Scilab 5.x | ❌ |

## Platform Compatibility

| Platform | Minimum Version |
|----------|----------------|
| Linux | Ubuntu 20.04 / Fedora 35 |
| macOS | 12 (Monterey) |
| Windows | 10 (64-bit) |

## Node.js Compatibility

| Version | Supported |
|---------|-----------|
| Node.js 18+ | ✅ |
| Node.js 16 | ❌ |
| Node.js 14 | ❌ |

## Browser Compatibility

The application uses the system webview:

| Platform | Engine |
|----------|--------|
| Linux | WebKitGTK |
| macOS | WebKit |
| Windows | WebView2 (Chromium) |

## Plugin Compatibility

### API Versions
- Plugin API version follows the platform version.
- Plugins declare compatibility in their manifest.
- Incompatible plugins are not loaded.

### Compatibility Range
```json
{
  "scilab_studio_version": ">=0.2 <1.0"
}
```

### Breaking Changes
- Breaking plugin API changes require a major version bump.
- Deprecated features are removed after 2 major versions.
- Migration guides are provided for breaking changes.

## Backward Compatibility

- v0.1 projects work in all future versions.
- Plugin API changes are backwards compatible within a major version.
- Widget definitions are backwards compatible within a major version.
- Chart configurations are backwards compatible within a major version.

## Forward Compatibility

- New features are opt-in.
- Existing behavior is not changed.
- New default values are backwards compatible.
