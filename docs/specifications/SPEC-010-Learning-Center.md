# SPEC-010 — Learning Center

## Purpose

Provide onboarding, educational content, and Scilab language reference integrated with the platform. The Learning Center is how users discover what Scilab Studio can do.

---

## Content Types

### Example Projects
Pre-built projects that demonstrate platform features. Each includes:
- Complete project structure (scripts, data, visualizations).
- README with description, difficulty, duration, prerequisites.
- Commented Scilab code explaining what each section does.

### Tutorials
Step-by-step guided experiences within the platform:
- Active tutorial panel with instructions.
- Validation of each step's completion.
- Hints and "I've done this" fallback.
- Progress tracking.

### Scilab Reference
Searchable function reference:
- Function name, syntax, parameters, return values, examples.
- Linked from code editor (click function name to see reference).
- Searchable via Learning Center search bar.

---

## Categories

| Category | Description |
|----------|-------------|
| Getting Started | Platform basics, first project |
| Data Analysis | CSV import, statistics, transforms |
| Visualization | Chart creation, customization, export |
| GUI Design | GUI Builder usage, components, events |
| Scilab Basics | Language fundamentals |
| Signal Processing | FFT, filtering, spectral analysis |
| Control Systems | Transfer functions, Bode, stability |
| Optimization | Linear programming, curve fitting |
| Numerical Methods | ODE solving, interpolation, integration |
| Reports | Report creation, data embedding |

---

## Difficulty Levels

| Level | Description |
|-------|-------------|
| Beginner | No prior knowledge required |
| Intermediate | Basic Scilab knowledge assumed |
| Advanced | Engineering domain knowledge required |

---

## Built-in Examples

| Example | Category | Difficulty | Duration |
|---------|----------|-----------|----------|
| Hello World | Getting Started | Beginner | 5 min |
| First Project | Getting Started | Beginner | 10 min |
| Import CSV | Data Analysis | Beginner | 10 min |
| Data Statistics | Data Analysis | Beginner | 15 min |
| Transform Pipeline | Data Analysis | Intermediate | 20 min |
| Line Chart | Visualization | Beginner | 10 min |
| Multi-Series Chart | Visualization | Intermediate | 15 min |
| Heatmap | Visualization | Intermediate | 15 min |
| Export Charts | Visualization | Beginner | 10 min |
| Basic GUI | GUI Design | Beginner | 15 min |
| GUI with Callbacks | GUI Design | Intermediate | 25 min |
| Signal FFT | Signal Processing | Intermediate | 20 min |
| Bode Plot | Control Systems | Advanced | 25 min |
| ODE Solver | Numerical Methods | Advanced | 30 min |
| Lab Report | Reports | Intermediate | 20 min |

---

## Tutorial Structure

```jsonc
{
  "id": "tutorial-first-chart",
  "title": "Create Your First Chart",
  "steps": [
    {
      "id": "step-1",
      "title": "Create a New Project",
      "instruction": "Click File → New Project. Name it 'My First Chart'.",
      "action": { "type": "command", "command": "project:create" },
      "validation": { "type": "project_exists", "name": "My First Chart" },
      "hint": "The project name should appear in the title bar."
    }
  ]
}
```

### Validation Types

| Type | Description |
|------|-------------|
| project_exists | A project with the given name exists |
| file_exists | A file with the given path exists |
| data_imported | A dataset has been imported |
| chart_created | A chart has been created |
| code_executed | Specific Scilab code was evaluated |
| command_run | A specific command was executed |
| manual | User clicks "I've done this" |

---

## Tutorial UI

- Tutorial panel at bottom or right of screen.
- Current step highlighted with instruction.
- "Check" button validates step completion.
- "Hint" button shows additional guidance.
- "Skip" button advances to next step.
- Progress bar (e.g., "Step 3 of 8").

---

## Search

Covers:
- Example titles and descriptions.
- Tutorial titles and step instructions.
- Scilab function names and descriptions.
- File contents within examples.

Features: fuzzy matching, category/difficulty filters, "Recently opened", "Continue where you left off".

---

## Content Management

### Bundled
All built-in examples and tutorials are in the `examples/` directory. Read-only.

### User Content
- User examples in `~/.scilab-studio/user-examples/`.
- User tutorials in `~/.scilab-studio/user-tutorials/`.
- Import from marketplace or shared `.scstudio` archives.

### Marketplace Content
Community-contributed examples and tutorials available from the marketplace.

---

## Scilab Reference

### Function Categories

| Category | Functions |
|----------|-----------|
| Basic | disp, who, clear, size, type, exists |
| Matrices | zeros, ones, rand, eye, diag, triu, tril |
| Plotting | plot, scatter, bar, histplot, title, xlabel, ylabel, legend |
| Data | csvRead, xlsRead, savemat, loadmat |
| Signal | fft, ifft, filter, correl, psd |
| Control | tf, ss, bode, nyquist, rlocus, step, impulse |
| Optimization | linpro, fsolve, lsq, qpsolve |
| Numerical | ode, ode45, interp, spline, intg |
| Statistics | mean, median, stdev, histc, corr, reglin |

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max examples | 50 (bundled) |
| Max user examples | Unlimited |
| Tutorial max steps | 50 |
| Search results max | 20 |
| Content cache TTL | 24 hours |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Example project corrupt | Skip, show error in Learning Center |
| Tutorial step validation fails | Show hint, allow retry or skip |
| Scilab reference lookup fails | Show "Function not found" |
| Marketplace content unavailable | Show cached version or offline message |

---

## Extension Points

- Custom content categories.
- Custom tutorial step validation.
- Custom Scilab reference sections.
- Community-contributed content.
- Interactive exercises (future).
