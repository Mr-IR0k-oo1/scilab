# Engineering Principles

These principles are the architectural constitution. Every design decision should be consistent with them.

---

## Principle 1: Scilab is the computation engine, not the UI framework.

Scilab computes. The UI renders. They communicate through a clean boundary (JSON-RPC). Scilab code never manipulates DOM elements. UI code never performs matrix operations.

---

## Principle 2: Every capability is modular.

No feature is hardcoded into the core. Every capability — visualization, data import, reporting, widgets — is a module that can be enabled, disabled, or replaced.

---

## Principle 3: Everything is reproducible.

A project saved today must produce the same results tomorrow. No hidden state. No random defaults. Every visualization can be regenerated from saved project data.

---

## Principle 4: Projects are portable.

A project created on Linux must work on macOS and Windows. No platform-specific paths. No OS-dependent behavior. No absolute paths in project files.

---

## Principle 5: Offline-first.

No feature requires an internet connection. No telemetry. No phone-home. All data is stored locally. Network access is optional and user-initiated.

---

## Principle 6: Plugins cannot modify the core runtime.

Plugins extend the platform through well-defined APIs. They cannot override core behavior, access other plugins' data, or modify the event bus structure.

---

## Principle 7: Every engineering result must be exportable.

Every chart, every dataset, every report, every GUI layout must be exportable to a standard format. No data is locked in the application.

---

## Principle 8: Every visualization should be reproducible from saved project data.

If a user creates a chart, the chart configuration and data source are saved in the project. Opening the project later reproduces the exact same chart.

---

## Principle 9: Error recovery over error prevention.

Engineering software encounters errors. The system should recover gracefully, not crash. Log errors, notify the user, disable the failing component, and continue.

---

## Principle 10: Measure, don't guess.

Every performance claim is backed by a benchmark. Every accessibility claim is backed by a test. Every compatibility claim is backed by a test matrix.

---

## Principle 11: The platform outlives any single feature.

Features come and go. The core runtime, the event bus, the plugin system, the project format — these are permanent. Design for permanence.

---

## Principle 12: Contribute back to the ecosystem.

Scilab Studio is part of FOSSEE. It should give back: contribute to Scilab, share tools with other FOSSEE projects, publish open data and open research tools.
