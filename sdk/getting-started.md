# Getting Started

## Installation

### Prerequisites

- Node.js 18 or later
- npm 9 or later
- Scilab 7.0 or later (on PATH)
- Scilab Studio 0.1 or later

### Install the SDK

```bash
npm install -g @scilab-studio/cli
```

Verify installation:

```bash
scilab-studio --version
```

## Create Your First Plugin

### Step 1: Scaffold

```bash
scilab-studio create plugin hello-world
cd hello-world
```

This creates:

```
hello-world/
├── plugin.json        # Manifest
├── index.js           # Entry point
├── README.md          # Documentation
└── test/
    └── index.test.js  # Tests
```

### Step 2: Edit the Manifest

```json
{
  "id": "com.example.hello-world",
  "name": "Hello World",
  "version": "1.0.0",
  "description": "My first Scilab Studio plugin",
  "author": "Your Name",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "permissions": ["ui.panel"]
}
```

### Step 3: Write the Code

```javascript
// index.js
module.exports = {
  onActivate(context) {
    // Register a panel
    context.registerPanel({
      id: 'hello-panel',
      title: 'Hello World',
      icon: 'greet',
      render: () => ({
        tag: 'div',
        props: { class: 'hello-world' },
        children: ['Hello from my plugin!']
      })
    });

    // Register a command
    context.registerCommand({
      id: 'hello-world.greet',
      label: 'Say Hello',
      keybinding: 'Ctrl+Shift+H',
      execute: () => {
        context.showInformationMessage('Hello, World!');
      }
    });

    context.getLogger().info('Hello World plugin activated');
  },

  onDeactivate(context) {
    context.getLogger().info('Hello World plugin deactivated');
  }
};
```

### Step 4: Test

```bash
scilab-studio preview
```

This opens Scilab Studio with your plugin loaded.

### Step 5: Package

```bash
scilab-studio package
```

Creates `hello-world-1.0.0.scplugin`.

## Create Your First Widget

```bash
scilab-studio create widget my-gauge
cd my-gauge
```

### Edit the Widget

```javascript
// index.js
module.exports = {
  type: 'gauge',
  name: 'Gauge',
  icon: 'gauge',
  category: 'display',
  version: '1.0.0',

  properties: [
    { name: 'value', type: 'number', default: 0, label: 'Value' },
    { name: 'min', type: 'number', default: 0, label: 'Min' },
    { name: 'max', type: 'number', default: 100, label: 'Max' },
    { name: 'color', type: 'color', default: '#4a9eff', label: 'Color' }
  ],

  render(props) {
    const percent = ((props.value - props.min) / (props.max - props.min)) * 100;
    return {
      tag: 'div',
      props: { class: 'ss-widget ss-widget-gauge' },
      children: [
        {
          tag: 'div',
          props: {
            class: 'gauge-fill',
            style: { width: `${percent}%`, backgroundColor: props.color }
          },
          children: []
        },
        {
          tag: 'span',
          props: { class: 'gauge-label' },
          children: [`${props.value}`]
        }
      ]
    };
  }
};
```

## Development Workflow

### Watch Mode

```bash
scilab-studio watch
```

Rebuilds on file changes and hot-reloads in Scilab Studio.

### Debug Mode

```bash
scilab-studio debug
```

Opens the developer tools and shows plugin logs.

### Run Tests

```bash
scilab-studio test
```

### Build for Distribution

```bash
scilab-studio build
```

Creates a distributable package in `dist/`.

## Next Steps

- [Plugin Development](plugin-development.md) — Complete plugin guide
- [Widget Development](widget-development.md) — Complete widget guide
- [Best Practices](best-practices.md) — Patterns and conventions
- [Examples](examples/) — Working example extensions
