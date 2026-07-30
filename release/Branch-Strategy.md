# Branch Strategy

## Branches

| Branch | Purpose | Lifetime |
|--------|---------|----------|
| `main` | Stable, production-ready code | Permanent |
| `develop` | Integration branch for next release | Permanent |
| `feature/*` | New features | Temporary |
| `fix/*` | Bug fixes | Temporary |
| `release/*` | Release preparation | Temporary |
| `hotfix/*` | Critical production fixes | Temporary |

## Workflow

```
main ─────────────────────────────────────────────
         │                         ▲
         ▼                         │
develop ───────────────────────────
    │          │            ▲
    ▼          ▼            │
feature/  feature/    fix/*
```

### Feature Branch
1. Create from `develop`.
2. Work on feature.
3. Open PR to `develop`.
4. Review and merge.
5. Delete branch.

### Release Branch
1. Create from `develop` when ready to release.
2. Bump version.
3. Final testing.
4. Merge to `main` and `develop`.
5. Tag release.
6. Delete branch.

### Hotfix Branch
1. Create from `main`.
2. Fix critical issue.
3. Merge to `main` and `develop`.
4. Tag hotfix release.
5. Delete branch.

## PR Requirements

- Title follows commit message format.
- Description explains the change.
- All CI checks pass.
- At least one approval.
- No unresolved comments.
- Branch is up to date.

## Commit Messages

```
type(scope): description

[optional body]

[optional footer]
```

### Types
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding tests |
| `chore` | Build, CI, tooling |

### Examples
```
feat(plugin): add plugin marketplace
fix(runtime): handle Scilab crash gracefully
docs(api): update Runtime API documentation
```
