# Internal APIs

Every platform service has a contract. These are the interfaces, not implementations.

## Visualization Service API

```typescript
interface VisualizationAPI {
  // Lifecycle
  initialize(): Promise<void>;
  shutdown(): Promise<void>;

  // Chart Management
  registerChartType(definition: ChartDefinition): void;
  unregisterChartType(typeId: string): void;
  getChartTypes(): ChartDefinition[];

  // Chart Operations
  create(data: DataDescriptor, options?: ChartOptions): Promise<Chart>;
  update(chartId: string, changes: Partial<Chart>): Promise<void>;
  destroy(chartId: string): void;
  get(chartId: string): Chart | null;
  getAll(): Chart[];

  // Data
  updateData(chartId: string, data: DataDescriptor): Promise<void>;

  // Export
  export(chartId: string, format: 'png' | 'svg' | 'pdf' | 'csv'): Promise<Blob>;

  // Theme
  setTheme(theme: ChartTheme): void;
}
```

## Widget Service API

```typescript
interface WidgetAPI {
  // Registration
  registerType(definition: WidgetDefinition): void;
  unregisterType(typeId: string): void;
  getType(typeId: string): WidgetDefinition | null;
  getTypes(): WidgetDefinition[];
  getTypesByCategory(category: string): WidgetDefinition[];

  // Instances
  create(typeId: string, props?: Record<string, any>): WidgetInstance;
  destroy(instanceId: string): void;
  get(instanceId: string): WidgetInstance | null;

  // Properties
  getProperty(instanceId: string, name: string): any;
  setProperty(instanceId: string, name: string, value: any): void;

  // Bindings
  bind(instanceId: string, property: string, expression: string): void;
  unbind(instanceId: string, property: string): void;

  // Serialization
  serialize(instanceId: string): WidgetJSON;
  deserialize(json: WidgetJSON): WidgetInstance;
}
```

## Plugin Service API

```typescript
interface PluginAPI {
  // Lifecycle
  install(source: string): Promise<Plugin>;
  uninstall(pluginId: string): Promise<void>;
  activate(pluginId: string): Promise<void>;
  deactivate(pluginId: string): Promise<void>;
  update(pluginId: string): Promise<Plugin>;

  // Query
  get(pluginId: string): Plugin | null;
  getAll(): Plugin[];
  getActive(): Plugin[];

  // Storage
  getStorage(pluginId: string): ScopedStorage;

  // Context
  getContext(pluginId: string): PluginContext | null;
}
```

## Data Pipeline API

```typescript
interface DataPipelineAPI {
  // Import
  importCSV(file: string, options?: CSVOptions): Promise<DataSet>;
  importExcel(file: string, options?: ExcelOptions): Promise<DataSet>;
  importSQLite(file: string, query: string): Promise<DataSet>;

  // Transform
  getTransforms(): TransformDefinition[];
  applyTransform(data: DataSet, transform: Transform): DataSet;

  // Export
  exportCSV(data: DataSet): string;
  exportJSON(data: DataSet): string;

  // Preview
  preview(file: string, options?: PreviewOptions): Promise<DataPreview>;
}
```

## Scilab Bridge API

```typescript
interface ScilabBridgeAPI {
  // Status
  getStatus(): RuntimeStatus;
  getVersion(): Promise<string>;
  ping(): Promise<boolean>;

  // Execution
  execute(code: string, options?: ExecuteOptions): Promise<ExecuteResult>;
  evaluate(expression: string): Promise<any>;

  // Variables
  getVariable(name: string): Promise<VariableValue>;
  setVariable(name: string, value: any): Promise<void>;
  listVariables(): Promise<VariableInfo[]>;

  // Control
  interrupt(): Promise<void>;
  reset(): Promise<void>;
  restart(): Promise<void>;
}
```

## Report Service API

```typescript
interface ReportAPI {
  // Document
  createDocument(title: string): ReportDocument;
  getDocument(docId: string): ReportDocument | null;

  // Blocks
  addBlock(docId: string, block: ReportBlock): void;
  removeBlock(docId: string, blockId: string): void;
  moveBlock(docId: string, blockId: string, position: number): void;

  // Content
  updateBlock(docId: string, blockId: string, content: any): void;

  // Export
  exportPDF(docId: string): Promise<Blob>;
  exportHTML(docId: string): Promise<string>;
  exportLatex(docId: string): Promise<string>;
}
```

## Storage API

```typescript
interface StorageAPI {
  // Key-Value
  get<T>(key: string): Promise<T | undefined>;
  set<T>(key: string, value: T): Promise<void>;
  delete(key: string): Promise<void>;
  has(key: string): Promise<boolean>;
  keys(pattern?: string): Promise<string[]>;

  // Scoped
  getPluginStorage(pluginId: string): ScopedStorage;
  getProjectStorage(projectId: string): ScopedStorage;

  // File System
  readFile(path: string): Promise<Buffer>;
  writeFile(path: string, data: Buffer): Promise<void>;
  watch(path: string, handler: FileChangeHandler): Disposable;
}
```

## Rules

- All APIs are versioned.
- Breaking changes require major version bump.
- Deprecated methods are removed after 2 major versions.
- All methods have TypeScript types.
- All methods have JSDoc documentation.
- All methods have error documentation.
