# ADR-004: JSON-RPC for Scilab Communication

**Status:** Accepted
**Date:** 2026-07-27
**Deciders:** Scilab Studio Core Team

## Context

The platform needs to communicate with the Scilab engine for scientific computation. Scilab runs as a separate process (it cannot be embedded in-process due to its process model). The communication must be:

- **Bidirectional** — Send commands, receive results
- **Debuggable** — Developers must be able to inspect messages
- **Cross-platform** — Work on Linux, macOS, Windows
- **Secure** — No open network ports for local usage
- **Simple** — Minimize implementation complexity

The Scilab Bridge is a Rust sidecar process that manages the Scilab child process lifetime and provides a typed API for the frontend.

## Decision

Use JSON-RPC 2.0 over stdin/stdout pipes between the Rust sidecar and the Scilab child process. The sidecar handles process lifecycle, command serialization, result parsing, and error handling.

## Alternatives Considered

### 1. Direct FFI (Foreign Function Interface)

Call Scilab's C API functions directly from Rust.

- **Pros:** Lowest latency, no process boundary
- **Cons:** Version-specific ABI (breaks across Scilab versions), complex build process (linking Scilab libraries), not portable, requires Scilab development headers
- **Verdict:** Rejected — too fragile and platform-specific

### 2. TCP Sockets

Scilab listens on a TCP port; the sidecar connects via TCP.

- **Pros:** Simple to implement, bidirectional, language-agnostic
- **Cons:** Security concerns (open port), port conflicts with other services, not suitable for sandboxed environments, requires Scilab to run a server
- **Verdict:** Rejected — security and sandboxing concerns

### 3. HTTP REST API

Scilab exposes HTTP endpoints that the sidecar calls.

- **Pros:** Standard protocol, easy to debug with curl, well-understood
- **Cons:** Overhead for simple operations (HTTP headers, connection setup), requires Scilab to run an HTTP server, not suitable for real-time interaction
- **Verdict:** Rejected — too heavy for simple variable reads and code evaluation

### 4. Shared Memory (Memory-Mapped Files)

Memory-mapped files for high-speed data exchange between processes.

- **Pros:** Fastest data transfer, zero-copy for large datasets
- **Cons:** Complex synchronization (need locks/semaphores), platform-specific APIs, hard to debug, requires careful memory management
- **Verdict:** Rejected — complexity outweighs performance benefits for our use case

### 5. JSON-RPC over stdin/stdout (Chosen)

Newline-delimited JSON messages over standard input/output pipes.

- **Pros:** Simple protocol, debuggable (any JSON tool), no network overhead, works in sandboxed environments, language-agnostic, standard specification
- **Cons:** Sequential command execution (one command at a time), large data transfer requires chunking, Scilab process must be running
- **Verdict:** Accepted — optimal balance of simplicity, debuggability, and security

## Consequences

### Positive

- Simple protocol — any developer can debug with `echo '{"method":"eval","params":{"code":"1+1"}}' | scilab`
- No network overhead or port conflicts
- Works in sandboxed environments (no network access required)
- Rust sidecar provides process lifecycle management (start, monitor, restart, stop)
- Standard JSON-RPC 2.0 specification — well-documented, widely understood
- Variable marshalling table provides clear Scilab ↔ JSON type mapping

### Negative

- Sequential command execution — only one command at a time per Scilab process (mitigated by running multiple Scilab processes for parallel computation)
- Large data transfer (e.g., 1000×1000 matrix) requires chunking or file-based transfer
- Scilab process must be running for any computation (mitigated by auto-start and keep-alive)
- stdin/stdout pipe can block if Scilab output buffer fills (mitigated by non-blocking I/O in Rust)

## References

- [System Architecture](../03_System_Architecture.md) §7 Scilab Integration Layer
- [Platform Architecture](../04_Platform_Architecture.md) §5 Scilab Integration Layer
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
