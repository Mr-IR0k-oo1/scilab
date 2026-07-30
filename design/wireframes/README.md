# Wireframes

All wireframes use ASCII. No mockups needed yet.

---

## Welcome Screen

```
+------------------------------------------------------------------+
|                                                                    |
|                         Scilab Studio                              |
|                                                                    |
|    +------------------+    +------------------+                   |
|    |                  |    |                  |                   |
|    |   New Project    |    |  Open Project    |                   |
|    |                  |    |                  |                   |
|    +------------------+    +------------------+                   |
|                                                                    |
|    +------------------+    +------------------+                   |
|    |                  |    |                  |                   |
|    |   From Template  |    |   Recent         |                   |
|    |                  |    |   Projects       |                   |
|    +------------------+    +------------------+                   |
|                                                                    |
|    Recent:                                                        |
|    +------------------------------------------------------------+ |
|    | signal-processing-lab          /home/user/projects/...     | |
|    | control-systems               /home/user/projects/...     | |
|    +------------------------------------------------------------+ |
|                                                                    |
+------------------------------------------------------------------+
```

---

## Main Workspace

```
+------------------------------------------------------------------+
| File  Edit  View  Run  Project  Plugins  Help          [-- □ ×] |
+------------------------------------------------------------------+
| [+New] [Open] [Save] | [▶ Run] [■ Stop] | [Undo] [Redo]        |
+------------------------------------------------------------------+
| Explorer    |  main.sce  utils.sce  data.csv      | Properties   |
|             |  +-------+--------+-----------+     |              |
| > project/  |  | Code Editor                       | Widget:     |
|   .scstudio |  |                                   | Button      |
|   main.sce  |  | function result = analyze(data)   |             |
|   utils.sce |  |     // Your code here             | Label:      |
|   data/     |  |     result = sin(data);           | [Run    ]   |
|     data.csv|  | endfunction                       |             |
|   gui/      |  |                                   | Width:      |
|     main.gui|  |                                   | [120     ]  |
|             |  |                                   |             |
|             |  |                                   | Height:     |
|             |  |                                   | [40      ]  |
+------------------------------------------------------------------+
| Console      Output      Problems      Terminal                   |
| > x = sin(0:0.1:10)                                               |
| > disp(x)                                                         |
| <result: 1x101 matrix>                                            |
+------------------------------------------------------------------+
| main.sce | Ln 42, Col 15 | Scilab 7.0.0 | UTF-8                 |
+------------------------------------------------------------------+
```

---

## GUI Builder

```
+------------------------------------------------------------------+
| File  Edit  View  Run  Project  Plugins  Help          [-- □ ×] |
+------------------------------------------------------------------+
| [+New] [Open] [Save] | [▶ Run] [Preview] | [Undo] [Redo]       |
+------------------------------------------------------------------+
| Widgets           |  Canvas                     | Properties     |
|                   |  +------------------------+ |                |
| > Input           |  |                        | | Widget:        |
|   Button          |  |  [Button]    [Label]   | | Button         |
|   Text Field      |  |                        | |                |
|   Slider          |  |  [________]  [■ Check] | | Label:         |
|   Checkbox        |  |                        | | [Run Sim]      |
|   Dropdown        |  |  [Dropdown]  [Table]   | |                |
|                   |  |                        | | Width:         |
| > Display         |  +------------------------+ | [120        ]  |
|   Label           |  Grid: [ON] Snap: [ON]     | |                |
|   Image           |  Zoom: [100%]              | | Height:        |
|   Table           |                            | | [40         ]  |
|   Panel           |                            | |                |
|                   |                            | | Events:        |
|                   |                            | | onClick:       |
|                   |                            | | [run_sim() ]   |
+------------------------------------------------------------------+
| Generated Scilab Code                                             |
| function create_gui()                                             |
|     uicontrol("style", "pushbutton", ...                         |
|               "string", "Run Sim", ...                            |
|               "callback", "run_sim()");                           |
| endfunction                                                       |
+------------------------------------------------------------------+
```

---

## Visualization Studio

```
+------------------------------------------------------------------+
| File  Edit  View  Run  Project  Plugins  Help          [-- □ ×] |
+------------------------------------------------------------------+
| [+New Chart] [Import Data] | [Export PNG] [Export CSV]           |
+------------------------------------------------------------------+
| Datasets          |  Chart                    | Properties       |
|                   |  +------------------------+ |                |
| > Measurements    |  |    *                   | | Chart Type:     |
|   voltage.csv     |  |   * *    *             | | [Line ▼]        |
|   current.csv     |  |  *   *  * *   *        | |                |
| > Calculated      |  | *     **   * *  *      | | Title:         |
|   power.sce       |  |           *    **      | | [Voltage vs    |
|                   |  +------------------------+ |  Current    ]  |
| Transforms        |  X: [Time] Y: [Voltage]   | |                |
|                   |                            | | X Label:       |
| > Normalize       |                            | | [Time (s)   ]  |
| > Filter          |                            | |                |
| > Aggregate       |                            | | Y Label:       |
|                   |                            | | [Voltage (V)]  |
+------------------------------------------------------------------+
```

---

## Plugin Manager

```
+------------------------------------------------------------------+
| Plugin Manager                                              [×]  |
+------------------------------------------------------------------+
| Installed    Available    Updates                                  |
+------------------------------------------------------------------+
| Search: [_________________________]                               |
|                                                                    |
| +----------------------------------------------------------------+
| | [Icon] Signal Analyzer                                          |
| | v1.2.0 | FOSSEE | GPL-3.0                                      |
| | Advanced signal processing tools                                |
| | [Configure] [Disable] [Uninstall]                              |
| +----------------------------------------------------------------+
| | [Icon] Circuit Simulator                                        |
| | v0.8.1 | Community | MIT                                       |
| | Simulate electrical circuits                                    |
| | [Configure] [Disable] [Uninstall]                              |
| +----------------------------------------------------------------+
| | [Icon] Data Cleaner                                             |
| | v1.0.0 | FOSSEE | GPL-3.0                                      |
| | Clean and validate datasets                                     |
| | [Configure] [Disable] [Uninstall]                              |
| +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

---

## Settings

```
+------------------------------------------------------------------+
| Settings                                                    [×]  |
+------------------------------------------------------------------+
| General    Editor    Scilab    Plugins    Themes    About         |
+------------------------------------------------------------------+
|                                                                    |
| Theme:                                                             |
| (●) Dark   ( ) Light   ( ) System                                 |
|                                                                    |
| Font Size:                                                         |
| [13] px                                                            |
|                                                                    |
| Auto-save:                                                         |
| [✓] Auto-save enabled                                              |
| Delay: [1000] ms                                                   |
|                                                                    |
| Scilab:                                                            |
| Version: [7.0.0 ▼]                                                |
| Path: [/usr/bin/scilab                                            ]
|                                                                    |
| Keyboard:                                                          |
| (●) Default (Ctrl on Linux/Windows)                               |
| ( ) macOS (Cmd)                                                    |
|                                                                    |
|                           [Save]  [Reset to Defaults]             |
+------------------------------------------------------------------+
```

---

## Report Generator

```
+------------------------------------------------------------------+
| File  Edit  View  Run  Project  Plugins  Help          [-- □ ×] |
+------------------------------------------------------------------+
| [+Block] [Add Chart] [Add Table] | [Export PDF] [Export HTML]   |
+------------------------------------------------------------------+
| Blocks              |  Editor                     | Properties    |
|                     |  +------------------------+ |               |
| > Content           |  | # Signal Analysis      | | Block Type:   |
|   Heading           |  |                        | | [Heading  ▼]  |
|   Paragraph         |  | This report analyzes   | |               |
|   Code Block        |  | the voltage signal     | | Level:        |
|   Equation          |  | from Experiment 1.     | | [2 ▼]         |
|                     |  |                        | |               |
| > Media             |  | ## Results             | | Content:      |
|   Image             |  |                        | | [Results  ]   |
|   Chart             |  | [Chart: voltage.png]   | |               |
|   Table             |  |                        | |               |
|                     |  | The signal shows...    | |               |
| > Data              |  |                        | |               |
|   Data Table        |  +------------------------+ |               |
|   Statistics        |                            |               |
+------------------------------------------------------------------+
```

---

## Template Gallery

```
+------------------------------------------------------------------+
| Templates                                                     [×] |
+------------------------------------------------------------------+
| All    Education    Research    Engineering    Blank               |
+------------------------------------------------------------------+
| Search: [_________________________]                               |
|                                                                    |
| +------------------+  +------------------+  +------------------+  |
| | Signal           |  | Control          |  | Data             |  |
| | Processing       |  | Systems          |  | Analysis         |  |
| |                  |  |                  |  |                  |  |
| | [Template        |  | [Template        |  | [Template        |  |
| |  Preview]        |  |  Preview]        |  |  Preview]        |  |
| |                  |  |                  |  |                  |  |
| | FOSSEE           |  | FOSSEE           |  | FOSSEE           |  |
| | 5 files          |  | 4 files          |  | 3 files          |  |
| | [Use Template]   |  | [Use Template]   |  | [Use Template]   |  |
| +------------------+  +------------------+  +------------------+  |
|                                                                    |
| +------------------+  +------------------+  +------------------+  |
| | Numerical        |  | Blank            |  | Custom...        |  |
| | Methods          |  |                  |  |                  |  |
| | FOSSEE           |  | Minimal          |  | Import from file |  |
| | 3 files          |  | 1 file           |  |                  |  |
| | [Use Template]   |  | [Use Template]   |  | [Import]         |  |
| +------------------+  +------------------+  +------------------+  |
+------------------------------------------------------------------+
```
