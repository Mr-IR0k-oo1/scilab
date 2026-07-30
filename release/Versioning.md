# Versioning

## Format

Semantic Versioning (SemVer): `MAJOR.MINOR.PATCH`

```
0.1.0
│ │ │
│ │ └── Patch: Bug fixes, security patches
│ └──── Minor: New features, backwards compatible
└────── Major: Breaking changes
```

## Pre-1.0

Before version 1.0, the API is not considered stable:

- `0.1.x` — Initial release
- `0.2.x` — Plugin system
- `0.3.x` — AI assistant
- `0.4.x` — Community features
- `0.9.x` — Pre-release

## Version Bump Rules

| Change | Bump |
|--------|------|
| Bug fix | Patch |
| New feature (backwards compatible) | Minor |
| Breaking API change | Major |
| Breaking UI change | Major |
| Breaking plugin API | Major |
| New plugin API (backwards compatible) | Minor |

## Version Tags

```bash
git tag v0.1.0
git tag v0.2.0
git tag v1.0.0
```

## Version in Code

```json
{
  "version": "0.1.0"
}
```

```rust
const VERSION: &str = "0.1.0";
```

```typescript
export const VERSION = '0.1.0';
```
