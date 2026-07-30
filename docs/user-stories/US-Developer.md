# User Stories — Plugin Developer

## US-D01: Create a Plugin in Under an Hour
> I want to build a plugin that adds a new chart type without studying the entire codebase.

**Acceptance Criteria:**
- Plugin SDK provides a clear template.
- `manifest.json` defines the plugin identity and contributions.
- `index.js` exports a Plugin subclass with `activate()` and `deactivate()`.
- Plugin can be installed from a local `.zip` file.
- Plugin appears in the Plugin Manager immediately.

---

## US-D02: Register a Panel in the Workspace
> I want my plugin to add a panel to the left sidebar.

**Acceptance Criteria:**
- Plugin calls `context.registerPanel()` in `activate()`.
- Panel appears in the sidebar with the specified title and icon.
- Panel is removed when the plugin is deactivated.
- Panel can be resized and collapsed like built-in panels.

---

## US-D03: Subscribe to Events
> I want my plugin to react when the user opens a project.

**Acceptance Criteria:**
- Plugin calls `context.subscribe('project:opened', handler)`.
- Handler is called with the project manifest when a project opens.
- Subscription is automatically cleaned up on deactivation.

---

## US-D04: Execute Scilab Code
> I want my plugin to run Scilab computations.

**Acceptance Criteria:**
- Plugin has `engine:eval` permission in manifest.
- Plugin calls `context.engine.eval("code")`.
- Result is returned as a typed value.
- Timeout is enforced (configurable).

---

## US-D05: Create a Custom Widget
> I want to add a new widget type to the GUI Builder.

**Acceptance Criteria:**
- Widget is defined in a JSON file in the `widgets/` directory.
- Widget implements `initialize()`, `render()`, `update()`, `destroy()`.
- Widget appears in the Component Palette.
- Widget can be dragged onto the canvas.
- Widget properties are editable in the Inspector.
- Widget state is serialized and deserializable.

---

## US-D06: Distribute via Marketplace
> I want other users to install my plugin from the marketplace.

**Acceptance Criteria:**
- Plugin is packaged as a `.zip` file.
- `scilab-studio plugin publish` uploads to the marketplace.
- Plugin appears in the marketplace with description, icon, and categories.
- Users can install with one click.
- Updates are delivered through the Plugin Manager.

---

## US-D07: Debug My Plugin
> I want to see logs and errors from my plugin during development.

**Acceptance Criteria:**
- Plugin can call `logger.info()`, `logger.warn()`, `logger.error()`.
- Logs appear in the Debug panel (Ctrl+Shift+D).
- Errors show stack traces and plugin ID.
- Plugin can be reloaded without restarting the application (dev mode).

---

## US-D08: Access Platform Services
> I want my plugin to read project files and show notifications.

**Acceptance Criteria:**
- `context.project.readFile(path)` reads project files.
- `context.ui.showNotification(message, type)` shows a toast.
- `context.ui.showConfirm(message)` shows a confirmation dialog.
- `context.settings.get(key)` reads plugin settings.
- All access is scoped to declared permissions.
