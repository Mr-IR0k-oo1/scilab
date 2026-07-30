# Release Checklist

## Pre-Release

- [ ] All issues in milestone are closed or deferred.
- [ ] All PRs are merged.
- [ ] Version is bumped in all files.
- [ ] Changelog is updated.
- [ ] Documentation is updated.
- [ ] All tests pass.
- [ ] Performance benchmarks pass.
- [ ] Accessibility tests pass.
- [ ] Security audit complete.
- [ ] Dependencies are updated.

## Build

- [ ] Clean build from fresh clone.
- [ ] Build succeeds on all platforms (Linux, macOS, Windows).
- [ ] Bundle size is within budget.
- [ ] No warnings in build output.

## Testing

- [ ] Manual testing on all platforms.
- [ ] Installation test on clean system.
- [ ] Upgrade test from previous version.
- [ ] Plugin compatibility test.
- [ ] Scilab compatibility test.

## Release

- [ ] Create release branch.
- [ ] Update version numbers.
- [ ] Create git tag.
- [ ] Build release artifacts.
- [ ] Test release artifacts.
- [ ] Write release notes.
- [ ] Publish to distribution channels.
- [ ] Update website.

## Post-Release

- [ ] Monitor issue tracker.
- [ ] Respond to bug reports.
- [ ] Plan next release.
- [ ] Retrospective.

## Release Notes Template

```markdown
# Scilab Studio v0.2.0

## What's New

### Feature 1
Description of the feature.

### Feature 2
Description of the feature.

## Bug Fixes

- Fixed issue #123
- Fixed issue #456

## Breaking Changes

- API change description
- Migration instructions

## Known Issues

- Issue description

## Contributors

Thanks to all contributors!

@contributor1 @contributor2
```
