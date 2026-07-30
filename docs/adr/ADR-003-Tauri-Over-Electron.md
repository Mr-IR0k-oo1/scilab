# ADR-003: Tauri Over Electron

**Status:** Accepted
**Date:** 2026-07-27
**Deciders:** Scilab Studio Core Team

## Context

The desktop application needs a shell that provides: native performance, small binary size, cross-platform support (Linux, macOS, Windows), web-based UI for rapid iteration, and a strong security model. The application wraps the Scilab engine, manages plugins, and renders engineering visualizations — all of which demand good performance and reasonable memory usage.

University lab machines often have limited resources (4GB RAM, older CPUs). The application must run acceptably on these constraints.

## Decision

Use Tauri 2.x as the application shell. Tauri uses a Rust backend with a system webview (WebKit on macOS, WebView2 on Windows, WebView on Linux), producing significantly smaller binaries than Electron while providing better security through capability-based permissions.

## Alternatives Considered

### 1. Electron

The most widely used desktop web framework (VS Code, Discord, Slack).

- **Pros:** Largest ecosystem, most documentation, proven at scale, Node.js backend
- **Cons:** Bundles Chromium (~150MB binary), higher memory usage (~200MB idle), weaker security model, no capability-based permissions
- **Verdict:** Rejected — binary size and memory usage are unacceptable for university lab machines

### 2. Native (Qt/GTK)

Platform-native UI toolkits.

- **Pros:** Native look and feel, best performance, smallest memory footprint
- **Cons:** Harder cross-platform development (different APIs per platform), no web-based UI, steeper learning curve for contributors, C++/Python required
- **Verdict:** Rejected — contributor accessibility is critical for an open-source project

### 3. Flutter Desktop

Cross-platform UI with Dart.

- **Pros:** Single codebase, good performance, growing ecosystem
- **Cons:** Dart ecosystem is smaller than JavaScript/TypeScript, less web integration, contributors need to learn Dart, no proven desktop IDE use cases
- **Verdict:** Rejected — technology risk and contributor accessibility

### 4. Tauri 2.x (Chosen)

Rust backend with system webview frontend.

- **Pros:** ~10MB binary, Rust backend (memory safety, performance), system webview (no bundled browser), capability-based security, web-based UI (Svelte/TypeScript)
- **Cons:** Tauri 2.x is newer than Electron (smaller ecosystem), contributors need Rust for backend changes, WebView rendering varies slightly across platforms
- **Verdict:** Accepted — optimal balance of size, performance, security, and contributor accessibility

## Consequences

### Positive

- 10x smaller binary than Electron (~10MB vs ~150MB)
- Lower memory usage — system webview is shared with the OS
- Rust backend provides memory safety without garbage collection
- Capability-based security model (plugins request specific permissions)
- Web-based frontend enables rapid UI iteration with Svelte
- Active community and growing ecosystem

### Negative

- Tauri 2.x ecosystem is smaller than Electron's
- Contributors need Rust knowledge for backend changes (mitigated by keeping backend minimal)
- WebView rendering varies slightly across platforms (mitigated by testing on all three platforms)
- System webview version depends on OS (mitigated by targeting modern OS versions)

## References

- [System Architecture](../03_System_Architecture.md) §8 Technology Stack
- [Tauri Documentation](https://v2.tauri.app/)
- [Tauri vs Electron Comparison](https://v2.tauri.app/concept/comparison-to-electron/)
