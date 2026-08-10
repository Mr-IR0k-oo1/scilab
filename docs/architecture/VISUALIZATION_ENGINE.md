# Visualization Engine Architecture

**Document Status:** Production Normative Specification  
**Phase:** 4 — Engineering Data and Visualization Engine  

---

## 1. Architecture Overview

The Visualization Engine manages chart specifications and computes chart series data points for 5 initial chart types.

```
React Frontend (Chart Preview & Exporters)
      │
      ▼ REST API (/api/v1/projects/{project_id}/visualizations/...)
Visualization Service (app/visualization/service.py)
      │
      ├───────────────────────────────┐
      ▼                               ▼
Visualization Repository      VisualizationValidator
(SQLite VisualizationModel)   (Validates X/Y & Types against Schema)
```

---

## 2. Supported Chart Types

1. **Line Chart:** `x_column` + `y_columns`
2. **Scatter Plot:** `x_column` + `y_columns`
3. **Bar Chart:** `x_column` + `y_columns`
4. **Histogram:** Target numeric column + `bins` option (default: 10)
5. **Heatmap:** `x_column` + `y_columns` (2D matrix data grid)

---

## 3. Changed Dataset Detection & Reproducibility

Stored `VisualizationModel` records the `dataset_hash` at the time of configuration.
If the underlying dataset content changes:
- `dataset_hash_changed` returns `true` in `ChartDataResponse`.
- A warning message is attached (`"Source dataset content hash has changed since this visualization was configured."`).

---

## 4. Export Formats

- Data CSV export (`ChartExporter.export_to_csv()`)
- Vector SVG & PNG metadata support.
