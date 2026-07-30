# SPEC-007 — Data Studio

## Purpose

Import, validate, transform, analyze, and export tabular datasets. Every dataset follows the same pipeline: Import → Validation → Cleaning → Transformation → Analysis → Visualization → Export.

---

## Supported Sources

| Source | Extension | Method | Notes |
|--------|-----------|--------|-------|
| CSV | .csv, .tsv | Built-in | Auto-detect delimiter and encoding |
| Excel | .xlsx, .xls | Built-in | All sheets accessible |
| SQLite | .db, .sqlite | Built-in | Query by table or SQL |
| PostgreSQL | — | Optional | Connection string required |
| JSON | .json | Built-in | Flat and nested |
| Scilab Data | .sod, .sav | Via engine | Binary format |
| Sensor Logs | .log | Custom parsers | Configurable column mapping |

---

## Import Pipeline

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

---

## Data Model

```typescript
interface Dataset {
  id: string;
  name: string;
  source: string;
  columns: ColumnDef[];
  rows: DataRow[];
  metadata: DatasetMetadata;
}

interface ColumnDef {
  name: string;
  type: "string" | "number" | "boolean" | "date" | "datetime";
  nullable: boolean;
  unit?: string;
  statistics?: ColumnStatistics;
}

type DataRow = (string | number | boolean | null)[];
```

---

## Validation

After import, every dataset is validated:

| Check | Description |
|-------|-------------|
| Type consistency | Each column has a consistent type |
| Null handling | Null counts computed |
| Range check | Numeric values within expected ranges |
| Uniqueness | Duplicate detection (optional) |

Validation errors are warnings, not failures. The dataset is still importable.

---

## Cleaning Operations

| Operation | Description |
|-----------|-------------|
| dropna | Remove rows with null values |
| fillna | Replace nulls (mean, median, constant, forward-fill) |
| deduplicate | Remove duplicate rows |
| cast | Convert column type |
| trim | Remove whitespace from strings |
| replace | Find and replace values |

---

## Transform Pipeline

A pipeline is an ordered sequence of operations:

| Transform | Parameters | Description |
|-----------|-----------|-------------|
| filter | column, operator, value | Keep matching rows |
| sort | column, direction | Sort by column |
| select | columns | Keep specified columns |
| rename | mapping | Rename columns |
| dropna | columns, how | Remove null rows |
| fillna | column, value | Fill nulls |
| deduplicate | columns, keep | Remove duplicates |
| cast | column, type | Convert type |
| aggregate | groupBy, aggregations | Group and aggregate |
| limit | count | Keep first N rows |
| offset | count | Skip first N rows |
| pivot | index, columns, values | Wide to long |
| unpivot | idColumns, valueName, varName | Long to wide |
| merge | rightDataset, on, how | Join datasets |
| derive | name, expression | Create computed column |

### Filter Operators

eq, neq, gt, gte, lt, lte, contains, startswith, endswith, in, between, isnull, notnull.

### Aggregate Functions

count, sum, mean, median, min, max, std, var, first, last, nunique.

---

## Analysis

### Column Statistics
Computed automatically on import:
- Numeric: count, nulls, min, max, mean, median, std dev, quartiles.
- String: count, nulls, unique count, most common values, avg length.
- Boolean: true count, false count, null count.

### Correlation
Pairwise Pearson correlation between numeric columns.

### Summary
Dataset summary: rows, columns, memory estimate, null percentage, duplicate rows.

---

## Scilab Integration

### Import from Scilab
Pull variable as dataset: `dataStudio.fromScilabVariable("measurements", { columns: [...] })`.

### Export to Scilab
Push dataset as matrix: `engine.setVariable("measurements", { type: "matrix", value: dataset.rows })`.

### Bidirectional Sync
Bound datasets update when Scilab variables change (configurable frequency).

---

## Export

| Format | Extension | Options |
|--------|-----------|---------|
| CSV | .csv | delimiter, encoding, includeHeader |
| Excel | .xlsx | sheetName |
| JSON | .json | indent, arrayFormat |
| Scilab | Via engine | Variable name |

---

## UI

### Data Preview
- Spreadsheet-style grid with frozen header row.
- Virtual scrolling for large datasets.
- Column sorting (click header).
- Column type indicators.
- Search/filter bar.
- Row and column count in footer.

### Transform Pipeline Editor
- Steps added from dropdown.
- Reorderable via drag-and-drop.
- Each step has inline configuration.
- Preview output updates as steps change.
- Enable/disable individual steps.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max preview rows | 1,000 |
| Max import size (streaming) | 100MB+ (chunked processing) |
| Transform pipeline max steps | 50 |
| Statistics computation | Background thread |
| Sidecar metadata max column stats | 100 columns |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| File not found | Show error, remove from recents |
| Unsupported format | Show "Format not supported" message |
| Encoding detection fails | Prompt user to select encoding |
| Parse error (malformed CSV) | Show row/column of error, offer skip |
| Disk full on export | Show error, offer different location |
| Scilab variable not found | Show "Variable not available" in binding UI |

---

## Extension Points

- Custom data source connectors.
- Custom transform operations.
- Custom export formats.
- Custom validation rules.
- Custom statistics functions.
