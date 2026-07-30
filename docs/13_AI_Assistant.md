# AI Assistant

## Overview

The AI Assistant is a conversational and context-aware engineering helper embedded throughout Scilab Studio. It assists users with Scilab programming, numerical method selection, debugging, visualization recommendations, and conceptual explanations — acting as a knowledgeable co-pilot that understands both the Scilab environment and the engineering domain.

The assistant is not a general-purpose chatbot. It is a purpose-built tool with deep awareness of the Scilab ecosystem, the user's current project state, and the conventions of engineering computation.

---

## Problem Statement

Students and engineers working with Scilab face recurring friction points:

1. **Syntax confusion.** Scilab's syntax differs from MATLAB, Python, and other languages. Functions have different names, indexing starts at 1 (but some functions return 0-based results), and matrix operations have subtle behavioral differences.

2. **Solver selection.** Choosing the right numerical method for a problem is non-trivial. Should the user solve this ODE with `ode()` (Adams) or `ode45()` (Runge-Kutta)? What about stiff systems — should they use `ode` with the `stiff` option, or switch to `lsoda`? Without guidance, students often pick methods that are slow, inaccurate, or numerically unstable.

3. **Debugging opaque errors.** Scilab error messages are often terse:

   ```
   ?? Error while evaluating function.
   ```

   This tells the user almost nothing about what went wrong.

4. **Visualization decisions.** There are dozens of ways to visualize data — line plots, scatter plots, surface plots, contour plots, heatmaps, bar charts. Choosing the right visualization for the data type and audience requires experience.

5. **Conceptual gaps.** A student might know how to call `bode()` but not understand what a Bode plot represents physically, or why a phase margin below 30° indicates potential instability.

The AI Assistant addresses all five of these pain points.

---

## Architecture

The AI Assistant consists of three core components:

```
┌──────────────────────────────────────────────────────┐
│                   AI Assistant                        │
│                                                      │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  LLM Backend    │  │  Context     │  │  Safety  │ │
│  │                 │  │  Engine      │  │  Layer   │ │
│  └────────┬───────┘  └──────┬───────┘  └─────┬────┘ │
│           │                 │                │      │
│           ▼                 ▼                ▼      │
│  ┌─────────────────────────────────────────────────┐│
│  │            Prompt Engineering Layer              ││
│  │    (domain-specific templates + context injection)││
│  └─────────────────────────────────────────────────┘│
│           │                 │                │      │
│           ▼                 ▼                ▼      │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐│
│  │  Editor   │  │  Chat Panel  │  │  Code Actions  ││
│  │  Inline   │  │  (sidebar)   │  │  (context menu)││
│  └──────────┘  └──────────────┘  └────────────────┘│
└──────────────────────────────────────────────────────┘
```

**LLM Backend.** The language model that generates responses. Configured to use a domain-tuned model optimized for engineering and scientific computing.

**Context Engine.** Gathers and maintains the contextual information needed to produce relevant responses: the user's current file, project structure, Scilab version, loaded toolboxes, recent execution output, and error history.

**Safety Layer.** Validates all assistant outputs before presenting them to the user. Ensures no malicious code is suggested, no dangerous operations are performed without confirmation, and no external data is leaked.

---

## Capabilities

### 1. Convert Mathematical Equations to Scilab Code

The user provides a mathematical equation in any notation (LaTeX, text, handwritten via image upload), and the assistant generates equivalent Scilab code.

**Example interaction:**

> **User:** "Convert this transfer function to Scilab: H(s) = (2s + 3) / (s² + 4s + 5)"
>
> **Assistant:**
> ```scilab
> s = %s;
> H = (2*s + 3) / (s^2 + 4*s + 5);
> 
> // Verify
> disp(H);          // Displays the transfer function
> bode(H);          // Bode plot
> step(H);          // Step response
> pole(H);          // Poles: -2 ± i
> ```

**Supported equation types:**

- Transfer functions (continuous and discrete)
- Differential equations (ODE, PDE)
- Matrix equations
- Integral/differential expressions
- Statistical formulas
- Optimization objective functions and constraints

### 2. Suggest Appropriate Numerical Solvers

Given a problem description, the assistant recommends the best solver with justification.

**Example interaction:**

> **User:** "I have a system of 5 coupled ODEs representing a chemical reaction network. The reactions happen on very different time scales — some fast, some slow."
>
> **Assistant:**
> Your system is **stiff** due to the multi-scale time constants. Use one of:
>
> ```scilab
> // Option 1: ode with stiff solver
> y = ode(y0, t0, t, list(f, params), "stiff");
>
> // Option 2: lsoda (auto-selects stiff/non-stiff)
> y = ode("lsoda", y0, t0, t, list(f, params));
>
> // Option 3: cvode (if SUNDIALS available)
> y = ode("cvode", y0, t0, t, list(f, params));
> ```
>
> **Recommendation:** Start with `ode("lsoda", ...)` — it automatically detects stiffness and switches between Adams (non-stiff) and BDF (stiff) methods. For production use, `cvode` gives the best performance on stiff systems.

**Solver categories covered:**

| Category | Solvers |
|---|---|
| ODE (non-stiff) | `ode` (Adams), `ode45` (RK45), `ode23` (RK23) |
| ODE (stiff) | `ode("stiff")`, `ode("lsoda")`, `ode("cvode")` |
| DAE | `dasrt`, `dassl` |
| BVP | `bvp4c` equivalents |
| Optimization | `fminsearch`, `fsolve`, `linprog`, `quadprog` |
| Linear algebra | `linsolve`, `lu`, `qr`, `svd`, `eig` |
| Interpolation | `interp1`, `spline`, `interp2` |
| Integration | `intg`, `integrate` |

### 3. Recommend Visualization Types for Data

Given a dataset description or actual data, the assistant recommends appropriate chart types.

**Example interaction:**

> **User:** "I have temperature readings from 10 sensors over 24 hours. What's the best way to visualize this?"
>
> **Assistant:**
> For time-series data from multiple sensors, I recommend:
>
> **Primary: Multi-line time plot**
> - X-axis: time (hours)
> - Y-axis: temperature
> - One line per sensor with a legend
> - Best for seeing trends and comparing sensors
>
> ```scilab
> plot(time, temp_matrix');
> xlabel("Time (hours)");
> ylabel("Temperature (°C)");
> legend(sensor_names);
> ```
>
> **Alternative views:**
> - **Heatmap** — sensor × time, good for spotting patterns across all sensors at once
> - **Box plot** — one box per sensor, good for comparing distributions
> - **Small multiples** — separate subplot per sensor, good for detailed individual analysis

### 4. Explain Convergence Problems

When a numerical method fails to converge, the assistant diagnoses the likely cause.

**Example interaction:**

> **User:** "My Newton-Raphson load flow isn't converging. It diverges after iteration 3."
>
> **Assistant:**
> Common causes for Newton-Raphson divergence in load flow:
>
> 1. **Ill-conditioned Jacobian.** Check the condition number:
>    ```scilab
>    disp(cond(J));  // If > 1e12, the system is ill-conditioned
>    ```
> 2. **Poor initial guess.** Flat start (all voltages = 1.0∠0°) is standard but may fail for heavily loaded systems. Try:
>    ```scilab
>    V_init = ones(nbus, 1);  // flat start
>    // or use DC power flow solution as initial guess
>    ```
> 3. **Reactive power limits violated.** A generator may be hitting Q_max, causing a PV bus to switch to PQ. Check for Q limit violations:
>    ```scilab
>    if abs(Q_gen(i)) > Q_max(i) then
>        // Bus switched from PV to PQ — this changes the Jacobian structure
>    end
>    ```
> 4. **Topology issues.** Isolated buses or zero-impedance branches can cause singularities.

### 5. Debug Scilab Scripts

The assistant analyzes error messages, identifies the root cause, and suggests fixes.

**Example interaction:**

> **User:** "I'm getting 'Undefined variable: H' when I call bode(H)"
>
> **Assistant:**
> The variable `H` hasn't been defined yet. Most likely:
>
> 1. The line defining `H` failed silently (check for errors above this line).
> 2. `H` is defined in a different scope or file.
> 3. A semicolon at the end of the previous line suppressed an error:
>    ```scilab
>    s = %s;
>    H = 1/(s + 1);    // <-- check this line
>    bode(H);
>    ```
>
> To verify, run `whos()` before the `bode()` call to see all defined variables.

### 6. Generate Example Datasets

The assistant can create synthetic datasets for testing and experimentation.

**Example interaction:**

> **User:** "Generate a noisy sinusoidal signal at 50 Hz with 10% noise, sampled at 1000 Hz for 1 second."
>
> **Assistant:**
> ```scilab
> fs = 1000;              // Sampling frequency (Hz)
> T = 1;                  // Duration (seconds)
> f = 50;                 // Signal frequency (Hz)
> A = 1;                  // Amplitude
> noise_level = 0.1;      // 10% noise
>
> t = 0:1/fs:T-1/fs;      // Time vector
> signal_clean = A * sin(2 * %pi * f * t);
> noise = noise_level * A * rand(1, length(t), "normal");
> signal_noisy = signal_clean + noise;
>
> // Plot
> subplot(2,1,1);
> plot(t, signal_clean);
> title("Clean signal");
> subplot(2,1,2);
> plot(t, signal_noisy);
> title("Noisy signal");
> ```

### 7. Explain Error Messages

The assistant translates terse Scilab errors into human-readable explanations.

| Scilab Error | Assistant Explanation |
|---|---|
| `Undefined variable: x` | The variable `x` hasn't been created yet. Check that the line defining `x` has been executed. |
| `Incompatible rows` | Two matrices being multiplied have incompatible dimensions. Matrix A must have the same number of columns as rows in B. |
| `Subscript mismatch` | You're trying to access an index that doesn't exist. Matrices are 1-indexed in Scilab. Check if `size(A,1)` is large enough. |
| `Stack overflow detected` | Likely infinite recursion. Check if a function calls itself without a base case. |
| `Division by zero` | A denominator is zero. Add a check: `if den ~= 0 then ...` |

### 8. Suggest Optimization Strategies

The assistant helps users improve their code's performance.

**Example interaction:**

> **User:** "My simulation takes 10 minutes to run. It's a Monte Carlo simulation with 10,000 iterations."
>
> **Assistant:**
> Optimization strategies for Monte Carlo in Scilab:
>
> 1. **Vectorize the loop.** Instead of:
>    ```scilab
>    for i = 1:N
>        results(i) = simulate(params(i,:));
>    end
>    ```
>    Try to rewrite `simulate` to accept a matrix of parameter sets and return a vector of results. Scilab's matrix operations are highly optimized.
>
> 2. **Preallocate memory.** Ensure `results` is initialized before the loop:
>    ```scilab
>    results = zeros(1, N);  // preallocate
>    ```
>
> 3. **Reduce plot calls inside the loop.** Plotting is slow. Collect all data first, plot once at the end.
>
> 4. **Use `parfor` for parallel execution** (if available):
>    ```scilab
>    parfor i = 1:N
>        results(i) = simulate(params(i,:));
>    end
>    ```

---

## Context Engine

The Context Engine maintains awareness of the user's working environment and injects this context into every LLM prompt.

### Context Sources

| Source | Information | Update Frequency |
|---|---|---|
| **Active editor** | Current file content, cursor position, selected text | On change |
| **Project structure** | Files in the project, their names and types | On file system change |
| **Scilab execution engine** | Version, loaded toolboxes, recent output | On execution |
| **Error history** | Last N error messages with stack traces | On error |
| **Data catalog** | Available datasets, their schemas | On data change |
| **User preferences** | Coding style, preferred methods, history of interactions | On change |

### Context Window Management

The context window is limited. The engine prioritizes:

1. The user's immediate question and selected code.
2. The most recent error message (if the user is debugging).
3. Relevant function signatures from Scilab documentation.
4. Project-level configuration (what toolboxes are available).
5. Conversation history (last 5 exchanges).

Older or less relevant context is pruned to stay within the model's context limit.

### Scilab Documentation Indexing

The Context Engine includes a pre-built index of:

- All core Scilab functions with their signatures, parameters, and return values.
- All toolbox functions organized by domain.
- Common error messages and their resolutions.
- Code examples from the official Scilab documentation.
- FAQ entries from the Scilab community.

This index allows the assistant to provide accurate, Scilab-specific answers rather than generic programming advice.

---

## Prompt Engineering

The AI Assistant uses domain-specific prompt templates to ensure high-quality, relevant responses.

### Prompt Structure

Every user interaction is wrapped in a structured prompt:

```
[System Context]
You are an expert Scilab programming assistant specializing in 
[relevant engineering domain]. The user is working on [project type]
using Scilab [version] with [loaded toolboxes] loaded.

[Relevant Documentation]
[Extracted function signatures and documentation]

[User's Current Code]
[Active file content with cursor position marked]

[User's Query]
[user's question or request]

[Response Format]
Provide: 
1. A direct answer
2. Working Scilab code (if applicable)
3. Brief explanation of why this approach works
```

### Domain-Specific Prompt Templates

| Domain | Additional Context Injected |
|---|---|
| Control Systems | Bode, Nyquist, root locus conventions; standard test systems (2nd order, PID) |
| Signal Processing | Window functions, FFT conventions, filter design parameters |
| Power Systems | Bus types (PQ, PV, Slack), per-unit system, standard test cases |
| Machine Learning | Evaluation metrics, cross-validation, preprocessing pipelines |
| Numerical Methods | Convergence criteria, stability regions, error bounds |
| Image Processing | Coordinate systems, pixel value ranges, morphological operations |

---

## Safety Guardrails

### No Code Execution Without Permission

The assistant never executes code on the user's system without explicit consent. When suggesting code:

- Code is presented as text for the user to review and run.
- If the assistant suggests running something, it asks: "Would you like me to run this?"
- The user must explicitly approve execution.

### Validate Suggestions

Before presenting code, the assistant performs:

1. **Syntax check.** Is the Scilab code syntactically valid?
2. **Dimension check.** Do matrix operations have compatible dimensions?
3. **Common pitfall check.** Are there known gotchas (e.g., 0-indexing confusion, missing `%s` for polynomial definition)?
4. **Performance warning.** Flag operations that are known to be slow for large inputs.

### Content Boundaries

The assistant:

- Does not generate code for weapons systems, surveillance, or other harmful applications.
- Does not help circumvent security systems or access controls.
- Does not provide advice that could lead to physical harm (e.g., incorrect structural engineering calculations without appropriate disclaimers).
- Always recommends verification of critical numerical results.

### Data Privacy

The assistant:

- Does not send user code or data to external services unless the user explicitly opts in.
- Processes all context locally when running in offline mode.
- When using cloud LLM backends, transmits only the prompt — not project files, user data, or execution history.
- Logs are anonymized and contain no source code.

---

## Integration Points

### Editor Integration

The AI Assistant is embedded in the Scilab code editor:

| Feature | Description |
|---|---|
| **Autocomplete** | Context-aware function and variable completions |
| **Hover info** | Tooltip with function signature and brief description |
| **Inline suggestions** | Ghost text suggestions as the user types |
| **Quick fixes** | Code actions triggered by error highlighting |
| **Refactoring** | Rename variable across file, extract function, simplify expression |

### Help System Integration

The assistant extends the built-in help system:

- `help bode` shows the official documentation.
- `ask bode` engages the AI assistant for a conversational explanation with examples.
- `ask "why is my bode plot wrong?"` performs contextual debugging.

### Lab Creator Integration

When Lab Creator generates a lab:

- The assistant can draft the theory section.
- The assistant can generate questions from the experiment metadata.
- The assistant can suggest GUI parameter ranges based on the physics of the system.

### Parameter Sweep Studio Integration

The assistant helps design sweep configurations:

- Suggests parameter ranges based on the system's expected behavior.
- Recommends the number of sweep points for adequate resolution.
- Interprets sweep results and highlights interesting regions.

### Report Generator Integration

The assistant assists with report writing:

- Drafts abstracts and methodology sections from experiment data.
- Suggests discussion points based on the results.
- Reviews and improves user-written text for clarity and technical accuracy.

---

## User Interface

### Chat Panel

The primary interaction mode is a sidebar chat panel:

```
┌──────────────────────────────┐
│  AI Assistant                │
├──────────────────────────────┤
│                              │
│  [User] How do I compute    │
│  the FFT of a signal?       │
│                              │
│  [Assistant] To compute     │
│  the FFT in Scilab:         │
│                              │
│  // y is your signal        │
│  // fs is sampling freq     │
│  Y = fft(y);                │
│  f = (0:length(y)-1)*fs/    │
│      length(y);             │
│  plot(f, abs(Y));           │
│                              │
│  For better frequency       │
│  resolution, use a window:  │
│  Y = fft(y .* hamming(...));│
│                              │
│  [User] What window should  │
│  I use for a narrowband     │
│  signal?                    │
│                              │
│  ┌─────────────────────┐    │
│  │ Type a message...   │    │
│  └─────────────────────┘    │
└──────────────────────────────┘
```

### Inline Suggestions

In the editor, the assistant provides ghost text suggestions:

```scilab
s = %s;
H = 1/(s^2 + 2*0.5*s + 1);    // ← ghost text appears here
                                //   suggesting: "bode(H);  // Bode plot"
```

The user accepts with Tab or dismisses with Escape.

### Code Actions

Right-clicking on code or error messages provides AI-powered actions:

- "Explain this code" → natural language explanation
- "Fix this error" → suggested correction
- "Optimize this function" → performance improvement suggestions
- "Add comments" → auto-generate inline documentation
- "Write tests" → generate unit tests for the function
- "Convert to Scilab" → translate from MATLAB/Python/other language

### Command Palette

Quick access via keyboard shortcut:

- `Ctrl+Shift+A` → Open AI Assistant chat
- `Ctrl+Shift+E` → Explain selected code
- `Ctrl+Shift+F` → Fix error at cursor
- `Ctrl+Shift+S` → Suggest solver for current problem

---

## Learning Mode

The assistant can switch to a pedagogical mode that prioritizes teaching over solution-providing:

### Concept Explanations

Instead of just giving the answer, the assistant explains the underlying concept:

> **User:** "What does eigenvalue decomposition do?"
>
> **Assistant:**
> Eigenvalue decomposition breaks a square matrix A into:
>
> A = V × D × V⁻¹
>
> where D is a diagonal matrix of eigenvalues and V contains the eigenvectors.
>
> **Intuition:** Think of A as a transformation. Eigenvectors are the directions that don't change direction when the transformation is applied — they only get scaled. Eigenvalues tell you the scaling factor.
>
> **In engineering:**
> - **Structural analysis:** Eigenvalues = natural frequencies, eigenvectors = mode shapes
> - **Control systems:** Eigenvalues = pole locations, determine stability
> - **Image processing:** Principal components (eigenvectors of covariance matrix) capture the most variance
>
> **Want to try it?** Here's a hands-on example...

### Suggested Tutorials

The assistant references relevant Spoken Tutorial content:

> This concept is covered in the Spoken Tutorial "Introduction to Scilab — Matrices." Would you like me to open it?

### Progressive Hints

When the user is stuck on a problem, the assistant provides hints in order of subtlety:

1. **Hint 1 (vague):** "Think about what happens to the denominator when ω approaches zero."
2. **Hint 2 (moderate):** "Try evaluating the transfer function at ω = 0 and ω = ∞."
3. **Hint 3 (specific):** "At DC (ω = 0), the transfer function evaluates to K/a. At high frequency, it approaches 0."

The user controls how many hints they see.

---

## Limitations

The AI Assistant has clear, documented limitations:

| Limitation | Description |
|---|---|
| **No real-time execution** | The assistant cannot run Scilab code in real time to verify results. All code suggestions are based on pattern matching and documentation knowledge. |
| **No custom model training** | The assistant uses a pre-trained model. It cannot be fine-tuned on institution-specific codebases (yet). |
| **No guaranteed accuracy** | Like all LLMs, the assistant can produce incorrect or hallucinated information. Users must verify all suggestions, especially for numerical results. |
| **Limited to Scilab** | The assistant does not provide cross-language advice (e.g., "here's how to do this in MATLAB instead") unless explicitly asked. |
| **No file system access** | The assistant cannot read files outside the current project or execute arbitrary system commands. |
| **No network access** | The assistant cannot fetch external data, check live documentation, or access online resources unless specifically enabled. |
| **Context window limits** | For very large files (>10,000 lines), the assistant may lose context about earlier parts of the code. |
| **No multi-user collaboration** | The assistant is per-user. It does not share context or conversation history between users. |
| **Numerical precision** | The assistant may not account for floating-point precision issues in its suggested code. |

### Disclaimer

A visible disclaimer appears in the assistant panel:

> AI-generated suggestions should be reviewed and verified. This tool is intended for educational assistance, not as a replacement for engineering judgment.

---

## Privacy and Data Handling

### Data Flow

```
User's code ──→ Context Engine ──→ Prompt ──→ LLM ──→ Response ──→ Safety Layer ──→ User
                                          │
                                          ▼
                                   [If cloud LLM]
                                   Encrypted transit (TLS 1.3)
                                   No code stored
                                   No user identity transmitted
```

### Privacy Policies

| Aspect | Policy |
|---|---|
| **Code storage** | User code is never stored by the LLM provider. Processing is stateless. |
| **Conversation history** | Stored locally on the user's machine. Encrypted at rest. |
| **Telemetry** | Optional, anonymized usage statistics (error types, feature usage). No code content. |
| **Cloud vs. local** | Users choose between cloud LLM (better quality, requires internet) and local LLM (privacy-first, lower quality). |
| **Data retention** | Local conversation history is retained for 30 days by default, configurable. |
| **FERPA compliance** | For educational deployments, student data is never shared with third parties. |
| **GDPR compliance** | Right to deletion, data export, and consent management are supported. |

### Opt-in / Opt-out

- Cloud LLM processing: opt-in, off by default.
- Telemetry: opt-in, off by default.
- Local LLM: always available, no opt-in needed.
- Code examples used for model improvement: opt-in, off by default.

---

## Future Enhancements

| Enhancement | Description | Priority |
|---|---|---|
| **Multi-modal input** | Accept screenshots of equations, diagrams, or handwritten notes as input | High |
| **Voice interaction** | Speak questions and receive spoken explanations | Low |
| **Collaborative sessions** | Multiple users can interact with the same assistant instance | Medium |
| **Custom knowledge base** | Institution-specific documentation and code examples integrated into context | High |
| **Fine-tuned models** | Domain-specific models trained on Scilab codebases and engineering textbooks | Medium |
| **Real-time code execution** | Sandbox for executing assistant-suggested code and showing results inline | Medium |
| **Version-aware suggestions** | Assistant knows the user's Scilab version and suggests version-appropriate code | High |
| **Integration with Spoken Tutorials** | Assistant can launch relevant video tutorials mid-conversation | Medium |
| **Error pattern learning** | System learns from resolved errors to improve future suggestions | Medium |
| **Cross-module awareness** | Assistant can reference Parameter Sweep results, Data Architecture contents, and Visualization outputs in responses | High |
| **Accessibility** | Screen reader support, high-contrast mode, keyboard-only navigation for the assistant panel | Medium |
| **Multi-language support** | Respond in the user's preferred language | Low |
| **Offline mode improvements** | Better local LLM performance through quantization and caching | Medium |
| **Assessment assistance** | Help instructors create rubrics, grade student code, and provide feedback | Low |
