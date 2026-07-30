# DRR-008: Rust Sidecar Over Tauri Plugin

## Status

Accepted

## Date

2025-01-15

## Context

The Scilab runtime management requires process spawning, monitoring, and communication. Tauri provides two approaches: Tauri plugins (Rust code compiled into the app) and sidecar processes (independent executables).

## Decision

Use a Rust sidecar process for Scilab runtime management instead of a Tauri plugin.

## Alternatives

1. **Tauri plugin**: Compiled into the app binary. Tighter integration. But harder to update independently.
2. **Rust sidecar**: Separate executable. Can be updated independently. Easier to test in isolation. But requires process management.
3. **Node.js sidecar**: Easier to write but higher memory usage and slower than Rust.

## Consequences

- **Easier**: Independent updates without rebuilding the app. Easier testing (test sidecar separately). Clear separation of concerns.
- **Harder**: Process management overhead. IPC serialization/deserialization cost. More moving parts.
- **Trade-off**: Slight architectural complexity for better maintainability and testability of the Scilab integration layer.
