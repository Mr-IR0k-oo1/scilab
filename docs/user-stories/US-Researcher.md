# User Stories — Researcher

## US-R01: Import and Analyze Experimental Data
> I want to import sensor data and compute statistics without writing boilerplate.

**Acceptance Criteria:**
- CSV and Excel import with auto-detection.
- Column statistics computed automatically.
- Transform pipeline for filtering and aggregation.
- Results exportable to Scilab variables for further analysis.

---

## US-R02: Compare Parameter Sweeps Visually
> I want to run a simulation with different parameters and compare results side-by-side.

**Acceptance Criteria:**
- Parameter sweep configuration (min, max, step per parameter).
- Multiple simulation runs execute sequentially.
- Results are plotted side-by-side on the same chart.
- Statistical summary (mean, std dev, min, max) for each sweep.
- Export comparison as PNG or PDF.

---

## US-R03: Create Publication-Quality Charts
> I want charts that look professional enough for journal papers.

**Acceptance Criteria:**
- High-resolution export (300+ DPI).
- Custom fonts, colors, and line styles.
- SVG export for vector graphics.
- LaTeX-compatible labels.
- Consistent theming across charts.

---

## US-R04: Reproduce Results Across Machines
> I want my project to work on any machine, regardless of Scilab version.

**Acceptance Criteria:**
- Project declares target Scilab version.
- Compatibility Layer warns about version differences.
- Deprecated functions are flagged with migration suggestions.
- Project can be exported and imported on another machine.

---

## US-R05: Work Offline
> I want all features to work without an internet connection.

**Acceptance Criteria:**
- All core features (editor, visualization, data, reports) work offline.
- No cloud accounts or telemetry.
- Marketplace is the only network feature.
- Plugin installation from local `.zip` files works.

---

## US-R06: Run Long Computations Without Blocking
> I want to start a long simulation and continue working while it runs.

**Acceptance Criteria:**
- Scilab evaluation runs in background.
- Progress indicator shows computation status.
- UI remains responsive during computation.
- User can abort at any time.
- Results appear when computation completes.

---

## US-R07: Export Results in Multiple Formats
> I want to export my analysis as CSV, PDF, and Scilab variables.

**Acceptance Criteria:**
- Data export: CSV, Excel, JSON.
- Chart export: PNG, SVG, JPEG.
- Report export: PDF, HTML.
- Scilab variable export for further computation.
- Batch export (all results at once).
