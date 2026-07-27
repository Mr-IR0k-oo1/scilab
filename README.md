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
| **Core** | |
| [Product Requirements](docs/00_Product_Requirements_Document.md) | Project scope, objectives, functional requirements |
| [Project Overview](docs/01_Project_Overview.md) | Why Scilab Studio exists |
| [Product Vision](docs/02_Product_Vision.md) | 5-year roadmap |
| [System Architecture](docs/03_System_Architecture.md) | Source of truth — architecture, protocols, schemas |
| [Platform Architecture](docs/04_Platform_Architecture.md) | Platform infrastructure (Event Bus, Plugin Manager, Scilab Bridge) |
| [Feature Modules](docs/05_Feature_Modules.md) | User-facing modules (GUI Builder, Viz Studio, Data Studio, etc.) |
| [MVP Specification](docs/MVP_Specification.md) | What ships in v0.1 |
| [Architecture Decisions](docs/adr/) | Why we made key technical choices |
| **Feature Details** | |
| [Data Architecture](docs/07_Data_Architecture.md) | Data import, transformation pipelines, storage |
| [Digital Twin Framework](docs/08_Digital_Twin_Framework.md) | Digital twin modeling architecture |
| [Visualization Engine](docs/09_Visualization_Engine.md) | Chart types, rendering, theming |
| [Lab Creator](docs/10_Lab_Creator.md) | Interactive lab builder |
| [Report Generator](docs/11_Report_Generator.md) | Report creation and export |
| [Project Templates](docs/12_Project_Templates.md) | Template system for new projects |
| [AI Assistant](docs/13_AI_Assistant.md) | AI-powered coding assistant |
| **Developer** | |
| [API Reference](docs/14_API_Reference.md) | Platform APIs for plugin developers |
| [File Format](docs/15_File_Format.md) | .scstudio and project.json schemas |
| [Roadmap](docs/16_Roadmap.md) | Detailed development roadmap |
| [Development Guide](docs/17_Development_Guide.md) | Setting up the development environment |
| [UI/UX Guidelines](docs/18_UI_UX_Guidelines.md) | Design system and interaction patterns |
| [Deployment](docs/19_Deployment.md) | Build and distribution |
| [Marketplace](docs/32_Marketplace.md) | Plugin and widget marketplace |
| **Technical Specifications** | |
| [Technical Architecture](docs/20_Technical_Architecture.md) | Runtime architecture, IPC, memory, error handling |
| [Component Specification](docs/21_Component_Specification.md) | Svelte component hierarchy and APIs |
| [Project File Format](docs/22_Project_File_Format.md) | .scstudio project format, schemas, validation |
| [Event System](docs/23_Event_System.md) | Event Bus protocol, types, dispatch rules |
| [Plugin SDK](docs/24_Plugin_SDK.md) | Plugin lifecycle, manifest, context API |
| [Widget SDK](docs/25_Widget_SDK.md) | Widget creation, data binding, packaging |
| [Visualization Framework](docs/26_Visualization_Framework.md) | Rendering engine, chart types, export |
| [Data Architecture](docs/27_Data_Architecture.md) | Data model, import pipeline, transforms |
| [GUI Builder Specification](docs/28_GUI_Builder_Specification.md) | Drag-and-drop GUI designer details |
| [Report Generator Specification](docs/29_Report_Generator_Specification.md) | Report blocks, templates, export formats |
| [Learning Center Specification](docs/30_Learning_Center_Specification.md) | Examples, tutorials, Scilab reference |
| [Scilab Compatibility Layer](docs/31_Scilab_Compatibility_Layer.md) | Scilab discovery, lifecycle, JSON-RPC, marshalling |

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
