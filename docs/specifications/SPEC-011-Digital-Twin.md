# SPEC-011 — Digital Twin

## Purpose

Model physical systems as real-time digital counterparts. Connect simulation models to live data, visualize system state, and run what-if scenarios.

---

## Concept

A Digital Twin is a Scilab simulation model that:
1. Receives live data from sensors or data streams.
2. Updates its internal state in real-time.
3. Predicts future behavior.
4. Allows parameter adjustment and scenario testing.

---

## Components

### Model Editor
- Visual block diagram editor (v0.3).
- Scilab script-based models (v0.1).
- Parameter configuration panel.
- Model validation and syntax checking.

### Data Connector
- Connect to live data sources (CSV streams, sensor APIs, Scilab variables).
- Configure data mapping (sensor → model variable).
- Set update frequency.
- Handle data gaps and errors.

### Simulation Engine
- Run Scilab simulation in real-time.
- Step-by-step execution with configurable time step.
- Pause, resume, step forward/backward.
- Record simulation history.

### Visualization Dashboard
- Real-time charts showing model state.
- Parameter sliders for live adjustment.
- Comparison view (simulated vs actual).
- Alert thresholds (e.g., temperature > 100°C).

### Scenario Manager
- Save parameter sets as scenarios.
- Run multiple scenarios in parallel.
- Compare results side-by-side.
- Export scenario results.

---

## Data Flow

```
Live Data Source
  │
  ▼
Data Connector (map, validate, buffer)
  │
  ▼
Simulation Engine (update model state)
  │
  ▼
State Snapshot (capture model variables)
  │
  ├──► Visualization Dashboard (real-time display)
  ├──► Scenario Manager (record for comparison)
  └──► Data Export (save to file)
```

---

## Model Types

### Script-Based (v0.1)
Scilab scripts that define system dynamics:
```scilab
function dxdt = dynamics(t, x, params)
    // System of ODEs
    dxdt = [-params.k * x(1) + params.u];
endfunction
```

### Block Diagram (v0.3)
Visual block editor using Xcos-style blocks:
- Integrators, gains, sum blocks.
- Transfer functions.
- Custom Scilab function blocks.

### Hybrid (v0.4)
Combination of script and block diagram models.

---

## Real-Time Sync

### Update Modes

| Mode | Description |
|------|-------------|
| push | Data source pushes updates to the twin |
| poll | Twin polls the data source at configurable intervals |
| manual | User manually feeds data to the twin |

### Update Frequency

| Frequency | Use Case |
|-----------|----------|
| 100ms | High-frequency sensor data |
| 1s | Standard monitoring |
| 10s | Slow-changing systems |
| manual | Offline analysis |

---

## What-If Scenarios

1. User adjusts parameters via sliders.
2. Simulation runs with new parameters.
3. Results are compared against baseline.
4. Differences are highlighted visually.
5. Scenario is saved for later comparison.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max simultaneous scenarios | 10 |
| Max simulation history | 10,000 time steps |
| Max model variables | 500 |
| Real-time update max frequency | 100ms |
| Scenario comparison max | 5 scenarios side-by-side |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Data source disconnected | Show "Offline" indicator, use last known values |
| Simulation diverges | Show warning, offer to reset parameters |
| Model syntax error | Show error with line number |
| Memory limit exceeded | Pause simulation, offer to reduce history |
| Time step too small | Warn user, suggest larger step |

---

## Extension Points

- Custom data connectors (OPC-UA, MQTT, REST API).
- Custom model types.
- Custom visualization widgets.
- Custom alert rules.
- Model import/export (Simulink, Xcos).
