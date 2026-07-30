# 31 — Scilab Compatibility Layer

Instead of tying Scilab Studio to one Scilab release, introduce an abstraction layer:

```
                Scilab Studio

                     │
          Compatibility Layer

     ┌───────────┼───────────┐

 Scilab 6.x   Scilab 2024   Future Versions

                     │
           Execution Runtime
```

This is a defining feature. For universities and research labs where different machines run different Scilab releases, this is practical rather than architectural. It positions Scilab Studio as a stable development environment instead of a thin wrapper around a single runtime.

For the Scilab Runtime that executes commands, see [28 — Scilab Runtime](28_Scilab_Runtime.md).

---

## 1. Responsibilities

| Responsibility | Description |
|----------------|-------------|
| Version Detection | Detect all installed Scilab versions on the system |
| API Normalization | Translate between Scilab version differences |
| Toolbox Compatibility | Check if required toolboxes are available |
| Deprecation Warnings | Warn about deprecated functions |
| Version Targeting | Allow projects to target a specific Scilab version |
| Feature Detection | Detect which features are available in the installed version |

---

## 2. Version Detection

### 2.1 Search Strategy

The Compatibility Layer searches for Scilab installations:

```
1. SCILAB_PATHS environment variable (comma-separated list of paths)
2. User setting: engine.paths[] (array of paths)
3. Platform default locations:
   Linux:   /usr/bin/scilab, /usr/local/bin/scilab, /opt/scilab-*/bin/scilab
   macOS:   /Applications/Scilab*.app/Contents/MacOS/bin/scilab
   Windows: C:\Program Files\Scilab*, C:\Program Files (x86)\Scilab*
4. System PATH lookup (all scilab binaries found)
5. Snap/Flatpak/AppImage locations
```

### 2.2 Version Query

For each found binary, query the version:

```bash
scilab --version --noexec
```

Output: `Scilab version "2024.1.0"`

### 2.3 Installed Versions Registry

```typescript
interface ScilabVersion {
  path: string;                    // Full path to binary
  version: string;                 // Semver (e.g., "2024.1.0")
  major: number;                   // 2024
  minor: number;                   // 1
  patch: number;                   // 0
  label: string;                   // "Scilab 2024.1.0"
  isDefault: boolean;              // Whether this is the default
  toolboxes: string[];             // Installed toolboxes
  lastVerified: number;            // Timestamp of last check
}
```

The registry is stored in `~/.config/scilab-studio/scilab-versions.json`.

---

## 3. API Normalization

### 3.1 Problem

Scilab's API changes between versions:
- Function signatures change.
- Functions are renamed or deprecated.
- New functions are added.
- Behavior of existing functions changes subtly.

### 3.2 Solution

The Compatibility Layer maintains a mapping table:

```jsonc
{
  "mappings": [
    {
      "function": "mtlb_diff",
      "scilab5": { "status": "available" },
      "scilab6": { "status": "renamed", "replacement": "diff" },
      "scilab2024": { "status": "available" }
    },
    {
      "function": "intg",
      "scilab5": { "status": "deprecated", "replacement": "integrate" },
      "scilab6": { "status": "deprecated", "replacement": "integrate" },
      "scilab2024": { "status": "removed" }
    }
  ]
}
```

### 3.3 Normalization Modes

| Mode | Behavior |
|------|----------|
| `strict` | Reject code using deprecated/removed functions |
| `warn` | Allow execution, show warnings for deprecated functions |
| `auto` | Automatically rewrite deprecated calls to replacements |
| `off` | No normalization (raw execution) |

Default: `warn`.

---

## 4. Toolbox Compatibility

### 4.1 Detection

The Compatibility Layer queries installed toolboxes:

```scilab
// Get list of installed atoms (toolboxes)
tbx_list = atomsGetInstalled();
```

### 4.2 Requirement Checking

Plugins and projects can declare toolbox dependencies:

```jsonc
{
  "engines": {
    "scilab": ">=7.0.0",
    "toolboxes": {
      "signal": ">=1.0",
      "control": "*",
      "optim": ">=2.0"
    }
  }
}
```

### 4.3 Compatibility Report

```typescript
interface CompatibilityReport {
  scilabVersion: string;
  compatible: boolean;
  issues: CompatibilityIssue[];
}

interface CompatibilityIssue {
  type: "version" | "toolbox" | "deprecated" | "removed";
  severity: "error" | "warning" | "info";
  message: string;
  function?: string;
  suggestion?: string;
}
```

---

## 5. Deprecation Warnings

### 5.1 Detection

When code is evaluated, the Compatibility Layer checks:
1. Parsed AST for function calls.
2. Each function against the deprecation mapping.
3. If deprecated, generates a warning.

### 5.2 Warning Format

```
[Deprecation] Function 'mtlb_diff' is deprecated since Scilab 6.0.
  Use 'diff' instead.
  See: https://help.scilab.org/diff
  Project targets: Scilab 2024.1.0
```

### 5.3 Suppression

Users can suppress specific deprecation warnings per project:

```jsonc
{
  "settings": {
    "scilab": {
      "suppressedWarnings": ["mtlb_diff", "intg"]
    }
  }
}
```

---

## 6. Version Targeting

### 6.1 Project Configuration

Every project declares its target Scilab version:

```jsonc
{
  "scilab_version": "2024.1.0",           // Exact version
  // OR
  "scilab_version": ">=7.0.0 <2025.0.0"  // Range
}
```

### 6.2 Version Selection

When a project is opened:

1. Read `scilab_version` from `project.json`.
2. Find installed versions that satisfy the constraint.
3. If exact match: use it.
4. If multiple matches: use the highest compatible version.
5. If no match: show a warning with options:
   - Use the closest version (with compatibility warnings).
   - Change the project's target version.
   - Install a compatible version.

### 6.3 Multi-Version Support

Users can have multiple Scilab versions installed simultaneously. The Compatibility Layer manages which version is used for each project:

```
Project A → Scilab 2024.1.0
Project B → Scilab 7.0.0
Project C → Scilab 2025.1.0
```

Each project's Scilab process runs independently.

---

## 7. Feature Detection

### 7.1 Available Features

| Feature | Scilab 6.x | Scilab 2024 | Scilab 2025+ |
|---------|-----------|-------------|--------------|
| `diff` function | Yes | Yes | Yes |
| `mtlb_diff` | Yes (deprecated) | Yes (deprecated) | No |
| Complex matrix support | Basic | Full | Full |
| GPU acceleration | No | No | Experimental |
| JSON import/export | No | Yes | Yes |
| Async evaluation | No | No | Yes |

### 7.2 Feature Gate API

Modules can check feature availability:

```typescript
const features = await engine.getFeatures();

if (features.has("json-io")) {
  // Use native JSON support
} else {
  // Fall back to string parsing
}
```

---

## 8. Migration Support

### 8.1 Project Migration

When a project targets an older Scilab version and is opened with a newer one:

1. The Compatibility Layer detects the version difference.
2. It checks the deprecation mapping for any affected functions.
3. It offers to automatically rewrite deprecated calls.
4. It updates `scilab_version` in `project.json` (with user consent).

### 8.2 Batch Migration

For classrooms or labs upgrading Scilab:

```bash
scilab-studio migrate --from 7.0.0 --to 2024.1.0 --project ./projects/
```

This:
1. Scans all projects in the directory.
2. Checks for deprecated/removed functions.
3. Offers automatic rewriting.
4. Updates `scilab_version` in each `project.json`.
5. Generates a migration report.

---

## 9. Configuration

### 9.1 User Settings

```jsonc
{
  "engine": {
    "defaultVersion": "2024.1.0",         // Default for new projects
    "normalizationMode": "warn",          // "strict" | "warn" | "auto" | "off"
    "autoDetectVersions": true,           // Scan for installations on startup
    "paths": [                            // Custom Scilab paths
      "/opt/scilab-2024/bin/scilab"
    ]
  }
}
```

### 9.2 UI

The Compatibility Layer exposes a "Scilab Versions" panel (Settings → Scilab):

- List of detected installations.
- Set default version.
- Add/remove custom paths.
- Test connection to each version.
- View compatibility report for the current project.

---

## 10. Benefits

| Benefit | Who Cares |
|---------|-----------|
| Projects work across Scilab versions | Everyone |
| Classrooms with mixed Scilab installs | Faculty |
| Gradual migration from old to new Scilab | Labs |
| Plugins declare version requirements | Plugin developers |
| Deprecation warnings before breaking changes | Everyone |
| Multiple Scilab versions side-by-side | Researchers |

This makes Scilab Studio a stable platform rather than a thin wrapper. It is the kind of systems thinking that makes a platform credible rather than just feature-rich.
