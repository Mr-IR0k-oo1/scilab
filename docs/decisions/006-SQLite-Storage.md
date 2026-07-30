# DRR-006: SQLite Storage

## Status

Accepted

## Date

2025-01-15

## Context

The application needs persistent storage for projects, settings, history, and cached data. Options range from file-based storage to full database servers.

## Decision

Use SQLite for all structured storage (projects, settings, history, user data) and the file system for project files and assets.

## Alternatives

1. **File-based (JSON/YAML)**: Simple but no query capability, no transactions, no concurrent access.
2. **SQLite**: Zero-config, single-file database, supports complex queries and transactions. Well-proven for desktop applications.
3. **IndexedDB**: Browser-based, but Tauri provides file system access, making this unnecessary.
4. **PostgreSQL/MySQL**: Overkill for a desktop application. Requires separate server.

## Consequences

- **Easier**: Zero configuration. Single file database. SQL queries for complex data. Transaction support. Battle-tested reliability.
- **Harder**: Requires schema migrations. Not human-readable like JSON files.
- **Trade-off**: Slight complexity increase for significant gain in data integrity and query capability.
