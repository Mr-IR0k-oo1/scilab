# DRR-003: Tauri Over Electron

## Status

Accepted

## Date

2025-01-15

## Context

The application needs to be cross-platform (Linux, macOS, Windows). Two dominant frameworks exist: Electron (Chromium-based) and Tauri (system webview-based).

## Decision

Use Tauri 2.x as the application framework with system webview (WebKit on macOS/Linux, WebView2 on Windows).

## Alternatives

1. **Electron**: Larger bundle size (~150MB), higher memory usage (~200MB+), but mature ecosystem and consistent rendering.
2. **Tauri**: Smaller bundle size (~10-20MB), lower memory usage (~30-50MB), Rust backend, but webview differences between platforms.
3. **Qt/QML**: Native look, but steeper learning curve and less web ecosystem access.

## Consequences

- **Easier**: Tiny bundle size. Low memory footprint. Rust backend for performance-critical operations. Active development and community.
- **Harder**: WebKit vs WebView2 differences require testing on all platforms. Some web APIs behave differently. Smaller ecosystem than Electron.
- **Trade-off**: Better performance and smaller footprint at the cost of more platform-specific testing.
