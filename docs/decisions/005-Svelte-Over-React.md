# DRR-005: Svelte Over React

## Status

Accepted

## Date

2025-01-15

## Context

The frontend needs a UI framework. Popular choices include React, Vue, and Svelte. The application has specific performance requirements (small bundle, fast rendering) and targets a technical audience.

## Decision

Use Svelte 5 with SvelteKit for the frontend.

## Alternatives

1. **React**: Largest ecosystem, most job market share. But larger bundle, requires virtual DOM, more boilerplate.
2. **Vue**: Good middle ground. But smaller ecosystem than React, less predictable performance.
3. **Svelte**: Compiles to vanilla JS, smallest bundle, best performance. But smaller ecosystem, fewer third-party components.
4. **Vanilla JS**: Maximum control. But no component model, no reactivity system, high development cost.

## Consequences

- **Easier**: Smallest bundle size. Best runtime performance. Simple syntax. Less code to write.
- **Harder**: Smaller ecosystem. Fewer pre-built components. Less community support than React.
- **Trade-off**: For a desktop application where performance and bundle size matter, Svelte's advantages outweigh its ecosystem limitations.
