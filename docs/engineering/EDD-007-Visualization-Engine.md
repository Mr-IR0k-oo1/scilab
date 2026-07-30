# EDD-007: Visualization Engine

## Purpose

The Visualization Engine renders engineering charts, handles interactions, and exports to multiple formats.

## Architecture

```
┌─────────────────────────────────────────┐
│        Visualization Engine              │
├─────────────────────────────────────────┤
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Chart     │  │ Renderer         │   │
│  │ Registry  │  │ Pipeline         │   │
│  └───────────┘  └──────────────────┘   │
│  ┌───────────┐  ┌──────────────────┐   │
│  │ Data      │  │ Export           │   │
│  │ Pipeline  │  │ Engine           │   │
│  └───────────┘  └──────────────────┘   │
│  ┌──────────────────────────────────┐  │
│  │ Interaction Handler              │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Chart Registry

```typescript
interface ChartRegistry {
  register(definition: ChartDefinition): void;
  get(type: string): ChartDefinition | null;
  getAll(): ChartDefinition[];
}
```

**Built-in Charts:**
- Line, Scatter, Bar, Heatmap (v0.1)
- Surface, Histogram, Pie, Bode, Nyquist, Root Locus (v0.2)
- Polar, Contour, Quiver, Stem, Box (v0.3)

## Renderer Pipeline

```
Data Source → Expression Eval → Transform → Render → Canvas Output
```

### Step 1: Data Source
```typescript
interface DataDescriptor {
  source: 'scilab' | 'inline' | 'file';
  expression?: string;
  columns?: ColumnDescriptor[];
}
```

### Step 2: Expression Evaluation
Scilab expressions evaluated asynchronously.

### Step 3: Data Transform
Normalize, filter, aggregate, downsample.

### Step 4: Render
Canvas 2D or WebGL rendering.

### Step 5: Canvas Output
Display on screen or export to file.

## Chart Instance

```typescript
interface ChartInstance {
  readonly id: string;
  readonly type: string;
  canvas: HTMLCanvasElement;
  data: DataDescriptor;
  options: ChartOptions;
  state: ChartState;
}
```

## Interaction Handler

```typescript
interface InteractionHandler {
  handleHover(point: Point): TooltipData | null;
  handleClick(point: Point): SelectionData | null;
  handleZoom(delta: number, center: Point): void;
  handlePan(delta: Point): void;
  handleBrush(rect: Rect): SelectionData | null;
}
```

## Export Engine

```typescript
interface ExportEngine {
  toPNG(chart: ChartInstance, options: ExportOptions): Promise<Blob>;
  toSVG(chart: ChartInstance, options: ExportOptions): Promise<string>;
  toPDF(chart: ChartInstance, options: ExportOptions): Promise<Blob>;
  toCSV(data: DataColumn[]): string;
  toJSON(data: DataColumn[]): string;
}
```

## Theme Integration

Charts inherit the application theme:

```typescript
function getChartTheme(appTheme: Theme): ChartTheme {
  return {
    background: 'transparent',
    text: appTheme.colors.text.primary,
    grid: appTheme.colors.border,
    colors: appTheme.chart.colors,
    fonts: appTheme.typography
  };
}
```

## Progressive Rendering

For large datasets (>10k points):

1. Render downsampled version immediately.
2. Full resolution renders in background.
3. Switch when ready.
4. Show loading indicator during full render.

## Error Handling

- Invalid data: show error state on chart.
- Scilab evaluation failure: show "Data unavailable".
- Render failure: show placeholder.
- Export failure: log, show error.

## Performance

| Dataset | Render Target |
|---------|--------------|
| 1k points | < 16ms (60 FPS) |
| 10k points | < 100ms |
| 100k points | < 500ms |
| 1M points | < 2s (progressive) |

## Memory

- Chart instance: < 5MB.
- 100k points: < 50MB.
- WebGL context: < 100MB.
