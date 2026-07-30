# Report Generator

## Overview

Report Generator is the module that transforms experiment results, data analyses, and engineering work into polished, publication-ready documents. It automates the most time-consuming part of the scientific workflow: assembling figures, tables, equations, methodology descriptions, and references into a coherent, formatted report.

The module targets four primary user needs:

1. **Students** writing lab reports after completing an experiment.
2. **Researchers** preparing technical papers and project reports.
3. **Instructors** generating answer keys and grading rubrics.
4. **Teams** producing collaborative technical documentation.

Report Generator integrates tightly with Visualization Studio (for figures), Data Architecture (for tables), Experiment Recorder (for methodology), and the AI Assistant (for text generation and editing).

---

## Problem Statement

Manual report creation is one of the most time-consuming tasks in engineering education and research. Consider a typical scenario:

1. A student runs a simulation and produces five plots.
2. The student opens a word processor and creates a new document.
3. The student manually copies each plot, resizes it, adds captions, and positions it in the document.
4. The student formats tables by hand — adjusting column widths, alignment, and decimal precision.
5. The student types mathematical equations using an equation editor or worse, screenshots from a whiteboard.
6. The student assembles references from various sources, manually formatting each citation.
7. The student repeats this process for every experiment, every semester.

The same burden applies to researchers, who spend hours reformatting the same types of content when switching between journal templates. Studies estimate that researchers spend 30–50% of their total project time on documentation and formatting.

Report Generator eliminates this repetitive work by automating content assembly while preserving full editorial control.

---

## Architecture

Report Generator is built on three core subsystems:

```
┌──────────────────────────────────────────────────────────┐
│                    Report Generator                       │
│                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────┐ │
│  │  Template       │  │  Content        │  │  PDF       │ │
│  │  Engine         │  │  Assembler      │  │  Renderer  │ │
│  └────────┬───────┘  └────────┬───────┘  └─────┬──────┘ │
│           │                   │                │        │
│           ▼                   ▼                ▼        │
│  ┌─────────────────────────────────────────────────────┐│
│  │              Report Document Model (RDM)             ││
│  └─────────────────────────────────────────────────────┘│
│           │                   │                │        │
│           ▼                   ▼                ▼        │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Export   │  │  Citation    │  │  Version         │  │
│  │  Formats  │  │  Manager     │  │  Controller      │  │
│  └──────────┘  └──────────────┘  └──────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Template Engine.** Manages document structure, layout rules, and formatting specifications. Templates define where each type of content appears and how it is styled.

**Content Assembler.** Gathers content from multiple sources — experiment logs, visualization outputs, data tables, user-written text — and assembles it into the Report Document Model.

**PDF Renderer.** Converts the Report Document Model into the final output format, applying typography, layout, and styling rules.

---

## Report Types

| Report Type | Audience | Typical Length | Sections |
|---|---|---|---|
| **Lab Report** | Instructor / TA | 5–15 pages | Objectives, Theory, Methodology, Results, Discussion, Conclusion |
| **Research Paper** | Peer reviewers / Conference | 8–20 pages | Abstract, Introduction, Related Work, Methodology, Results, Discussion, Conclusion, References |
| **Project Report** | Manager / Client | 10–30 pages | Executive Summary, Background, Approach, Results, Timeline, Budget, Recommendations |
| **Technical Brief** | Team members | 2–5 pages | Problem, Solution, Implementation, Results |
| **Thesis Chapter** | Committee | 30–100+ pages | Literature Review, Methodology, Experiments, Analysis, Discussion |
| **Answer Key** | Instructor only | 3–8 pages | Questions, Solutions, Rubrics, Grading notes |

### Template Selection

Users select a report type at creation time. The selected type determines:

- Available sections and their ordering.
- Required vs. optional sections.
- Default formatting rules.
- Citation style (IEEE, APA, Chicago, ACM, custom).
- Page layout (margins, columns, fonts).

---

## Report Structure

A generated report follows a standardized structure. Not all sections are required for every report type — the template determines which sections are active.

### Title Page

Auto-populated with:

- Report title
- Author name(s) and affiliation(s)
- Course name and number (for lab reports)
- Instructor name
- Date (submission date or experiment date)
- Institution logo (configurable)

### Abstract

A structured abstract with labeled sections:

> **Objective:** [auto-generated from experiment metadata]
> **Method:** [auto-generated from experiment configuration]
> **Results:** [auto-generated from result summary]
> **Conclusion:** [student or AI-generated]

The AI Assistant can generate a draft abstract from the experiment data, which the user then edits.

### Objectives

Listed from the experiment metadata. Each objective is mapped to a Bloom's taxonomy level with a visual indicator.

### Methodology

The methodology section is auto-generated from the experiment's recorded parameters:

```markdown
## Methodology

### Experimental Setup
The experiment was conducted using Scilab [version] on [date]. 
The following parameters were used:

| Parameter | Value | Unit |
|---|---|---|
| Resistance (R) | 1000 | Ω |
| Capacitance (C) | 1.0 | μF |
| Frequency range | 1 – 10⁶ | Hz |
| Number of points | 500 | — |

### Procedure
1. The RC circuit transfer function was defined as H(s) = 1/(RCs + 1).
2. Bode plot analysis was performed over the specified frequency range.
3. Corner frequency was computed as f_c = 1/(2πRC).
4. Gain and phase margins were extracted from the plot.
```

### Results

Results are assembled from multiple sources:

- **Figures.** Plots from Visualization Studio are embedded with auto-generated captions and figure numbers.
- **Tables.** Data from Data Architecture is formatted into publication-quality tables.
- **Key values.** Computed results are extracted and highlighted.
- **Observations.** The AI Assistant can suggest observations based on the data patterns.

### Discussion

The discussion section provides guided prompts:

> - How do your experimental results compare with theoretical predictions?
> - What sources of error might account for discrepancies?
> - How would the system behavior change if [parameter] were doubled?
> - What practical applications does this experiment demonstrate?

Students write their discussion around these prompts. The AI Assistant can review and suggest improvements.

### Conclusion

A structured conclusion template:

> In this experiment, [restate objectives]. The key findings were:
> 1. [finding 1]
> 2. [finding 2]
> 3. [finding 3]
>
> These results [confirm/reject/extend] the theoretical prediction that [theory statement].

### References

Auto-generated from the citation database (see Citation Management below).

---

## Graph Integration

Report Generator integrates directly with Visualization Studio to embed figures.

### Embedding Workflow

1. The user selects figures from their project's visualization library.
2. Figures are placed in the report at the current cursor position (or appended to the Results section).
3. Auto-generated captions are based on:
   - Figure title from Visualization Studio
   - Key parameter values displayed in the plot
   - Dataset name and summary statistics

### Figure Management

| Feature | Description |
|---|---|
| Auto-numbering | Figures are numbered sequentially (Fig. 1, Fig. 2, ...) |
| Cross-referencing | Text can reference figures: "As shown in Fig. 3 ..." |
| Resolution control | Export at 150 DPI (screen), 300 DPI (print), or 600 DPI (publication) |
| Format options | PNG (raster), SVG (vector), PDF (vector) |
| Cropping | In-report cropping and resizing without modifying the source |
| Subfigures | Multiple plots grouped as Fig. 1a, 1b, 1c |

### Figure Quality

All embedded figures are:

- Rendered at the highest available resolution.
- Checked for minimum legibility (font sizes, axis labels).
- Colorblind-safe palettes applied by default (configurable).
- Consistent styling applied (font family, size, line widths).

---

## Table Integration

Data tables are auto-formatted from query results:

### Table Formatting Rules

```yaml
table_defaults:
  style: scientific        # scientific, casual, minimal
  alignment:
    text: left
    numbers: decimal       # right-aligned on decimal point
  borders: 
    top: thick
    bottom: thick
    header_bottom: thin
    others: none           # no vertical lines (scientific style)
  precision: 3             # significant figures for floats
  thousands_separator: ","
  scientific_notation: auto  # >10⁴ or <10⁻² → scientific
  header_style: bold
  caption_position: below
```

### Table Types

| Type | Use Case |
|---|---|
| Data table | Raw or processed data values |
| Summary table | Statistical summaries (mean, std, min, max) |
| Comparison table | Side-by-side results for different parameters |
| Parameter table | Experiment configuration values |
| Bibliography table | References in specific citation styles |

### Example Auto-Formatted Table

```
Table 2: Bode Plot Analysis Results

┌─────────────────────┬────────────┬────────────┐
│ Parameter           │ Simulated  │ Theoretical│
├─────────────────────┼────────────┼────────────┤
│ Corner frequency    │ 158.2 Hz   │ 159.2 Hz   │
│ Gain at DC          │ 0.00 dB    │ 0.00 dB    │
│ Phase at f_c        │ -44.8°     │ -45.0°     │
│ -3 dB bandwidth     │ 162.4 Hz   │ 159.2 Hz   │
│ Slope (high freq)   │ -20.1 dB/dec│-20 dB/dec │
└─────────────────────┴────────────┴────────────┘
```

---

## Equation Support

Report Generator supports inline and display equations rendered from LaTeX syntax.

### Inline Equations

Wrapped in `$...$`:

```markdown
The transfer function is $H(s) = \frac{1}{RCs + 1}$, where $R$ is the resistance and $C$ is the capacitance.
```

### Display Equations

Wrapped in `$$...$$`:

```markdown
$$G(j\omega) = \frac{1}{\sqrt{1 + (\omega RC)^2}} \cdot e^{-j\arctan(\omega RC)}$$
```

### Equation Features

| Feature | Description |
|---|---|
| Full LaTeX math mode | All standard math symbols, operators, and structures |
| Numbered equations | Auto-numbered with cross-reference support |
| Matrices | `\bmatrix`, `\pmatrix`, `\vmatrix` |
| Piecewise functions | `\cases` or `aligned` environments |
| Chemical equations | `mhchem` package support |
| Unit notation | `\unit` for SI unit formatting |
| Aligned equations | `aligned` for multi-line derivations |

### Equation Rendering

Equations are rendered using:

1. **PDF output.** KaTeX or native LaTeX rendering via pdflatex/xelatex.
2. **HTML output.** KaTeX client-side rendering.
3. **DOCX output.** OMML (Office Math Markup Language) conversion.

---

## Methodology Section

The methodology section is auto-generated from the experiment's recorded parameters and procedure.

### Content Sources

| Source | Content Generated |
|---|---|
| Experiment Recorder | Step-by-step procedure with timestamps |
| Parameter Sweep Studio | Parameter ranges, optimization settings |
| Data Architecture | Data source descriptions, preprocessing steps |
| Scilab Execution Engine | Script versions, function calls, library versions |
| GUI Builder | Interface description, widget settings |

### Generation Process

1. The assembler collects metadata from all sources.
2. A prose generator (rule-based or AI-assisted) converts structured metadata into readable paragraphs.
3. Tables of parameters are formatted.
4. References to figures and equations are inserted.
5. The user reviews and edits the generated text.

### Example Generated Methodology

> **2.1 Simulation Environment**
>
> The simulation was performed using Scilab 2024.1.0 on a Linux workstation (Ubuntu 22.04, 16 GB RAM). The `signal` and `control` toolboxes were loaded for frequency-domain analysis.
>
> **2.2 System Configuration**
>
> A second-order underdamped system was modeled with the following parameters:
>
> | Parameter | Symbol | Value | Unit |
> |---|---|---|---|
> | Natural frequency | ω_n | 100 | rad/s |
> | Damping ratio | ζ | 0.4 | — |
> | Input amplitude | A | 1.0 | V |
>
> **2.3 Procedure**
>
> The simulation executed the following steps:
> 1. Transfer function G(s) = ω_n² / (s² + 2ζω_n·s + ω_n²) was constructed.
> 2. Bode plot was generated over the frequency range 0.1–1000 rad/s.
> 3. Step response was computed with a time vector of 0 to 0.1 s (500 points).
> 4. Peak overshoot, settling time, and rise time were extracted from the step response.
> 5. Results were stored in `results/simulation_output.yaml`.

---

## Template Library

The template library provides pre-designed report templates for different contexts:

### Built-in Templates

| Template | Citation Style | Layout | Target |
|---|---|---|---|
| `lab-report-standard` | IEEE | Single column, 12pt | Undergraduate labs |
| `lab-report-compact` | APA | Single column, 11pt | Quick lab reports |
| `research-paper-ieee` | IEEE | Double column, 10pt | Conference papers |
| `research-paper-acm` | ACM | Double column, 9pt | ACM publications |
| `thesis-chapter` | Custom | Single column, 12pt | Thesis chapters |
| `technical-brief` | None | Single column, 11pt | Internal documentation |
| `project-report` | APA | Single column, 12pt | Industry project reports |
| `poster` | — | Landscape A0/A1 | Conference posters |

### Template Preview

Before committing to a template, users can preview:

- Title page layout
- Section ordering
- Font choices
- Margin settings
- Example content rendered in the template

---

## Customization

### Fonts

Configurable font settings:

```yaml
fonts:
  title:
    family: "Times New Roman"
    size: 16pt
    weight: bold
  heading1:
    family: "Times New Roman"
    size: 14pt
    weight: bold
  heading2:
    family: "Times New Roman"
    size: 12pt
    weight: bold
  body:
    family: "Times New Roman"
    size: 12pt
    weight: normal
  code:
    family: "Courier New"
    size: 10pt
  caption:
    family: "Times New Roman"
    size: 10pt
    style: italic
```

### Layout

```yaml
layout:
  page_size: A4
  margins:
    top: 2.5cm
    bottom: 2.5cm
    left: 3cm
    right: 2.5cm
  columns: 1
  line_spacing: 1.5
  paragraph_spacing: 6pt
  header_footer:
    header: "{title} — {author}"
    footer: "Page {page_num}"
```

### Branding

Institutions can configure:

- Logo placement (title page, header, footer)
- Color scheme (primary, secondary, accent colors)
- Custom cover page template
- Disclaimer and copyright text
- Watermark (e.g., "DRAFT" or "CONFIDENTIAL")

---

## Export Formats

| Format | Extension | Use Case | Fidelity |
|---|---|---|---|
| **PDF** | `.pdf` | Final submission, printing | Highest |
| **HTML** | `.html` | Web viewing, interactive elements | High |
| **LaTeX** | `.tex` | Further editing in LaTeX editors | Highest (source) |
| **DOCX** | `.docx` | Microsoft Word editing | High |
| **Markdown** | `.md` | Version control, lightweight sharing | Medium |
| **EPUB** | `.epub` | E-book readers | Medium |

### Export Options

```python
report.export(
    format="pdf",
    options={
        "quality": "print",          # "screen" | "print" | "press"
        "color_mode": "color",       # "color" | "grayscale" | "bw"
        "embed_fonts": True,
        "compress": True,
        "metadata": {
            "title": "Bode Plot Analysis — Lab 3",
            "author": "Jane Smith",
            "subject": "EE 301 — Signals and Systems",
            "keywords": ["Bode plot", "frequency response", "RC circuit"]
        }
    }
)
```

---

## Citation Management

### Reference Database

Citations are stored in a project-level BibTeX database:

```
project_root/
├── references/
│   ├── library.bib          # Main citation database
│   ├── library.yaml         # Machine-readable index
│   └── pdfs/                # Linked PDF files
│       ├── smith2024.pdf
│       └── doe2023.pdf
```

### Adding References

| Method | Description |
|---|---|
| Manual entry | Fill in a form with title, authors, year, etc. |
| DOI import | Paste a DOI → auto-fetch metadata |
| ISBN import | Paste an ISBN → auto-fetch book metadata |
| URL import | Paste a URL → extract metadata from page |
| File import | Import `.bib`, `.ris`, `.enw` files |
| PDF import | Parse metadata from PDF files |
| AI-assisted | Paste a description → AI generates a formatted reference |

### Citation Styles

Supported citation styles include:

- IEEE
- APA (7th edition)
- ACM
- Chicago
- Vancouver
- Harvard
- MLA
- Custom (user-defined CSL or style file)

### Bibliography Generation

When the report is exported, all cited references are:

1. Collected from the text.
2. Formatted according to the active citation style.
3. Sorted (alphabetical, numerical, or order of appearance).
4. Rendered in the bibliography section.
5. Cross-checked for completeness (every citation has a bibliography entry, every bibliography entry is cited).

---

## Version Control

Report versions are linked to experiment versions:

### Version Linkage

```yaml
report_version:
  id: rpt_003
  created: 2024-01-20T16:00:00Z
  linked_experiment_version: exp_v007
  linked_data_versions:
    - ds_sensor_v003
    - ds_analysis_v001
  linked_visualizations:
    - viz_bode_plot_001
    - viz_step_response_002
  author: "Jane Smith"
  status: "submitted"
```

### Version History

Every edit to the report is tracked:

- Content changes (diffs at paragraph level).
- Figure updates (new version of a linked figure → notification).
- Structure changes (sections added, removed, reordered).
- Metadata changes (title, author, date).

### Diff View

Users can compare any two versions:

- Side-by-side text comparison with change highlighting.
- Figure comparison (old vs. new overlay).
- Table diff (cell-level change detection).

---

## Batch Report Generation

For instructors who need to generate reports for an entire class:

### Batch Workflow

1. Select the experiment and report template.
2. Select the student roster (or a subset).
3. The system generates personalized reports for each student, populated with:
   - That student's simulation results.
   - That student's answers and scores.
   - That student's name and metadata.
4. Reports are exported as individual PDFs or combined into a single file.

### Batch Options

```yaml
batch_config:
  template: "lab-report-standard"
  students: "course_roster_ee301.csv"
  experiment: "bode_plot_analysis"
  include:
    - student_name
    - student_id
    - simulation_results
    - question_responses
    - grade_summary
  output:
    format: pdf
    naming: "{student_name}_Lab3_Report.pdf"
    output_dir: "./reports/lab3/"
    combine: false  # true → single merged PDF
```

---

## Integration with Experiment Recorder

Report Generator reads from Experiment Recorder (module 06):

- **Timestamps.** When each step was performed.
- **Parameter values.** Exact values used in the experiment.
- **Console output.** Scilab command output and logs.
- **Screenshots.** GUI states captured during the experiment.
- **Artifacts.** Generated files, plots, and data exports.

This integration allows the methodology section to be auto-generated with precise, reproducible detail — not a vague description, but the exact commands that were executed.

---

## Integration with Data Studio

Report Generator reads from Data Architecture (module 07):

- **Dataset metadata.** Names, descriptions, sizes, column definitions.
- **Query results.** Tables can be pulled directly from the Query API.
- **Statistics.** Summary statistics computed during import or analysis.
- **Lineage.** Data provenance information for methodology sections.
- **Exported data.** Raw data can be attached as appendices.

---

## Example: Generate a Complete Lab Report from Simulation Results

### Scenario

A student has completed a Bode plot analysis of an RC circuit and needs to submit a lab report.

### Step 1 — Open Report Generator

The student clicks "Generate Report" from the experiment workspace. The report type "Lab Report" is pre-selected.

### Step 2 — Select Template

The student selects `lab-report-standard` (IEEE format, single column, Times New Roman 12pt).

### Step 3 — Auto-populate

The system auto-populates:

**Title:** "Frequency Response Analysis of a First-Order RC Low-Pass Filter"

**Objectives:**
> 1. Analyze the frequency response of an RC low-pass filter using Bode plots.
> 2. Determine the corner frequency from simulated data.
> 3. Compare simulated results with theoretical predictions.

**Methodology** (auto-generated from Experiment Recorder):
> The simulation was performed using Scilab 2024.1.0. The RC circuit was configured with R = 1000 Ω and C = 1.0 μF. Bode plot analysis was performed over the frequency range 1 Hz to 1 MHz with 500 logarithmically spaced points. The transfer function H(s) = 1/(RCs + 1) was evaluated...

**Results** (auto-assembled):
> - Fig. 1: Bode magnitude plot (auto-embedded from Visualization Studio)
> - Fig. 2: Bode phase plot (auto-embedded)
> - Table 1: Key frequency response parameters
> - Table 2: Theoretical vs. simulated corner frequency comparison

**References:**
> [1] B. C. Kuo, *Automatic Control Systems*, 8th ed., Prentice Hall, 2003.
> [2] R. C. Dorf and J. A. Svoboda, *Introduction to Electric Circuits*, 9th ed., Wiley, 2013.

### Step 4 — Student Adds Discussion

The student writes their discussion section, guided by the provided prompts. The AI Assistant suggests:

> "Consider discussing why the phase shift approaches -90° at high frequencies and how the -3 dB bandwidth relates to the time constant RC."

### Step 5 — Review and Export

The student reviews the complete document in the preview panel, makes minor edits, and exports as PDF. The report is 8 pages, fully formatted, with correctly numbered figures, formatted tables, and a properly sorted bibliography.

---

## Future Enhancements

| Enhancement | Description | Priority |
|---|---|---|
| **AI writing assistant** | Full integration with LLM for drafting, editing, and improving prose | High |
| **Real-time collaboration** | Multiple authors editing the same report simultaneously | Medium |
| **Plagiarism checking** | Cross-reference student text against web and database | Medium |
| **Accessibility checking** | Verify PDFs meet PDF/UA accessibility standards | Medium |
| **Journal submission integration** | Direct submission to journals via API | Low |
| **Poster generation** | Auto-generate conference posters from report content | Medium |
| **Presentation mode** | Generate slide decks from report sections | High |
| **Voice dictation** | Speech-to-text for drafting discussion sections | Low |
| **Template marketplace** | Community-contributed report templates | Medium |
| **Multi-language reports** | Generate reports in different languages from the same source | Low |
| **Annotation and review** | Built-in peer review and annotation tools | Medium |
