# Development Guide

> Complete guide for developers working on Scilab Studio — from setup to release.

---

## Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 18+ LTS | Runtime and build tools |
| npm | 9+ | Package management |
| Git | 2.30+ | Version control |
| Scilab | 2024.0+ | Numerical engine |
| C/C++ compiler | Recent | Native module compilation |
| VS Code | Latest | Recommended IDE |

### Scilab Installation

**Linux:**
```bash
sudo apt-get install scilab
# Or download from https://www.scilab.org/download
```

**macOS:**
```bash
brew install scilab
```

**Windows:**
Download from https://www.scilab.org/download and add to PATH.

Verify:
```bash
scilab -version
```

---

## Development Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/scilab-studio/scilab-studio.git
cd scilab-studio
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your local settings:
```env
SCILAB_PATH=/usr/local/bin/scilab
DEV_PORT=3000
LOG_LEVEL=debug
```

### 4. Build the Project

```bash
npm run build
```

### 5. Start Development Mode

```bash
npm run dev
```

This starts the application with hot-reload enabled. Changes to source files will automatically rebuild and refresh.

### 6. Recommended VS Code Extensions

Install when prompted by the workspace, or manually:

- TypeScript Hero
- ESLint
- Prettier
- Jest Runner
- GitLens
- Tailwind CSS IntelliSense

---

## Repository Structure

```
scilab-studio/
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml          # Continuous integration
│       ├── release.yml     # Release automation
│       └── docs.yml        # Documentation build
├── docs/                   # Project documentation
│   ├── 01_Getting_Started.md
│   ├── 02_Architecture.md
│   ├── ...
│   └── 20_Marketplace.md
├── src/                    # Application source code
│   ├── core/               # Core runtime
│   │   ├── plugin-runtime/ # Plugin loading and lifecycle
│   │   ├── module-bus/     # Inter-module communication
│   │   ├── config/         # Configuration management
│   │   └── project-model/  # Project file management
│   ├── modules/            # Feature modules (18 total)
│   │   ├── gui-builder/
│   │   ├── visualization/
│   │   ├── data-studio/
│   │   ├── ai-assistant/
│   │   ├── parameter-sweep/
│   │   ├── experiment-recorder/
│   │   ├── report-generator/
│   │   ├── lab-creator/
│   │   ├── digital-twin/
│   │   ├── xcos-builder/
│   │   ├── learning-center/
│   │   ├── marketplace-client/
│   │   ├── code-editor/
│   │   ├── terminal/
│   │   ├── file-explorer/
│   │   ├── version-control/
│   │   ├── settings/
│   │   └── theme-manager/
│   ├── engine/             # Scilab engine integration
│   │   ├── wrapper.ts      # Engine process management
│   │   ├── session.ts      # Session lifecycle
│   │   ├── executor.ts     # Code execution
│   │   └── ipc.ts          # IPC communication
│   ├── ui/                 # Shared UI components
│   │   ├── components/     # Reusable components
│   │   ├── layouts/        # Layout components
│   │   ├── hooks/          # Custom React hooks
│   │   └── styles/         # Global styles
│   ├── services/           # Shared services
│   │   ├── marketplace.ts  # Marketplace API client
│   │   ├── auth.ts         # Authentication
│   │   ├── analytics.ts    # Usage analytics (opt-in)
│   │   └── updater.ts      # Auto-update
│   ├── types/              # TypeScript type definitions
│   └── main.ts             # Application entry point
├── modules/                # Module definitions (manifests)
│   ├── gui-builder/
│   │   └── manifest.json
│   └── ...
├── sdk/                    # SDKs for extension development
│   ├── plugin-sdk/         # Plugin development kit
│   ├── template-sdk/       # Template development kit
│   └── widget-sdk/         # Widget development kit
├── tests/                  # Test suites
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
├── scripts/                # Build and utility scripts
├── .vscode/                # VS Code workspace settings
├── package.json            # Project manifest
├── tsconfig.json           # TypeScript configuration
├── .eslintrc.json          # ESLint configuration
├── .prettierrc.json        # Prettier configuration
├── vite.config.ts          # Build configuration
├── jest.config.js          # Test configuration
├── playwright.config.ts    # E2E test configuration
└── README.md
```

---

## Building from Source

### Standard Build
```bash
npm run build
```

### Development Build (with source maps)
```bash
npm run build:dev
```

### Production Build (optimized)
```bash
npm run build:prod
```

### Clean Build
```bash
npm run clean
npm install
npm run build
```

### Build for Specific Platform
```bash
npm run build:linux
npm run build:macos
npm run build:windows
```

---

## Running Tests

### All Tests
```bash
npm run test
```

### Unit Tests Only
```bash
npm run test:unit
```

### Integration Tests Only
```bash
npm run test:integration
```

### E2E Tests Only
```bash
npm run test:e2e
```

### With Coverage
```bash
npm run test:coverage
```

### Watch Mode (during development)
```bash
npm run test:watch
```

### Running a Specific Test File
```bash
npx jest tests/unit/core/plugin-runtime.test.ts
```

---

## Code Architecture for Developers

### Module Communication

Modules communicate through the **Event Bus** — a publish-subscribe system that decouples modules from each other.

```typescript
// Publishing an event
import { eventBus } from '@scilab-studio/core';

eventBus.publish('data:imported', {
  datasetId: 'ds_001',
  rowCount: 1000,
  columns: ['timestamp', 'value']
});

// Subscribing to an event
eventBus.subscribe('data:imported', (event) => {
  console.log(`Dataset ${event.datasetId} imported with ${event.rowCount} rows`);
});
```

### Plugin Lifecycle

Plugins go through a defined lifecycle:

```
load → activate → [running] → deactivate → unload
```

```typescript
// Plugin entry point
export function activate(context: PluginContext) {
  // Register commands, views, event handlers
  context.commands.register('my-command', handleCommand);
  context.views.register('my-panel', MyPanelComponent);
}

export function deactivate(context: PluginContext) {
  // Clean up resources
}
```

### State Management

Application state is managed through Zustand stores:

```typescript
import { create } from 'zustand';

interface ProjectState {
  currentProject: Project | null;
  recentProjects: Project[];
  openProject: (path: string) => Promise<void>;
  closeProject: () => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  recentProjects: [],
  openProject: async (path) => {
    const project = await projectService.open(path);
    set({ currentProject: project });
  },
  closeProject: () => set({ currentProject: null }),
}));
```

---

## Adding a New Module

### 1. Create the Module Directory

```bash
mkdir -p src/modules/my-module/src
mkdir -p src/modules/my-module/tests
```

### 2. Create the Manifest

```json
{
  "name": "my-module",
  "version": "0.1.0",
  "description": "Description of my module",
  "entryPoint": "src/index.ts",
  "dependencies": ["core"],
  "permissions": ["read:project"]
}
```

### 3. Implement the Module

```typescript
// src/modules/my-module/src/index.ts
import { Module, ModuleContext } from '@scilab-studio/core';

export class MyModule implements Module {
  id = 'my-module';

  async activate(context: ModuleContext) {
    // Register views, commands, event handlers
    context.views.register('main', MyMainView);
    context.commands.register('my-action', handleAction);
    context.eventBus.subscribe('project:opened', onProjectOpened);
  }

  async deactivate() {
    // Clean up
  }
}
```

### 4. Add Tests

```typescript
// src/modules/my-module/tests/my-module.test.ts
import { MyModule } from '../src/index';

describe('MyModule', () => {
  it('should activate without errors', async () => {
    const mod = new MyModule();
    await expect(mod.activate(mockContext)).resolves.not.toThrow();
  });
});
```

### 5. Register the Module

Add the module to `src/core/module-registry/modules.json`.

---

## Adding a New Plugin

### 1. Scaffold the Plugin

```bash
npx @scilab-studio/sdk plugin create my-plugin
```

### 2. Edit the Manifest

Edit `plugin.json` with your plugin metadata.

### 3. Implement the Plugin

```typescript
// src/index.ts
import { PluginContext } from '@scilab-studio/plugin-sdk';

export function activate(context: PluginContext) {
  context.commands.register('hello', () => {
    context.window.showInformationMessage('Hello from my plugin!');
  });
}

export function deactivate(context: PluginContext) {
  // Cleanup
}
```

### 4. Test Locally

```bash
npm run dev
# In the app, go to Settings > Plugins > Load from Directory
# Select your plugin directory
```

### 5. Package for Distribution

```bash
npm run plugin:package
# Creates my-plugin.v1.0.0.spkg
```

---

## Adding a New Visualization Type

### 1. Create the Chart Module

```typescript
// src/modules/visualization/src/charts/my-chart.ts
import { Chart, ChartConfig, ChartData } from '../types';

export class MyChart implements Chart {
  type = 'my-chart';

  render(canvas: HTMLCanvasElement, data: ChartData, config: ChartConfig) {
    // Implement rendering logic
  }

  update(data: ChartData) {
    // Implement data update
  }

  export(format: 'png' | 'svg' | 'pdf'): Blob {
    // Implement export
  }
}
```

### 2. Register the Chart Type

```typescript
// src/modules/visualization/src/registry.ts
chartRegistry.register('my-chart', MyChart);
```

### 3. Add to the Chart Picker

Update the chart type list in the visualization module's UI.

### 4. Write Tests

Test rendering with various data shapes and configurations.

---

## Debugging Guide

### Application Logs

Logs are stored in:
- **Linux:** `~/.scilab-studio/logs/`
- **macOS:** `~/Library/Logs/Scilab Studio/`
- **Windows:** `%APPDATA%/Scilab Studio/logs/`

### Debug Mode

```bash
# Run with debug logging
DEBUG=scilab-studio:* npm run dev

# Run with specific module debugging
DEBUG=scilab-studio:engine npm run dev
```

### VS Code Debug Configuration

Use the provided `.vscode/launch.json`:
1. Open the Debug panel (Ctrl+Shift+D)
2. Select "Scilab Studio" from the dropdown
3. Press F5 to start debugging

### Scilab Engine Debugging

```bash
# Run Scilab in interactive mode for debugging
scilab -nw

# Check engine connectivity
npm run debug:engine
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Plugin fails to load | Check plugin.json syntax and entry point path |
| Engine won't start | Verify SCILAB_PATH in .env |
| Build fails | Run `npm run clean && npm install` |
| Tests fail in CI but pass locally | Check environment variables and Scilab version |

---

## Performance Profiling

### Frontend Profiling

1. Open Chrome DevTools (Electron: Ctrl+Shift+I)
2. Go to the Performance tab
3. Record a session
4. Analyze flame chart for bottlenecks

### Backend Profiling

```bash
# Profile Node.js process
node --inspect-brk dist/main.js

# Connect Chrome DevTools to Node.js
# Open chrome://inspect in Chrome
```

### Scilab Engine Profiling

```scilab
// In Scilab, profile code execution
tic();
// ... your code ...
elapsed = toc();
mprintf("Execution time: %.3f seconds\n", elapsed);
```

### Performance Benchmarking

```bash
npm run benchmark
```

Runs standardized benchmarks for:
- Application startup time
- Chart rendering speed
- Data import performance
- Code execution latency

---

## CI/CD Pipeline

### Pipeline Stages

```
Push/PR → Lint → Type Check → Unit Tests → Integration Tests → Build → E2E Tests → Deploy
```

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | Push, PR | Run all checks |
| `release.yml` | Tag push | Build and publish release |
| `docs.yml` | Docs change | Build and deploy documentation |
| `nightly.yml` | Cron (daily) | Run full test suite + security scan |

### Quality Gates

All PRs must pass:
- ESLint with zero errors
- TypeScript compilation with zero errors
- Unit test pass rate: 100%
- Code coverage: ≥ 80%
- Build succeeds on all 3 platforms
- E2E critical path tests pass

---

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR:** Breaking changes to APIs or file formats.
- **MINOR:** New features, backward-compatible.
- **PATCH:** Bug fixes, backward-compatible.

### Release Steps

1. **Create a release branch:**
   ```bash
   git checkout -b release/v0.2.0 main
   ```

2. **Update version in package.json:**
   ```bash
   npm version minor --no-git-tag-version
   ```

3. **Update CHANGELOG.md** with all changes.

4. **Create a PR and get approval.**

5. **Merge to main.**

6. **Create a GitHub Release with a tag:**
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

7. **CI builds and publishes:**
   - GitHub Release with binaries for Linux, macOS, Windows.
   - npm package update.
   - Documentation site update.

### Post-Release

- Announce on community channels.
- Update the project website.
- Monitor issue tracker for regression reports.
