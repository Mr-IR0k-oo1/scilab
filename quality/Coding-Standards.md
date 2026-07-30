# Coding Standards

## Language

- **Frontend**: TypeScript + Svelte 5
- **Backend**: Rust (Tauri + sidecar)
- **SDK**: CommonJS JavaScript
- **Build**: Vite (frontend), Cargo (backend)

## TypeScript

### Style
- Use `const` by default, `let` when reassignment is needed.
- Never use `var`.
- Use arrow functions for callbacks.
- Use async/await, not `.then()` chains.
- Use template literals, not string concatenation.
- Use destructuring for objects and arrays.
- Use optional chaining (`?.`) and nullish coalescing (`??`).

### Types
- Define interfaces for all data structures.
- Use `type` for unions and aliases.
- Export all public types.
- Avoid `any`. Use `unknown` if the type is truly unknown.
- Use generics for reusable components.

### Naming
- `camelCase` for variables and functions.
- `PascalCase` for types, interfaces, and classes.
- `SCREAMING_SNAKE_CASE` for constants.
- `kebab-case` for file names.
- Prefix interfaces with `I` only if there's ambiguity.

### Imports
```typescript
// Group imports: external, internal, types
import React from 'react';
import { EventEmitter } from 'events';
import { PluginContext } from '../types';
import type { PluginManifest } from '../types';
```

## Rust

### Style
- Follow the Rust API Guidelines.
- Use `rustfmt` for formatting.
- Use `clippy` for linting.
- Prefer `Result<T, E>` over panics.
- Use `thiserror` for error types.
- Use `serde` for serialization.

### Naming
- `snake_case` for variables and functions.
- `PascalCase` for types and traits.
- `SCREAMING_SNAKE_CASE` for constants.
- Prefix error types with the module name.

## CSS

### Style
- Use CSS custom properties for all values.
- Use BEM naming: `.ss-block__element--modifier`.
- One property per line.
- Alphabetize properties.
- Use shorthand when possible.

### Class Naming
```
.ss-button                    /* Block */
.ss-button__icon              /* Element */
.ss-button--primary           /* Modifier */
.ss-button--large             /* Modifier */
.ss-button--disabled          /* Modifier */
.ss-button.icon-only          /* Combination */
```

## Comments

- Use JSDoc for public APIs.
- Use `//` for implementation comments.
- Don't comment obvious code.
- Explain why, not what.
- Keep comments up to date.

## Formatting

- 2 spaces for indentation.
- 100 character line limit.
- Single quotes for strings.
- Semicolons required.
- Trailing commas in multi-line structures.
