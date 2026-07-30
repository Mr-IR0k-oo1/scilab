# Best Practices

Guidelines for building high-quality Scilab Studio extensions.

## General Principles

### 1. Single Responsibility
Each extension should do one thing well. A plugin that handles data import shouldn't also handle visualization.

### 2. Explicit Dependencies
Declare all dependencies in your manifest. Don't assume other extensions are installed.

### 3. Graceful Degradation
Handle missing dependencies, failed Scilab connections, and empty data gracefully. Show helpful error messages, not crashes.

### 4. Consistent UX
Follow the platform's interaction patterns. Use consistent naming, icons, and keyboard shortcuts.

## Plugin Development

### Naming

- Use reverse domain notation for IDs: `com.example.my-plugin`.
- Use descriptive command IDs: `my-plugin.analyze-data`, not `my-plugin.cmd1`.
- Use labels that describe what the command does.

### Commands

```javascript
// Good
context.registerCommand({
  id: 'data-import.import-csv',
  label: 'Import CSV File',
  execute: async () => { /* ... */ }
});

// Bad
context.registerCommand({
  id: 'data-import.cmd1',
  label: 'Do Thing',
  execute: async () => { /* ... */ }
});
```

### Events

- Use namespaced event names: `data:imported`, `chart:rendered`.
- Include relevant data in event payloads.
- Always dispose event subscriptions.

### Error Handling

```javascript
// Good
try {
  const result = await context.executeScilab(code);
  if (result.error) {
    context.showErrorMessage(`Scilab error: ${result.error.message}`);
    return;
  }
  // Process result
} catch (error) {
  context.showErrorMessage(`Failed to execute: ${error.message}`);
  context.getLogger().error('Execution failed', error);
}

// Bad
const result = await context.executeScilab(code);
// Assume result is always valid
```

### Storage

- Use meaningful keys: `import:last-file`, not `key1`.
- Clean up storage when the plugin is deactivated.
- Don't store large data in storage. Use the file system.

## Widget Development

### Properties

- Provide sensible defaults for all properties.
- Use the `group` field to organize properties in the inspector.
- Include descriptions for all properties.
- Use `enum` types for properties with fixed options.

### Rendering

- Keep render functions pure. No side effects.
- Handle missing or invalid data gracefully.
- Use CSS classes, not inline styles.
- Support both dark and light themes.
- Test at different sizes.

### Data Binding

- Support both static values and Scilab expressions.
- Handle binding errors without crashing.
- Show placeholders when data is loading.

### Performance

- Don't create new objects in render loops.
- Use requestAnimationFrame for animations.
- Memoize expensive calculations.
- Test with 100+ widgets on screen.

## Visualization Development

### Data

- Validate data before rendering.
- Handle empty datasets.
- Downsample large datasets for performance.
- Support both Scilab variables and inline data.

### Rendering

- Use theme colors, not hard-coded values.
- Support interactive features (hover, click, zoom).
- Export to multiple formats.
- Test with different screen sizes.

### Performance

- Meet the performance budgets in RFC-0004.
- Use progressive rendering for large datasets.
- Cache expensive calculations.
- Profile rendering performance regularly.

## Template Development

### Structure

- Keep templates focused on one use case.
- Include sample data and documentation.
- Provide sensible defaults for all variables.
- Test with different variable values.

### Documentation

- Explain what the template is for.
- List prerequisites.
- Describe the directory structure.
- Include usage instructions.

## Code Style

### JavaScript

- Use CommonJS modules (not ES modules).
- Use async/await, not callbacks.
- Use meaningful variable names.
- Add JSDoc comments for public APIs.
- Handle errors explicitly.

### JSON

- Use 2-space indentation.
- Sort keys alphabetically.
- Include all required fields.
- Use consistent naming conventions.

## Testing

- Write tests for all public APIs.
- Test error conditions.
- Test with different Scilab versions.
- Test with large datasets.
- Test accessibility.
- Test performance.

## Documentation

- Document all public APIs.
- Include code examples.
- Explain error conditions.
- Describe limitations.
- Keep documentation up to date.
