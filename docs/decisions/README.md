# Decision Log

This directory contains architectural and design decision records. Each record captures the context, decision, alternatives considered, and consequences of a significant choice.

## Index

| # | Decision | Date | Status |
|---|----------|------|--------|
| 001 | Plugin-First Architecture | 2025-01-15 | Accepted |
| 002 | Event-Driven Communication | 2025-01-15 | Accepted |
| 003 | Tauri Over Electron | 2025-01-15 | Accepted |
| 004 | JSON-RPC 2.0 Protocol | 2025-01-15 | Accepted |
| 005 | Svelte Over React | 2025-01-15 | Accepted |
| 006 | SQLite Storage | 2025-01-15 | Accepted |
| 007 | Canvas 2D With WebGL Fallback | 2025-01-15 | Accepted |
| 008 | Rust Sidecar Over Tauri Plugin | 2025-01-15 | Accepted |

## Format

Each decision follows the template:

```
# DRR-NNN: Title

## Status
Accepted / Proposed / Superseded by DRR-XXX

## Date
YYYY-MM-DD

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing or have agreed to implement?

## Alternatives
What other options were considered?

## Consequences
What becomes easier or more difficult to do because of this change?
```
