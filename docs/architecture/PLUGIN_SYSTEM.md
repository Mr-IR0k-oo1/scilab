# Plugin and Extension SDK Architecture

**Document Status:** Production Normative Specification  
**Phase:** 7 — Plugin and Extension SDK  

---

## 1. Architecture Overview

The Plugin and Extension System allows developers to extend Scilab Studio's capabilities (GUI components, visualization types, dataset loaders, report templates) without modifying core application code.

```
Core Application (Scilab Studio)
        │
        ▼ Public SDK Layer (app.sdk)
   Plugin Base & PluginContext
        │
        ▼ Plugin Manager (app.plugins)
Discovery ──► Validation ──► Dynamic Load ──► Initialized ──► Running
        │
        ▼ Extension Registries
 GUI Components | Visualizations | Dataset Loaders | Report Templates
```

---

## 2. Security Model & Isolation

- **Trust Model:** Installed plugins are trusted local Python software running with the privileges of the backend process.
- **No Remote Code Execution:** HTTP endpoints expose metadata only. Plugin installation/download via API is strictly prohibited.
- **Failure Isolation:** Lifecycle exceptions during plugin initialization are caught safely. A broken plugin is marked `FAILED` and logged; it **never** crashes the core application.
