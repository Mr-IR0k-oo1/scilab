# Project Templates

## Overview

Project Templates are pre-configured starting points that give students and engineers a complete, working project scaffold for specific engineering domains. Instead of beginning with an empty editor and building everything from scratch, a user selects a template and immediately has runnable scripts, sample data, configuration files, documentation, and a pre-built GUI — all verified to work together.

Templates are the bridge between abstract Scilab capabilities and concrete engineering tasks. They encode domain expertise: which functions to call, how to set up parameters, what visualizations to produce, and how to interpret results.

---

## Template Architecture

### Template Format

Each template is a self-contained directory with a standardized structure:

```
template_name/
├── manifest.yaml            # Template metadata and configuration
├── README.md                # Human-readable description
├── scripts/                 # Scilab scripts
│   ├── main.sce             # Entry point
│   ├── setup.sce            # Initialization and toolbox loading
│   ├── analysis.sce         # Core computation
│   ├── visualize.sce        # Plotting and visualization
│   └── utils.sce            # Helper functions
├── data/                    # Sample or reference data
│   ├── input/               # Input datasets
│   └── expected/            # Expected output for validation
├── config/                  # Configuration files
│   ├── parameters.yaml      # User-configurable parameters
│   ├── gui.yaml             # GUI layout definition
│   └── defaults.yaml        # Default settings
├── gui/                     # GUI components
│   └── interface.yaml       # Widget definitions and layout
├── docs/                    # Documentation
│   ├── theory.md            # Mathematical background
│   ├── usage.md             # How to use the template
│   └── references.md        # Bibliography
├── tests/                   # Validation tests
│   ├── test_main.sce        # Script execution tests
│   └── test_outputs.sce     # Output correctness tests
└── examples/                # Worked examples
    ├── example_1.sce
    └── example_2.sce
```

### manifest.yaml

```yaml
name: "RC Circuit Bode Analysis"
id: tpl_ee_bode_rc_001
version: 2.1.0
author: "Scilab Studio Team"
license: "MIT"
category: "Control Systems"
subcategory: "Frequency Response"
difficulty: beginner
estimated_time: 45  # minutes
tags: [Bode plot, frequency response, RC circuit, transfer function]
scilab_version: ">=2024.1"
toolboxes_required:
  - control
  - signal
toolboxes_optional:
  - xcos
parameters:
  - name: R
    label: "Resistance (Ω)"
    type: real
    default: 1000
    min: 100
    max: 100000
  - name: C
    label: "Capacitance (F)"
    type: real
    default: 1e-6
    min: 1e-9
    max: 1e-3
output_types: [plot, data, report]
gui_available: true
lab_template_compatible: true
```

### Configuration System

Templates use a layered configuration system:

```yaml
# defaults.yaml (template defaults — do not edit)
R: 1000
C: 1e-6
f_start: 1
f_stop: 1e6
N_points: 500
plot_format: "bode"
output_dir: "./output"

# parameters.yaml (user overrides — edit this)
R: 2200
C: 470e-9
# f_start, f_stop, N_points use defaults
```

Scripts load configuration at runtime:

```scilab
// Load configuration
exec("config/defaults.sce");
exec("config/parameters.sce");  // overrides defaults
```

---

## Template Categories

### Power Systems

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `ps_load_flow` | Newton-Raphson load flow analysis on IEEE bus systems | Intermediate | 90 min |
| `ps_fault_analysis` | Symmetrical and unsymmetrical fault calculations | Advanced | 120 min |
| `ps_protection` | Overcurrent relay coordination and grading | Advanced | 150 min |
| `ps_power_flow_dc` | DC power flow approximation for fast screening | Beginner | 45 min |
| `ps_economic_dispatch` | Generator scheduling with cost minimization | Intermediate | 90 min |
| `ps_state_estimation` | Weighted least squares state estimation | Advanced | 180 min |

**Example: `ps_load_flow`**

The template includes:

- IEEE 14-bus, 30-bus, and 57-bus test systems as data files.
- Newton-Raphson solver with configurable convergence tolerance.
- Visualization of voltage magnitudes, phase angles, and line flows on a single-line diagram.
- Interactive GUI with bus selection, load adjustment, and generation dispatch sliders.
- Output tables: bus voltages, line flows, losses, Jacobian condition number.

### Signal Processing

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `sp_fft_analysis` | FFT computation, windowing, spectral analysis | Beginner | 45 min |
| `sp_filter_design` | FIR and IIR filter design with frequency response | Intermediate | 60 min |
| `sp_wavelet_analysis` | Continuous and discrete wavelet transforms | Advanced | 120 min |
| `sp_spectral_estimation` | PSD estimation (Welch, periodogram, MUSIC) | Intermediate | 75 min |
| `sp_audio_processing` | Audio file analysis, filtering, effects | Beginner | 60 min |
| `sp_digital_comm` | Digital modulation (ASK, FSK, PSK, QAM) | Intermediate | 90 min |

**Example: `sp_fft_analysis`**

- Input: arbitrary signal (built-in waveforms or user-uploaded audio).
- Configurable FFT length, window function (Hanning, Hamming, Blackman, Kaiser), and overlap.
- Output: time-domain plot, magnitude spectrum, phase spectrum, power spectral density.
- GUI: signal selector, window type dropdown, FFT length slider, frequency axis toggle (Hz/rad/s).

### Machine Learning

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `ml_classification` | KNN, SVM, decision tree classification | Intermediate | 90 min |
| `ml_regression` | Linear, polynomial, ridge, lasso regression | Beginner | 60 min |
| `ml_clustering` | K-means, DBSCAN, hierarchical clustering | Intermediate | 75 min |
| `ml_nn_basics` | Simple neural network for function approximation | Advanced | 120 min |
| `ml_pca` | Principal component analysis and dimensionality reduction | Intermediate | 60 min |
| `ml_cross_validation` | Train/test split, k-fold CV, performance metrics | Beginner | 45 min |

**Example: `ml_classification`**

- Built-in datasets: Iris, Wine, Breast Cancer Wisconsin.
- Configurable classifier type, hyperparameters, train/test split ratio.
- Output: confusion matrix, ROC curve, precision/recall/F1 metrics, decision boundary visualization.
- GUI: dataset selector, classifier dropdown, hyperparameter sliders, metric toggles.

### Optimization

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `opt_linear` | Simplex method for linear programming | Intermediate | 60 min |
| `opt_nonlinear` | Gradient descent, Newton's method, BFGS | Intermediate | 75 min |
| `opt_constrained` | SQP and interior-point methods | Advanced | 120 min |
| `opt_genetic` | Genetic algorithm for global optimization | Advanced | 90 min |
| `opt_multiobj` | Pareto front computation (NSGA-II) | Advanced | 150 min |
| `opt_sensitivity` | Sensitivity analysis of optimization solutions | Intermediate | 60 min |

### Control Systems

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `ctrl_pid` | PID controller design and tuning | Beginner | 45 min |
| `ctrl_state_space` | State-space modeling and pole placement | Intermediate | 75 min |
| `ctrl_frequency` | Bode, Nyquist, and Nichols analysis | Intermediate | 60 min |
| `ctrl_robust` | H-infinity robust control design | Advanced | 180 min |
| `ctrl_discrete` | Discrete-time control systems and Z-transform | Intermediate | 75 min |
| `ctrl_nonlinear` | Nonlinear system analysis (describing function, describing function) | Advanced | 120 min |

### Image Processing

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `img_segmentation` | Thresholding, region growing, watershed | Intermediate | 75 min |
| `img_filtering` | Spatial and frequency domain filtering | Beginner | 45 min |
| `img_features` | Edge detection, corner detection, HOG | Intermediate | 60 min |
| `img_morphology` | Erosion, dilation, opening, closing | Beginner | 45 min |
| `img_recognition` | Template matching and feature-based recognition | Advanced | 120 min |
| `img_restoration` | Deblurring, denoising, inpainting | Advanced | 90 min |

### Robotics

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `rob_kinematics` | Forward and inverse kinematics for serial arms | Intermediate | 90 min |
| `rob_dynamics` | Lagrangian dynamics, Newton-Euler formulation | Advanced | 150 min |
| `rob_path_planning` | A*, RRT, potential field methods | Advanced | 120 min |
| `rob_pid_control` | Robot joint PID control with trajectory tracking | Intermediate | 90 min |
| `rob_vision` | Camera calibration and visual servoing | Advanced | 180 min |
| `rob_slam` | Simultaneous localization and mapping basics | Advanced | 180 min |

### Renewable Energy

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `re_solar_pv` | PV panel modeling and MPPT analysis | Intermediate | 75 min |
| `re_wind_turbine` | Wind turbine power curve and capacity factor | Intermediate | 60 min |
| `re_hybrid_system` | Solar-wind-battery hybrid system sizing | Advanced | 120 min |
| `re_grid_integration` | Grid-connected inverter control | Advanced | 150 min |
| `re_energy_storage` | Battery modeling and charge management | Intermediate | 75 min |
| `re_microgrid` | Microgrid power management and islanding | Advanced | 180 min |

### Numerical Methods

| Template | Description | Difficulty | Time |
|---|---|---|---|
| `num_ode` | ODE solvers: Euler, RK4, Adams-Bashforth | Beginner | 45 min |
| `num_pde` | Finite difference for heat, wave, Laplace equations | Intermediate | 90 min |
| `num_interpolation` | Polynomial, spline, and surface interpolation | Beginner | 45 min |
| `num_integration` | Numerical integration (trapezoidal, Simpson, Gauss) | Beginner | 30 min |
| `num_linear_algebra` | Matrix decompositions, eigenvalue problems | Intermediate | 60 min |
| `num_roots` | Root finding: bisection, Newton-Raphson, secant | Beginner | 30 min |

---

## Template Structure

Every template, regardless of domain, includes the following components:

### Scripts

| File | Purpose |
|---|---|
| `main.sce` | Entry point. Loads config, runs analysis, generates output. |
| `setup.sce` | Clears workspace, loads toolboxes, sets paths. |
| `analysis.sce` | Core computation. Parameterized and well-commented. |
| `visualize.sce` | All plotting and visualization code. |
| `utils.sce` | Helper functions reused across scripts. |

### Data

| Directory | Purpose |
|---|---|
| `data/input/` | Sample datasets the template ships with. |
| `data/expected/` | Expected output values for validation tests. |

### Configuration

| File | Purpose |
|---|---|
| `parameters.yaml` | User-editable parameters (the primary customization point). |
| `defaults.yaml` | Template defaults (fallback values). |
| `gui.yaml` | GUI layout and widget definitions. |

### Documentation

| File | Purpose |
|---|---|
| `theory.md` | Mathematical background (LaTeX-enabled). |
| `usage.md` | Step-by-step instructions for using the template. |
| `references.md` | Bibliography and further reading. |

### Tests

| File | Purpose |
|---|---|
| `test_main.sce` | Verifies the main script runs without error. |
| `test_outputs.sce` | Verifies outputs match expected values within tolerance. |

---

## Template Creation Guide

### Step 1 — Define the Problem

Write a clear description of what the template solves:

- What engineering problem does it address?
- What are the inputs and outputs?
- What level of expertise is required?

### Step 2 — Implement the Core Algorithm

Write the core computation in `analysis.sce`. Follow these rules:

- All configurable parameters must be variables at the top of the file.
- No hardcoded file paths.
- No hardcoded constants without comments explaining their origin.
- Include error handling for common failure modes.
- Add inline comments explaining non-obvious steps.

### Step 3 — Add Visualization

Write plotting code in `visualize.sce`. Follow these rules:

- Use descriptive axis labels with units.
- Include legends for multi-series plots.
- Use consistent color schemes across plots.
- Set appropriate axis limits (or use auto-scaling with sensible margins).
- Add titles that include key parameter values.

### Step 4 — Create the GUI

Define the GUI in `gui.yaml`:

```yaml
layout:
  rows: 2
  columns: 2
  widgets:
    - id: param_R
      type: slider
      row: 0
      col: 0
      label: "Resistance (Ω)"
      min: 100
      max: 100000
      default: 1000
      log_scale: true
    - id: param_C
      type: slider
      row: 0
      col: 1
      label: "Capacitance (F)"
      min: 1e-9
      max: 1e-3
      default: 1e-6
      log_scale: true
    - id: plot_bode
      type: plot
      row: 1
      col: 0
      colspan: 2
      source: "visualize.sce::bode_plot"
      reactive: [param_R, param_C]
```

### Step 5 — Write Documentation

- `theory.md`: Explain the math with LaTeX. Assume the reader has the relevant prerequisite knowledge but may not know the specific application.
- `usage.md`: Step-by-step instructions, numbered. Include screenshots if possible.
- `references.md`: At minimum 3 relevant references.

### Step 6 — Write Tests

```scilab
// test_main.sce
// Verify main.sce runs without error
exec("scripts/main.sce");
assert_checktrue(isdef("bode_mag"));
assert_checktrue(isdef("bode_phase"));
assert_checkequal(size(bode_mag, 2), N_points);

// test_outputs.sce
// Verify corner frequency is within 1% of theoretical value
f_c_theoretical = 1 / (2 * %pi * R * C);
f_c_measured = find_corner_frequency(bode_mag, f);
assert_checktrue(abs(f_c_measured - f_c_theoretical) / f_c_theoretical < 0.01);
```

### Step 7 — Package and Validate

1. Run the full test suite.
2. Verify the template loads in the Scilab Studio template browser.
3. Verify the GUI renders and responds to parameter changes.
4. Verify all exported plots and tables are correct.
5. Tag the template version and publish to the registry.

---

## Template Sharing

### Institutional Registry

Each institution running Scilab Studio has a private template registry:

- Instructors publish templates for their courses.
- Students can browse and use templates published by their instructors.
- Department admins can curate and approve templates for widespread use.
- Version history and authorship are tracked.

### Public Registry

Templates can be published to the open Scilab Studio community registry:

- Anyone can browse, download, and use public templates.
- Templates are rated and reviewed by the community.
- Authors receive attribution and usage statistics.
- A moderation pipeline checks for quality, correctness, and licensing.

### Template Versioning

```yaml
versions:
  - version: 1.0.0
    date: 2024-01-15
    changes: "Initial release"
    scilab_compat: ">=2024.1"
  - version: 1.1.0
    date: 2024-03-20
    changes: "Added GUI, improved convergence for edge cases"
    scilab_compat: ">=2024.1"
  - version: 2.0.0
    date: 2024-09-01
    changes: "Rewritten for Scilab 2024.2 API changes, added wavelet support"
    scilab_compat: ">=2024.2"
    breaking: true
```

Semantic versioning is enforced:

- **Major** (X.0.0): Breaking changes to parameters, outputs, or API.
- **Minor** (0.X.0): New features, additional data, GUI improvements.
- **Patch** (0.0.X): Bug fixes, documentation corrections, performance improvements.

---

## Template Customization

### Parameter Override

Users can modify any parameter in `parameters.yaml` without touching the scripts:

```yaml
# Original defaults
R: 1000
C: 1e-6
N_points: 500

# User override
R: 4700
C: 100e-9
N_points: 1000
```

### Script Extension

Users can add custom scripts that build on the template:

```
my_project/
├── (template files...)
├── my_analysis.sce          # Custom analysis extending the template
└── my_visualization.sce     # Custom plots
```

### GUI Modification

Users can modify the GUI layout in the visual editor:

- Add new widgets.
- Remove unnecessary widgets.
- Reorder the layout.
- Change widget types (e.g., slider → text input).

### Config Profile

Users can save named parameter configurations:

```yaml
# config/profiles/experiment_1.yaml
name: "Experiment 1 — High Capacitance"
description: "Testing with C = 10μF to observe low corner frequency"
parameters:
  R: 1000
  C: 10e-6
```

Multiple profiles can be switched between with one click.

---

## Integration with Lab Creator

Templates serve as sources for the Lab Creator module:

1. An instructor selects a template in Lab Creator.
2. Lab Creator pulls the template's scripts, documentation, and GUI.
3. Lab Creator wraps the template content into a full lab structure (objectives, theory, questions, report template).
4. The instructor customizes the generated lab.
5. The lab is deployed to students.

This means that every template in the registry automatically becomes available as a lab source, multiplying the value of each template.

---

## Integration with GUI Builder

Templates with pre-built GUIs integrate with the GUI Builder module:

- The template's `gui.yaml` provides the initial GUI layout.
- GUI Builder loads this layout as a starting point.
- Users can modify the GUI visually without editing YAML.
- Changes are saved back to the project configuration.
- The template author's GUI is preserved as a "default" that can be restored.

---

## Example: Walk Through a Power Systems Template

### Template: `ps_load_flow`

**What it does:**

Performs Newton-Raphson load flow analysis on an IEEE test system. Computes bus voltage magnitudes and phase angles, line flows, and system losses.

### Step 1 — User opens the template

The user navigates to Project Templates → Power Systems → Load Flow Analysis and clicks "Use Template."

A new project is created with all template files copied in. The main script runs immediately, showing the default IEEE 14-bus system results.

### Step 2 — User explores the GUI

The GUI shows:

- **Left panel:** Bus selector (dropdown), load/generation sliders for each bus.
- **Center:** Single-line diagram with voltage magnitude coloring and flow arrows.
- **Right panel:** Summary table (total generation, total load, total losses, max voltage deviation).
- **Bottom:** Convergence plot showing mismatch vs. iteration.

### Step 3 — User modifies parameters

The user switches to the IEEE 30-bus system via a dropdown. The load flow re-runs in under 1 second. The single-line diagram updates to show the 30-bus topology. The user increases load on bus 7 and observes the voltage sag and increased losses.

### Step 4 — User inspects results

The user opens the results table:

```
┌──────┬────────────┬──────────┬────────────┬─────────────┐
│ Bus  │ V (p.u.)   │ δ (deg)  │ P_gen (MW) │ P_load (MW) │
├──────┼────────────┼──────────┼────────────┼─────────────┤
│ 1    │ 1.060      │ 0.00     │ 232.4      │ 0.0         │
│ 2    │ 1.045      │ -4.98    │ 40.0       │ 21.7        │
│ 3    │ 1.010      │ -12.73   │ 0.0        │ 24.3        │
│ ...  │ ...        │ ...      │ ...        │ ...         │
└──────┴────────────┴──────────┴────────────┴─────────────┘
```

### Step 5 — User exports results

The user exports:

- Voltage profile plot as PNG for inclusion in a lab report.
- Results table as CSV for further analysis in Data Architecture.
- Complete project as a shareable bundle for a teammate.

---

## Future Templates

| Template | Category | Description | Status |
|---|---|---|---|
| `ps潮流计算_三相` | Power Systems | Three-phase unbalanced load flow | Planned |
| `sp_语音识别` | Signal Processing | Speech recognition pipeline | Planned |
| `ml_深度学习` | Machine Learning | CNN and RNN basics with Scilab | Research |
| `ctrl_model_predictive` | Control Systems | Model predictive control | Planned |
| `rob_无人机控制` | Robotics | Quadrotor dynamics and control | Research |
| `re_储能优化` | Renewable Energy | Battery energy storage optimization | Planned |
| `img_医学影像` | Image Processing | DICOM loading and medical image analysis | Research |
| `num_有限元` | Numerical Methods | 2D finite element analysis | Research |
| `chem_反应动力学` | Chemical Engineering | Chemical reactor modeling | Planned |
| `civil_结构分析` | Civil Engineering | Frame and truss analysis | Planned |
| `opt_供应链` | Optimization | Supply chain network optimization | Planned |
| `quantum_量子计算` | Quantum Computing | Basic quantum circuit simulation | Research |
