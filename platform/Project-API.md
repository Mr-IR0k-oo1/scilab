# Project API

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Since | 0.1 |
| Stability | Stable |

---

## Purpose

Manages project creation, loading, saving, and file operations.

## Methods

### project.create(name: string, options?: CreateOptions): Promise\<Project\>

Creates a new project.

```javascript
const project = await project.create('My Project', {
  template: 'blank',
  location: '/home/user/projects'
});
console.log(project.path); // "/home/user/projects/my-project"
```

### project.open(path: string): Promise\<Project\>

Opens an existing project.

```javascript
const project = await project.open('/home/user/projects/my-project');
console.log(project.name); // "My Project"
```

### project.save(): Promise\<void\>

Saves the current project.

```javascript
await project.save();
```

### project.close(): Promise\<void\>

Closes the current project.

```javascript
await project.close();
```

### project.getCurrent(): Project | null

Returns the current project.

```javascript
const project = project.getCurrent();
if (project) {
  console.log(project.name);
}
```

### project.getFiles(): FileNode[]

Returns the project file tree.

```javascript
const files = project.getFiles();
console.log(files.length); // 5
```

### project.createFile(name: string, content?: string): Promise\<FileNode\>

Creates a file in the project.

```javascript
const file = await project.createFile('main.sce', '// Start here');
```

### project.createDirectory(name: string): Promise\<FileNode\>

Creates a directory in the project.

```javascript
const dir = await project.createDirectory('data');
```

### project.deleteFile(path: string): Promise\<void\>

Deletes a file or directory.

```javascript
await project.deleteFile('old-file.sce');
```

### project.renameFile(oldPath: string, newPath: string): Promise\<void\>

Renames a file or directory.

```javascript
await project.renameFile('temp.sce', 'analysis.sce');
```

### project.readFile(path: string): Promise\<string\>

Reads a file's contents.

```javascript
const content = await project.readFile('main.sce');
```

### project.writeFile(path: string, content: string): Promise\<void\>

Writes content to a file.

```javascript
await project.writeFile('main.sce', 'x = 1:10;');
```

### project.getSettings(): ProjectSettings

Returns project settings.

```javascript
const settings = project.getSettings();
console.log(settings.scilabVersion); // ">=7.0"
```

### project.updateSettings(settings: Partial\<ProjectSettings\>): Promise\<void\>

Updates project settings.

```javascript
await project.updateSettings({
  scilabVersion: '>=7.0',
  plugins: ['com.example.my-plugin']
});
```

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `project:created` | `{ project: Project }` | Project was created |
| `project:opened` | `{ project: Project }` | Project was opened |
| `project:saved` | `{ project: Project }` | Project was saved |
| `project:closed` | `{ project: Project }` | Project was closed |
| `project:fileCreated` | `{ file: FileNode }` | File was created |
| `project:fileDeleted` | `{ path: string }` | File was deleted |
| `project:fileRenamed` | `{ oldPath: string, newPath: string }` | File was renamed |
| `project:fileModified` | `{ path: string }` | File was modified |

## Examples

### Create Project from Template

```javascript
const project = await project.create('Signal Processing Lab', {
  template: 'edu.signal-processing',
  location: '/home/user/projects',
  variables: {
    course_name: 'Signal Processing',
    student_name: 'John Doe'
  }
});
```

### Watch for File Changes

```javascript
project.on('project:fileModified', (event) => {
  console.log(`File modified: ${event.path}`);
  // Auto-save or reload
});
```

## Errors

| Error | Code | Description |
|-------|------|-------------|
| `ProjectNotFound` | PJ-001 | Project path does not exist |
| `InvalidProject` | PJ-002 | Directory is not a valid project |
| `FileAlreadyExists` | PJ-003 | File already exists |
| `FileNotFound` | PJ-004 | File does not exist |
| `AccessDenied` | PJ-005 | No permission to access file |
| `ProjectCorrupted` | PJ-006 | project.json is invalid |

## Version

| Version | Changes |
|---------|---------|
| 1.0 | Initial API |
