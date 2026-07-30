# Contributing to Scilab Studio

Thank you for your interest in contributing to Scilab Studio! Every contribution matters — whether it is a bug fix, a new feature, a documentation improvement, or a template for the community.

This guide will walk you through the process of contributing and help you understand our standards and expectations.

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior by opening an issue or emailing the maintainers.

---

## How to Contribute

### Reporting Bugs

If you encounter a bug, please open a GitHub issue with the following information:

1. **Title:** A clear, concise description of the bug.
2. **Environment:** Operating system, Scilab version, Scilab Studio version.
3. **Steps to Reproduce:** A numbered list of steps that reliably trigger the bug.
4. **Expected Behavior:** What you expected to happen.
5. **Actual Behavior:** What actually happened, including error messages and screenshots.
6. **Logs:** Attach relevant log files if available (found in `~/.scilab-studio/logs/`).

Before filing, search existing issues to avoid duplicates. If a similar issue exists, add a comment with your additional information.

### Suggesting Features

Feature suggestions are welcome. Please open an issue with:

1. **Problem Statement:** What problem does this feature solve?
2. **Proposed Solution:** Describe your ideal solution.
3. **Alternatives Considered:** What other approaches did you consider?
4. **Use Cases:** Who benefits and how?
5. **Scope:** Is this a core feature, a plugin, or a module?

For large features, consider opening a discussion thread first to gather community feedback before committing to implementation.

### Contributing Code

1. **Find or Create an Issue:** Look for issues labeled `good first issue` or `help wanted`. If you want to work on something not yet tracked, open an issue first.
2. **Fork the Repository:** Fork `scilab-studio/scilab-studio` to your GitHub account.
3. **Clone Your Fork:**
   ```bash
   git clone https://github.com/your-username/scilab-studio.git
   cd scilab-studio
   ```
4. **Create a Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make Your Changes:** Follow the coding standards below.
6. **Write or Update Tests:** Ensure your changes are covered by tests.
7. **Run the Test Suite:**
   ```bash
   npm run test
   npm run lint
   npm run typecheck
   ```
8. **Commit with a Clear Message:** Follow the commit message conventions below.
9. **Push and Open a Pull Request:** Reference the related issue in your PR description.

### Contributing Documentation

Documentation improvements are always welcome:

- **API Documentation:** Improve clarity, add examples, fix typos in `docs/`.
- **User Guides:** Add tutorials, how-to guides, or cookbook entries.
- **Code Comments:** Add inline documentation for complex logic (do not over-comment obvious code).
- **Translations:** Help translate documentation into other languages.

Submit documentation changes as pull requests to the `docs/` directory.

### Contributing Templates

To create a project template:

1. Use the Template Development Kit (included in `sdk/templates/`).
2. Follow the [Template Format Specification](docs/15_File_Format.md).
3. Include: boilerplate code, sample data, a README, and a preview image.
4. Test the template by creating a new project from it.
5. Submit your template as a pull request or publish it to the marketplace.

### Contributing Widgets

To create a widget for the marketplace:

1. Use the Widget Development Kit (included in `sdk/widgets/`).
2. Follow the [Widget Definition Format](docs/15_File_Format.md).
3. Include: the widget source, a manifest, tests, and documentation.
4. Test across all supported platforms.
5. Publish to the marketplace or submit as a pull request.

---

## Development Setup

> **Note:** Detailed setup instructions are in [Development Guide](docs/17_Development_Guide.md). Below is a quick-start summary.

### Prerequisites
- Node.js 18+ and npm 9+
- Scilab 2024.0+ installed and on PATH
- Git 2.30+
- A C/C++ compiler (for native modules)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/scilab-studio/scilab-studio.git
cd scilab-studio

# Install dependencies
npm install

# Build the project
npm run build

# Run the application
npm run dev

# Run tests
npm run test
```

### IDE Setup
- **Recommended:** VS Code with the project's `.vscode/` settings.
- Install recommended extensions when prompted.
- Use the workspace settings for consistent formatting.

---

## Coding Standards

### Code Style

- **Language:** TypeScript for frontend and core logic. Scilab for engine-side computations.
- **Formatter:** Prettier with the project configuration (`.prettierrc`).
- **Linter:** ESLint with the project configuration (`.eslintrc`).
- **Naming:**
  - `camelCase` for variables and functions.
  - `PascalCase` for classes, interfaces, types, and React components.
  - `SCREAMING_SNAKE_CASE` for constants.
  - `kebab-case` for file names and CSS classes.
- **Imports:** Use absolute imports from the project root. Group imports: external → internal → relative.
- **No comments** unless specifically requested. Code should be self-documenting through clear naming and structure.

### Commit Messages

Follow Conventional Commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Code style changes (formatting, no logic change) |
| `refactor` | Code refactoring (no feature or fix) |
| `test` | Adding or updating tests |
| `chore` | Build, CI, or tooling changes |
| `perf` | Performance improvement |

**Examples:**
```
feat(visualization): add heatmap chart type
fix(data-studio): handle UTF-8 BOM in CSV import
docs(api): add examples for Project API endpoints
```

### Pull Request Process

1. **Title:** Use the same Conventional Commits format as commit messages.
2. **Description:** Explain what the PR does and why. Reference the related issue.
3. **Size:** Keep PRs focused. One logical change per PR. If a feature is large, break it into incremental PRs.
4. **Tests:** All new code must include tests. All existing tests must pass.
5. **Lint and Type Check:** Run `npm run lint` and `npm run typecheck` before submitting.
6. **Screenshots:** If the PR includes UI changes, attach before/after screenshots.
7. **Review:** At least one maintainer approval is required before merge.
8. **Squash Merge:** We use squash merge to keep the commit history clean.

---

## Architecture Guidelines

### Plugin Development

Plugins are the primary extension mechanism. A plugin consists of:

- **Manifest (`plugin.json`):** Declares metadata, entry point, dependencies, and permissions.
- **Entry Point:** A module that exports lifecycle hooks (`activate`, `deactivate`).
- **API Surface:** The plugin can register commands, views, menus, and event handlers.

Follow the [Plugin API Reference](docs/14_API_Reference.md) for the full API.

### Module Structure

Each of the 18 modules follows a consistent structure:

```
modules/
  module-name/
    src/
      index.ts          # Module entry point
      commands/         # Registered commands
      views/            # UI components
      services/         # Business logic
      types/            # TypeScript type definitions
    tests/              # Module-specific tests
    manifest.json       # Module metadata
    README.md           # Module documentation
```

### API Conventions

- All APIs are versioned (e.g., `/v1/projects`).
- Use standard HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove).
- Return consistent response envelopes: `{ success, data, error, metadata }`.
- Errors use standard HTTP status codes with descriptive messages.
- All API changes require a deprecation period of at least one minor version.

---

## Documentation Standards

- **Format:** Markdown for all documentation files.
- **Structure:** Each document starts with a title and overview section.
- **Code Examples:** All API endpoints and functions must include working code examples.
- **Screenshots:** UI documentation should include annotated screenshots.
- **Updates:** When changing behavior, update the relevant documentation in the same PR.
- **Style:** Write in clear, concise language. Use active voice. Address the reader directly ("you").

---

## Testing Requirements

- **Unit Tests:** Every function and class must have unit tests.
- **Integration Tests:** Module interactions must be covered by integration tests.
- **End-to-End Tests:** Critical user flows must have E2E tests.
- **Coverage Target:** Maintain at least 80% code coverage.
- **Test Framework:** Jest for unit/integration, Playwright for E2E.
- **Run Tests Locally:**
  ```bash
  npm run test              # All tests
  npm run test:unit         # Unit tests only
  npm run test:integration  # Integration tests only
  npm run test:e2e          # End-to-end tests
  npm run test:coverage     # Coverage report
  ```

---

## Review Process

1. **Automated Checks:** CI must pass (lint, typecheck, tests, build).
2. **Code Review:** At least one maintainer reviews for correctness, style, and architecture.
3. **Testing Verification:** Reviewer verifies that tests adequately cover the changes.
4. **Documentation Check:** Reviewer confirms documentation is updated.
5. **Approval and Merge:** After approval, the PR is squash-merged into the main branch.

Reviewers may request changes. Please respond to feedback constructively and push additional commits as needed.

---

## Community Guidelines

- **Be Respectful:** Treat all community members with respect and professionalism.
- **Be Constructive:** Provide actionable feedback. Focus on the problem, not the person.
- **Be Inclusive:** Welcome contributors of all backgrounds, skill levels, and perspectives.
- **Be Patient:** Not everyone works at the same pace. Help newcomers when you can.
- **Ask Questions:** There are no stupid questions. If something is unclear, ask.

### Communication Channels

| Channel | Purpose |
|---------|---------|
| GitHub Issues | Bug reports, feature requests |
| GitHub Discussions | Design discussions, Q&A |
| Mailing List | Announcements, governance |
| Chat (Discord/Matrix) | Real-time community chat |

---

## Getting Help

- **First-Time Contributors:** Look for issues labeled `good first issue`.
- **Development Help:** Ask in the `#development` channel or open a discussion.
- **Architecture Questions:** Tag a maintainer in a discussion thread.
- **Stuck?** Open a draft PR early. We are happy to provide guidance before you invest too much time.

---

## Recognition

We value every contribution. Contributors are recognized through:

- ** CONTRIBUTORS.md:** All contributors are listed in the CONTRIBUTORS file.
- **Release Notes:** Significant contributions are mentioned in release notes.
- **GitHub Badges:** Contributors earn badges for various types of contributions.
- **Annual Awards:** Outstanding contributors are recognized at the annual community event.
- **Commit Access:** Trusted contributors may be granted commit access based on sustained, quality contributions.

Thank you for helping make Scilab Studio better for engineers and educators everywhere.
