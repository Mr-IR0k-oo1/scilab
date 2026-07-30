# Extension Points

## Overview

Scilab Studio is a platform. Third parties can extend it without modifying core code.

## Extension Types

| Type | Purpose | Example |
|------|---------|---------|
| Widgets | Custom GUI components | Gauge, LED, Matrix Display |
| Charts | Custom visualization types | Waterfall, Bode, Nyquist |
| Templates | Project templates | Signal Processing Lab |
| Report Blocks | Custom report elements | Equation, Code Block |
| Importers | Data import formats | MAT files, HDF5 |
| Exporters | Data export formats | LaTeX, PowerPoint |
| Solvers | Custom Scilab solvers | Custom ODE solver |
| Toolboxes | Domain-specific toolkits | Control Systems Toolbox |
| Themes | Visual themes | Ocean, Monokai |
| Language Packs | UI translations | Hindi, Spanish |

## Extension Registration

### Widgets
```typescript
widgetService.registerType({
  type: 'gauge',
  name: 'Gauge',
  category: 'display',
  properties: [...],
  render: (props) => { ... }
});
```

### Charts
```typescript
visualizationService.registerChartType({
  type: 'waterfall',
  name: 'Waterfall Chart',
  category: 'engineering',
  options: {...],
  dataRequirements: {...],
  render: (canvas, data, options, theme) => { ... }
});
```

### Templates
```typescript
templateService.register({
  id: 'edu.signal-processing',
  name: 'Signal Processing Lab',
  category: 'education',
  files: [...],
  variables: {...]
});
```

### Report Blocks
```typescript
reportService.registerBlockType({
  type: 'equation',
  name: 'Equation',
  category: 'content',
  render: (content) => { ... }
});
```

### Importers
```typescript
dataService.registerImporter({
  type: 'mat',
  name: 'MAT File',
  extensions: ['.mat'],
  import: (file) => { ... }
});
```

### Themes
```typescript
themeService.registerTheme({
  id: 'ocean',
  name: 'Ocean',
  extends: 'dark',
  colors: {...]
});
```

## Extension Lifecycle

```
Discovery → Registration → Activation → Running → Deactivation
```

### Discovery
Scan extension directories for manifests.

### Registration
Validate manifest, register with service.

### Activation
Extension begins providing functionality.

### Running
Extension is active and responsive.

### Deactivation
Extension releases resources.

## Extension Manifest

Every extension has a manifest:

```json
{
  "id": "com.example.my-extension",
  "name": "My Extension",
  "version": "1.0.0",
  "type": "widget",
  "description": "A custom widget",
  "author": "Author Name",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "permissions": []
}
```

## Extension Directory Structure

```
~/.scilab-studio/
├── plugins/           # Plugin extensions
├── widgets/           # Widget extensions
├── themes/            # Theme extensions
├── templates/         # Template extensions
└── extensions/        # Other extensions
```

## Extension Marketplace (v0.2+)

Community extensions are published to the Marketplace:

1. Developer publishes extension.
2. Automated security scan.
3. Automated compatibility test.
4. Manual review (if required).
5. Published to Marketplace.
6. Users install with one click.

## Rules

- Extensions cannot modify core code.
- Extensions communicate through events.
- Extensions are sandboxed.
- Extensions declare permissions.
- Extensions are versioned.
- Breaking changes require major version bump.
