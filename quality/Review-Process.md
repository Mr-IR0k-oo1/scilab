# Review Process

## Code Review

### Requirements
- All code must be reviewed before merge.
- At least one approval required.
- All CI checks must pass.
- No unresolved comments.

### Review Checklist

#### Functionality
- [ ] Code does what it claims.
- [ ] Edge cases are handled.
- [ ] Error handling is appropriate.
- [ ] Performance is acceptable.

#### Code Quality
- [ ] Code follows coding standards.
- [ ] Code is readable and maintainable.
- [ ] No unnecessary complexity.
- [ ] No code duplication.

#### Testing
- [ ] Tests are included.
- [ ] Tests cover happy path and errors.
- [ ] Tests are deterministic.
- [ ] Coverage meets requirements.

#### Documentation
- [ ] API documentation is updated.
- [ ] README is updated (if needed).
- [ ] Changelog is updated.
- [ ] Comments explain why, not what.

#### Security
- [ ] Input is validated.
- [ ] No secrets in code.
- [ ] Permissions follow least privilege.
- [ ] No path traversal.

#### Accessibility
- [ ] Keyboard accessible.
- [ ] ARIA attributes present.
- [ ] Focus indicators visible.
- [ ] Contrast ratios met.

### Review Guidelines

#### For Reviewers
- Be constructive, not critical.
- Suggest improvements, not just problems.
- Approve when concerns are addressed.
- Don't block on style preferences.

#### For Authors
- Respond to all comments.
- Don't take feedback personally.
- Explain your reasoning.
- Make requested changes promptly.

## RFC Review

### Process
1. Author writes RFC.
2. RFC is submitted as a PR.
3. Team reviews for 1 week.
4. Feedback is incorporated.
5. RFC is accepted or rejected.

### Criteria
- Solves a real problem.
- Doesn't over-engineer.
- Considers alternatives.
- Has a clear rollout plan.

## Design Review

### Process
1. Designer creates mockup.
2. Mockup is reviewed against design language.
3. Accessibility is verified.
4. Responsive behavior is confirmed.
5. Design is approved.

### Criteria
- Follows design language.
- Meets accessibility standards.
- Works at all breakpoints.
- Consistent with existing UI.

## Merge Requirements

- All CI checks pass.
- At least one approval.
- No unresolved comments.
- Branch is up to date with main.
- Changelog is updated.
- No merge conflicts.
