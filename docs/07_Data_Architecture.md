# Data Architecture

## Overview

The Data Architecture module provides the infrastructure for importing, managing, processing, and accessing data across the entire Scilab Studio platform. It serves as the central data layer that all other modules — Parameter Sweep Studio, Visualization Studio, Report Generator, Lab Creator, and the AI Assistant — rely on for consistent, reliable data access.

Engineering workflows are inherently data-intensive. A single experiment might involve sensor readings, reference datasets, configuration parameters, and output results in half a dozen different formats. The Data Architecture module eliminates the friction of format conversion, data cleaning, and data management so that engineers and students can focus on analysis rather than plumbing.

---

## Data Layer Architecture

The data layer follows a three-tier architecture:

```
┌──────────────────────────────────────────────────────┐
│                  Application Layer                    │
│  (Parameter Sweep, Visualization, Report Gen, etc.)  │
├──────────────────────────────────────────────────────┤
│                    Query API Layer                    │
│         (Unified data access, filtering, joins)       │
├──────────────────────────────────────────────────────┤
│                  Processing Layer                     │
│  (Parsers, Validators, Transformers, Preprocessors)  │
├──────────────────────────────────────────────────────┤
│                   Connector Layer                     │
│   (CSV, Excel, SQLite, PostgreSQL, MAT, IoT, etc.)   │
├──────────────────────────────────────────────────────┤
│                   Storage Layer                       │
│     (Project data store, versioning, metadata)        │
└──────────────────────────────────────────────────────┘
```

### Connectors

Connectors are adapter components that know how to read from and write to specific data sources. Each connector implements a standard interface:

```
DataConnector {
    identify(source) -> FormatInfo
    read(source, options) -> RawData
    write(data, destination, options) -> bool
    supports_streaming() -> bool
    validate(source) -> ValidationResult
}
```

### Processors

Processors transform raw data into clean, normalized form. They operate on a data pipeline model:

```
RawData → Parser → Validator → Transformer → Preprocessor → CleanData
```

### Storage

The storage layer manages project-scoped data persistence with versioning, metadata indexing, and access control.

---

## Supported Formats

### Tabular Data

| Format | Extension(s) | Read | Write | Notes |
|---|---|---|---|---|
| CSV | `.csv` | Yes | Yes | Auto-detect delimiter, encoding |
| Excel | `.xls`, `.xlsx` | Yes | Yes | Multiple sheets, formula evaluation |
| TSV | `.tsv` | Yes | Yes | Tab-separated variant |
| Parquet | `.parquet` | Yes | Yes | Columnar, compressed |
| JSON Lines | `.jsonl` | Yes | Yes | One JSON object per line |
| Fixed-width | `.fw` | Yes | No | Column positions defined in config |

### Database Formats

| Format | Read | Write | Notes |
|---|---|---|---|
| SQLite | Yes | Yes | Embedded, file-based |
| PostgreSQL | Yes | Yes | Requires connection config |
| MySQL | Yes | Yes | Requires connection config |
| In-memory (Scilab) | Yes | Yes | Native Scilab matrices |

### Scientific Formats

| Format | Extension(s) | Read | Write | Notes |
|---|---|---|---|---|
| MAT file | `.mat` | Yes | Yes | MATLAB compatibility layer |
| HDF5 | `.h5`, `.hdf5` | Yes | Yes | Hierarchical, large datasets |
| NetCDF | `.nc` | Yes | No | Climate and geoscience data |
| FITS | `.fits` | Yes | No | Astronomy data |

### Domain-Specific Formats

| Format | Description | Read | Write |
|---|---|---|---|
| Sensor logs | Timestamped sensor readings (CSV variant with metadata header) | Yes | Yes |
| Weather data | NOAA, WMO formatted datasets | Yes | No |
| Energy data | Smart meter, SCADA export formats | Yes | No |
| IoT streams | MQTT payloads, JSON sensor telemetry | Yes | Yes |
| Image stacks | Directory of numbered images or multi-page TIFF | Yes | Yes |
| Audio | WAV, raw PCM | Yes | Yes |

### Automatic Format Detection

When a user drags a file into the project, the system:

1. Inspects the file extension.
2. Reads the first 8KB of content.
3. Applies heuristic detection (delimiter inference, encoding detection, header pattern matching).
4. Presents the detected format with confidence score.
5. If confidence is below threshold, asks the user to confirm.

---

## Connector Architecture

Adding a new data format to the system requires implementing the `DataConnector` interface and registering it with the connector registry.

### Adding a New Connector

1. Create a new class implementing the `DataConnector` interface.
2. Define the format detection heuristics in the `identify` method.
3. Implement `read` to parse the format into the internal `RawData` representation.
4. Implement `write` to serialize from internal representation to the target format.
5. Register the connector in `connectors/registry.yaml`:

```yaml
- id: custom_sensor_format
  class: CustomSensorConnector
  extensions: [".csf", ".csl"]
  mime_types: ["application/x-custom-sensor"]
  priority: 10  # lower = higher priority for ambiguous files
  dependencies: []
```

6. Add format-specific validation rules in `connectors/validators/custom_sensor.yaml`.
7. Write tests in `tests/connectors/test_custom_sensor.py`.

### Connector Lifecycle

```
User drops file
       │
       ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Registry    │ ──→ │  Connector   │ ──→ │  RawData    │
│  Lookup      │     │  Selection   │     │  Object     │
└─────────────┘     └──────────────┘     └─────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  Best match         invoke read()         passed to
  selected           on selected           processing
                     connector             pipeline
```

### Connector Testing

Each connector ships with a test suite:

- **Unit tests.** Verify parsing of well-formed input files.
- **Edge cases.** Empty files, files with BOM, mixed line endings, Unicode content.
- **Round-trip tests.** Read → Write → Read and compare.
- **Performance tests.** Benchmark read/write speed against expected thresholds.
- **Corruption tests.** Truncated files, invalid characters, wrong format claims.

---

## Data Import Pipeline

The import pipeline is a five-stage process:

```
Parse → Validate → Transform → Enrich → Store
```

### Stage 1 — Parse

The parser reads raw bytes from the source and produces an intermediate columnar representation:

- Column names are extracted from headers (or generated as `col_0`, `col_1`, ...).
- Data types are inferred per-column (integer, float, string, datetime, boolean).
- Encodings are normalized to UTF-8.
- Line endings are normalized.

### Stage 2 — Validate

The validator checks the parsed data against a schema:

- **Type conformance.** Are all values in a column of the declared type?
- **Range checks.** Are numeric values within expected bounds?
- **Uniqueness.** Are primary key columns unique?
- **Completeness.** Are required columns present?
- **Referential integrity.** Do foreign key columns reference valid values?

Validation produces a report:

```yaml
valid: false
errors:
  - column: temperature
    row: 1423
    expected: float
    actual: "N/A"
    severity: warning
  - column: timestamp
    row: 567
    expected: datetime
    actual: "2024-13-45"
    severity: error
warnings:
  - column: pressure
    message: "12% of values are below expected range"
    severity: info
summary:
  total_rows: 10000
  error_count: 1
  warning_count: 3
  info_count: 1
```

### Stage 3 — Transform

The transformer applies format-specific and user-configured transformations:

- Rename columns.
- Reorder columns.
- Merge or split columns.
- Apply unit conversions (e.g., °C to K, psi to Pa).
- Parse composite fields (e.g., split "MM/DD/YYYY" into year, month, day).
- Pivot or unpivot tables.

### Stage 4 — Enrich

The enricher adds computed columns:

- Timestamps → derived columns (hour, day_of_week, is_weekend).
- Numeric → binned categories.
- Coordinates → distance calculations.
- Text → token counts, sentiment scores (if AI module is available).

### Stage 5 — Store

The enriched data is persisted to the project's data store:

- Stored in a normalized internal format (columnar, compressed).
- Metadata is indexed (column names, types, statistics, provenance).
- Original source file is preserved for provenance tracking.
- A data catalog entry is created.

---

## Automatic Preprocessing

When data is imported, the system applies automatic preprocessing to handle common data quality issues:

### Missing Values

| Strategy | Description | Default? |
|---|---|---|
| `drop_rows` | Remove rows with any missing value | No |
| `drop_columns` | Remove columns with >50% missing values | No |
| `fill_mean` | Replace with column mean | Yes (numeric) |
| `fill_median` | Replace with column median | No |
| `fill_mode` | Replace with most frequent value | Yes (categorical) |
| `fill_forward` | Carry last valid value forward | No |
| `fill_interpolate` | Linear interpolation | No |
| `fill_constant` | Replace with user-specified value | No |

The default strategy is configurable per project and per column.

### Type Detection and Coercion

The type inference engine examines each column and suggests the most appropriate type:

1. Try integer parsing.
2. Try float parsing.
3. Try datetime parsing (with multiple format candidates).
4. Try boolean parsing (true/false, yes/no, 1/0).
5. Fall back to string.

If a column contains mostly one type with some exceptions, the system flags the exceptions as type mismatches and suggests:

- Correcting the values.
- Keeping the column as string.
- Splitting into two columns.

### Normalization

For numeric columns, the system optionally computes and stores:

- Min-max normalized values (scaled to [0, 1]).
- Z-score normalized values (mean 0, std 1).
- Log-transformed values (for right-skewed distributions).
- Rank-transformed values.

Normalization is not applied by default — it is offered as a one-click option during import.

### Outlier Handling

Outlier detection is performed using:

| Method | Description | When to use |
|---|---|---|
| IQR | Values beyond 1.5× IQR from Q1/Q3 | General purpose |
| Z-score | Values beyond 3 standard deviations | Normal distributions |
| Modified Z-score | Uses median absolute deviation | Robust to skewness |
| Grubbs' test | Statistical test for single outlier | Small samples |
| DBSCAN | Density-based clustering | Multi-dimensional data |

Detected outliers are flagged but not removed by default. The user can choose to:

- Keep outliers.
- Cap outliers at the boundary.
- Replace with column mean/median.
- Remove outlier rows.
- Mark outliers as a separate category.

---

## Data Store

### Project-Level Data Management

Each Scilab Studio project has an isolated data store:

```
project_root/
├── data/
│   ├── catalog.yaml          # Index of all datasets
│   ├── raw/                  # Original imported files
│   │   ├── sensor_log_2024.csv
│   │   └── weather_jan.json
│   ├── processed/            # Cleaned, normalized versions
│   │   ├── sensor_log_2024.parquet
│   │   └── weather_jan.parquet
│   ├── metadata/             # Per-dataset metadata
│   │   ├── sensor_log_2024.yaml
│   │   └── weather_jan.yaml
│   └── cache/                # Computation caches
│       └── sweep_results/
```

### Versioning

Every dataset modification creates a new version:

```yaml
dataset: sensor_log_2024
versions:
  - version: 1
    created: 2024-01-15T10:30:00Z
    source: raw/sensor_log_2024.csv
    hash: sha256:abc123...
    rows: 50000
    columns: 12
    operation: initial_import
  - version: 2
    created: 2024-01-15T11:00:00Z
    parent: 1
    operation: remove_nulls
    changes:
      - column: temperature
        action: fill_mean
        affected_rows: 234
  - version: 3
    created: 2024-01-15T14:00:00Z
    parent: 2
    operation: add_column
    changes:
      - column: temperature_k
        action: derived
        formula: "temperature + 273.15"
```

Versions can be compared, diffed, and rolled back. The system stores only deltas after the initial version to minimize storage overhead.

### Metadata Index

Every dataset in the catalog has rich metadata:

```yaml
id: ds_sensor_log_2024
name: "Temperature Sensor Log — Jan 2024"
source: /data/raw/sensor_log_2024.csv
format: csv
size_bytes: 2456789
row_count: 50000
column_count: 12
columns:
  - name: timestamp
    type: datetime
    format: "%Y-%m-%dT%H:%M:%SZ"
    nullable: false
  - name: temperature
    type: float
    min: -15.3
    max: 42.7
    mean: 21.4
    nullable: true
    null_count: 234
  - name: humidity
    type: float
    min: 5.0
    max: 100.0
    nullable: false
tags: [sensor, temperature, indoor, lab-experiment-3]
provenance:
  author: "Dr. Smith"
  created: 2024-01-15
  source_device: "DHT22 sensor array"
  license: "CC-BY-4.0"
```

---

## Data Query API

All modules access data through a unified Query API. The API provides:

### Basic Selection

```python
# Select columns
data = query.select("sensor_log", columns=["timestamp", "temperature"])

# Filter rows
data = query.select("sensor_log", 
    filters={"temperature": {">": 30.0}},
    columns=["timestamp", "temperature", "humidity"]
)

# Aggregate
data = query.aggregate("sensor_log",
    group_by="hour",
    aggregations={"temperature": ["mean", "std", "min", "max"]}
)
```

### Join Operations

```python
# Join two datasets
merged = query.join(
    left="sensor_readings",
    right="sensor_calibration",
    on="sensor_id",
    how="left"
)
```

### Time-Series Operations

```python
# Resample to different frequency
resampled = query.resample("sensor_log",
    time_column="timestamp",
    frequency="1H",
    aggregations={"temperature": "mean"}
)

# Rolling window
rolling = query.rolling("sensor_log",
    column="temperature",
    window=60,
    functions=["mean", "std"]
)
```

### Expressions

```python
# Computed columns
result = query.transform("sensor_log",
    expressions={
        "temp_fahrenheit": "temperature * 9/5 + 32",
        "is_hot": "temperature > 35"
    }
)
```

---

## Data Visualization Integration

The Data Architecture module provides one-click data-to-chart functionality:

1. User selects a dataset in the data browser.
2. Clicks "Visualize."
3. The system analyzes column types and suggests appropriate chart types:

| Data Pattern | Suggested Charts |
|---|---|
| Single numeric column | Histogram, box plot, density plot |
| Two numeric columns | Scatter plot, line chart |
| Numeric + categorical | Grouped bar chart, violin plot |
| Time-series | Line chart, area chart |
| Geospatial | Map overlay, heatmap |
| Multi-dimensional | Parallel coordinates, radar chart |

4. A default chart is rendered immediately using Visualization Studio.
5. The user can customize via the Visualization Studio GUI.

The data and chart remain linked: updating the underlying data automatically updates the chart.

---

## Data Export

Datasets can be exported in any supported format:

```python
# Export to CSV
export.to_csv("sensor_log", "output/sensor_cleaned.csv", 
    options={"delimiter": ",", "encoding": "utf-8"})

# Export to Excel with multiple sheets
export.to_excel("analysis_results", "output/report.xlsx",
    sheets={
        "Raw Data": "sensor_log",
        "Summary": "sensor_summary",
        "Outliers": "outlier_records"
    })

# Export to database
export.to_postgres("sensor_log", 
    connection="postgresql://localhost:5432/labdb",
    table="sensor_data_2024")
```

### Format Conversion

The export engine handles:

- Type coercion (e.g., datetime to string with format specifier).
- Precision adjustment (e.g., float64 to float32 for smaller files).
- Encoding conversion (e.g., UTF-8 to Latin-1 for legacy systems).
- Compression (e.g., CSV.gz, Parquet with Snappy).

---

## Streaming Data

For real-time data sources, the system supports streaming ingestion:

### IoT and Sensor Streams

```yaml
stream_config:
  source: mqtt
  broker: "mqtt://localhost:1883"
  topics:
    - "sensors/temperature/#"
    - "sensors/humidity/#"
  payload_format: json
  buffer_size: 1000
  flush_interval: 5s
  storage: ring_buffer
  max_retention: 24h
```

### Stream Processing

Streaming data passes through a lightweight processing pipeline:

1. **Deserialization.** JSON/MQTT payload → key-value record.
2. **Schema validation.** Check required fields, types, ranges.
3. **Windowing.** Aggregate over tumbling or sliding windows.
4. **Anomaly detection.** Flag values exceeding configured thresholds in real time.
5. **Storage.** Append to ring buffer or persistent store.

### Stream Visualization

Streaming data feeds a live-updating chart in Visualization Studio:

- Configurable refresh rate (100ms to 60s).
- Plot types: scrolling line chart, live heatmap, gauge panel.
- Alert overlay when values exceed thresholds.

---

## Large Dataset Handling

For datasets that exceed available memory, the system employs several strategies:

### Chunked Processing

Data is processed in configurable chunks:

```python
for chunk in data.iter_chunks("sensor_log", chunk_size=10000):
    result = process(chunk)
    accumulator.append(result)
final = accumulator.merge()
```

### Lazy Loading

Columns and row ranges are loaded on demand:

- Only the columns needed for a visualization are read from disk.
- Row ranges are loaded as the user scrolls through a data table.
- Full dataset scans are only performed when explicitly requested.

### Caching

Computation results are cached at multiple levels:

| Cache Level | What is cached | Invalidation |
|---|---|---|
| Query cache | Results of recent queries | TTL (5 min) or data change |
| Column cache | Individual column data in memory | LRU eviction |
| Aggregation cache | Pre-computed aggregations | Parent data change |
| Plot cache | Rendered chart images | Data or parameter change |

### Approximate Queries

For exploratory analysis of very large datasets, approximate methods are available:

- **Sampling.** Query runs on a random sample (configurable size).
- **HyperLogLog.** Approximate distinct count.
- **t-digest.** Approximate quantiles.

---

## Data Security

### Encryption

- Data at rest: AES-256 encryption for project data stores.
- Data in transit: TLS 1.3 for all database and streaming connections.
- Encryption keys are managed by the platform's key management system.

### Access Control

| Role | Read | Write | Delete | Share | Admin |
|---|---|---|---|---|---|
| Student | Own projects | Own projects | No | No | No |
| Teaching Assistant | Assigned projects | Assigned projects | No | No | No |
| Instructor | All course projects | All course projects | Own | Yes | Course-level |
| Admin | All | All | All | Yes | Full |

### Audit Logging

Every data operation is logged:

```yaml
audit_entry:
  timestamp: 2024-01-15T14:30:00Z
  user: "student_42"
  action: data.import
  dataset: "sensor_log_2024"
  details:
    format: csv
    row_count: 50000
    file_hash: "sha256:def456..."
  ip_address: "192.168.1.42"
```

Audit logs are immutable and retained for a configurable period (default: 1 year).

---

## Data Lineage

Data lineage tracks the complete history of a dataset from source to output:

### Lineage Graph

```
sensor_log_raw.csv (external)
       │
       ▼
  Import (v1) ──── validation_report.yaml
       │
       ▼
  Clean (v2) ───── fill_mean(temperature), drop(humidity_null)
       │
       ▼
  Transform (v3) ── add_column(temp_k), add_column(hour)
       │
       ├──→ Parameter Sweep Studio (sweep_results)
       │
       ├──→ Visualization Studio (bode_plot.png)
       │
       └──→ Report Generator (lab_report.pdf)
```

### Lineage Metadata

Each transformation records:

- Input dataset version(s).
- Operation performed.
- Parameters of the operation.
- Output dataset version.
- Timestamp and user.
- Reproducibility hash (deterministic hash of the operation + inputs).

This enables full reproducibility: any downstream artifact can be traced back to its exact source data and transformation chain.

---

## Integration with Parameter Sweep Studio

The Parameter Sweep Studio (module 08) reads data from the Data Architecture module:

- **Input datasets.** Sweep configurations can reference project datasets as parameter sources.
- **Output datasets.** Sweep results are written back to the data store as new datasets.
- **Cross-sweep analysis.** Multiple sweep results can be joined and compared through the Query API.
- **Parameter optimization.** Historical sweep data informs recommended parameter ranges.

---

## Integration with Report Generator

The Report Generator (module 11) accesses data through the Query API:

- **Table generation.** Data tables are auto-formatted from query results.
- **Figure captions.** Dataset metadata is used to generate descriptive captions.
- **Data appendices.** Raw or processed data can be attached to reports.
- **Lineage references.** Reports can include data provenance sections.

---

## Future Enhancements

| Enhancement | Description | Priority |
|---|---|---|
| **Column store backend** | Migrate to a proper columnar database for analytical queries | High |
| **Data marketplace** | Shared datasets across institutions with licensing | Medium |
| **Auto-schema inference** | ML-based schema detection for unknown formats | Medium |
| **Federated queries** | Query across multiple project data stores simultaneously | Low |
| **Data versioning with DVC** | Integration with Data Version Control for Git-like data workflows | Medium |
| **Streaming SQL** | SQL interface for real-time stream queries | Medium |
| **Data quality scoring** | Automated quality metrics for imported datasets | High |
| **Privacy-preserving analytics** | Differential privacy for sensitive datasets | Low |
| **Cross-platform sync** | Sync project data across devices via cloud storage | Medium |
