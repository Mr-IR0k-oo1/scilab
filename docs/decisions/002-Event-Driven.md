# DRR-002: Event-Driven Communication

## Status

Accepted

## Date

2025-01-15

## Context

With a plugin-first architecture, modules need a way to communicate without tight coupling. Direct function calls create dependencies that make it hard to enable/disable features independently.

## Decision

All inter-module communication uses an event bus. Modules publish events and subscribe to events they care about. No direct function calls between modules.

## Alternatives

1. **Direct imports**: Module A imports Module B. Simple but creates tight coupling.
2. **Shared state**: Global state store. Works but makes debugging and testing harder.
3. **Message passing**: Like events but with guaranteed delivery. Overhead is unnecessary for in-process communication.

## Consequences

- **Easier**: Modules can be added/removed without modifying others. Testing is simpler (mock the event bus). Features can be conditionally loaded.
- **Harder**: Debugging event flows is harder than following function calls. Events can be lost or misrouted. Performance overhead from indirection.
- **Trade-off**: Slight increase in complexity for significant gain in modularity and testability.
