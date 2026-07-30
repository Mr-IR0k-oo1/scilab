# Scilab Studio — Digital Twin Framework

## 1. Overview

The Digital Twin Framework enables engineers to create virtual replicas of
physical assets — buildings, machines, power grids, water systems — that are
synchronized with real-time sensor data and driven by mathematical models
executed through the Scilab engine. Each digital twin is a composable unit
with defined assets, sensors, relationships, and computation models that can
be visualized, simulated, and analyzed.

---

## 2. Framework Architecture

### 2.1 Architecture Diagram

```
+------------------------------------------------------------------+
|                  DIGITAL TWIN FRAMEWORK                            |
|                                                                    |
|  +-------------------+  +------------------+  +----------------+  |
|  |  Asset Model       |  |  Sensor Model    |  | Relationship   |  |
|  |                    |  |                  |  | Model          |  |
|  |  - Types           |  |  - Sensor types  |  |                |  |
|  |  - Properties      |  |  - Calibration   |  | - Hierarchical |  |
|  |  - Hierarchy       |  |  - Sampling      |  | - Spatial      |  |
|  |  - Metadata        |  |  - Drift model   |  | - Functional   |  |
|  +--------+-----------+  +--------+---------+  | - Causal       |  |
|           |                       |             +-------+--------+  |
|           +-----------+-----------+                     |          |
|                       |                                  |          |
|                       v                                  v          |
|           +---------------------+           +------------------+  |
|           |  Twin Registry       |<--------->| Relationship     |  |
|           |  (instances, state,  |           | Graph            |  |
|           |   history)           |           | (Neo4j-like)     |  |
|           +----------+----------+           +------------------+  |
|                      |                                            |
|           +----------v----------+                                |
|           |  Computation Engine  |                                |
|           |                      |                                |
|           |  - ODE solver        |                                |
|           |  - PDE solver        |                                |
|           |  - Statistical       |                                |
|           |  - ML inference      |                                |
|           |  - Hybrid models     |                                |
|           |  - Scilab integration|                                |
|           +----------+----------+                                |
|                      |                                            |
|           +----------v----------+                                |
|           |  Data Integration    |                                |
|           |                      |                                |
|           |  - MQTT subscriber   |                                |
|           |  - REST polling      |                                |
|           |  - File watcher      |                                |
|           |  - Simulation mode   |                                |
|           +----------+----------+                                |
|                      |                                            |
|           +----------v----------+                                |
|           |  Visualization       |                                |
|           |                      |                                |
|           |  - 3D rendering      |                                |
|           |  - Dashboards        |                                |
|           |  - Alerts            |                                |
|           |  - Trend lines       |                                |
|           +---------------------+                                |
+------------------------------------------------------------------+
```

### 2.2 Core Concepts

| Concept | Description |
|---|---|
| **Asset** | A physical or logical entity (building, motor, pipe) |
| **Sensor** | A measurement point on an asset (temperature, pressure, flow) |
| **Relationship** | A connection between assets (contains, feeds, powers) |
| **Mathematical Model** | Equations that predict asset behavior |
| **Time Series** | Ordered data points from sensors or simulations |
| **Twin Instance** | A running digital twin with live state and history |
| **Simulation** | Forward execution of models without live data |

---

## 3. Core Concepts

### 3.1 Concept Relationships

```
+-----------+       +-----------+       +-------------+
|   Asset   |1----N|  Sensor   |1----N| Time Series  |
|           |       |           |       |              |
| id        |       | id        |       | timestamp[]  |
| type      |       | assetId   |       | values[]     |
| name      |       | type      |       | quality[]    |
| props     |       | unit      |       | metadata     |
| metadata  |       | sampleRate|       +--------------+
+-----+-----+       | calibration|
      |              +-----+-----+
      |                    |
      | N               N |
      |                    |
+-----v-----+       +-----v-----+
|Relation-  |       | Math Model |
|  ship     |       |            |
|           |       | type: ODE  |
| source    |       | equations  |
| target    |       | params     |
| type      |       | solver     |
| weight    |       | inputs     |
+-----------+       | outputs    |
                    +------------+
```

---

## 4. Asset Definition

### 4.1 Asset Types

| Category | Types | Description |
|---|---|---|
| **Building** | Room, Floor, Zone, Wing | HVAC zones, occupancy areas |
| **Equipment** | Motor, Pump, Compressor, Fan, Valve | Rotating and static equipment |
| **Electrical** | Generator, Transformer, Bus, Load, Breaker | Power system components |
| **Hydraulic** | Pipe, Tank, Reservoir, Pump Station | Water and fluid systems |
| **Process** | Heat Exchanger, Boiler, Cooling Tower | Thermal process equipment |
| **Renewable** | Solar Panel, Wind Turbine, Battery | Energy generation/storage |
| **Infrastructure** | Road, Bridge, Pipeline | Civil infrastructure |
| **Custom** | User-defined types | Any physical entity |

### 4.2 Asset Definition Schema

```jsonc
{
  "id": "asset-hvac-ahu-01",
  "type": "equipment.ahu",
  "name": "AHU-01 (Main Building)",
  "description": "Primary air handling unit for zones A1-A4",

  "properties": {
    "manufacturer": "Carrier",
    "model": "42AH012",
    "serialNumber": "SN-2024-001",
    "installDate": "2023-06-15",
    "ratedAirflow": { "value": 5000, "unit": "CFM" },
    "ratedPower": { "value": 15, "unit": "kW" },
    "efficiency": { "value": 0.85, "unit": "ratio" },
    "designTemperature": { "value": 22, "unit": "C" }
  },

  "hierarchy": {
    "parent": "building-main",
    "children": ["zone-a1", "zone-a2", "zone-a3", "zone-a4"]
  },

  "sensors": ["sensor-ahu01-temp-supply", "sensor-ahu01-temp-return",
              "sensor-ahu01-fan-speed", "sensor-ahu01-power"],

  "models": ["model-ahu-thermal"],

  "metadata": {
    "location": { "lat": 37.7749, "lng": -122.4194 },
    "floor": 1,
    "room": "Mechanical Room B",
    "criticality": "high"
  }
}
```

### 4.3 Asset Hierarchy

```
Building: Main Campus
|
+-- Floor 1
|   +-- Zone A1 (Office)
|   |   +-- AHU-01 (Air Handler)
|   |   |   +-- Sensor: Supply Temp
|   |   |   +-- Sensor: Return Temp
|   |   |   +-- Sensor: Fan Speed
|   |   |   +-- Sensor: Power
|   |   +-- VAV-101 (Damper)
|   |   +-- VAV-102 (Damper)
|   +-- Zone A2 (Lab)
|   |   +-- AHU-02
|   |   +-- Fume Hood Controller
|   +-- Electrical Room
|       +-- Transformer T-01
|       +-- Breaker Panel BP-01
|
+-- Floor 2
|   +-- Zone B1
|   +-- Zone B2
|
+-- Rooftop
    +-- Cooling Tower CT-01
    +-- Solar Array SA-01
    |   +-- Panel Group 1
    |   +-- Panel Group 2
    +-- Exhaust Fan EF-01
```

---

## 5. Sensor Model

### 5.1 Sensor Types

| Type | Unit | Description | Typical Rate |
|---|---|---|---|
| Temperature | C / F | Thermal measurement | 1-60 Hz |
| Pressure | Pa / bar / psi | Fluid/gas pressure | 1-100 Hz |
| Flow | L/s / CFM / m3/h | Volumetric flow rate | 0.1-10 Hz |
| Power | W / kW / MW | Electrical power | 1 Hz |
| Voltage | V / kV | Electrical potential | 60 Hz |
| Current | A | Electrical current | 60 Hz |
| Vibration | mm/s / g | Mechanical vibration | 1-10 kHz |
| Humidity | %RH | Relative humidity | 0.1 Hz |
| Level | m / ft | Liquid level | 0.1-1 Hz |
| Speed | RPM | Rotational speed | 1-100 Hz |
| Torque | Nm | Rotational force | 1-100 Hz |
| Acoustic | dB | Sound level | 1-10 Hz |
| Air Quality | ppm / AQI | CO2, PM2.5, VOC | 0.1 Hz |
| Custom | User-defined | Any measurable quantity | Variable |

### 5.2 Sensor Definition

```jsonc
{
  "id": "sensor-ahu01-temp-supply",
  "type": "temperature",
  "name": "AHU-01 Supply Air Temperature",
  "assetId": "asset-hvac-ahu-01",

  "sampling": {
    "rate": 1,            // samples per second
    "mode": "periodic",   // periodic | on-change | event-driven
    "buffer": 3600,       // ring buffer size (1 hour at 1Hz)
    "aggregation": {
      "1min": "average",
      "5min": "average",
      "1hour": "average",
      "1day": ["min", "max", "average"]
    }
  },

  "calibration": {
    "offset": 0.0,
    "scale": 1.0,
    "unit": "C",
    "range": { "min": -40, "max": 85 },
    "accuracy": { "value": 0.25, "unit": "C" },
    "lastCalibrated": "2026-01-15T10:00:00Z",
    "calibrationCertificate": "CAL-2026-001"
  },

  "drift": {
    "model": "linear",
    "ratePerYear": 0.05,   // 0.05 C per year
    "lastDriftCheck": "2026-06-01",
    "nextCalibration": "2027-01-15"
  },

  "quality": {
    "method": "limit_check",
    "limits": { "min": 10, "max": 35 },
    "rateOfChange": { "maxPerSecond": 2.0 },
    "stuckSensor": { "window": 300, "threshold": 0.001 }
  },

  "source": {
    "type": "mqtt",
    "broker": "mqtt://building.local:1883",
    "topic": "sensors/ahu01/temp/supply",
    "decode": "json",
    "field": "value"
  }
}
```

### 5.3 Sensor Data Pipeline

```
Physical Sensor
      |
      v
+-------------+     +-------------+     +-------------+
| Acquisition |---->| Calibration |---->| Quality     |
| (read raw)  |     | (offset,    |     | Check       |
|             |     |  scale,     |     | (limits,    |
|             |     |  linearize) |     |  rate,      |
|             |     |             |     |  stuck)     |
+-------------+     +-------------+     +------+------+
                                             |
                                    +--------+--------+
                                    |                  |
                              [PASS]              [FAIL]
                                    |                  |
                                    v                  v
                            +-------------+    +-------------+
                            | Ring Buffer  |    | Alarm       |
                            | (in-memory)  |    | (sensor     |
                            |              |    |  fault)     |
                            +------+------+    +-------------+
                                   |
                                   v
                            +-------------+
                            | Time Series |
                            | Store       |
                            +-------------+
```

---

## 6. Relationship Model

### 6.1 Relationship Types

| Type | Description | Example |
|---|---|---|
| **Hierarchical** | Parent-child containment | Building contains Floor contains Room |
| **Spatial** | Physical proximity or location | Pipe connects Tank to Pump |
| **Functional** | Operational dependency | Pump powers Cooling Tower |
| **Causal** | Cause-effect interaction | Motor vibration causes Bearing wear |
| **Energy** | Energy flow connection | Generator supplies Bus |
| **Material** | Material flow connection | Pipe feeds Boiler with water |
| **Information** | Data flow connection | Sensor publishes to Dashboard |
| **Temporal** | Time-based sequence | Startup causes Warmup leads to Operating |

### 6.2 Relationship Schema

```jsonc
{
  "id": "rel-001",
  "type": "functional",
  "subtype": "powers",
  "source": "transformer-t01",
  "target": "bus-main",
  "properties": {
    "capacity": { "value": 500, "unit": "kVA" },
    "currentLoad": { "value": 320, "unit": "kVA" },
    "loadFactor": 0.64
  },
  "direction": "unidirectional",  // or "bidirectional"
  "bidirectional": false
}
```

### 6.3 Relationship Graph

```
  +-------------+     powers     +-------------+
  | Transformer |--------------->| Main Bus    |
  | T-01        |                |             |
  +-------------+                +------+------+
                                        |
                                   feeds |
                                        v
                                 +-------------+
                                 | Panel BP-01 |
                                 +------+------+
                                        |
                              +---------+---------+
                              |                   |
                         powers              powers
                              |                   |
                              v                   v
                       +----------+        +----------+
                       | HVAC     |        | Lighting |
                       | System   |        | System   |
                       +----------+        +----------+

  Graph traversal queries:
  - "What does T-01 power?" -> BP-01 -> HVAC, Lighting
  - "What feeds the HVAC?"  -> BP-01 -> T-01
  - "Critical path to HVAC?" -> T-01 -> BP-01 -> HVAC
```

---

## 7. Mathematical Models

### 7.1 Model Types

| Type | Description | Scilab Functions |
|---|---|---|
| **ODE** | Ordinary differential equations | `ode()`, `dasrt()`, `dassl()` |
| **PDE** | Partial differential equations | `pde()` (finite element) |
| **Statistical** | Regression, time series | `regress()`, `ar()`, `arma()` |
| **ML-based** | Neural networks, trees | `nntool`, custom `.sci` |
| **Hybrid** | Combinations of above | Custom composition |
| **Empirical** | Lookup tables, curves | `interp1()`, `spline()` |
| **Transfer Function** | Laplace domain models | `tf()`, `freq()` |
| **State Space** | Linear system models | `ss2tf()`, `tf2ss()` |

### 7.2 Model Definition

```jsonc
{
  "id": "model-ahu-thermal",
  "name": "AHU Thermal Model",
  "type": "ode",
  "assetId": "asset-hvac-ahu-01",

  "equations": {
    "description": "First-order thermal model of air handling unit",
    "variables": {
      "T_supply": { "type": "state", "unit": "C", "description": "Supply air temp" },
      "T_return": { "type": "input", "unit": "C", "description": "Return air temp" },
      "T_outdoor": { "type": "input", "unit": "C", "description": "Outdoor temp" },
      "Q_cooling": { "type": "input", "unit": "kW", "description": "Cooling capacity" },
      "m_dot": { "type": "input", "unit": "kg/s", "description": "Air mass flow" },
      "cp_air": { "type": "param", "value": 1.005, "unit": "kJ/kg/K" },
      "tau": { "type": "param", "value": 120, "unit": "s", "description": "Time constant" }
    },
    "scilab": "d(T_supply)/dt = (m_dot * cp_air * (T_return - T_supply) - Q_cooling) / (tau * m_dot * cp_air)"
  },

  "parameters": {
    "tau": { "nominal": 120, "range": [60, 300], "estimateFrom": "step_response" },
    "cp_air": { "nominal": 1.005, "fixed": true }
  },

  "solver": {
    "method": "ode45",
    "stepSize": 1.0,
    "tolerance": 1e-6,
    "maxStep": 10.0
  },

  "calibration": {
    "method": "least_squares",
    "dataRange": ["2026-01-01", "2026-06-30"],
    "metrics": {
      "RMSE": 0.5,
      "R_squared": 0.94,
      "MAE": 0.3
    }
  }
}
```

### 7.3 Model Execution in Scilab

```scilab
// AHU Thermal Model - executed by computation engine
function dTdt = ahu_thermal_model(t, T_supply, T_return, T_outdoor, Q_cooling, m_dot)
    cp_air = 1.005;   // kJ/kg/K
    tau = 120;         // s (time constant)

    // Heat balance
    Q_air_in = m_dot * cp_air * (T_return - T_supply);
    Q_removed = Q_cooling;

    // First-order ODE
    dTdt = (Q_air_in - Q_removed) / (tau * m_dot * cp_air);
endfunction

// Solver invocation
tspan = 0:1:3600;   // 1 hour, 1 second steps
T0 = 22;             // Initial supply temperature
T_supply = ode(T0, tspan, list(ahu_thermal_model, T_return, T_outdoor, Q_cooling, m_dot));
```

---

## 8. Computation Engine

### 8.1 Solver Selection

```
+------------------------------------------------------------------+
|  SOLVER SELECTION MATRIX                                          |
|                                                                    |
|  Model Type    | Stiff? | Events? | Recommended Solver           |
|  ------------- | ------ | ------- | --------------------------   |
|  ODE (non-stiff)| No    | No      | ode45 (Runge-Kutta)          |
|  ODE (stiff)   | Yes   | No      | ode15s (BDF)                 |
|  ODE with events| Any  | Yes     | dasrt (root finding)         |
|  DAE           | Yes   | No      | dassl (DAE solver)           |
|  PDE (1D)      | -     | No      | pdepe (method of lines)      |
|  PDE (2D/3D)   | -     | No      | FEM via Scilab toolbox       |
|  Discrete      | -     | No      | Direct iteration             |
|  Stochastic    | -     | -       | Euler-Maruyama / Milstein    |
|  Optimization  | -     | -       | fsolve / fmincon             |
+------------------------------------------------------------------+
```

### 8.2 Parallel Execution

```
+-----------------------------------------------------------+
|  PARALLEL COMPUTATION                                       |
|                                                             |
|  Twin Instance A          Twin Instance B                   |
|  +----------------+      +----------------+                |
|  | Model: HVAC    |      | Model: Power   |                |
|  | Solver: ode45  |      | Solver: dasrt  |                |
|  | Step: 1s       |      | Step: 0.01s    |                |
|  +-------+--------+      +-------+--------+                |
|          |                      |                           |
|          v                      v                           |
|  +--------------------------------------------------+     |
|  |  Scilab Engine Pool (N workers)                   |     |
|  |                                                    |     |
|  |  Worker 1: [Model A, step 1]                      |     |
|  |  Worker 2: [Model B, step 1]                      |     |
|  |  Worker 3: [Model A, step 2]                      |     |
|  |  Worker 4: [Model B, step 2]                      |     |
|  |  ...                                               |     |
|  +--------------------------------------------------+     |
|                                                             |
|  Scaling:                                                   |
|  - Independent twins run on separate workers               |
|  - Coupled twins coordinate via shared state               |
|  - Worker pool sized to CPU core count (default: N-1)      |
|  - Queue-based scheduling with priority support            |
+-----------------------------------------------------------+
```

### 8.3 Caching Strategy

| Cache Level | Content | TTL | Size |
|---|---|---|---|
| L1 (Per-model) | Last computed state | Until next step | 1 KB |
| L2 (Per-twin) | Recent time series | 1 hour | 10 MB |
| L3 (Global) | Shared computations | 5 minutes | 100 MB |
| Scilab Eval | Intermediate variables | Until reeval | 50 MB |

---

## 9. Real-Time Data Integration

### 9.1 Data Source Types

```
+------------------------------------------------------------------+
|  DATA INTEGRATION SOURCES                                         |
|                                                                    |
|  +----------+    +----------+    +----------+    +----------+    |
|  |  MQTT    |    |  REST    |    |  File    |    | Simula-  |    |
|  |          |    |  API     |    |  Watcher |    | tion     |    |
|  | - Real-  |    |          |    |          |    |          |    |
|  |   time   |    | - Polling|    | - CSV    |    | - Scilab |    |
|  | - Pub/   |    | - Batch  |    | - JSON   |    | - Manual |    |
|  |   Sub    |    | - GraphQL|    | - HDF5   |    | - Record |    |
|  | - QoS    |    | - OAuth  |    | - Excel  |    |   & play |    |
|  +----+-----+    +----+-----+    +----+-----+    +----+-----+    |
|       |               |               |               |           |
|       +-------+-------+-------+-------+-------+-------+           |
|               |               |               |                   |
|               v               v               v                   |
|       +--------------------------------------------------+       |
|       |  Data Normalization Layer                         |       |
|       |                                                    |       |
|       |  - Timestamp alignment                            |       |
|       |  - Unit conversion                                 |       |
|       |  - Missing value interpolation                     |       |
|       |  - Outlier detection                               |       |
|       |  - Rate limiting                                   |       |
|       +----------------------+---------------------------+       |
|                              |                                    |
|                              v                                    |
|       +--------------------------------------------------+       |
|       |  Twin State Engine                                |       |
|       |                                                    |       |
|       |  - Update sensor values                           |       |
|       |  - Trigger model re-computation                   |       |
|       |  - Check alarm conditions                         |       |
|       |  - Record to time series store                    |       |
|       +--------------------------------------------------+       |
+------------------------------------------------------------------+
```

### 9.2 MQTT Integration

```
MQTT Topic Structure:
  scilab-studio/twins/{twin-id}/sensors/{sensor-id}/raw
  scilab-studio/twins/{twin-id}/sensors/{sensor-id}/calibrated
  scilab-studio/twins/{twin-id}/state
  scilab-studio/twins/{twin-id}/alerts
  scilab-studio/twins/{twin-id}/commands

Message Format:
  {
    "timestamp": "2026-07-27T14:30:00.123Z",
    "sensorId": "sensor-ahu01-temp-supply",
    "value": 22.4,
    "unit": "C",
    "quality": "good"
  }

QoS Levels:
  - QoS 0: Non-critical sensors (humidity, light)
  - QoS 1: Normal sensors (temperature, pressure)
  - QoS 2: Critical sensors (safety, emergency)
```

### 9.3 Simulation Mode

```
+-----------------------------------------------------------+
|  SIMULATION MODE                                           |
|                                                             |
|  When live data is unavailable, the framework enters        |
|  simulation mode:                                          |
|                                                             |
|  1. Load initial conditions from last known state          |
|  2. Run mathematical models forward in time                |
|  3. Generate synthetic sensor readings                     |
|  4. Apply noise models for realism                         |
|  5. Allow parameter sweeps and what-if scenarios           |
|                                                             |
|  Simulation types:                                         |
|  +------------------------------------------------------+ |
|  | Forward    | Start from t0, step forward to t_end    | |
|  | What-If    | Change parameters, observe impact       | |
|  | Backward   | Reconstruct past from sparse data       | |
|  | Monte Carlo| Run N simulations with random params    | |
|  | Stress Test| Push beyond normal operating limits     | |
|  +------------------------------------------------------+ |
+-----------------------------------------------------------+
```

---

## 10. Visualization

### 10.1 3D Twin Rendering

```
+-----------------------------------------------------------+
|  3D DIGITAL TWIN VIEW                                       |
|                                                             |
|  +------------------------------------------------------+ |
|  |                                                        | |
|  |        +--------+                                      | |
|  |       /|       /|    3D Model of Building/Asset       | |
|  |      / |  AHU  / |                                     | |
|  |     /  |  01  /  |    Color-coded by:                  | |
|  |    +--------+   |    - Temperature (red=hot, blue=cold)| |
|  |    |   |    |   |    - Status (green=ok, red=alarm)    | |
|  |    |   +----|---+    - Load (gradient)                 | |
|  |    |  / AHU |  /                                      | |
|  |    | /  02  | /     Click on asset to:                 | |
|  |    |/       |/      - View sensor values              | |
|  |    +--------+        - Open trend chart                | |
|  |                     - Edit properties                  | |
|  |                     - View alerts                      | |
|  |                                                        | |
|  +------------------------------------------------------+ |
|                                                             |
|  Controls:                                                  |
|  [Orbit] [Pan] [Zoom] [Reset] [Wireframe] [Transparency]  |
|  [Color By: Temp | Status | Load | Custom]                  |
|  [Time Slider: <--- 14:30 ----------> Now]                 |
+-----------------------------------------------------------+
```

### 10.2 Dashboard Layout

```
+------------------------------------------------------------------+
|  DIGITAL TWIN DASHBOARD: Campus Energy                            |
|                                                                    |
|  +-- KPIs ----------------------------------------------------+ |
|  |  Total Load: 1,247 kW  |  Efficiency: 87%  |  Alerts: 2    | |
|  +--------------------------------------------------------------+ |
|                                                                    |
|  +-- Real-Time Trend ------------------+  +-- 3D View ----------+|
|  |  Power (kW)                         |  |                      ||
|  |  1500 |    /\    /\                 |  |   [Building model   ||
|  |       |   /  \  /  \    /\          |  |    with color-coded  ||
|  |  1000 |  /    \/    \  /  \         |  |    thermal overlay]  ||
|  |       | /            \/    \        |  |                      ||
|  |   500 |/                    \       |  +----------------------+
|  |       +------------------------     |  +-- Alerts ------------+|
|  |        12:00  13:00  14:00  15:00  |  | CRITICAL  AHU-02     ||
|  |                                      |  |   Supply temp high   ||
|  +--------------------------------------+  | WARNING   Pump P-03  ||
|  |  +-- Power Breakdown --+             |  |   Vibration above    ||
|  |  |  HVAC: 45%           |             |  |   threshold          ||
|  |  |  Lighting: 25%       |             |  | INFO       T-01     ||
|  |  |  Plug Load: 20%      |             |  |   Load at 90%        ||
|  |  |  Other: 10%          |             |  +----------------------+
|  |  +----------------------+             |
|  +----------------------------------------+
+------------------------------------------------------------------+
```

### 10.3 Alert System

```jsonc
{
  "rules": [
    {
      "id": "rule-temp-high",
      "name": "High Temperature Alert",
      "sensorId": "sensor-ahu01-temp-supply",
      "condition": "value > 28",
      "severity": "warning",
      "message": "AHU-01 supply temperature above 28C",
      "actions": ["notify", "log", "dashboard"],
      "cooldown": 300
    },
    {
      "id": "rule-temp-critical",
      "name": "Critical Temperature",
      "sensorId": "sensor-ahu01-temp-supply",
      "condition": "value > 35",
      "severity": "critical",
      "message": "AHU-01 CRITICAL: supply temperature above 35C",
      "actions": ["notify", "log", "dashboard", "email", "sms"],
      "cooldown": 60
    },
    {
      "id": "rule-anomaly",
      "name": "AI Anomaly Detection",
      "sensorId": "*",
      "condition": "model.predict(value) < 0.05",
      "severity": "warning",
      "message": "Anomalous reading detected on {sensor.name}",
      "actions": ["notify", "log"]
    }
  ]
}
```

---

## 11. Use Cases

### 11.1 Supported Use Cases

| Use Case | Assets | Sensors | Models | Key Metrics |
|---|---|---|---|---|
| **Campus Energy** | Buildings, HVAC, meters | Temp, power, flow, occupancy | Thermal, energy balance | kWh, COP, comfort |
| **Factory** | Machines, conveyors, robots | Vibration, temp, cycle time |磨损, throughput | OEE, cycle time, defects |
| **Power Grid** | Generators, transformers, loads | V power, I current, freq | Power flow, stability | Load factor, losses |
| **Water Plant** | Pumps, pipes, tanks, valves | Flow, pressure, level | Hydraulics, water quality | GPM, pressure, turbidity |
| **Hospital** | HVAC, medical equipment, rooms | Temp, humidity, air quality | Thermal, airflow | Comfort, air changes |
| **Solar Farm** | Panels, inverters, transformers | Irradiance, temp, power | PV model, degradation | kWh, efficiency, availability |
| **Data Center** | Servers, CRAC, PDUs | Temp, power, airflow | Thermal, power distribution | PUE, hot spots |
| **Bridge** | Deck, cables, bearings | Strain, displacement, accel | Structural dynamics | Stress, fatigue, deflection |

### 11.2 Campus Energy Example

```
  Campus Digital Twin Structure:

  +-- Campus "Main"
  |   +-- Building "Engineering Hall"
  |   |   +-- HVAC System
  |   |   |   +-- AHU-01 (Zone A)
  |   |   |   +-- AHU-02 (Zone B)
  |   |   |   +-- Chiller CH-01
  |   |   |   +-- Cooling Tower CT-01
  |   |   +-- Electrical System
  |   |   |   +-- Transformer T-01
  |   |   |   +-- Panels P-01, P-02
  |   |   +-- Lighting System
  |   |   +-- Solar Array SA-01
  |   |
  |   +-- Building "Research Lab"
  |   |   +-- HVAC System
  |   |   +-- Fume Hoods
  |   |   +-- Electrical System
  |   |
  |   +-- Distribution
  |       +-- Medium Voltage Ring
  |       +-- Chill Water Loop
  |       +-- Condenser Water Loop
  |
  +-- Models
      +-- Campus energy balance
      +-- Building thermal models
      +-- HVAC performance curves
      +-- Solar generation forecast
      +-- Load prediction (ML)
```

---

## 12. Digital Twin Library

### 12.1 Ready-Made Twins

| Twin | Category | Description |
|---|---|---|
| **AHU Generic** | HVAC | Air handling unit with thermal model |
| **Chiller Centrifugal** | HVAC | Water-cooled centrifugal chiller |
| **Cooling Tower** | HVAC | Induced-draft cooling tower |
| **PV Panel Monocrystalline** | Renewable | Solar panel with temperature derating |
| **Wind Turbine Horizontal** | Renewable | HAWT with power curve model |
| **Li-Ion Battery Pack** | Storage | Battery with SOC/SOH model |
| **Induction Motor** | Equipment | 3-phase induction motor |
| **Centrifugal Pump** | Equipment | Pump with affinity laws |
| **Transformer 3-Phase** | Electrical | Power transformer with losses |
| **Diesel Generator** | Electrical | Backup generator with fuel model |
| **Water Tank Elevated** | Hydraulic | Gravity-fed water storage |
| **Boiler Fire-Tube** | Thermal | Gas-fired fire-tube boiler |
| **Cooling Coil** | HVAC | DX or chilled water coil |

### 12.2 Library API

```javascript
// Search the digital twin library
const results = await twinLibrary.search({
  category: "HVAC",
  query: "air handling unit",
  tags: ["thermal", "first-order"],
  minRating: 4,
});

// Install a twin template
const template = await twinLibrary.install("twin-hvac-ahu-generic");

// Create an instance from template
const myAHU = await twin.create({
  template: "twin-hvac-ahu-generic",
  name: "AHU-01 Engineering Building",
  parameters: {
    ratedAirflow: 5000,
    ratedPower: 15,
  },
});

// Share a custom twin
await twinLibrary.publish({
  twinId: myCustomTwin.id,
  name: "Custom VRF Heat Pump",
  description: "Variable refrigerant flow model",
  license: "MIT",
  tags: ["HVAC", "heat-pump", "VRF"],
});
```

---

## 13. API Reference

### 13.1 Twin Management API

```javascript
// Create a digital twin
const twin = await twinEngine.create({
  id: "campus-energy",
  name: "Campus Energy System",
  description: "Main campus energy digital twin",
});

// Add assets
await twin.addAsset({
  type: "equipment.ahu",
  name: "AHU-01",
  properties: { ratedAirflow: 5000 },
});

// Add sensors
await twin.addSensor({
  assetId: "ahu-01",
  type: "temperature",
  name: "Supply Temp",
  source: { type: "mqtt", topic: "sensors/ahu01/supply" },
});

// Add relationships
await twin.addRelationship({
  type: "functional.powers",
  source: "transformer-t01",
  target: "panel-bp01",
});

// Bind a model
await twin.bindModel({
  assetId: "ahu-01",
  modelId: "model-ahu-thermal",
});

// Start the twin (begins data ingestion + computation)
await twin.start();

// Query current state
const state = await twin.getState("ahu-01");
// { temperature: 22.4, power: 12.3, status: "normal" }

// Get time series
const history = await twin.getTimeSeries("sensor-ahu01-supply", {
  from: "2026-07-26T00:00:00Z",
  to: "2026-07-27T00:00:00Z",
  aggregation: "1min",
});

// Run simulation
const simResult = await twin.simulate({
  modelId: "model-ahu-thermal",
  duration: 3600,
  inputs: {
    T_return: 24,
    T_outdoor: 35,
    Q_cooling: 20,
    m_dot: 2.5,
  },
});

// Stop the twin
await twin.stop();
```

### 13.2 Scilab Integration API

```scilab
// Create twin from Scilab script
twin_id = twin_create("my-motor", "equipment.motor");

// Set properties
twin_set_property(twin_id, "rated_power", 75, "kW");
twin_set_property(twin_id, "speed", 1750, "RPM");

// Add sensor
twin_add_sensor(twin_id, "temperature", "winding_temp", ...
                "mqtt://localhost/sensors/motor01/temp");

// Bind model
twin_bind_model(twin_id, "model-motor-thermal");

// Start
twin_start(twin_id);

// Read sensor value
temp = twin_get_sensor_value(twin_id, "winding_temp");

// Get model prediction
predicted = twin_eval_model(twin_id, "model-motor-thermal", ...
                            load: 0.8, ambient: 25);

// Plot twin data
twin_plot(twin_id, "winding_temp", "2026-07-26", "2026-07-27");
```

---

## 14. Configuration

### 14.1 Framework Configuration

```jsonc
{
  "digitalTwin": {
    "enabled": true,
    "dataDirectory": "./data/twins",

    "computation": {
      "maxWorkers": 4,
      "defaultSolver": "ode45",
      "maxStepSize": 10,
      "tolerance": 1e-6,
      "timeout": 30000
    },

    "dataIntegration": {
      "mqtt": {
        "broker": "mqtt://localhost:1883",
        "clientId": "scilab-studio-{pid}",
        "qos": 1,
        "reconnect": true
      },
      "rest": {
        "timeout": 10000,
        "retries": 3,
        "pollInterval": 5000
      },
      "fileWatcher": {
        "debounce": 1000,
        "patterns": ["*.csv", "*.json"]
      }
    },

    "timeSeries": {
      "retention": "90d",
      "maxPoints": 1000000,
      "compression": true,
      "downsampleThreshold": 500000
    },

    "alerts": {
      "enabled": true,
      "maxActive": 100,
      "acknowledgment": "required",
      "escalation": true,
      "historyRetention": "1y"
    },

    "visualization": {
      "3dEnabled": true,
      "maxAssets3D": 500,
      "refreshRate": 1,
      "theme": "engineering-dark"
    }
  }
}
```

---

## 15. Performance Considerations

| Strategy | Description |
|---|---|
| **Incremental Computation** | Only recompute models affected by changed inputs |
| **Model Coarsening** | Use simplified models at low time resolution |
| **Worker Pool** | Parallel model execution across CPU cores |
| **Time Series Compression** | Gorilla compression for numeric time series |
| **Lazy 3D Loading** | Load 3D models on demand, not at startup |
| **LOD Rendering** | Simplify 3D meshes at distance |
| **Batch Sensor Updates** | Buffer sensor writes, flush at fixed intervals |
| **Selective Precision** | High-precision for active twins, low for background |

### Performance Budgets

| Metric | Target |
|---|---|
| Twin startup (100 assets) | < 5 seconds |
| Model step (ODE, 100 states) | < 10 ms |
| Sensor update throughput | > 10,000 points/second |
| 3D render (100 assets) | 60 FPS |
| Dashboard refresh | 1 second |
| Alert detection latency | < 500 ms |
| Time series query (1 day) | < 100 ms |
| Memory per twin instance | < 500 MB |

---

*This document defines the digital twin framework architecture for Scilab Studio.
All twin definitions, models, and visualizations must conform to these specifications.*
