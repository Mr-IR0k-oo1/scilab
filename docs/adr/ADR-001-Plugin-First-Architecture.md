# ADR-001: Plugin-First Architecture

**Status:** Accepted
**Date:** 2026-07-27
**Deciders:** Scilab Studio Core Team

## Context

Scilab Studio needs to be extensible. The FOSSEE ecosystem has multiple tools (Scilab, Xcos, eSim, OpenModelica) and community contributions should be able to add new capabilities without modifying the core platform. Without a plugin system, every new feature requires core team involvement, creating a bottleneck.

The platform aims to serve students, educators, researchers, and developers across multiple engineering domains. No single team can build everything. The architecture must enable community contributions at every level — from widgets to full modules.

## Decision

Adopt a plugin-first architecture where ALL features — including built-in modules — are plugins that register with the platform through standardized APIs. The core platform is minimal:

- **Event Bus** — Inter-module communication
- **Plugin Manager** — Lifecycle and sandboxing
- **Scilab Bridge** — Scientific computation
- **Workspace Manager** — Layout and panels

Everything else — GUI Builder, Visualization Studio, Data Studio, Report Generator, Learning Center — is a plugin that follows the same lifecycle and API contracts as third-party extensions.

## Alternatives Considered

### 1. Monolithic Architecture

All features compiled directly into the application binary.

- **Pros:** Simpler to build initially, no plugin overhead
- **Cons:** No extensibility, community can't contribute, every feature requires core team, hard to maintain as codebase grows
- **Verdict:** Rejected — contradicts the open-source community model

### 2. Core + Optional Plugins

Core features compiled in, extras available as plugins.

- **Pros:** Simpler initial development, core features always available
- **Cons:** Inconsistency between built-in and third-party modules, two different development models, harder to test
- **Verdict:** Rejected — creates a two-tier system that discourages community contributions

### 3. Microkernel with Hot-Swappable Plugins (Chosen)

Minimal core with all features as plugins following standardized APIs. Built-in plugins are bundled but follow the same lifecycle as third-party plugins.

- **Pros:** Full extensibility, consistent API for all modules, community can contribute at any level, features can be independently versioned
- **Cons:** Initial API design overhead, slight performance overhead from event bus indirection
- **Verdict:** Accepted — proven pattern (VS Code, Eclipse, IntelliJ), aligned with FOSSEE community model

## Consequences

### Positive

- Community can build and distribute extensions without core team involvement
- Features can be independently developed, tested, and released
- Users install only what they need — lightweight for students, full-featured for researchers
- Plugin marketplace creates a network effect — more contributors = more value
- Built-in modules serve as reference implementations for plugin developers

### Negative

- Initial development overhead for designing the plugin API
- Performance overhead from event bus indirection (mitigated by request/response pattern for latency-sensitive operations)
- Plugin compatibility management across versions requires versioned SDK
- Testing matrix grows with each plugin (mitigated by sandboxing)

## References

- [System Architecture](../03_System_Architecture.md) §5 Plugin Architecture
- [Platform Architecture](../04_Platform_Architecture.md) §4 Plugin Manager
- [VS Code Extension Host Architecture](https://code.visualstudio.com/api/advanced-topics/extension-host)
