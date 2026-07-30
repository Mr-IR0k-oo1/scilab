# Scilab Studio — Product Requirements Document

**Document ID:** PRD-001
**Version:** 1.0.0
**Status:** Approved
**Author:** Scilab Studio Core Team
**Last Updated:** 2026-07-27
**Review Cycle:** Quarterly

> This document is the authoritative source of truth for Scilab Studio's product scope.
> No feature may be added or removed without updating this document.

---

## 1. Executive Summary

Scilab Studio is an open-source engineering development platform that modernizes Scilab with a visual GUI builder, integrated engineering visualization, reusable labs, project templates, and a plugin ecosystem. Built on Tauri with TypeScript/Svelte frontends and a Rust sidecar, it wraps the Scilab numerical engine in a modern desktop experience that removes the friction of script-only development.

The objective of Scilab Studio is to make Scilab easier to learn, faster to develop with, and more suitable for engineering education and research. By providing visual development tools, integrated workflows, and a community marketplace, the platform lowers the barrier to entry for students while giving researchers and faculty the productivity they need to build, share, and reuse engineering work at scale.

## 2. Problem Statement

Current Scilab users face the following challenges:

1. **Complex GUI development** — Building GUIs requires hundreds of lines of `uicontrol` code with no visual designer, forcing developers to prototype layouts through trial and error.
2. **Limited visualization** — Plotting requires manual scripting for every chart type; there is no drag-and-drop dashboard builder or interactive exploration.
3. **Fragmented project organization** — No integrated workspace exists for organizing scripts, data, results, and reports in a single project.
4. **Manual report creation** — Reports are built by hand, copying graphs and tables from separate tools into external documents.
5. **Repeated development** — Common engineering workflows are rebuilt from scratch each time with no mechanism for reuse.
6. **No extension ecosystem** — There is no marketplace or plugin system for sharing libraries, widgets, or tools across the community.
7. **Limited collaboration** — No way to share, discover, or reuse community contributions within the Scilab ecosystem.

## 3. Objectives

### Primary Objectives

| ID | Objective | Success Criteria |
|----|-----------|-----------------|
| OBJ-001 | Modernize Scilab development | Users can build GUIs visually instead of hand-coding |
| OBJ-002 | Reduce engineering development time | Common tasks complete 3x faster than raw Scilab |
| OBJ-003 | Improve engineering education | Educators create interactive labs in under 30 minutes |
| OBJ-004 | Encourage reusable components | Community publishes 50+ widgets within 2 years |
| OBJ-005 | Increase Scilab adoption | 10 universities adopt Scilab Studio within 3 years |

### Secondary Objectives

| ID | Objective | Success Criteria |
|----|-----------|-----------------|
| OBJ-006 | Provide professional visualization | Charts match MATLAB/matplotlib quality |
| OBJ-007 | Enable experiment reproducibility | All parameters and outputs are automatically recorded |
| OBJ-008 | Support offline-first workflows | Core features work without internet connection |

## 4. Non-Objectives

This section prevents feature creep. Scilab Studio is NOT:

| ID | Non-Objective | Rationale |
|----|---------------|-----------|
| NO-001 | A MATLAB replacement | Scilab Studio extends Scilab; it does not replace it |
| NO-002 | A cloud IDE | v0.1 is desktop-first; cloud is a distant future consideration |
| NO-003 | A web-based IDE | Scilab requires native execution; browser-only is not viable |
| NO-004 | A CAD/CAE package | We visualize results; we don't do 3D modeling or FEA meshing |
| NO-005 | A game engine | Out of scope for engineering development |
| NO-006 | A machine learning platform | We may use ML (AI assistant); we are not an ML training platform |
| NO-007 | A generic code editor | We use Monaco for scripting; we are not competing with VS Code |
| NO-008 | A real-time control system | We are not a PLC or RTOS environment |
| NO-009 | A commercial simulation suite | We complement commercial tools; we don't replicate every feature |

## 5. Stakeholders

| Stakeholder | Primary Need | How Scilab Studio Serves Them |
|-------------|-------------|-------------------------------|
| Students (UG/PG) | Learn Scilab quickly, complete assignments | Learning Center, example projects, GUI Builder |
| Faculty/Professors | Create interactive labs, teaching materials | Lab Creator, Report Generator, Project Templates |
| Researchers | Data analysis, parameter studies, publication | Data Studio, Visualization Studio, Experiment Recorder |
| Plugin Developers | Stable SDK, documentation, APIs | Plugin System, Widget Framework, Marketplace |
| FOSSEE (IIT Bombay) | Ecosystem growth, education, open-source adoption | FOSSEE integration, community marketplace |
| Industry Engineers | Rapid prototyping without license costs | Full platform, professional output |

## 6. User Personas

### 6.1 Student (Priya)

- **Role:** 3rd year Electrical Engineering undergraduate
- **Goal:** Complete lab assignments on circuit analysis using Scilab
- **Current Pain:** Spends 3 hours writing GUI code for each assignment instead of understanding circuits
- **Scilab Studio Value:** Opens Lab Creator, selects "Circuit Analysis," gets a complete interactive lab with GUI, simulation, and assessment. Done in 30 minutes.
- **Success Metric:** Completes assignments 5x faster

### 6.2 Faculty (Dr. Rajesh)

- **Role:** Associate Professor, Mechanical Engineering
- **Goal:** Create interactive vibration analysis labs for 200 students
- **Current Pain:** Rebuilds lab exercises from scratch each semester, manually grades 200 reports
- **Scilab Studio Value:** Uses Lab Creator to generate a complete lab with auto-grading. Shares via marketplace.
- **Success Metric:** Lab creation time drops from 3 days to 1 hour

### 6.3 Researcher (Ananya)

- **Role:** PhD candidate, Renewable Energy
- **Goal:** Analyze solar panel performance across 1000 parameter combinations
- **Current Pain:** Writes custom scripts for each parameter sweep, manually tracks results
- **Scilab Studio Value:** Uses Parameter Sweep Studio for batch execution, Experiment Recorder for tracking, Visualization Studio for response surfaces.
- **Success Metric:** Parameter study completed in 2 hours instead of 2 days

### 6.4 Plugin Developer (Vikram)

- **Role:** Software engineer, contributes to FOSSEE
- **Goal:** Build and publish a robotics kinematics widget
- **Current Pain:** No platform to distribute Scilab tools; shares via email
- **Scilab Studio Value:** Uses Widget SDK, publishes to Marketplace, gets community feedback.
- **Success Metric:** Widget installed by 100+ users within 3 months

## 7. Functional Requirements

### 7.1 Project Management (v0.1)

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-001 | Create new project | High | User enters name, location → project directory and project.json created |
| FR-002 | Open existing project | High | User browses to project → workspace loads with file tree |
| FR-003 | Save project | High | All changes persisted to project.json and workspace state |
| FR-004 | File explorer | High | Tree view with create, rename, delete, search |
| FR-005 | Tab-based editor | High | Open multiple files, unsaved indicator, cursor position preserved |

### 7.2 Visual GUI Builder (v0.1)

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-010 | Drag-and-drop canvas | High | 9 component types draggable onto grid-snapped canvas |
| FR-011 | Property panel | High | Select component → edit text, size, color, position |
| FR-012 | Preview mode | High | Render GUI in separate window |
| FR-013 | Save/load layout | High | Layout persisted as JSON, reloadable |
| FR-014 | Generate Scilab code | High | Layout → valid Scilab GUI function |

### 7.3 Visualization Studio (v0.1)

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-020 | Line chart | High | Plot line chart from dataset |
| FR-021 | Scatter chart | High | Plot scatter chart from dataset |
| FR-022 | Bar chart | High | Plot bar chart from dataset |
| FR-023 | Heatmap | High | Plot heatmap from 2D dataset |
| FR-024 | Interactive zoom/pan | High | Mouse wheel zoom, drag pan |
| FR-025 | Hover tooltip | High | Show data values on hover |
| FR-026 | Export PNG/SVG/PDF | High | Download chart in 3 formats |
| FR-027 | Chart customization | Medium | Title, axis labels, colors, legend |

### 7.4 Data Studio (v0.1)

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-030 | Import CSV | High | Auto-detect delimiter, headers, types |
| FR-031 | Import Excel | High | Read .xlsx and .xls files |
| FR-032 | Data preview | High | Tabular preview with pagination |
| FR-033 | Column statistics | Medium | Min, max, mean, nulls per column |
| FR-034 | Export CSV | Medium | Write data to CSV |

### 7.5 Report Generator (v0.1)

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-040 | Select template | High | Choose from Lab Report, Technical Brief |
| FR-041 | Embed charts | High | Reference charts from Visualization Studio |
| FR-042 | Embed tables | High | Reference data from Data Studio |
| FR-043 | Export PDF | High | Valid PDF with embedded content |
| FR-044 | Export HTML | Medium | Viewable in any browser |

### 7.6 Learning Center (v0.1)

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|-------------------|
| FR-050 | Example projects | High | 5-10 bundled examples |
| FR-051 | Open example | High | Copy example to user workspace |
| FR-052 | Search examples | Medium | Filter by name and description |

### 7.7 Future Requirements (v0.2+)

| ID | Requirement | Version | Priority |
|----|------------|---------|----------|
| FR-060 | Plugin system | v0.2 | High |
| FR-061 | Widget marketplace | v0.2 | High |
| FR-062 | Lab creator | v0.2 | High |
| FR-063 | Xcos builder | v0.2 | Medium |
| FR-064 | Project templates | v0.2 | Medium |
| FR-070 | AI assistant | v0.3 | Medium |
| FR-071 | Digital twin framework | v0.3 | Medium |
| FR-072 | Parameter sweep | v0.3 | Medium |
| FR-073 | Dashboard builder | v0.3 | Medium |
| FR-080 | Community marketplace | v0.4 | Low |
| FR-081 | Engineering library | v0.4 | Low |
| FR-082 | Research workspace | v0.4 | Low |

## 8. Non-Functional Requirements

| ID | Requirement | Target | Rationale |
|----|------------|--------|-----------|
| NFR-001 | Cross-platform | Linux, macOS, Windows | FOSSEE serves global education |
| NFR-002 | Open-source | GPL v3 | Core FOSSEE principle |
| NFR-003 | Modular | Independent modules | Enables incremental adoption |
| NFR-004 | Plugin-based | Extension without core changes | Community contributions |
| NFR-005 | Offline-first | Core features work without internet | Engineering labs may lack connectivity |
| NFR-006 | Low memory | < 500MB typical usage | University lab machines have limited RAM |
| NFR-007 | Fast startup | < 2 seconds | Users expect responsive applications |
| NFR-008 | Reproducible | All parameters recorded | Scientific rigor |
| NFR-009 | Accessible | Keyboard navigation, screen reader | Inclusive design |
| NFR-010 | Localizable | UI text externalized | Global adoption |

## 9. Success Metrics

### 9.1 User Experience Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Build a GUI | < 10 minutes | User testing with 5 students |
| Import a dataset | < 30 seconds | Timed testing with 100MB CSV |
| Create a chart | < 2 minutes | User testing with 5 students |
| Generate a report | < 1 minute (one click) | User testing |
| Create a lab exercise | < 30 minutes | Faculty testing |
| Install a plugin | < 1 minute | User testing |

### 9.2 Platform Metrics (Year 1)

| Metric | Target |
|--------|--------|
| GitHub stars | 200+ |
| Downloads | 1,000+ |
| Beta testers | 50+ |
| University adoptions | 2+ |
| Community plugins | 10+ |

### 9.3 Platform Metrics (Year 3)

| Metric | Target |
|--------|--------|
| GitHub stars | 2,000+ |
| Monthly active users | 2,000+ |
| University adoptions | 10+ |
| Community plugins | 100+ |
| Marketplace transactions | 5,000+ |

## 10. Release Plan

### Version 0.1 — Foundation (Jul–Oct 2026)

**Scope:** Core platform + 6 modules
- Project Workspace + Manager
- GUI Builder (9 components)
- Visualization Studio (4 chart types)
- Data Studio (CSV, Excel)
- Report Generator (PDF, HTML)
- Learning Center (examples)

### Version 0.2 — Extensibility (Nov 2026–Feb 2027)

**Scope:** Plugin system + engineering modules
- Plugin System (install, activate, sandbox)
- Widget Marketplace
- Lab Creator
- Xcos Builder
- Project Templates (9 domains)

### Version 0.3 — Intelligence (Mar–Jun 2027)

**Scope:** AI + advanced simulation
- AI Engineering Assistant
- Digital Twin Framework
- Parameter Sweep Studio
- Dashboard Builder

### Version 0.4 — Community (Jul–Oct 2027)

**Scope:** Ecosystem + research
- Community Marketplace
- Open Engineering Library
- Research Workspace
- Experiment Recorder

### Version 2.0 — Platform (Future)

**Scope:** Cloud + collaboration
- Cloud deployment
- Real-time collaboration
- Web-based version (WASM)
- Enterprise features

## 11. Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | High | High | Strict PRD enforcement, versioned releases |
| GUI Builder complexity | Medium | High | Component-based design, incremental feature additions |
| Plugin compatibility | Medium | Medium | Versioned SDK, compatibility testing |
| Performance issues | Medium | Medium | Lazy loading, caching, profiling from day one |
| Community adoption | Medium | High | Strong documentation, examples, FOSSEE backing |
| Scilab version changes | Low | Medium | Abstraction layer in Scilab Bridge |
| Tauri maturity | Low | Medium | Tauri 2.x is production-ready; fallback to Electron |
| Developer turnover | Medium | High | Comprehensive documentation, ADRs, low bus factor |

## 12. Competitive Analysis

| Tool | Strength | Weakness | Scilab Studio Advantage |
|------|----------|----------|------------------------|
| MATLAB App Designer | Mature GUI tools, Simulink integration | Proprietary, expensive license | Free, open-source, FOSSEE ecosystem |
| GNU Octave | MATLAB compatibility | Limited modern tooling, no visual GUI builder | Visual development, integrated workspace |
| Jupyter Notebooks | Interactive computing, widely adopted | Not Scilab-native, no engineering widgets | Scilab-native, engineering-specific modules |
| VS Code | Rich extension ecosystem, excellent editor | No scientific runtime | Built-in Scilab engine, engineering focus |
| Scilab (raw) | Powerful numerical engine | No visual tools, fragmented workflow | Modern IDE wrapping the same engine |

**Key insight:** Scilab Studio does NOT compete with Scilab. It EXTENDS Scilab by adding the modern development experience that the engine alone lacks.

## 13. Assumptions

1. Scilab 7.0+ is available on target platforms
2. Tauri 2.x provides adequate cross-platform support
3. Users have basic familiarity with engineering concepts
4. FOSSEE continues to support the Scilab ecosystem
5. Community contributions will grow organically after v0.2

## 14. Dependencies

| Dependency | Type | Risk | Mitigation |
|-----------|------|------|------------|
| Scilab engine | External | High | Abstract via JSON-RPC bridge; test against multiple versions |
| Tauri framework | External | Medium | Pin to stable releases; have Electron fallback plan |
| Svelte ecosystem | External | Low | Mature framework with strong community |
| Monaco Editor | External | Low | Microsoft-maintained, VS Code's editor |
| SQLite | External | Low | Embedded, no server dependency |

## 15. Open Questions

1. Should v0.1 ship with or without the Plugin System? (Currently planned for v0.2)
2. What is the minimum Scilab version to support? (Currently 7.0)
3. Should the Learning Center include Spoken Tutorial integration from v0.1?
4. What is the target binary size for the desktop application?
5. Should we support ARM architectures (Apple Silicon, Raspberry Pi)?

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Module | An independent feature unit that integrates with the platform via the Event Bus |
| Plugin | A third-party extension that follows the plugin manifest and lifecycle |
| Widget | A reusable UI component implementing the Widget interface |
| Workspace | The user's project environment (panels, tabs, layout) |
| Scilab Bridge | The JSON-RPC layer connecting the platform to the Scilab engine |
| Digital Twin | A virtual replica of a physical system with sensors and mathematical models |
| Parameter Sweep | Systematic exploration of a parameter space through batch simulation |
