# Engineering Report Engine Architecture

**Document Status:** Production Normative Specification  
**Phase:** 5 — Experiment Results and Engineering Report Engine  

---

## 1. Architecture Overview

The Report Engine generates versioned, technical engineering reports from stored project metadata, experiment results, execution traces, datasets, and visualizations.

```
React Frontend (Report Builder / Preview)
      │
      ▼ REST API (/api/v1/projects/{project_id}/reports/...)
ReportService.generate_report()
      │
      ├───────────────────────────────┬───────────────────────────────┐
      ▼                               ▼                               ▼
ReportValidator                 ReportRenderer                  ReportExporter
(Pre-generation checks)         (Jinja2 HTML template)          (HTML & PDF export)
```

---

## 2. Default Report Structure (13 Sections)

1. Title Header
2. Objective & Description
3. Project Metadata
4. Experiment Metadata
5. Execution Trace (stdout/stderr & duration)
6. Input Dataset Summary & SHA-256 Content Hash
7. Visualizations List
8. Associated Result Artifacts
9. Methods & Script Path
10. Execution Parameters
11. Findings Summary
12. Notes & Comments
13. Reproducibility & Provenance Information

---

## 3. Storage & Hashing

- Output Location: `outputs/reports/{report_id}/report.html` and `report.pdf`.
- Report Integrity: SHA-256 hash calculated over generated HTML content.
