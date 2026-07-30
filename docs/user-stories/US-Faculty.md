# User Stories — Faculty

## US-F01: Create a Reusable Lab Exercise
> I want to create a lab once and reuse it every semester.

**Acceptance Criteria:**
- Lab project includes scripts, data, GUI, and report template.
- Project is exportable as a `.scstudio` archive.
- Archive can be imported on any machine with Scilab installed.
- Students get a working project when they open the archive.

---

## US-F02: Generate Lab Reports Automatically
> I want students to generate reports from their data with one click.

**Acceptance Criteria:**
- Report template is included in the lab project.
- Students fill in results; charts and tables auto-populate.
- PDF export produces a formatted report.
- Report includes title page, data, analysis, and conclusion sections.

---

## US-F03: Create Interactive Demonstrations
> I want to build interactive GUIs that demonstrate engineering concepts.

**Acceptance Criteria:**
- GUI Builder produces working Scilab GUIs.
- Sliders and inputs update plots in real-time.
- Students can modify parameters and see results instantly.
- Code is generated and ready to run.

---

## US-F04: Share Projects with Students
> I want to distribute lab materials to 50 students easily.

**Acceptance Criteria:**
- Project is packaged as a single `.scstudio` file.
- File is small (< 10MB including data).
- Students import it via File → Import Project.
- No internet connection required to open.

---

## US-F05: Track Student Progress
> I want to see which examples students have completed.

**Acceptance Criteria (v0.3):**
- Learning Center tracks completed tutorials.
- Faculty dashboard shows class progress.
- Individual student progress is viewable.
- Exportable as CSV for grading.

---

## US-F06: Customize Templates for My Course
> I want to modify existing templates to match my curriculum.

**Acceptance Criteria:**
- Faculty can save modified projects as custom templates.
- Custom templates appear in "My Templates".
- Templates include course-specific data and scripts.
- Templates are shareable with other faculty.

---

## US-F07: Create Multi-Part Labs
> I want labs to have multiple parts (Part A: Theory, Part B: Simulation, Part C: Report).

**Acceptance Criteria:**
- Project supports multiple scripts and GUI layouts.
- Each part has its own directory and script.
- Report template includes all parts.
- Student can complete parts independently.
