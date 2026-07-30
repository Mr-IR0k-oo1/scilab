# ADR-006: SQLite for Local Storage

**Status:** Accepted
**Date:** 2026-07-27
**Deciders:** Scilab Studio Core Team

## Context

The platform needs to store structured data locally: project metadata, workspace state, plugin configurations, recent files, user settings, and experiment records. This data is local to each user's machine and must work fully offline — university labs may not have reliable internet connectivity.

The storage solution must be:
- **Embedded** — No separate server process
- **Reliable** — ACID guarantees to prevent data corruption
- **Portable** — Easy to backup, share, and migrate
- **Queryable** — Support searching, filtering, and sorting
- **Cross-platform** — Identical behavior on Linux, macOS, Windows

## Decision

Use SQLite for all structured local storage. SQLite is embedded (links directly into the application), ACID compliant, portable (single file), and supports SQL queries. Each project stores its manifest in `project.json`; global settings and metadata are stored in a SQLite database at `~/.config/scilab-studio/`.

## Alternatives Considered

### 1. JSON Files Only

Store everything in JSON files on the filesystem.

- **Pros:** Simple, human-readable, no dependencies, easy to inspect
- **Cons:** No indexing (slow searches on large datasets), no ACID guarantees (corruption on crash), concurrent read/write issues, no query language, must load entire file to read one field
- **Verdict:** Rejected — acceptable for `project.json` but not for settings, recent files, or experiment records

### 2. PostgreSQL / MySQL

Full database server.

- **Pros:** Full SQL, ACID, concurrent access, mature ecosystem
- **Cons:** Requires server process (not offline-first), installation complexity, overkill for local storage, not portable (single file)
- **Verdict:** Rejected — violates offline-first principle, too heavy for desktop app

### 3. LevelDB / RocksDB

Key-value stores from Google.

- **Pros:** Fast reads/writes, embedded, no server
- **Cons:** No SQL queries (only key-value access), less portable, harder to inspect data, no relational queries, less tooling
- **Verdict:** Rejected — we need SQL queries for searching and filtering

### 4. SQLite (Chosen)

Embedded relational database.

- **Pros:** No server process (truly offline-first), single-file database (easy backup/share), ACID guarantees, SQL queries (efficient searching/filtering), excellent tooling (DB Browser for SQLite), portable across platforms, widely used and battle-tested
- **Cons:** Not suitable for multi-user concurrent access (but we don't need that), file can grow if not vacuumed, schema migrations need careful handling
- **Verdict:** Accepted — optimal for desktop application local storage

## Consequences

### Positive

- No server process required — truly offline-first
- Single-file database is easy to backup, copy, and share
- ACID guarantees prevent data corruption on crashes
- SQL queries enable efficient searching, filtering, and sorting
- Excellent tooling — developers can inspect the database with any SQLite client
- Portable across platforms — same file works on Linux, macOS, Windows
- Battle-tested — SQLite is the most widely deployed database in the world

### Negative

- Not suitable for multi-user concurrent access — but Scilab Studio is a single-user desktop app, so this is not a concern
- SQLite file can grow if records are added repeatedly without cleanup (mitigated by periodic VACUUM and record pruning)
- Schema migrations need careful handling — we use a version field in the database and migration scripts
- Concurrent writes from multiple threads require careful locking (mitigated by SQLite's built-in locking and our single-writer pattern)

## References

- [System Architecture](../03_System_Architecture.md) §8 Technology Stack
- [Platform Architecture](../04_Platform_Architecture.md) §9 File System Service
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite vs JSON Performance](https://www.sqlite.org/whentouse.html)
