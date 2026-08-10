# Experiment Result Engine Architecture

**Document Status:** Production Normative Specification  
**Phase:** 5 — Experiment Results and Engineering Report Engine  

---

## 1. Architecture Overview

The Result Engine captures structured results from completed Scilab experiment executions, associating execution metadata, dataset references, visualizations, and generic result artifacts (`TEXT`, `TABLE`, `IMAGE`, `DATASET`, `VISUALIZATION`, `FILE`, `REPORT`).

```
Scilab Execution Completed
        │
        ▼ ResultService.create_result()
 ExperimentResultModel (ID, Project, Experiment, Execution, Status)
        │
        ▼ ResultService.add_artifact()
 ResultArtifactModel (TEXT, TABLE, IMAGE, DATASET, VISUALIZATION, FILE, REPORT)
```

---

## 2. Result Lifecycle & Status

- **Status States:** `PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `CANCELLED`, `PARTIAL`.
- **Artifact Management:** Files stored in `outputs/results/{result_id}/` (metadata in SQLite).
