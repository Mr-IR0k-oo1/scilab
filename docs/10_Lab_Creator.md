# Lab Creator

## Overview

Lab Creator is the module responsible for the semi-automated generation of complete interactive laboratory exercises for engineering education. It provides educators with a guided workflow that transforms a selected topic and experiment choice into a fully-structured lab — complete with objectives, theoretical background, runnable simulations, interactive GUIs, auto-graded questions, and student reports.

The module sits at the intersection of pedagogy and tooling. Rather than requiring instructors to author every piece of a lab from scratch, Lab Creator assembles high-quality, pre-verified components into a coherent package that can be deployed to students immediately or customized further before release.

---

## Problem Statement

Creating laboratory exercises today is a repetitive and inconsistent process. An instructor teaching a signals and systems course, for example, must:

1. Write the lab objective and theory section by hand.
2. Write or adapt a Scilab script that demonstrates the concept.
3. Build an interactive GUI (usually in a separate tool or by hand-coding).
4. Author questions and grading rubrics.
5. Format everything into a distributable document or LMS package.
6. Repeat the entire process next semester with minor adjustments.

This workflow has several concrete problems:

- **Repetition.** Most labs across institutions cover the same canonical experiments (RC circuit, Bode plot, FFT of a signal). The authoring effort is duplicated thousands of times.
- **Inconsistency.** Without a shared structure, labs vary wildly in depth, accuracy, and pedagogical quality.
- **Fragility.** Scilab syntax changes or library deprecations can silently break older labs. Without a central component registry, broken labs go unnoticed.
- **Time cost.** A single well-crafted lab can take 8–20 hours to produce from scratch.

Lab Creator addresses these problems through a template-driven generation pipeline backed by a verified component library.

---

## Architecture

Lab Creator is composed of three primary subsystems:

```
┌─────────────────────────────────────────────────────────┐
│                      Lab Creator                         │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Template     │  │  Component   │  │  Generation  │  │
│  │  Engine       │  │  Library     │  │  Pipeline    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         ▼                 ▼                 ▼           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Unified Lab Model (ULM)             │   │
│  └──────────────────────────────────────────────────┘   │
│         │                 │                 │           │
│         ▼                 ▼                 ▼           │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Export   │  │  Question    │  │  Evaluation      │  │
│  │  Engine   │  │  Bank        │  │  Engine          │  │
│  └──────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Template Engine.** Manages the structural skeleton of a lab. Templates define section ordering, required placeholders, metadata fields, and rendering rules. The engine merges a selected template with concrete content to produce a lab document.

**Component Library.** A curated, versioned repository of reusable lab components: experiment scripts, GUI definitions, theory snippets, question sets, and rubrics. Every component is tested against the current Scilab execution engine version.

**Generation Pipeline.** The orchestration layer. Given a template, a set of component selections, and teacher customizations, the pipeline assembles the final lab artifact through parse → validate → compose → render steps.

---

## Workflow

The end-to-end workflow is a five-stage process:

```
Stage 1          Stage 2          Stage 3          Stage 4          Stage 5
Select Topic  →  Choose Exp.   →  Configure     →  Preview &     →  Deploy
                                   Parameters        Customize
```

### Stage 1 — Select Topic

The teacher browses a taxonomy of engineering disciplines:

- Electrical Engineering
- Mechanical Engineering
- Computer Science
- Civil Engineering
- Chemical Engineering

Each discipline branches into sub-topics (e.g., Electrical → Control Systems → Frequency Response → Bode Plot Analysis).

### Stage 2 — Choose Experiment

Within a topic, the teacher sees a list of available experiments drawn from the Component Library. Each experiment card shows:

- Title and one-line description
- Difficulty level (beginner / intermediate / advanced)
- Estimated student time
- Scilab toolbox dependencies
- Preview of the generated GUI

The teacher selects one or more experiments to include in the lab.

### Stage 3 — Configure Parameters

The teacher adjusts configurable parameters:

- Numerical values (e.g., resistance range, sampling frequency)
- Number of questions
- Grading weight
- Time limits
- Whether the student report template is included

### Stage 4 — Preview and Customize

The generation pipeline runs and produces a live preview. Every section is editable:

- Theory text can be rewritten or extended.
- Scilab scripts can be modified in the embedded editor.
- GUI layouts can be rearranged via drag-and-drop.
- Questions can be added, removed, or reworded.
- Rubric criteria can be adjusted.

### Stage 5 — Deploy

The finalized lab is exported in the desired format:

- Standalone Scilab project (`.sce` bundle)
- Web-deliverable package (HTML + JS execution via JSCILAB)
- LTI-compatible package for Moodle / Open edX
- PDF handout with embedded Scilab scripts

---

## Lab Structure

Every generated lab follows a standardized internal structure defined by the Unified Lab Model. The sections are:

| Section | Description | Auto-generated? |
|---|---|---|
| **Objectives** | Learning outcomes mapped to Bloom's taxonomy | Yes (template-driven) |
| **Theory** | Mathematical background and derivations | Partial (template + teacher edit) |
| **Simulation** | Runnable Scilab experiment script | Yes (from component) |
| **Interactive GUI** | Manipulable interface for parameter exploration | Yes (from GUI generator) |
| **Questions** | Conceptual and computational assessment items | Yes (from question bank) |
| **Evaluation** | Rubrics and grading criteria | Yes (from rubric templates) |
| **Student Report** | Structured template for student submission | Yes (from report generator) |

### Objectives

Objectives are generated using a mapping from experiment metadata to Bloom's taxonomy verbs. For example, an experiment tagged with "analysis" and "frequency domain" produces objectives such as:

> - Analyze the frequency response of a second-order system using Bode plots.
> - Evaluate the gain margin and phase margin from simulated data.

### Theory

The theory section is assembled from discipline-specific knowledge blocks stored in the Component Library. Each block contains:

- LaTeX-formatted mathematical expressions
- Explanatory prose (written at a configurable reading level)
- References to standard textbooks

Teachers can replace or augment any theory block.

### Simulation

The simulation section contains a complete, runnable Scilab script. Scripts are parameterized: configurable values are exposed as named variables at the top of the script with inline comments explaining their role.

```scilab
// === Lab Parameters (modify these) ===
R = 1000;          // Resistance in ohms
C = 1e-6;          // Capacitance in farads
f_start = 1;       // Start frequency in Hz
f_stop = 1e6;      // Stop frequency in Hz
N_points = 500;    // Number of frequency points
// ======================================

s = %s;
H = 1 / (R*C*s + 1);
f = logspace(log10(f_start), log10(f_stop), N_points);
bode(H, f);
```

### Interactive GUI

The GUI section is auto-generated from the experiment's parameter set. For the RC circuit example, the GUI would include sliders for R and C, a real-time Bode plot, and a readout panel showing computed corner frequency, gain margin, and phase margin.

### Questions

Questions are drawn from the Question Bank (see below). A typical lab includes 5–15 questions mixing:

- Multiple choice (conceptual)
- Numeric input (computational)
- Short answer (explanatory)
- Plot interpretation

### Evaluation

Each question is tagged with a rubric that specifies:

- Point value
- Acceptable answer range (for numeric questions)
- Keyword requirements (for short answer)
- Partial credit rules

### Student Report

A structured template guides the student through writing their lab report. Placeholders are pre-filled with the student's simulation results and GUI screenshots.

---

## Component Library

The Component Library is a versioned, indexed repository of reusable building blocks. Components are organized by type:

### Experiment Components

| Component ID | Discipline | Topic | Difficulty |
|---|---|---|---|
| `EE-CTRL-001` | Electrical | Control Systems | Beginner |
| `EE-CTRL-002` | Electrical | Control Systems | Intermediate |
| `EE-SP-001` | Electrical | Signal Processing | Beginner |
| `ME-THML-001` | Mechanical | Thermodynamics | Intermediate |
| `CS-ML-001` | Computer Science | Machine Learning | Advanced |

Each experiment component contains:

- `manifest.json` — metadata, dependencies, parameter schema
- `experiment.sce` — the Scilab script
- `gui.yaml` — GUI layout definition
- `theory.md` — theory content in Markdown/LaTeX
- `questions/` — directory of question files
- `rubric.yaml` — grading rubric
- `tests/` — automated tests verifying the script runs without error

### Theory Components

Standalone theory blocks that can be injected into any lab:

- Mathematical derivations (LaTeX)
- Conceptual explanations (prose)
- Diagrams (SVG/PNG)
- Animated demonstrations (Scilab-generated GIFs)

### Question Components

Pre-authored question sets tagged by topic, difficulty, and Bloom's level. Questions are stored in a normalized format:

```yaml
- id: Q-CTRL-001
  type: numeric
  bloom_level: apply
  difficulty: 2
  question: "For a system with transfer function G(s) = 1/(s+1)(s+2), calculate the steady-state error for a unit step input."
  answer: 0.5
  tolerance: 0.01
  points: 5
  hint: "Use the final value theorem: e_ss = lim(s→0) s·E(s)"
```

### Rubric Components

Standard rubrics for different assessment types:

- Procedural rubrics (step-by-step grading)
- Holistic rubrics (overall quality rating)
- Analytic rubrics (criteria-based scoring)

---

## Template System

Templates define the overall structure and flow of a lab. They do not contain domain-specific content — they define the skeleton into which components are placed.

### Template Categories

| Template | Use Case | Sections |
|---|---|---|
| `standard-lab` | Traditional 2-hour lab | Objectives → Theory → Simulation → GUI → Questions → Report |
| `guided-tutorial` | Step-by-step beginner lab | Theory → Mini-simulation → Theory → Mini-simulation → ... → Summary |
| `project-based` | Open-ended multi-session project | Problem Statement → Research → Design → Implement → Report → Presentation |
| `inquiry-based` | Student-driven exploration | Observation → Hypothesis → Experiment → Analysis → Conclusion |
| `assessment-only` | Exam or quiz format | Questions (timed, no GUI) |

### Template Format

A template is a YAML file that declares:

```yaml
name: standard-lab
version: 2.1
sections:
  - id: objectives
    type: auto-generated
    source: experiment_metadata
  - id: theory
    type: component-ref
    required: true
    editable: true
  - id: simulation
    type: component-ref
    required: true
    editable: true
  - id: gui
    type: auto-generated
    source: gui_generator
  - id: questions
    type: question-bank
    count: configurable
    default: 10
  - id: evaluation
    type: auto-generated
    source: rubric_engine
  - id: student_report
    type: component-ref
    required: true
    editable: true
metadata:
  estimated_time: 120  # minutes
  difficulty_range: [1, 3]
  supported_disciplines: [all]
```

### Custom Templates

Teachers can create custom templates by:

1. Duplicating an existing template.
2. Adding, removing, or reordering sections.
3. Defining new section types.
4. Publishing to their institution's template registry.

---

## GUI Generation

Lab Creator includes an automatic GUI generation engine that creates interactive interfaces from experiment parameters.

### How It Works

1. The experiment component declares its configurable parameters with types, ranges, and labels.
2. The GUI generator maps each parameter to an appropriate widget:

| Parameter Type | Widget |
|---|---|
| Continuous real, bounded | Slider |
| Integer, bounded | Spinner |
| Boolean | Toggle |
| String selection | Dropdown |
| File path | File picker |
| Color | Color picker |

3. The generator produces a layout using a constraint-based grid system.
4. Output plots are wired to update reactively when any widget value changes.

### Example Parameter Declaration

```yaml
parameters:
  - name: R
    label: "Resistance (Ω)"
    type: real
    min: 100
    max: 100000
    default: 1000
    step: 100
  - name: C
    label: "Capacitance (F)"
    type: real
    min: 1e-9
    max: 1e-3
    default: 1e-6
    log_scale: true
```

### Generated GUI Output

The generator produces a Scilab figure with:

- A control panel (left) containing all parameter widgets.
- A plot area (right) containing one or more linked axes.
- A status bar showing computed derived values.
- Export buttons for saving the current plot.

Teachers can modify the generated GUI by:

- Reordering widgets.
- Changing widget types.
- Adding custom annotations.
- Injecting additional Scilab code into the update callback.

---

## Question Bank

The Question Bank is a searchable, tagged repository of assessment items.

### Question Types

| Type | Description | Auto-gradable? |
|---|---|---|
| `multiple_choice` | Select one or more correct options | Yes |
| `numeric` | Enter a number within tolerance | Yes |
| `expression` | Enter a mathematical expression (symbolically evaluated) | Yes |
| `short_answer` | Free-text response (keyword-matched) | Partially |
| `plot_interpretation` | Identify features on a generated plot | Yes (with image matching) |
| `ordering` | Arrange steps in correct order | Yes |
| `matching` | Match terms to definitions | Yes |

### Difficulty Levels

| Level | Bloom's Target | Description |
|---|---|---|
| 1 | Remember | Recall facts and definitions |
| 2 | Understand | Explain concepts in own words |
| 3 | Apply | Use formulas in standard contexts |
| 4 | Analyze | Break down problems, compare |
| 5 | Evaluate | Justify choices, critique results |
| 6 | Create | Design new solutions, synthesize |

### Question Generation

For each experiment, the Question Bank can auto-generate questions by:

1. **Template-based generation.** Parameterized question templates with variable substitution.
   - "What is the corner frequency when R = {R} and C = {C}?"
2. **Concept-based generation.** Mapping experiment concepts to question patterns.
3. **Randomized generation.** Creating unique instances of the same question for different students (anti-cheating).

### Question Quality Metrics

Each question tracks:

- Difficulty calibration (based on student response data)
- Discrimination index (distinguishes high/low performers)
- Average time to answer
- Common wrong answers (for diagnostic feedback)

---

## Evaluation System

### Auto-Grading

The evaluation engine grades student submissions automatically:

1. **Numeric answers.** Compared against computed expected value within configurable tolerance.
2. **Multiple choice.** Direct match.
3. **Expression answers.** Symbolically evaluated against expected expression.
4. **Short answers.** Keyword scoring with configurable weights.
5. **Plot answers.** Feature detection (peak locations, slope values, intercept points).

### Rubrics

Every question carries an associated rubric. Rubrics support:

- Point allocation per criterion
- Partial credit curves (linear, step, custom)
- Penalty for incorrect attempts (configurable)
- Bonus points for elegant solutions

### Analytics

After grading, the system produces:

- Per-question statistics (mean, median, std dev, histogram)
- Per-student summaries (total score, time spent, attempt count)
- Class-wide analytics (distribution shape, outlier detection)
- Bloom's taxonomy coverage report (are all levels assessed?)
- Concept gap analysis (which concepts did the class struggle with?)

### Feedback Generation

For each question, the system generates:

- Correct/incorrect indication
- The correct answer with explanation
- Reference to the relevant theory section
- Suggested follow-up exercises for missed questions

---

## Student Report Generation

Lab Creator produces a structured report template for each student. The template:

1. Pre-fills the student's name, date, and lab title.
2. Provides sections matching the lab structure.
3. Includes placeholder slots for:
   - Simulation results (auto-inserted from the student's execution log).
   - GUI screenshots (captured from the student's session).
   - Plots and figures (embedded from the Scilab output).
4. Provides guided prompts in each section (e.g., "Describe the effect of increasing R on the corner frequency.").
5. Includes a bibliography section pre-populated with references from the theory block.

Students fill in their analysis and discussion around the pre-filled content. The report is exportable as PDF or HTML.

---

## Customization

Lab Creator is designed to produce drafts, not final products. Every generated element is editable:

| Element | Editing Mode |
|---|---|
| Objectives | Text editor with Bloom's taxonomy helper |
| Theory | Rich text editor with LaTeX support |
| Simulation scripts | Embedded Scilab editor with syntax highlighting |
| GUIs | Visual drag-and-drop editor |
| Questions | Form-based editor with live preview |
| Rubrics | Spreadsheet-style rubric editor |
| Report template | Section-level enable/disable, reorder, annotate |

### Override Mechanism

Teachers can mark any auto-generated section as "locked" (preventing further automatic updates) or "linked" (keeping it synchronized with the component library). This allows:

- Local modifications that track upstream changes.
- Complete overrides that diverge from the component library.

---

## Reusability

### Semester-to-Semester Reuse

Each published lab version is immutable. When a teacher re-uses a lab from a previous semester:

- The lab is cloned with a new version tag.
- Any upstream component updates can be reviewed and selectively merged.
- Student data from previous semesters is not carried over.

### Sharing Between Educators

Labs can be shared through:

- **Institutional registry.** Labs published within a university's Scilab Studio instance are visible to all instructors in the same department.
- **Public registry.** Labs can be published to the open Scilab Studio community registry with metadata, ratings, and reviews.
- **Export/import.** Labs can be exported as self-contained `.slab` bundles and shared via any file transfer mechanism.

### Attribution

Every shared lab carries provenance metadata:

- Original author
- Component sources and their authors
- Version history
- License (default: CC-BY-SA 4.0)

---

## Integration with Scilab Execution Engine

Lab Creator depends on the Scilab Execution Engine (module 05) for:

- **Script validation.** Every generated script is executed in a sandboxed Scilab instance to verify it runs without errors.
- **Output capture.** Plot images, numeric results, and console output are captured during validation and embedded in the lab preview.
- **Performance profiling.** Scripts that exceed execution time limits are flagged for optimization.
- **Version compatibility.** The engine checks that all Scilab function calls are valid against the configured Scilab version.

---

## Integration with Spoken Tutorials

Labs can link to relevant Spoken Tutorial video content:

- Each experiment component can declare associated Spoken Tutorial IDs.
- The generated lab includes a "Video Resources" section with embedded links.
- Teachers can add or remove video links during customization.
- Student report templates can include a "Video Reflection" section asking students to connect the video content with their experimental findings.

---

## Example: Generate a Control Systems Lab End-to-End

### Step 1 — Teacher opens Lab Creator

The teacher selects **Electrical Engineering → Control Systems → Frequency Response**.

### Step 2 — Choose Experiment

Available experiments are displayed:

1. Bode Plot of First-Order System (Beginner, 45 min)
2. Bode Plot of Second-Order System (Intermediate, 60 min)
3. Stability Analysis via Nyquist Plot (Advanced, 90 min)
4. PID Tuning via Frequency Response (Advanced, 120 min)

The teacher selects **experiment #2** and checks **experiment #1** as a warm-up.

### Step 3 — Configure Parameters

For experiment #2:

- Damping ratio range: 0.1 to 2.0 (default: 0.5)
- Natural frequency: 10 rad/s (fixed)
- Number of questions: 12
- Include student report template: Yes
- Time limit: None (untimed)

### Step 4 — Preview

The generation pipeline assembles the lab in approximately 3 seconds. The preview shows:

**Objectives:**
> - Analyze the effect of damping ratio on the frequency response of a second-order system.
> - Determine resonant peak magnitude and frequency from a Bode plot.
> - Compare simulated results with theoretical predictions.

**Theory section** contains the standard second-order transfer function derivation, the formulas for resonant peak and frequency, and the relationship between damping ratio and bandwidth. The teacher reviews and adds a note about underdamped vs. overdamped behavior.

**Simulation script:**

```scilab
// === Configurable Parameters ===
zeta = 0.5;           // Damping ratio (0.1 to 2.0)
wn = 10;              // Natural frequency (rad/s)
// ==============================

s = %s;
G = wn^2 / (s^2 + 2*zeta*wn*s + wn^2);
bode(G);
title("Bode Plot — Second-Order System (ζ = " + string(zeta) + ")");
```

**GUI:** A window with a damping ratio slider (0.1–2.0), a natural frequency spinner, a Bode plot with magnitude and phase subplots, and a readout panel showing resonant peak, resonant frequency, bandwidth, gain margin, and phase margin. All values update in real time as the slider moves.

**Questions:** 12 questions including:

- "What is the resonant peak magnitude when ζ = 0.3?" (numeric, difficulty 3)
- "At what frequency does the phase reach -90°?" (numeric, difficulty 2)
- "Explain why the resonant peak disappears for ζ ≥ 1/√2." (short answer, difficulty 4)
- "Select the correct Bode plot for ζ = 0.7 and ωn = 20." (multiple choice with plot options, difficulty 3)

**Evaluation:** Rubrics are auto-populated. The short answer question's rubric awards full points for mentioning the condition ζ < 1/√2 and partial points for any correct related reasoning.

**Student Report:** Template is generated with sections for Introduction, Methodology (pre-filled with the experiment parameters), Results (placeholders for Bode plot screenshots and tabulated resonant peak data), Discussion prompts, and Conclusion.

### Step 5 — Teacher customizes and deploys

The teacher:

- Rewrites one question to use different numerical values.
- Adds a paragraph to the theory section about practical applications in audio equalizer design.
- Removes one question they consider too advanced.
- Exports the lab as an LTI package for Moodle.

The lab is ready for 200 students to access the following week.

---

## Future Enhancements

| Enhancement | Description | Priority |
|---|---|---|
| **AI-powered question generation** | Use LLM to generate novel questions from experiment metadata | High |
| **Adaptive difficulty** | Adjust question difficulty based on student performance data | Medium |
| **Peer review integration** | Students review each other's reports using generated rubrics | Medium |
| **Live collaboration** | Multiple teachers co-author a lab simultaneously | Low |
| **AR/VR experiment modules** | Generate augmented reality overlays for physical experiments | Low |
| **Multilingual generation** | Auto-translate labs to different languages | Medium |
| **Accessibility audit** | Auto-check generated labs for WCAG compliance | High |
| **Learning analytics dashboard** | Real-time view of student engagement and performance across all labs | High |
| **Prerequisite enforcement** | Automatically suggest prerequisite labs based on content analysis | Low |
| **Integration with plagiarism detection** | Cross-reference student reports against database | Medium |
