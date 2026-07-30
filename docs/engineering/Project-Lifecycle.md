# Project Lifecycle

## Overview

Every Scilab Studio project follows this lifecycle. Every feature should support this lifecycle.

## Lifecycle Stages

```
Create → Configure → Develop → Test → Run → Analyze → Export → Archive
```

### 1. Create

```typescript
interface CreateStage {
  fromTemplate(templateId: string, variables: Record<string, any>): Project;
  fromScratch(name: string): Project;
}
```

- User selects template or starts blank.
- Project directory is created.
- `project.json` is initialized.
- Template files are copied.

### 2. Configure

```typescript
interface ConfigureStage {
  setScilabVersion(version: string): void;
  addPlugin(pluginId: string): void;
  setSettings(settings: Record<string, any>): void;
}
```

- Scilab version is specified.
- Required plugins are added.
- Project settings are configured.

### 3. Develop

```typescript
interface DevelopStage {
  editCode(file: string): void;
  buildGUI(layout: WidgetInstance[]): void;
  importData(file: string): DataSet;
  writeScript(code: string): void;
}
```

- Code is written in the editor.
- GUIs are built with the GUI Builder.
- Data is imported with Data Studio.
- Scripts are developed iteratively.

### 4. Test

```typescript
interface TestStage {
  runScript(file: string): ExecuteResult;
  testGUI(guiId: string): void;
  validateData(dataSet: DataSet): ValidationResult;
}
```

- Scripts are executed in Scilab.
- GUIs are tested in preview mode.
- Data is validated.

### 5. Run

```typescript
interface RunStage {
  execute(file: string): Promise<ExecuteResult>;
  runAll(): Promise<ExecuteResult[]>;
  debug(file: string): void;
}
```

- Scripts are executed.
- Results are displayed.
- Errors are debugged.

### 6. Analyze

```typescript
interface AnalyzeStage {
  visualize(data: DataSet, chartType: string): Chart;
  inspect(data: DataSet): DataPreview;
  compare(results: ExecuteResult[]): ComparisonResult;
}
```

- Data is visualized.
- Results are inspected.
- Comparisons are made.

### 7. Export

```typescript
interface ExportStage {
  exportReport(format: 'pdf' | 'html'): Promise<Blob>;
  exportData(format: 'csv' | 'json'): string;
  exportChart(format: 'png' | 'svg'): Promise<Blob>;
  exportCode(): string;
}
```

- Reports are generated.
- Data is exported.
- Charts are exported.
- Code is exported.

### 8. Archive

```typescript
interface ArchiveStage {
  saveProject(): void;
  versionProject(): void;
  shareProject(): void;
}
```

- Project is saved.
- Version is tagged.
- Project is shared (optional).

## Feature Support Matrix

| Feature | Create | Configure | Develop | Test | Run | Analyze | Export | Archive |
|---------|--------|-----------|---------|------|-----|---------|--------|---------|
| Workspace | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GUI Builder | ✅ | | ✅ | ✅ | ✅ | | | ✅ |
| Visualization | | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data Studio | | | ✅ | ✅ | | ✅ | ✅ | ✅ |
| Report Gen | | | ✅ | ✅ | | | ✅ | ✅ |
| Templates | ✅ | ✅ | | | | | | |
| Scilab Bridge | | ✅ | ✅ | ✅ | ✅ | | | |

## Rules

- Every feature should fit into at least one lifecycle stage.
- Data flows forward through the lifecycle.
- Users can move backward (undo, re-run).
- State is preserved between stages.
- The lifecycle is non-destructive (no data loss).
