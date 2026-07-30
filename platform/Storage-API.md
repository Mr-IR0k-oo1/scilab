# Storage API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.1 |
| Stability | Stable |

---

## Purpose

Persistent key-value storage for plugins, settings, and user data.

## Methods

### storage.get(key: string): Promise\<any\>

Gets a value by key.

```javascript
const value = await storage.get('my-key');
console.log(value); // { nested: "object" }
```

### storage.set(key: string, value: any): Promise\<void\>

Sets a value. Values must be JSON-serializable.

```javascript
await storage.set('my-key', { nested: 'object' });
```

### storage.delete(key: string): Promise\<void\>

Deletes a key.

```javascript
await storage.delete('my-key');
```

### storage.has(key: string): Promise\<boolean\>

Checks if a key exists.

```javascript
const exists = await storage.has('my-key');
console.log(exists); // true
```

### storage.keys(): Promise\<string[]\>

Returns all keys.

```javascript
const keys = await storage.keys();
console.log(keys); // ["key1", "key2", "key3"]
```

### storage.clear(): Promise\<void\>

Clears all storage.

```javascript
await storage.clear();
```

### storage.getSize(): Promise\<number\>

Returns storage size in bytes.

```javascript
const size = await storage.getSize();
console.log(size); // 1024
```

### storage.getPluginStorage(pluginId: string): PluginStorage

Returns a namespaced storage for a plugin.

```javascript
const pluginStorage = storage.getPluginStorage('com.example.my-plugin');
await pluginStorage.set('settings', { theme: 'dark' });
```

## Scope

| Scope | Description | Persistence |
|-------|-------------|-------------|
| `global` | Application-wide settings | Across sessions |
| `project` | Project-specific data | Per project |
| `plugin` | Plugin-specific data | Per plugin |
| `session` | Current session only | Lost on restart |

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `storage:set` | `{ key: string, value: any }` | Value was set |
| `storage:delete` | `{ key: string }` | Key was deleted |
| `storage:clear` | `{}` | Storage was cleared |

## Examples

### Store User Settings

```javascript
// Save settings
await storage.set('user:settings', {
  theme: 'dark',
  fontSize: 14,
  autoSave: true
});

// Load settings
const settings = await storage.get('user:settings');
```

### Plugin Storage

```javascript
// Each plugin gets its own namespace
const pluginStore = storage.getPluginStorage('com.example.my-plugin');

await pluginStore.set('lastRun', new Date().toISOString());
await pluginStore.set('runCount', 42);

const lastRun = await pluginStore.get('lastRun');
```

### Project Storage

```javascript
// Store project-specific data
const projectStore = storage.getProjectStorage(project.id);

await projectStore.set('recentFiles', ['main.sce', 'data.csv']);
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `StorageQuotaExceeded` | ST-001 | Storage limit reached |
| `InvalidKey` | ST-002 | Key is empty or invalid |
| `InvalidValue` | ST-003 | Value is not JSON-serializable |
| `StorageCorrupted` | ST-004 | Storage data is corrupted |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
