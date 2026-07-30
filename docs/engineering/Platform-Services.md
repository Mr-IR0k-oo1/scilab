# Platform Services

## Service Architecture

Scilab Studio is organized as a set of platform services. Applications consume these services. Services never depend on applications.

```
                Scilab Studio

┌────────────────────────────────────────┐
│ Applications                           │
│  • Lab Creator                         │
│  • Dashboard Builder                   │
│  • Report Studio                       │
└────────────────────────────────────────┘
                 ▲
┌────────────────────────────────────────┐
│ Platform Services                      │
│  • Visualization Engine                │
│  • Widget Framework                    │
│  • Plugin Runtime                      │
│  • Data Pipeline                       │
│  • Scilab Bridge                       │
│  • Report Generator                    │
│  • Theme Service                       │
│  • AI Service (v0.3)                   │
└────────────────────────────────────────┘
                 ▲
┌────────────────────────────────────────┐
│ Core Runtime                           │
│  • Event Bus                           │
│  • Workspace Manager                   │
│  • Project System                      │
│  • Configuration                       │
│  • Logging                             │
│  • Storage                             │
│  • Command System                      │
└────────────────────────────────────────┘
```

## Service Definitions

### Visualization Service

```typescript
interface VisualizationService {
  createChart(type: string, data: DataDescriptor, options?: ChartOptions): Promise<Chart>;
  updateChart(chartId: string, options: Partial<ChartOptions>): Promise<void>;
  destroyChart(chartId: string): void;
  exportChart(chartId: string, options: ExportOptions): Promise<Blob>;
}
```

### Widget Service

```typescript
interface WidgetService {
  registerType(definition: WidgetDefinition): void;
  createInstance(type: string, props?: object): WidgetInstance;
  destroyInstance(instanceId: string): void;
  getProperty(instanceId: string, name: string): any;
  setProperty(instanceId: string, name: string, value: any): void;
}
```

### Plugin Service

```typescript
interface PluginService {
  install(source: string): Promise<Plugin>;
  uninstall(pluginId: string): Promise<void>;
  activate(pluginId: string): Promise<void>;
  deactivate(pluginId: string): Promise<void>;
  getAll(): Plugin[];
}
```

### Data Pipeline Service

```typescript
interface DataPipelineService {
  import(file: string, options?: ImportOptions): Promise<DataSet>;
  transform(data: DataSet, pipeline: Transform[]): DataSet;
  export(data: DataSet, options: ExportOptions): Promise<void>;
  getTransforms(): TransformDefinition[];
}
```

### Scilab Bridge Service

```typescript
interface ScilabBridgeService {
  execute(code: string): Promise<ExecuteResult>;
  evaluate(expression: string): Promise<any>;
  getVariable(name: string): Promise<VariableValue>;
  setVariable(name: string, value: any): Promise<void>;
  listVariables(): Promise<VariableInfo[]>;
  interrupt(): Promise<void>;
  reset(): Promise<void>;
  ping(): Promise<boolean>;
}
```

### Report Service

```typescript
interface ReportService {
  createDocument(): ReportDocument;
  addBlock(doc: ReportDocument, block: ReportBlock): void;
  removeBlock(doc: ReportDocument, blockId: string): void;
  export(doc: ReportDocument, format: 'pdf' | 'html' | 'latex'): Promise<Blob>;
}
```

### Theme Service

```typescript
interface ThemeService {
  getTheme(): Theme;
  setTheme(themeId: string): void;
  getAvailable(): ThemeDescriptor[];
  registerTheme(theme: Theme): void;
}
```

### Storage Service

```typescript
interface StorageService {
  get<T>(key: string, scope?: StorageScope): Promise<T | undefined>;
  set<T>(key: string, value: T, scope?: StorageScope): Promise<void>;
  delete(key: string, scope?: StorageScope): Promise<void>;
}
```

## Service Registration

Services are registered with the Core Runtime:

```typescript
coreRuntime.registerService('visualization', new VisualizationServiceImpl());
coreRuntime.registerService('widget', new WidgetServiceImpl());
coreRuntime.registerService('plugin', new PluginServiceImpl());
```

## Service Discovery

```typescript
const vizService = coreRuntime.getService<VisualizationService>('visualization');
await vizService.createChart('line', data);
```

## Service Lifecycle

```
Registration → Initialization → Running → Shutdown
```

- Services are initialized in dependency order.
- Services are shut down in reverse order.
- Service errors are isolated and logged.
