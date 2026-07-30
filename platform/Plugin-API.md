# Plugin API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.2 |
| Stability | Stable |

---

## Purpose

Manages plugin lifecycle, registration, and communication.

## Methods

### plugin.getPlugin(pluginId: string): Plugin | null

Returns a plugin descriptor.

```javascript
const plugin = plugin.getPlugin('com.example.my-plugin');
console.log(plugin.status); // "active"
```

### plugin.getAllPlugins(): Plugin[]

Returns all installed plugins.

```javascript
const plugins = plugin.getAllPlugins();
console.log(plugins.length); // 5
```

### plugin.activatePlugin(pluginId: string): Promise\<void\>

Activates a deactivated plugin.

```javascript
await plugin.activatePlugin('com.example.my-plugin');
```

### plugin.deactivatePlugin(pluginId: string): Promise\<void\>

Deactivates an active plugin.

```javascript
await plugin.deactivatePlugin('com.example.my-plugin');
```

### plugin.installPlugin(source: string): Promise\<Plugin\>

Installs a plugin from a file path or URL.

```javascript
const newPlugin = await plugin.installPlugin('./my-plugin.scplugin');
console.log(newPlugin.id); // "com.example.my-plugin"
```

### plugin.uninstallPlugin(pluginId: string): Promise\<void\>

Removes a plugin and its data.

```javascript
await plugin.uninstallPlugin('com.example.my-plugin');
```

### plugin.updatePlugin(pluginId: string): Promise\<Plugin\>

Updates a plugin to the latest version.

```javascript
const updated = await plugin.updatePlugin('com.example.my-plugin');
console.log(updated.version); // "1.1.0"
```

### plugin.getPluginStorage(pluginId: string): PluginStorage

Returns the storage interface for a plugin.

```javascript
const storage = plugin.getPluginStorage('com.example.my-plugin');
await storage.set('key', 'value');
```

### plugin.getPluginContext(pluginId: string): PluginContext | null

Returns the context object for a running plugin.

```javascript
const ctx = plugin.getPluginContext('com.example.my-plugin');
ctx.emit('custom:event', { data: 42 });
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `plugin:installed` | `{ plugin: Plugin }` | Plugin was installed |
| `plugin:uninstalled` | `{ pluginId: string }` | Plugin was uninstalled |
| `plugin:activated` | `{ plugin: Plugin }` | Plugin was activated |
| `plugin:deactivated` | `{ pluginId: string }` | Plugin was deactivated |
| `plugin:updated` | `{ plugin: Plugin }` | Plugin was updated |
| `plugin:error` | `{ pluginId: string, error: Error }` | Plugin encountered an error |

## Examples

### Install and Activate

```javascript
// Install from file
const plugin = await plugin.installPlugin('./my-plugin.scplugin');

// Activate
await plugin.activatePlugin(plugin.id);

// Verify
const p = plugin.getPlugin(plugin.id);
console.log(p.status); // "active"
```

### List Active Plugins

```javascript
const activePlugins = plugin.getAllPlugins()
  .filter(p => p.status === 'active');

activePlugins.forEach(p => {
  console.log(`${p.name} v${p.version}`);
});
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `PluginNotFound` | PL-001 | Plugin ID does not exist |
| `PluginAlreadyInstalled` | PL-002 | Plugin is already installed |
| `PluginAlreadyActive` | PL-003 | Plugin is already active |
| `PluginNotActive` | PL-004 | Plugin is not active |
| `PluginLoadFailed` | PL-005 | Plugin failed to load |
| `DependencyMissing` | PL-006 | Required dependency not installed |
| `VersionConflict` | PL-007 | Version incompatibility |
| `PermissionDenied` | PL-008 | Insufficient permissions |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
