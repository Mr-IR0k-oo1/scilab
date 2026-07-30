<div align="center">

# Scilab Studio

### The Open Engineering Development Platform

![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)
![Scilab 7.0+](https://img.shields.io/badge/Scilab-7.0%2B-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Status](https://img.shields.io/badge/Status-Alpha-orange.svg)

A modern development environment for Scilab — visual GUI building, interactive
visualization, and project management in one desktop application.

[Getting Started](#installation) | [Documentation](#documentation) | [Contributing](#contributing)

</div>

---

## What is Scilab Studio?

Scilab Studio wraps the Scilab numerical computing engine in a modern desktop
application built with Tauri. Instead of scripting GUIs by hand or juggling
separate tools for plotting, data import, and reporting, you get an integrated
environment where these workflows live side by side.

The platform is modular. Each feature — GUI Builder, Visualization Studio, Data
Studio, and so on — is an independent module that communicates with Scilab
through a JSON-RPC sidecar. This means modules can be developed, tested, and
shipped independently. If you only need the charting tool, you can use just that.
If you want the full experience, everything works together.

Scilab Studio is part of the
[FOSSEE](https://fossee.in/) (Free and Open Source Software for Education)
ecosystem at IIT Bombay. Version 0.1 is the foundation — it ships with six
working modules and establishes the core architecture. More modules are on the
roadmap and will land in subsequent releases.

---

## Current Features (v0.1)

| Feature | Status | Description |
|---------|--------|-------------|
| Project Workspace | ✅ v0.1 | Create, open, and manage projects with a built-in file explorer |
| Visual GUI Builder | ✅ v0.1 | Drag-and-drop GUI designer with 9 component types (buttons, labels, text fields, sliders, checkboxes, dropdowns, panels, images, and tables) |
| Visualization Studio | ✅ v0.1 | Line, scatter, bar, and heatmap charts with interactive zoom and pan |
| Data Studio | ✅ v0.1 | Import CSV and Excel files with automatic type detection and a data preview table |
| Report Generator | ✅ v0.1 | Export PDF and HTML reports with embedded charts, tables, and formatted text |
| Learning Center | ✅ v0.1 | Browse and open 5-10 example projects covering common engineering workflows |

### Coming in Future Releases

- **v0.2:** Plugin system, Widget Marketplace, Lab Creator, Xcos Builder, Project Templates
- **v0.3:** AI Assistant, Digital Twin Framework, Parameter Sweep, Dashboard Builder
- **v0.4:** Community Marketplace, Open Engineering Library, Research Workspace

See [Product Vision](docs/02_Product_Vision.md) for the full roadmap.

---

## Architecture

Scilab Studio uses a layered architecture. The core platform provides a plugin
manager, event bus, and Scilab bridge. Modules sit on top of the core and
communicate through well-defined interfaces. At the bottom, the Scilab engine
runs as a sidecar process, receiving JSON-RPC calls over stdin/stdout.

```
┌─────────────────────────────────────────────────┐
│                 SCILAB STUDIO                    │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌───────────────────────────────────────────┐  │
│  │          CORE PLATFORM                     │  │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────┐  │  │
│  │  │ Plugin  │ │ Event    │ │ Scilab    │  │  │
│  │  │ Manager │ │ Bus      │ │ Bridge    │  │  │
│  │  └─────────┘ └──────────┘ └───────────┘  │  │
│  └───────────────────────────────────────────┘  │
│                                                   │
│  ┌───────────────────────────────────────────┐  │
│  │          v0.1 MODULES                      │  │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────┐ │  │
│  │  │ GUI      │ │ Viz      │ │ Data      │ │  │
│  │  │ Builder  │ │ Studio   │ │ Studio    │ │  │
│  │  └──────────┘ └──────────┘ └───────────┘ │  │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────┐ │  │
│  │  │ Report   │ │ Project  │ │ Learning  │ │  │
│  │  │ Gen      │ │ Manager  │ │ Center    │ │  │
│  │  └──────────┘ └──────────┘ └───────────┘ │  │
│  └───────────────────────────────────────────┘  │
│                                                   │
│  ┌───────────────────────────────────────────┐  │
│  │          SCILAB ENGINE                     │  │
│  │  (via JSON-RPC over stdin/stdout)          │  │
│  └───────────────────────────────────────────┘  │
│                                                   │
└─────────────────────────────────────────────────┘
```

The UI is built with TypeScript and Svelte. The backend and Scilab bridge are
written in Rust using the Tauri framework. This gives us a small binary size,
native performance, and a web-based frontend that's easy to iterate on.

---

## Installation

### Prerequisites

- Scilab 7.0 or later (must be on your `PATH`)
- Git

### Quick Start

```bash
git clone https://github.com/fossee/scilab-studio.git
cd scilab-studio
# Linux/macOS
./install.sh
# Windows
install.bat
```

### Platform Notes

| Platform | Requirements |
|----------|-------------|
| Linux | Ubuntu 20.04+ / Fedora 35+ |
| macOS | 12+ (Monterey or later) |
| Windows | 10+ (64-bit) |

---

## Documentation

| Document | Description |
|----------|-------------|
| **Product** | |
| [Product Requirements](docs/00_Product_Requirements_Document.md) | Project contract — scope, objectives, FR/NFR IDs |
| [Project Overview](docs/01_Project_Overview.md) | Why Scilab Studio exists |
| [Product Vision](docs/02_Product_Vision.md) | 5-year roadmap |
| [System Architecture](docs/03_System_Architecture.md) | Source of truth — architecture, protocols, schemas |
| [Platform Architecture](docs/04_Platform_Architecture.md) | Event Bus, Plugin Manager, Scilab Bridge |
| [Feature Modules](docs/05_Feature_Modules.md) | User-facing modules (GUI Builder, Viz Studio, etc.) |
| [MVP Specification](docs/MVP_Specification.md) | What ships in v0.1 |
| [Architecture Decisions](docs/adr/) | Why we made key technical choices |
| **Feature Details** | |
| [Data Architecture](docs/07_Data_Architecture.md) | Data import, transformation pipelines |
| [Digital Twin Framework](docs/08_Digital_Twin_Framework.md) | Digital twin modeling |
| [Visualization Engine](docs/09_Visualization_Engine.md) | Chart types, rendering |
| [Lab Creator](docs/10_Lab_Creator.md) | Interactive lab builder |
| [Report Generator](docs/11_Report_Generator.md) | Report creation and export |
| [Project Templates](docs/12_Project_Templates.md) | Template system |
| [AI Assistant](docs/13_AI_Assistant.md) | AI-powered coding assistant |
| **Developer** | |
| [API Reference](docs/14_API_Reference.md) | Platform APIs |
| [File Format](docs/15_File_Format.md) | .scstudio schemas |
| [Roadmap](docs/16_Roadmap.md) | Development roadmap |
| [Development Guide](docs/17_Development_Guide.md) | Dev environment setup |
| [UI/UX Guidelines](docs/18_UI_UX_Guidelines.md) | Design patterns |
| [Deployment](docs/19_Deployment.md) | Build and distribution |
| [Marketplace](docs/32_Marketplace.md) | Plugin and widget marketplace |
| **Technical Specifications** | |
| [Technical Architecture](docs/20_Technical_Architecture.md) | Runtime lifecycle, DI, error handling |
| [Component Specification](docs/21_Component_Specification.md) | Per-component: API, state, events, failure modes |
| [Project File Format](docs/22_Project_File_Format.md) | .scstudio extension, project.json, layouts |
| [Event System](docs/23_Event_System.md) | Event lifecycle, priority, async, error propagation |
| [Plugin SDK](docs/24_Plugin_SDK.md) | Plugin structure, lifecycle, manifest, sandboxing |
| [Widget SDK](docs/25_Widget_SDK.md) | Common widget interface, data binding, serialization |
| [Visualization Framework](docs/26_Visualization_Framework.md) | 10 chart types, rendering pipeline, theming |
| [Data Pipeline](docs/27_Data_Pipeline.md) | Import → validation → transform → export flow |
| [Scilab Runtime](docs/28_Scilab_Runtime.md) | Command queue, process management, marshalling |
| [UI Design System](docs/29_UI_Design_System.md) | Typography, colors, spacing, animations, shortcuts |
| [Development Roadmap](docs/30_Development_Roadmap.md) | Sprint-based milestones |
| [Scilab Compatibility Layer](docs/31_Scilab_Compatibility_Layer.md) | Version detection, API normalization, multi-version |
| **Supporting** | |
| [Report Generator](docs/33_Report_Generator.md) | Report blocks, templates, export formats |
| [Learning Center](docs/34_Learning_Center.md) | Examples, tutorials, Scilab reference |
| **Engineering Specifications** | |
| [SPEC-001 Workspace](docs/specifications/SPEC-001-Workspace.md) | File explorer, tabs, project lifecycle |
| [SPEC-002 GUI Designer](docs/specifications/SPEC-002-GUI-Designer.md) | Canvas, components, properties, code gen |
| [SPEC-003 Widget System](docs/specifications/SPEC-003-Widget-System.md) | Widget lifecycle, SDK, data binding |
| [SPEC-004 Visualization](docs/specifications/SPEC-004-Visualization.md) | Chart types, rendering, theming |
| [SPEC-005 Plugin Architecture](docs/specifications/SPEC-005-Plugin-Architecture.md) | Plugin lifecycle, SDK, sandboxing |
| [SPEC-006 Templates](docs/specifications/SPEC-006-Templates.md) | Template system, marketplace |
| [SPEC-007 Data Studio](docs/specifications/SPEC-007-Data-Studio.md) | Data import, preview, transforms |
| [SPEC-008 Scilab Execution](docs/specifications/SPEC-008-Scilab-Execution.md) | Runtime management, JSON-RPC |
| [SPEC-009 Report Generator](docs/specifications/SPEC-009-Report-Generator.md) | Block editor, export, batch |
| [SPEC-010 Learning Center](docs/specifications/SPEC-010-Learning-Center.md) | Examples, tutorials, reference |
| [SPEC-011 Digital Twins](docs/specifications/SPEC-011-Digital-Twins.md) | Twin modeling, sync, scenarios |
| [SPEC-012 AI Assistant](docs/specifications/SPEC-012-AI-Assistant.md) | Chat, completion, explanation |
| **User Stories** | |
| [Student](docs/user-stories/US-Student.md) | Student persona — tutorials, labs, reports |
| [Faculty](docs/user-stories/US-Faculty.md) | Faculty persona — course materials, labs |
| [Researcher](docs/user-stories/US-Researcher.md) | Researcher persona — analysis, twins, papers |
| [Developer](docs/user-stories/US-Developer.md) | Developer persona — plugins, widgets, CLI |
| **Design System** | |
| [Design Principles](docs/design/01-Design-Principles.md) | Core design philosophy |
| [Accessibility](docs/design/02-Accessibility.md) | WCAG 2.1 AA, keyboard, screen reader |
| [Interaction Patterns](docs/design/03-Interaction-Patterns.md) | Selection, drag-drop, context menu |
| [Keyboard Shortcuts](docs/design/04-Keyboard-Shortcuts.md) | Global and module shortcuts |
| [Color System](docs/design/05-Color-System.md) | Dark/light themes, chart colors |
| [Iconography](docs/design/06-Iconography.md) | Icon system, sizes, usage rules |
| [Layout Rules](docs/design/07-Layout-Rules.md) | Panel layout, breakpoints, spacing |
| [Animation Rules](docs/design/08-Animation-Rules.md) | Duration, easing, reduced motion |
| **Decisions** | |
| [Decision Log](docs/decisions/) | Architectural decision records (DRR-001 through DRR-008) |
| [Feature Matrix](docs/FEATURE_MATRIX.md) | Version-gated module status |
| **RFCs (Request for Comments)** | |
| [RFC-0001 Project Workspace](docs/rfcs/RFC-0001-Project-Workspace.md) | How the workspace behaves |
| [RFC-0002 Plugin API](docs/rfcs/RFC-0002-Plugin-API.md) | How plugins are loaded and sandboxed |
| [RFC-0003 Widget API](docs/rfcs/RFC-0003-Widget-API.md) | How widgets are created and rendered |
| [RFC-0004 Visualization API](docs/rfcs/RFC-0004-Visualization-API.md) | How charts are created and exported |
| [RFC-0005 Project Templates](docs/rfcs/RFC-0005-Project-Templates.md) | How templates are defined and instantiated |
| [RFC-0006 Scilab Bridge](docs/rfcs/RFC-0006-Scilab-Bridge.md) | How the app communicates with Scilab |
| [RFC-0007 Command System](docs/rfcs/RFC-0007-Command-System.md) | How user actions are dispatched |
| [RFC-0008 Extension Permissions](docs/rfcs/RFC-0008-Extension-Permissions.md) | How plugin security works |
| [RFC-0009 Theme System](docs/rfcs/RFC-0009-Theme-System.md) | How themes are defined and applied |
| [RFC-0010 Package Manager](docs/rfcs/RFC-0010-Package-Manager.md) | How extensions are installed and managed |
| **SDK Documentation** | |
| [SDK Overview](sdk/README.md) | Build plugins, widgets, visualizations |
| [Getting Started](sdk/getting-started.md) | Setup and first extension |
| [Plugin Development](sdk/plugin-development.md) | Complete plugin guide |
| [Widget Development](sdk/widget-development.md) | Complete widget guide |
| [Visualization Development](sdk/visualization-development.md) | Custom chart types |
| [Template Development](sdk/template-development.md) | Project templates |
| [Best Practices](sdk/best-practices.md) | Patterns and conventions |
| [Examples](sdk/examples/) | Working example extensions |
| **Platform APIs** | |
| [Workspace API](platform/Workspace-API.md) | Tabs, panels, layout |
| [Plugin API](platform/Plugin-API.md) | Plugin lifecycle and management |
| [Widget API](platform/Widget-API.md) | Widget creation and data binding |
| [Visualization API](platform/Visualization-API.md) | Chart creation and export |
| [Project API](platform/Project-API.md) | Project file operations |
| [Runtime API](platform/Runtime-API.md) | Scilab execution and variables |
| [Storage API](platform/Storage-API.md) | Persistent key-value storage |
| [Logging API](platform/Logging-API.md) | Structured logging |
| **Design Language** | |
| [Typography](design/Typography.md) | Font families, type scale |
| [Spacing](design/Spacing.md) | Spacing scale and usage |
| [Icons](design/Icons.md) | Icon system and usage |
| [Component Library](design/Component-Library.md) | Buttons, inputs, cards, badges |
| [Windows](design/Windows.md) | Window layout and controls |
| [Panels](design/Panels.md) | Panel types and behavior |
| [Dialogs](design/Dialogs.md) | Modals, toasts, confirmations |
| [Toolbars](design/Toolbars.md) | Toolbar layout and buttons |
| [Docking](design/Docking.md) | Panel docking and splitting |
| [Menus](design/Menus.md) | Menu structure and behavior |
| [Themes](design/Themes.md) | Theme system and customization |
| [Accessibility](design/Accessibility.md) | WCAG 2.1 AA compliance |
| **Quality Standards** | |
| [Coding Standards](quality/Coding-Standards.md) | TypeScript, Rust, CSS conventions |
| [Documentation Standards](quality/Documentation-Standards.md) | How to write docs |
| [Testing Standards](quality/Testing-Standards.md) | Test pyramid and coverage |
| [Performance Standards](quality/Performance-Standards.md) | Performance budgets |
| [Accessibility Standards](quality/Accessibility-Standards.md) | Accessibility requirements |
| [Security Standards](quality/Security-Standards.md) | Security practices |
| [Review Process](quality/Review-Process.md) | Code review checklist |
| [Benchmarks](quality/Benchmarks.md) | Performance targets |
| [Governance](quality/Governance.md) | Project roles and decisions |
| **Release Process** | |
| [Versioning](release/Versioning.md) | SemVer and version bumps |
| [Branch Strategy](release/Branch-Strategy.md) | Git workflow |
| [Release Checklist](release/Release-Checklist.md) | Pre-release steps |
| [Migration Guide](release/Migration-Guide.md) | Upgrading between versions |
| [Compatibility Policy](release/Compatibility-Policy.md) | Platform and plugin compatibility |
| [Deprecation Policy](release/Deprecation-Policy.md) | How features are deprecated |
| [Milestone Alpha](release/Milestone-Alpha.md) | First public release scope |
| **Testing** | |
| [Testing Strategy](tests/Testing-Strategy.md) | Test pyramid and approach |
| **Engineering Design Documents** | |
| [EDD-001 Core Runtime](docs/engineering/EDD-001-Core-Runtime.md) | Event bus, modules, config, logging |
| [EDD-002 Workspace System](docs/engineering/EDD-002-Workspace-System.md) | Tabs, panels, layout |
| [EDD-003 Module System](docs/engineering/EDD-003-Module-System.md) | Module lifecycle and isolation |
| [EDD-004 Plugin Runtime](docs/engineering/EDD-004-Plugin-Runtime.md) | Plugin sandboxing and lifecycle |
| [EDD-005 Widget Engine](docs/engineering/EDD-005-Widget-Engine.md) | Widget rendering and data binding |
| [EDD-006 GUI Framework](docs/engineering/EDD-006-GUI-Framework.md) | Canvas, components, code generation |
| [EDD-007 Visualization Engine](docs/engineering/EDD-007-Visualization-Engine.md) | Chart rendering and export |
| [EDD-008 Scilab Bridge](docs/engineering/EDD-008-Scilab-Bridge.md) | Process management, JSON-RPC |
| [EDD-009 Storage System](docs/engineering/EDD-009-Storage-System.md) | Key-value store, file system |
| [EDD-010 Command System](docs/engineering/EDD-010-Command-System.md) | Commands, undo/redo, palette |
| [EDD-011 Logging System](docs/engineering/EDD-011-Logging-System.md) | Structured logging |
| [EDD-012 Configuration System](docs/engineering/EDD-012-Configuration-System.md) | Settings and preferences |
| [EDD-013 Error Handling](docs/engineering/EDD-013-Error-Handling.md) | Error recovery strategy |
| [EDD-014 Performance](docs/engineering/EDD-014-Performance.md) | Performance budgets and monitoring |
| [EDD-015 Security](docs/engineering/EDD-015-Security.md) | Threat model and security practices |
| **Engineering Architecture** | |
| [Platform Services](docs/engineering/Platform-Services.md) | Service definitions and interfaces |
| [Internal APIs](docs/engineering/Internal-APIs.md) | Service contracts |
| [Dependency Rules](docs/engineering/Dependency-Rules.md) | Layer architecture enforcement |
| [State Management](docs/engineering/State-Management.md) | State layers and persistence |
| [Error Recovery](docs/engineering/Error-Recovery.md) | Graceful degradation strategy |
| [Extension Points](docs/engineering/Extension-Points.md) | What can be extended |
| [Project Lifecycle](docs/engineering/Project-Lifecycle.md) | Create → Archive workflow |
| [Engineering Principles](docs/engineering/Engineering-Principles.md) | Architectural constitution |
| [Success Criteria](docs/engineering/Success-Criteria.md) | Measurable quality targets |
| [Ecosystem](docs/engineering/Ecosystem.md) | Community, marketplace, integrations |
| **Design Artifacts** | |
| [System Diagrams](design/system/) | Mermaid: context, components, deployment, runtime |
| [Sequence Diagrams](design/sequence/) | Create project, run Scilab, import data, export report |
| [Wireframes](design/wireframes/) | ASCII wireframes for all screens |
| [Components](design/components/) | Component definitions and states |
| [Icons](design/icons/) | Icon system and naming |
| [Themes](design/themes/) | Dark, light, high contrast themes |
| [Interaction Flows](design/Interaction-Flows.md) | User task flows |
| [MVP Specification](design/MVP-Specification.md) | What ships, what doesn't |
| [GitHub Project](design/GitHub-Project.md) | Epics, features, tasks |

---

## Roadmap

```text
v0.1 (Current) — Foundation
├── Project Workspace
├── GUI Builder
├── Visualization Studio
├── Data Studio
├── Report Generator
└── Learning Center

v0.2 — Extensibility
├── Plugin System
├── Widget Marketplace
├── Lab Creator
├── Xcos Builder
└── Project Templates

v0.3 — Intelligence
├── AI Assistant
├── Digital Twins
├── Parameter Sweep
└── Dashboard Builder

v0.4 — Community
├── Marketplace
├── Engineering Library
└── Research Workspace
```

---

## Contributing

We welcome contributions from engineers, educators, students, and developers.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.
Bug reports, documentation improvements, and feature ideas are all appreciated —
you don't have to write code to contribute.

---

## Relationship to FOSSEE

Scilab Studio is part of the FOSSEE ecosystem at IIT Bombay. It complements
existing FOSSEE projects:

| Project | Relationship |
|---------|-------------|
| Scilab | Core numerical engine that Scilab Studio wraps |
| Xcos | Block-based modeling — integration planned for v0.2 |
| eSim | Circuit simulation — future integration target |
| OpenModelica | Multi-domain modeling — future integration target |
| Spoken Tutorials | Video-based learning — referenced in the Learning Center |

---

## License

Scilab Studio is licensed under the [GNU General Public License v3.0](LICENSE).

---

<div align="center">

Open Source. Open Science. Open Engineering.

</div>
# scilab
