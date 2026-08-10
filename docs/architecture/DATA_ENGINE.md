# Engineering Data Engine Architecture

**Document Status:** Production Normative Specification  
**Phase:** 4 — Engineering Data and Visualization Engine  

---

## 1. Architecture Overview

The Data Engine handles dataset inspection, memory-safe previewing, schema inference, data validation, and reproducible data transformations without mutating underlying raw dataset files.

```
Raw Files (CSV / JSON)
        │
        ▼ BaseDataLoader (CSVDataLoader / JSONDataLoader)
   Schema & Stats Inference + SHA-256 Hashing
        │
        ▼ DatasetValidator
 Validation Results (Warnings, Errors, Numeric Statistics)
        │
        ▼ DataTransformer
Reproducible Pipeline (Select, Filter, Sort, Rename, Fill, Normalize)
```

---

## 2. Supported Formats & Hashing

- **Formats:** CSV, JSON (extensible interface `BaseDataLoader`).
- **Content Hashing:** Calculates SHA-256 content hashes to detect whenever a dataset file is modified on disk.

---

## 3. Transformations

Transformation specifications are saved as reproducible JSON pipelines:

```json
{
  "operations": [
    { "type": "select_columns", "params": { "columns": ["time", "temperature"] } },
    { "type": "drop_missing", "params": {} },
    { "type": "sort", "params": { "column": "time", "ascending": true } }
  ]
}
```

---

## 4. Performance & Memory Capping

- `DATASET_PREVIEW_ROWS`: Default limit 100 preview rows.
- `VISUALIZATION_MAX_POINTS`: Capped at 5,000 points with automatic uniform sampling.
- `DATASET_MAX_SIZE_MB`: Streaming calculation for schema statistics.
