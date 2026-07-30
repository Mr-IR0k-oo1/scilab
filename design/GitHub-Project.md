# GitHub Project Structure

## Milestones

### Milestone 0: Foundation
- Repository setup
- Documentation
- Architecture diagrams
- Design artifacts

### Milestone 1: Workspace
- Main window with Tauri
- File explorer
- Tab system
- Project system (.scstudio)
- Settings

### Milestone 2: Runtime
- Scilab sidecar process
- JSON-RPC bridge
- Code editor
- Console output
- Variable inspection

### Milestone 3: GUI Builder
- Canvas with grid
- Widget palette (9 widgets)
- Drag and drop
- Property inspector
- Code generation
- Preview mode

### Milestone 4: Visualization
- Chart registry
- Line chart
- Scatter chart
- Bar chart
- Heatmap
- Export (PNG, SVG, CSV)

### Milestone 5: Data & Reports
- CSV import
- Data preview
- Column statistics
- Report editor
- PDF export
- HTML export

## Epic → Feature → Task Breakdown

### Epic: Workspace

**Feature: Project System**
- Task: Define project.json schema
- Task: Create project directory structure
- Task: Implement project creation
- Task: Implement project open
- Task: Implement project save
- Task: Add project settings

**Feature: File Explorer**
- Task: Build directory tree component
- Task: Implement file icons by extension
- Task: Add right-click context menu
- Task: Implement file create/delete/rename
- Task: Watch for external changes

**Feature: Tab System**
- Task: Build tab bar component
- Task: Implement tab open/close/switch
- Task: Add dirty indicator
- Task: Implement tab reordering
- Task: Handle tab overflow

**Feature: Status Bar**
- Task: Build status bar component
- Task: Show current file path
- Task: Show line/column
- Task: Show Scilab version

### Epic: Runtime

**Feature: Scilab Bridge**
- Task: Spawn Scilab process
- Task: Implement JSON-RPC client
- Task: Implement command queue
- Task: Add timeout handling
- Task: Add crash recovery

**Feature: Code Editor**
- Task: Integrate code editor component
- Task: Add syntax highlighting
- Task: Implement run command (F5)
- Task: Show errors in problems panel

**Feature: Console**
- Task: Build console panel
- Task: Stream Scilab output
- Task: Implement command history
- Task: Add clear command

### Epic: GUI Builder

**Feature: Canvas**
- Task: Build canvas component
- Task: Implement grid and snap
- Task: Add zoom/pan
- Task: Implement selection (click, rubber band)

**Feature: Widget Palette**
- Task: Build palette component
- Task: Implement drag from palette
- Task: Add 9 built-in widgets
- Task: Group by category

**Feature: Property Inspector**
- Task: Build inspector panel
- Task: Show selected widget properties
- Task: Implement property editing
- Task: Add data binding

**Feature: Code Generation**
- Task: Generate Scilab GUI code
- Task: Preview generated code
- Task: Sync with canvas changes

### Epic: Visualization

**Feature: Chart Engine**
- Task: Build chart registry
- Task: Implement Canvas 2D renderer
- Task: Add theme integration

**Feature: Chart Types**
- Task: Line chart
- Task: Scatter chart
- Task: Bar chart
- Task: Heatmap

**Feature: Chart Interaction**
- Task: Tooltip on hover
- Task: Zoom/pan
- Task: Data point selection

**Feature: Chart Export**
- Task: Export PNG
- Task: Export SVG
- Task: Export CSV

### Epic: Data & Reports

**Feature: Data Import**
- Task: CSV parser
- Task: Auto-detect types
- Task: Data preview table
- Task: Column statistics

**Feature: Report Editor**
- Task: Block-based editor
- Task: Add heading block
- Task: Add paragraph block
- Task: Add chart block
- Task: Add table block
- Task: Add code block

**Feature: Report Export**
- Task: Export PDF
- Task: Export HTML
- Task: Embed charts
