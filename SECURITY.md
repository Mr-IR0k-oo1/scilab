# Security Policy

The Scilab Studio team takes security seriously. We appreciate your efforts to responsibly disclose security vulnerabilities.

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x (current development) | Yes |
| < 0.1.0 | No |

We provide security fixes for the latest minor release and backport critical fixes to supported versions as needed.

---

## Reporting a Vulnerability

If you discover a security vulnerability in Scilab Studio, please report it responsibly. **Do not open a public GitHub issue for security vulnerabilities.**

### How to Report

1. **Email:** Send a detailed report to **security@scilab-studio.org**.
2. **Subject Line:** Use the format `[SECURITY] Brief Description`.
3. **Include:**
   - Description of the vulnerability and its potential impact.
   - Steps to reproduce the issue.
   - Affected versions.
   - Any proposed fix or mitigation (if applicable).
   - Your contact information for follow-up.

### What to Expect

- **Acknowledgment:** We will acknowledge receipt within 48 hours.
- **Assessment:** We will assess the vulnerability and determine its severity within 5 business days.
- **Resolution:** We will work on a fix and coordinate disclosure with you.
- **Credit:** We will credit you in the release notes (unless you prefer to remain anonymous).

### Severity Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | Remote code execution, data exfiltration, privilege escalation | Immediate |
| High | Authentication bypass, significant data exposure | 72 hours |
| Medium | Limited data exposure, denial of service | 1 week |
| Low | Informational, minimal impact | 2 weeks |

---

## Security Response Process

1. **Triage:** Security team reviews the report and confirms the vulnerability.
2. **Assignment:** A team member is assigned to develop a fix.
3. **Fix Development:** A patch is developed in a private fork.
4. **Testing:** The fix is tested against the reported vulnerability and regression-tested.
5. **Release:** A patched version is released with a security advisory.
6. **Disclosure:** The vulnerability is publicly disclosed after the patch is available.
7. **Post-Mortem:** A review is conducted to prevent similar issues in the future.

---

## Security Best Practices for Users

### Installation
- Only download Scilab Studio from official sources (GitHub releases, official website).
- Verify checksums and signatures for downloaded packages.
- Keep Scilab Studio updated to the latest version.

### Configuration
- Do not run Scilab Studio as root or administrator unless absolutely necessary.
- Use strong, unique passwords for marketplace accounts.
- Enable two-factor authentication where available.
- Restrict network access to Scilab Studio instances in production environments.

### Plugin Security
- Only install plugins from trusted sources.
- Review plugin permissions before installation.
- Monitor installed plugins for updates and security patches.
- Remove unused plugins to reduce the attack surface.

### Data Protection
- Encrypt sensitive project data at rest and in transit.
- Use environment variables or secure vaults for credentials — never hardcode secrets.
- Regularly back up project data.
- Be cautious when importing data from untrusted sources.

### Network Security
- Use HTTPS for all marketplace and API communications.
- Configure firewalls to restrict outbound connections to trusted domains.
- Monitor network traffic for anomalous activity.

---

## Dependency Management

- **Automated Scanning:** We use Dependabot and Snyk to monitor dependencies for known vulnerabilities.
- **Update Policy:** Critical security patches are applied within 48 hours. Other updates follow our regular release cycle.
- **Lock Files:** `package-lock.json` is committed to ensure reproducible builds.
- **Audit:** Run `npm audit` regularly to check for vulnerable dependencies.
- **Minimal Dependencies:** We keep the dependency tree as small as possible to reduce risk.

---

## Data Privacy

- **No Telemetry by Default:** Scilab Studio does not collect telemetry data unless the user explicitly opts in.
- **Local-First:** Project data is stored locally by default. Cloud features require explicit opt-in.
- **Marketplace Data:** Marketplace interactions transmit only the minimum data necessary for the operation (package downloads, ratings).
- **User Accounts:** Marketplace accounts store only necessary profile information. Passwords are hashed with bcrypt.
- **GDPR Compliance:** We respect user data rights. Users can request data deletion at any time.
- **Open Source:** Our code is publicly auditable. Security through transparency.

---

## Contact

For security-related inquiries, contact **security@scilab-studio.org**.

For general issues, use [GitHub Issues](https://github.com/scilab-studio/scilab-studio/issues).
