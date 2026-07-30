# Scilab Studio SDK

Build plugins, widgets, visualizations, and templates for Scilab Studio.

## Quick Start

```bash
# Install the CLI
npm install -g @scilab-studio/cli

# Create a new plugin
scilab-studio create plugin my-plugin

# Create a new widget
scilab-studio create widget my-widget

# Preview your extension
scilab-studio preview
```

## What Can You Build?

| Type | Description | Docs |
|------|-------------|------|
| **Plugins** | Extend the platform with new features | [Plugin Development](plugin-development.md) |
| **Widgets** | Create custom GUI components | [Widget Development](widget-development.md) |
| **Visualizations** | Add new chart types | [Visualization Development](visualization-development.md) |
| **Templates** | Create project templates | [Template Development](template-development.md) |

## Architecture

```
Your Extension
    ↓
Scilab Studio SDK
    ↓
Platform API (stable, versioned)
    ↓
Scilab Studio Core
```

Your code never touches the core directly. The SDK provides a stable abstraction layer.

## Prerequisites

- Node.js 18+ (for SDK tooling)
- Scilab 7.0+ (for testing)
- Scilab Studio 0.1+ (for preview)

## Resources

- [Getting Started](getting-started.md) — Setup and first extension
- [Best Practices](best-practices.md) — Patterns and conventions
- [API Reference](../platform/) — Complete API documentation
- [Examples](examples/) — Working example extensions
