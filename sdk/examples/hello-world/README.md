# Example: Hello World Plugin

A minimal plugin that demonstrates the basic plugin structure.

## Files

```
hello-world/
├── plugin.json
├── index.js
└── README.md
```

## plugin.json

```json
{
  "id": "com.example.hello-world",
  "name": "Hello World",
  "version": "1.0.0",
  "description": "A minimal example plugin",
  "author": "Scilab Studio Team",
  "license": "MIT",
  "scilab_studio_version": ">=0.1",
  "main": "index.js",
  "permissions": ["ui.panel"]
}
```

## index.js

```javascript
module.exports = {
  onActivate(context) {
    // Register a panel
    context.registerPanel({
      id: 'hello-world.panel',
      title: 'Hello World',
      icon: 'greet',
      location: 'right',
      render: () => ({
        tag: 'div',
        props: {
          style: {
            padding: '16px',
            fontFamily: 'var(--ss-font-family)'
          }
        },
        children: [
          {
            tag: 'h2',
            props: {},
            children: ['Hello World!']
          },
          {
            tag: 'p',
            props: {},
            children: ['This is a simple example plugin.']
          },
          {
            tag: 'button',
            props: {
              class: 'ss-button ss-button-primary',
              onClick: () => {
                context.showInformationMessage('Hello from the plugin!');
              }
            },
            children: ['Say Hello']
          }
        ]
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

## Usage

1. Copy this directory to `~/.scilab-studio/plugins/hello-world/`
2. Restart Scilab Studio
3. The "Hello World" panel appears in the right sidebar
4. Press Ctrl+Shift+H to say hello

## What This Demonstrates

- Plugin manifest structure
- `onActivate` / `onDeactivate` lifecycle
- Panel registration and rendering
- Command registration with keyboard shortcut
- Logging
- UI messages
