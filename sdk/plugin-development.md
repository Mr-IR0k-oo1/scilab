# Plugin Development

Plugins extend Scilab Studio with new features. They can add panels, commands, menu items, status bar items, and interact with the Scilab runtime.

## Plugin Structure

```
my-plugin/
├── plugin.json        # Manifest (required)
├── index.js           # Entry point (required)
├── styles.css         # Optional styles
├── README.md          # Documentation
└── test/
    └── index.test.js  # Tests
```

## Manifest (plugin.json)

```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": "Author Name",
  "license": "MIT",
  "repository": "https://github.com/example/my-plugin",
  "scilab_studio_version": ">=0.1",
  "scilab_version": ">=7.0",
  "main": "index.js",
  "permissions": ["ui.panel", "scilab.execute"],
  "dependencies": {},
  "contributes": {
    "commands": [
      {
        "id": "my-plugin.run",
        "label": "Run Analysis",
        "keybinding": "Ctrl+Shift+R"
      }
    ],
    "panels": [
      {
        "id": "my-plugin.panel",
        "title": "My Panel",
        "icon": "chart",
        "location": "right"
      }
    ],
    "menus": [
      {
        "id": "my-plugin.menu",
        "label": "My Plugin",
        "items": [
          { "command": "my-plugin.run" }
        ]
      }
    ],
    "settings": [
      {
        "id": "my-plugin.setting1",
        "label": "Setting 1",
        "type": "string",
        "default": "value"
      }
    ]
  }
}
```

## Entry Point

```javascript
module.exports = {
  onActivate(context) {
    // Called when plugin is activated
    // Register commands, panels, menus, etc.
  },

  onDeactivate(context) {
    // Called when plugin is deactivated
    // Clean up resources
  }
};
```

## PluginContext API

### Events

```javascript
// Subscribe to events
const disposable = context.on('event:name', (data) => {
  console.log(data);
});

// Emit events
context.emit('event:name', { key: 'value' });

// Dispose subscription
disposable.dispose();
```

### Commands

```javascript
context.registerCommand({
  id: 'my-plugin.my-command',
  label: 'My Command',
  category: 'My Plugin',
  icon: 'run',
  keybinding: 'Ctrl+M',
  enabled: () => true,
  execute: async (args) => {
    // Do something
    return result;
  },
  undo: async (args) => {
    // Undo the command
  }
});
```

### Panels

```javascript
context.registerPanel({
  id: 'my-plugin.panel',
  title: 'My Panel',
  icon: 'chart',
  location: 'right', // 'left' | 'right' | 'bottom'
  render: (props) => {
    return {
      tag: 'div',
      props: { class: 'my-panel' },
      children: ['Panel content']
    };
  }
});
```

### Menu Items

```javascript
context.registerMenu({
  id: 'my-plugin.menu',
  label: 'My Plugin',
  items: [
    {
      label: 'Action 1',
      command: 'my-plugin.action1'
    },
    {
      type: 'separator'
    },
    {
      label: 'Action 2',
      command: 'my-plugin.action2'
    }
  ]
});
```

### Status Bar

```javascript
context.registerStatusBar({
  id: 'my-plugin.status',
  text: 'Ready',
  position: 'left', // 'left' | 'right'
  priority: 100
});

// Update later
statusBarItem.setText('Processing...');
```

### Scilab

```javascript
// Execute code
const result = await context.executeScilab('x = sin(0:0.1:10)');
console.log(result.output);

// Get a variable
const x = await context.getScilabVariable('x');
console.log(x.value);

// List variables
const vars = await context.listScilabVariables();
```

### Storage

```javascript
const storage = context.getStorage();

// Save data
await storage.set('myKey', { nested: 'object' });

// Load data
const data = await storage.get('myKey');

// Delete data
await storage.delete('myKey');

// List keys
const keys = await storage.keys();
```

### Logger

```javascript
const logger = context.getLogger();

logger.info('Plugin activated');
logger.warn('Something might be wrong');
logger.error('Something failed', error);
logger.debug('Debug details', { extra: 'data' });
```

### UI Messages

```javascript
context.showInformationMessage('Operation completed');
context.showErrorMessage('Something failed');
context.showWarningMessage('Check your input');
```

## Lifecycle

```
Discovery → Activation → Running → Deactivation
```

1. **Discovery**: Plugin Manager finds plugin.json.
2. **Activation**: `onActivate(context)` is called.
3. **Running**: Plugin is active and responding to events.
4. **Deactivation**: `onDeactivate(context)` is called. Resources are released.

## Error Handling

- Errors in `onActivate` prevent the plugin from loading.
- Errors in command execution are caught and logged.
- Errors in event handlers are caught and logged.
- Throwing in `onDeactivate` logs a warning but doesn't block.

## Best Practices

- Use meaningful command IDs: `your-plugin.action-name`.
- Always dispose event subscriptions in `onDeactivate`.
- Don't block the UI thread. Use async operations.
- Log important operations for debugging.
- Handle errors gracefully. Don't let errors propagate.
- Test your plugin with `scilab-studio preview`.

## Next Steps

- [Best Practices](best-practices.md)
- [Widget Development](widget-development.md)
- [API Reference](../platform/)
- [Examples](examples/)
