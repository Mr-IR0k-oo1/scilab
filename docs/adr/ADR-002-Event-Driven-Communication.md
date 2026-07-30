# ADR-002: Event-Driven Communication

**Status:** Accepted
**Date:** 2026-07-27
**Deciders:** Scilab Studio Core Team

## Context

Modules need to communicate without direct dependencies. If Module A imports Module B, they are tightly coupled — changing B breaks A. With 18+ modules planned, direct dependencies create a dependency nightmare where changing one module requires testing every other module.

The communication pattern must support:
- Broadcasting state changes to multiple listeners
- Requesting data from another module and getting a response
- Sharing frequently accessed data across modules

## Decision

All inter-module communication flows through a centralized Event Bus using three patterns:

1. **Event Bus (Fire-and-Forget)** — For broadcasts where no return value is needed
2. **Request/Response (RPC)** — For operations that need a return value
3. **Shared State (Observable Store)** — For frequently read data that changes occasionally

Modules emit events and subscribe to events. They never import each other directly.

## Alternatives Considered

### 1. Direct Function Calls

Module A calls Module B's exported functions directly.

- **Pros:** Simple, type-safe, no indirection
- **Cons:** Tight coupling, circular dependencies, can't replace or mock modules independently
- **Verdict:** Rejected — creates unmanageable dependency graph

### 2. Async Message Queue

All communication via an asynchronous message queue (like RabbitMQ or ZeroMQ).

- **Pros:** Decoupled, supports distributed systems
- **Cons:** Unnecessary complexity for a desktop app, adds latency, requires message broker process
- **Verdict:** Rejected — overengineered for single-user desktop application

### 3. Shared Database

All modules read/write to a shared SQLite database, using it as the communication layer.

- **Pros:** Persistent, queryable, ACID guarantees
- **Cons:** No real-time reactivity (need polling), race conditions on writes, no typed contracts, hard to debug
- **Verdict:** Rejected — database is for storage, not communication

### 4. Event Bus + Shared State (Chosen)

Centralized event bus with three communication patterns, plus a shared state store for frequently accessed data.

- **Pros:** Fully decoupled, real-time reactivity, typed contracts, debuggable, proven pattern
- **Cons:** Debugging harder (event chains vs call stacks), requires disciplined naming
- **Verdict:** Accepted — industry-standard pattern for modular applications

## Consequences

### Positive

- Modules are fully decoupled — can be developed, tested, and replaced independently
- New modules can subscribe to existing events without modifying emitters
- Clear communication contracts (event names and payload schemas)
- Plugin system integrates naturally — plugins participate in the same event bus
- Debugging tools can visualize event flows

### Negative

- Debugging is harder — event chains instead of call stacks (mitigated by correlation IDs and event logging)
- Event naming must be disciplined — the `domain:action:detail` convention prevents chaos
- Potential for event storms if modules emit too many events (mitigated by rate limiting and event filtering)
- Initial learning curve for contributors unfamiliar with event-driven architecture

## References

- [System Architecture](../03_System_Architecture.md) §4 Module Interaction
- [Platform Architecture](../04_Platform_Architecture.md) §3 Event Bus
