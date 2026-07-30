# DRR-004: JSON-RPC 2.0 Protocol

## Status

Accepted

## Date

2025-01-15

## Context

The Scilab runtime runs as a separate process. The frontend needs to send commands to Scilab and receive results. A structured protocol is needed for reliable communication.

## Decision

Use JSON-RPC 2.0 over stdin/stdout for communication between the Tauri frontend and the Scilab sidecar process.

## Alternatives

1. **Custom protocol**: Simpler but reinvents the wheel. No standard error handling.
2. **gRPC**: Too heavy for local process communication. Requires protobuf tooling.
3. **WebSockets**: Overkill for local IPC. Adds unnecessary complexity.
4. **JSON-RPC 2.0**: Standard protocol with well-defined error handling. Simple to implement. Widely supported.

## Consequences

- **Easier**: Standard error codes and message format. Easy to debug (human-readable JSON). Well-documented protocol.
- **Harder**: Slightly more verbose than a custom protocol. Requires JSON parsing overhead.
- **Trade-off**: Negligible performance cost for significant gain in reliability and debuggability.
