# 27 — Data Pipeline

Every dataset follows the same flow:

```
Import
  │
  ▼
Validation
  │
  ▼
Cleaning
  │
  ▼
Transformation
  │
  ▼
Analysis
  │
  ▼
Visualization
  │
  ▼
Export
```

For the Data Studio feature, see [Feature Modules §2.4](05_Feature_Modules.md). For the Scilab integration, see [28 — Scilab Runtime](28_Scilab_Runtime.md).

---

## 1. Data Model

```typescript
interface Dataset {
  id: string;
  name: string;
  source: string;                  // Origin file or Scilab variable
  columns: ColumnDef[];
  rows: DataRow[];
  metadata: DatasetMetadata;
  createdAt: number;
  updatedAt: number;
}

interface ColumnDef {
  name: string;
  type: "string" | "number" | "boolean" | "date" | "datetime";
  nullable: boolean;
  unit?: string;
  description?: string;
  statistics?: ColumnStatistics;
}

interface ColumnStatistics {
  count: number;
  nullCount: number;
  min?: number;
  max?: number;
  mean?: number;
  median?: number;
  stdDev?: number;
  uniqueCount?: number;
}

type DataRow = (string | number | boolean | null)[];

interface DatasetMetadata {
  format: "csv" | "xlsx" | "json" | "scilab" | "sqlite" | "postgresql";
  encoding?: string;
  delimiter?: string;
  sourceSize?: number;
  hash?: string;
  importedAt?: string;
}
```

---

## 2. Supported Sources

| Source | Extension | Method | Notes |
|--------|-----------|--------|-------|
| CSV | `.csv`, `.tsv` | Built-in (Rust `csv` crate) | Auto-detect delimiter and encoding |
| Excel | `.xlsx`, `.xls` | Built-in (Rust `calamine` crate) | All sheets accessible |
| SQLite | `.db`, `.sqlite` | Built-in (Rust `rusqlite` crate) | Query by table or SQL |
| PostgreSQL | — | Via `sqlx` (optional) | Connection string required |
| JSON | `.json` | Built-in (Rust `serde_json`) | Flat and nested structures |
| Scilab Data | `.sod`, `.sav` | Via Scilab engine | Binary format |
| Sensor Logs | `.log`, `.csv` | Custom parsers | Configurable column mapping |

---

## 3. Import Pipeline

### 3.1 Flow

```
User selects file
  │
  ▼
Format Detection (extension + content sniffing)
  │
  ▼
Parse (format-specific parser)
  │
  ▼
Validate (types, nulls, ranges)
  │
  ▼
Generate Metadata (column types, statistics, hash)
  │
  ▼
Store (in-memory + sidecar .meta.json)
  │
  ▼
Emit data:imported
```

### 3.2 CSV Import Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `delimiter` | string | auto | Column separator |
| `encoding` | string | auto | File encoding |
| `hasHeader` | boolean | `true` | First row is column names |
| `skipRows` | number | `0` | Rows to skip |
| `maxRows` | number | unlimited | Maximum rows to import |
| `columnTypes` | string[] | auto | Force column types |
| `nullValues` | string[] | `["", "NA", "N/A", "null", "None"]` | Null representations |
| `dateFormats` | string[] | `["YYYY-MM-DD", "MM/DD/YYYY"]` | Date parsing |

### 3.3 Import Result

```typescript
interface ImportResult {
  dataset: Dataset;
  warnings: ImportWarning[];
  stats: {
    totalRows: number;
    importedRows: number;
    totalColumns: number;
    skippedRows: number;
    duration: number;               // ms
  };
}

interface ImportWarning {
  row: number;
  column: string;
  message: string;
  value: string;
}
```

### 3.4 Streaming Import

For files > 100MB:
- Parse 10,000 rows at a time.
- Validate and transform each chunk.
- Append to storage buffer.
- Update progress indicator.
- Emit `data:import:progress` events.

---

## 4. Validation

After import, every dataset is validated:

| Check | Description |
|-------|-------------|
| Type consistency | Each column has a consistent type |
| Null handling | Null counts are computed |
| Range check | Numeric values within expected ranges |
| Uniqueness | Duplicate detection (optional) |
| Schema match | If a schema is provided, validate against it |

Validation errors are reported as warnings, not failures. The dataset is still importable.

---

## 5. Cleaning

Common cleaning operations:

| Operation | Description |
|-----------|-------------|
| `dropna` | Remove rows with null values |
| `fillna` | Replace nulls with a value (mean, median, constant, forward-fill) |
| `deduplicate` | Remove duplicate rows |
| `cast` | Convert column type (e.g., string → number) |
| `trim` | Remove leading/trailing whitespace from strings |
| `replace` | Find and replace values |

Cleaning operations are applied as pipeline steps (see §6).

---

## 6. Transformation Pipeline

A pipeline is an ordered sequence of operations:

```typescript
interface TransformPipeline {
  id: string;
  name: string;
  sourceDatasetId: string;
  steps: TransformStep[];
}

interface TransformStep {
  id: string;
  type: string;
  params: Record<string, any>;
  enabled: boolean;
}
```

### 6.1 Available Transforms

| Transform | Parameters | Description |
|-----------|-----------|-------------|
| `filter` | `{ column, operator, value }` | Keep matching rows |
| `sort` | `{ column, direction }` | Sort by column |
| `select` | `{ columns }` | Keep specified columns |
| `rename` | `{ mapping }` | Rename columns |
| `dropna` | `{ columns?, how }` | Remove null rows |
| `fillna` | `{ column, value }` | Fill nulls |
| `deduplicate` | `{ columns?, keep }` | Remove duplicates |
| `cast` | `{ column, type }` | Convert type |
| `aggregate` | `{ groupBy, aggregations }` | Group and aggregate |
| `limit` | `{ count }` | Keep first N rows |
| `offset` | `{ count }` | Skip first N rows |
| `pivot` | `{ index, columns, values }` | Wide to long |
| `unpivot` | `{ idColumns, valueName, varName }` | Long to wide |
| `merge` | `{ rightDataset, on, how }` | Join datasets |
| `derive` | `{ name, expression }` | Create computed column |

### 6.2 Filter Operators

| Operator | Description |
|----------|-------------|
| `eq`, `neq` | Equal / not equal |
| `gt`, `gte` | Greater than / >= |
| `lt`, `lte` | Less than / <= |
| `contains` | String contains |
| `startswith`, `endswith` | String prefix/suffix |
| `in` | Value in list |
| `between` | Value in range |
| `isnull`, `notnull` | Null checks |

### 6.3 Aggregate Functions

`count`, `sum`, `mean`, `median`, `min`, `max`, `std`, `var`, `first`, `last`, `nunique`.

---

## 7. Analysis

### 7.1 Column Statistics

Computed automatically on import and cached in `.meta.json`:

| Type | Statistics |
|------|-----------|
| Numeric | count, nulls, min, max, mean, median, std dev, quartiles |
| String | count, nulls, unique count, most common values, avg length |
| Boolean | true count, false count, null count |

### 7.2 Correlation

Compute pairwise correlation between numeric columns:

```typescript
interface CorrelationResult {
  columns: string[];
  matrix: number[][];              // Pearson correlation coefficients
}
```

### 7.3 Summary

Generate a dataset summary:

```typescript
interface DatasetSummary {
  rows: number;
  columns: number;
  memoryEstimate: number;          // bytes
  nullPercentage: number;
  duplicateRows: number;
  columnStats: ColumnStatistics[];
}
```

---

## 8. Scilab Integration

### Import from Scilab

```typescript
// Pull variable as dataset
const dataset = await dataStudio.fromScilabVariable("measurements", {
  columns: ["time", "voltage", "current"]
});
```

### Export to Scilab

```typescript
// Push dataset as Scilab matrix
await engine.setVariable("measurements", {
  type: "matrix",
  value: dataset.rows
});
```

### Bidirectional Sync

When a dataset is bound to a Scilab variable:
- Variable changes update the dataset (configurable frequency).
- Dataset changes update the variable (on save or explicit sync).

---

## 9. Export

| Format | Extension | Options |
|--------|-----------|---------|
| CSV | `.csv` | delimiter, encoding, includeHeader |
| Excel | `.xlsx` | sheetName |
| JSON | `.json` | indent, arrayFormat |
| Scilab | Via engine | Variable name |

---

## 10. Performance

| Feature | Strategy |
|---------|----------|
| Large datasets (>10MB) | Memory-mapped files, virtual scrolling |
| Streaming import | 10,000-row chunks, progress events |
| Statistics | Background thread computation |
| Transform pipelines | Lazy evaluation (only visible subset computed) |
| Parallel operations | Independent transform steps run concurrently |
