# ADR-005: Svelte Over React/Vue

**Status:** Accepted
**Date:** 2026-07-27
**Deciders:** Scilab Studio Core Team

## Context

The frontend framework must provide: compile-time reactivity (no virtual DOM overhead), small bundle size, TypeScript support, and ease of learning for contributors. The application renders engineering visualizations, manages complex panel layouts, and handles real-time data updates — all of which demand good rendering performance.

Contributors to FOSSEE projects are typically engineers and students, not professional frontend developers. The framework must be easy to learn.

## Decision

Use Svelte 5 with TypeScript. Svelte compiles components to vanilla JavaScript at build time, eliminating the virtual DOM runtime overhead. This produces smaller bundles and faster rendering. SvelteKit provides routing and SSR capabilities for future web deployment.

## Alternatives Considered

### 1. React

The most widely used frontend framework.

- **Pros:** Largest ecosystem, most pre-built components, most job market demand, most documentation
- **Cons:** Virtual DOM overhead (re-rendering entire subtrees), larger bundle size (~40KB gzipped for core), more complex state management (Redux/Context), JSX learning curve for non-frontend developers
- **Verdict:** Rejected — bundle size and runtime overhead are suboptimal for a performance-sensitive engineering tool

### 2. Vue

Progressive framework with good ergonomics.

- **Pros:** Good learning curve, smaller than React, excellent documentation, Composition API
- **Cons:** Still has runtime overhead (virtual DOM), less compile-time optimization than Svelte, smaller ecosystem than React
- **Verdict:** Rejected — Svelte offers better performance characteristics with similar ergonomics

### 3. SolidJS

Compile-time reactivity without virtual DOM.

- **Pros:** Similar compile-time approach to Svelte, excellent performance, fine-grained reactivity
- **Cons:** Smaller ecosystem, less mature tooling, fewer contributors know it, less documentation
- **Verdict:** Rejected — ecosystem risk for an open-source project that needs broad contributor access

### 4. Svelte 5 (Chosen)

Compile-time framework with no virtual DOM.

- **Pros:** Smallest bundle size (~50KB gzipped for core), compile-time reactivity eliminates virtual DOM overhead, simple readable component syntax (HTML-first), excellent TypeScript support, SvelteKit provides routing/SSR, easy to learn for engineers
- **Cons:** Smaller ecosystem than React (fewer pre-built components), contributors may need to learn Svelte, Svelte 5 is relatively new
- **Verdict:** Accepted — optimal balance of performance, bundle size, and contributor accessibility

## Consequences

### Positive

- Smallest bundle size among major frameworks — important for desktop app startup time
- Compile-time reactivity eliminates virtual DOM overhead — critical for real-time visualization updates
- Simple, readable component syntax — HTML-first with `<script>` blocks, easy for engineers to learn
- SvelteKit provides file-based routing and SSR — enables future web deployment
- TypeScript-first — full type safety across the frontend
- Growing community and ecosystem

### Negative

- Smaller ecosystem than React — fewer pre-built UI component libraries (mitigated by building our own component library)
- Contributors may need to learn Svelte — though it's designed to be easy (mitigated by good documentation and examples)
- Svelte 5 is relatively new — some ecosystem packages may lag behind (mitigated by targeting stable releases)
- Fewer Stack Overflow answers than React (mitigated by active Discord community)

## References

- [System Architecture](../03_System_Architecture.md) §8 Technology Stack
- [Svelte Documentation](https://svelte.dev/)
- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Svelte vs React Benchmark](https://krausest.github.io/js-framework-benchmark/)
