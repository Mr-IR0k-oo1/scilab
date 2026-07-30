# Community Marketplace

> The Scilab Studio Marketplace -- a central hub for discovering, sharing, and distributing engineering tools, widgets, plugins, templates, and more.

---

## Overview

The Scilab Studio Marketplace is an open ecosystem where the community can publish, discover, and install reusable components. It supports:

- **Plugins** -- Extend Scilab Studio functionality.
- **Widgets** -- Reusable UI components for the GUI builder.
- **Templates** -- Project scaffolds for specific engineering domains.
- **Reports** -- Report templates for the Report Generator.
- **Data Sets** -- Sample and reference datasets.
- **Tutorials** -- Interactive learning modules.
- **Digital Twin Definitions** -- Reusable twin configurations.

The marketplace is accessible from within Scilab Studio (Settings > Marketplace) and at [marketplace.scilab-studio.org](https://marketplace.scilab-studio.org).

---

## Marketplace Architecture

### Components

The marketplace consists of several interconnected services:

- **Marketplace Frontend** -- React SPA for browsing, searching, and installing packages.
- **API Gateway** -- Handles authentication, rate limiting, and request routing.
- **Package Service** -- Manages package metadata, versions, and storage.
- **Search Service** -- Full-text search with filtering and ranking.
- **Review Service** -- Manages the review and approval workflow.
- **User Service** -- User accounts, profiles, and contribution history.
- **Auth Service** -- OAuth 2.0 and API key authentication.
- **Analytics Service** -- Download statistics and usage metrics.

### Package Storage

- **Registry Database:** Package metadata in PostgreSQL.
- **Binary Storage:** Package files in S3-compatible object storage.
- **CDN:** Static assets and package downloads served via CDN.
- **Cache:** Popular package metadata cached in Redis.

---

## Publishing Process

### 1. Create an Account

Register at marketplace.scilab-studio.org or from within Scilab Studio (Settings > Marketplace > Sign Up).

### 2. Prepare Your Package

Use the appropriate SDK:

```bash
# For plugins
npx @scilab-studio/sdk plugin create my-plugin

# For widgets
npx @scilab-studio/sdk widget create my-widget

# For templates
npx @scilab-studio/sdk template create my-template
```

### 3. Test Locally

```bash
# Load in development mode
scilab-studio plugin load ./my-plugin

# Run the test suite
npm test
```

### 4. Publish

```bash
# Login
scilab-studio marketplace login

# Publish
scilab-studio marketplace publish ./my-plugin
```

Or upload via the web interface at marketplace.scilab-studio.org/publish.

### 5. Review

Submissions undergo automated and optional manual review.

### 6. Live

Once approved, your package is visible and available for installation.

---

## Package Format

All marketplace packages use the `.spkg` format (Scilab Studio Package):

```
my-package-1.0.0.spkg
  manifest.json          # Package metadata
  README.md              # Documentation
  icon.png               # Package icon (512x512)
  screenshots/           # Screenshots (optional)
  dist/                  # Compiled/distributed code
  tests/                 # Test suite
  LICENSE                # License file
```

### manifest.json

Key fields:

- `formatVersion` -- Schema version.
- `id` -- Unique package identifier (reverse-domain notation).
- `name` -- Human-readable package name.
- `version` -- Semantic version.
- `description` -- Short description.
- `author` -- Author information (name, email, URL).
- `license` -- SPDX license identifier.
- `category` -- Primary category.
- `tags` -- Searchable tags array.
- `type` -- Package type (plugin, widget, template, etc.).
- `engines` -- Required Scilab Studio version.
- `entryPoint` -- Main entry file.
- `permissions` -- Required permissions.
- `dependencies` -- Required packages and versions.
- `repository` -- Source code repository URL.
- `changelog` -- Version history.

---

## Versioning and Dependencies

### Semantic Versioning

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix | Patch | 1.0.0 to 1.0.1 |
| New feature (backward-compatible) | Minor | 1.0.0 to 1.1.0 |
| Breaking change | Major | 1.0.0 to 2.0.0 |

### Version Range Syntax

| Syntax | Meaning |
|--------|---------|
| `^1.0.0` | Compatible with 1.0.0 (>=1.0.0 <2.0.0) |
| `~1.2.0` | Approximately 1.2.0 (>=1.2.0 <1.3.0) |
| `>=1.0.0` | 1.0.0 or newer |
| `1.0.0` | Exactly 1.0.0 |

### Dependency Resolution

- Packages are installed in dependency order.
- Conflicts are detected and reported before installation.
- Circular dependencies are rejected.

---

## Quality Standards

### Automated Checks

- **Manifest validity:** Correct schema, required fields present.
- **License compliance:** Must be an OSI-approved open-source license.
- **No malicious code:** Automated security scan (static analysis).
- **No secrets:** Scan for hardcoded API keys, passwords, tokens.
- **Dependency audit:** No known critical vulnerabilities.
- **Icon and screenshots:** Present, correct dimensions, appropriate content.

### Manual Review (for Featured Packages)

- **Code quality:** Clean, readable, well-structured code.
- **Documentation:** Clear README with usage instructions.
- **Tests:** Meaningful test coverage.
- **Functionality:** Package does what it claims.
- **UI quality:** Follows Scilab Studio design guidelines.

### Quality Score

Each package receives a quality score based on:

- Documentation completeness (20%)
- Test coverage (20%)
- Code quality metrics (20%)
- Community feedback (20%)
- Maintenance activity (20%)

---

## Review Process

### Automated Review (Immediate)

Every submission goes through:

1. Manifest validation.
2. Security scan for vulnerabilities.
3. License check for OSI-approved license.
4. Package integrity verification.
5. Dependency compatibility check.

### Manual Review (Optional)

Packages seeking Featured or Verified status:

1. A reviewer examines the submission.
2. Code is tested in a sandboxed environment.
3. Functionality is verified against the description.
4. Feedback is provided to the author.
5. Approved packages receive the Featured or Verified badge.

### Review Timeline

| Type | Expected Time |
|------|---------------|
| Automated pass | Immediate |
| Manual review (standard) | 3-5 business days |
| Manual review (Featured) | 5-10 business days |
| Resubmission after fix | 1-2 business days |

---

## Categories and Tags

### Categories

| Category | Description |
|----------|-------------|
| Analysis | Data analysis and processing tools |
| Visualization | Charts, plots, and visual tools |
| Simulation | Simulation and modeling packages |
| Education | Teaching and learning resources |
| Data | Data import, export, and transformation |
| Engineering | Domain-specific engineering tools |
| Utilities | General-purpose utilities |
| Themes | UI themes and visual customization |
| Integration | Third-party tool integrations |

### Tags

Tags are free-form and searchable. Popular tags include:

`signal-processing`, `control-systems`, `filters`, `FFT`, `FEM`, `CFD`, `thermodynamics`, `electronics`, `robotics`, `aerospace`, `biomedical`, `finance`, `education`, `beginner`, `advanced`, `open-data`

---

## Search and Discovery

### Search Features

- **Full-text search** across name, description, tags, and documentation.
- **Category and tag filtering** for narrowing results.
- **Sort by:** Relevance, downloads, rating, recently updated, newest.
- **Advanced search** with multiple filters combined.
- **Saved searches** for registered users.

### Discovery Features

- **Featured packages** curated by the community team.
- **Trending packages** based on recent download velocity.
- **Recommended packages** based on installed packages and usage patterns.
- **Collections** curated lists for specific workflows or courses.
- **New and Noteworthy** highlighting recently published quality packages.

---

## Ratings and Reviews

### Rating System

- 1-5 star rating scale.
- Only users who have installed and used the package can rate.
- One rating per user per package (can be updated).
- Ratings are not anonymous -- linked to user profiles.

### Review System

- Text reviews with the rating.
- Minimum 10 characters, maximum 2000 characters.
- Reviews can include code snippets and screenshots.
- Package authors can respond to reviews.
- Reviews can be flagged for moderation.

### Display

- Average rating displayed prominently on the package page.
- Rating distribution histogram shown.
- Most helpful reviews shown first.
- Author responses are visually distinguished.

---

## Download Statistics

### Metrics Tracked

- Total downloads (all time).
- Downloads in the last 7 days, 30 days, 90 days.
- Unique downloaders (estimated).
- Geographic distribution (country level).
- Scilab Studio version distribution.
- Platform distribution (Linux, macOS, Windows).

### Visibility

- Download counts are public on the package page.
- Trending algorithms use recent download velocity.
- Authors have access to detailed analytics in their dashboard.

---

## Security Scanning

### Automated Security Measures

- **Static analysis:** Every package is scanned for known vulnerability patterns.
- **Dependency audit:** npm audit checks for known CVEs in dependencies.
- **Secret scanning:** Detection of hardcoded credentials, API keys, and tokens.
- **Malware detection:** Signature-based and behavioral analysis.
- **Code signing:** Packages can be signed by verified publishers for integrity verification.

### Sandboxed Execution

- Packages submitted for manual review are executed in an isolated sandbox.
- Network access, file system access, and system calls are monitored and restricted.

### Reporting

- Users can report security concerns on any package.
- Security reports are triaged within 24 hours.
- Confirmed vulnerabilities result in immediate package suspension.

---

## License Compliance

### Accepted Licenses

All packages must use an OSI-approved open-source license. Common accepted licenses:

- GPL v2, GPL v3
- MIT
- Apache 2.0
- BSD 2-Clause, BSD 3-Clause
- LGPL v2.1, LGPL v3
- MPL 2.0
- EPL 2.0

### License Validation

- License is declared in the manifest.
- A LICENSE file must be present in the package.
- Automated checks verify the declared license matches the LICENSE file.
- Incompatible licenses are flagged and rejected.

### Dependency License Compatibility

- The system checks that all transitive dependency licenses are compatible with the declared license.
- Conflicts are reported to the publisher before approval.

---

## Community Guidelines

### Publisher Responsibilities

- Maintain your packages with timely bug fixes and updates.
- Respond to issues and reviews within a reasonable time.
- Follow semantic versioning for all releases.
- Provide accurate descriptions and documentation.
- Respect the community code of conduct.

### User Responsibilities

- Rate and review packages honestly.
- Report bugs and security issues through appropriate channels.
- Give credit to package authors when building upon their work.
- Contribute back when possible.

### Moderation

- The community team moderates reviews, ratings, and discussions.
- Spam, harassment, and inappropriate content are removed immediately.
- Repeat violations may result in account suspension.

---

## Monetization

### Free and Open Source

The Scilab Studio Marketplace is free and open source. All packages are free to install and use under their declared open-source license.

### Supported Models

While all packages are free, authors may:

- Accept donations via linked funding platforms (GitHub Sponsors, Open Collective).
- Offer commercial support or consulting separately.
- Provide premium documentation or training services.

### Future Considerations

- **Enterprise/Private Registries:** Organizations may host private registries for internal packages (planned).
- **Sponsored Packages:** Community-sponsored packages with priority support (under discussion).

---

## API for Marketplace

The marketplace is fully API-driven. All operations available in the UI are also available via the API.

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/marketplace/packages` | GET | Search packages |
| `/v1/marketplace/packages/:id` | GET | Get package details |
| `/v1/marketplace/packages/:id/install` | POST | Install a package |
| `/v1/marketplace/packages/:id/rate` | POST | Rate a package |
| `/v1/marketplace/packages/:id/review` | POST | Write a review |
| `/v1/marketplace/publish` | POST | Publish a package |
| `/v1/marketplace/categories` | GET | List categories |
| `/v1/marketplace/featured` | GET | Get featured packages |
| `/v1/marketplace/trending` | GET | Get trending packages |
| `/v1/users/:id/packages` | GET | List a user's packages |

### Authentication

- **Public endpoints:** Search, browse, package details (read-only).
- **Authenticated endpoints:** Install, rate, review, publish.
- **API keys** for programmatic access.
- **OAuth 2.0** for user-facing integrations.

### Rate Limits

| Tier | Requests per Minute | Requests per Hour |
|------|--------------------:|-------------------:|
| Anonymous | 30 | 500 |
| Authenticated | 60 | 1,000 |
| Publisher | 120 | 5,000 |

For full API documentation, see [API Reference](14_API_Reference.md).
