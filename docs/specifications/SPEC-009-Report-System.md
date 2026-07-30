# SPEC-009 — Report System

## Purpose

Build reports visually using drag-and-drop blocks. Reports embed charts, tables, text, and images. Export to PDF and HTML.

---

## Block Types

### Heading
| Property | Type | Default |
|----------|------|---------|
| text | string | "Heading" |
| level | number | 1 (1–6) |
| fontSize | number | auto from level |
| fontColor | string | "#000000" |
| align | string | "left" |

### Paragraph
| Property | Type | Default |
|----------|------|---------|
| text | string | "" |
| fontSize | number | 11 |
| lineHeight | number | 1.5 |
| align | string | "left" |

### Chart
| Property | Type | Default |
|----------|------|---------|
| chartId | string? | null (linked to Visualization Studio) |
| chartType | string | "line" |
| data | ChartData? | null (inline) |
| width | number | 100% |
| height | number | 300 |

### Table
| Property | Type | Default |
|----------|------|---------|
| dataSource | string? | null (linked to Data Studio) |
| headers | string[] | [] |
| rows | (string\|number)[][] | [] |
| showHeader | boolean | true |
| showGrid | boolean | true |
| altRowColor | string | "#f5f5f5" |

### Image
| Property | Type | Default |
|----------|------|---------|
| src | string | "" |
| alt | string | "" |
| width | number | 100% |
| align | string | "center" |

### Code
| Property | Type | Default |
|----------|------|---------|
| code | string | "" |
| language | string | "scilab" |
| showLineNumbers | boolean | false |
| fontSize | number | 10 |

### Divider
| Property | Type | Default |
|----------|------|---------|
| style | string | "solid" |
| color | string | "#cccccc" |
| thickness | number | 1 |

### Page Break
No properties. Forces a page break.

---

## Page Layout

| Size | Dimensions (pt) | Margins |
|------|-----------------|---------|
| A4 | 595 × 842 | 72pt |
| Letter | 612 × 792 | 72pt |
| Custom | User-defined | User-defined |

Orientation: portrait or landscape.

---

## Templates

### Built-in
- blank, lab-report, project-report, data-analysis, presentation

### Custom
Save any report as a template. Stored in `~/.scilab-studio/templates/`.

---

## Data Binding

| Source | Syntax | Description |
|--------|--------|-------------|
| Scilab Variable | scilab:variableName | Live value |
| Dataset | dataset:datasetId | Imported dataset |
| Chart | chart:chartId | Visualization Studio chart |
| Template Variable | {{variableName}} | Filled at generation |

### Auto-Fill Variables

| Variable | Value |
|----------|-------|
| {{title}} | Report title |
| {{date}} | Current date |
| {{author}} | Project author |
| {{page}} | Current page number |
| {{totalPages}} | Total page count |

---

## Export

### PDF
- Rendered via Rust `printpdf` crate.
- All blocks, images, styled text supported.
- Page breaks honored.
- Fonts embedded (subset).

### HTML
- Self-contained HTML file.
- All styles inlined.
- Images base64-embedded.
- Responsive layout.

### LaTeX (v0.2)
- Rendered as `.tex` file.
- Compilable with `pdflatex`.

---

## Generation Flow

```
1. User clicks "Generate Report"
2. Validate all data bindings
3. Fetch data (Scilab, files, inline)
4. Render charts at block dimensions
5. Paginate tables
6. Flow text through pages
7. Insert page breaks
8. Add headers/footers
9. Write to reports/<name>_v<N>.<format>
10. Show notification
11. Offer to open in system viewer
```

---

## UI

### Report Canvas
- WYSIWYG editor with page layout.
- Blocks dragged from palette.
- Reorderable via drag-and-drop.
- Resize handles on each block.
- Property inspector on right sidebar.

### Block Palette
- Text blocks (heading, paragraph).
- Data blocks (chart, table, image).
- Code blocks.
- Layout blocks (divider, page break).

---

## Constraints

| Constraint | Value |
|------------|-------|
| Max blocks per report | 200 |
| Max pages | 100 |
| Max embedded images | 50 |
| Image max resolution | 300 DPI |
| Report generation timeout | 60s |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Data binding source missing | Show "Data unavailable" placeholder |
| Chart render fails | Show error block |
| Image not found | Show broken image icon |
| PDF generation fails | Show error, offer HTML fallback |
| Page overflow | Auto-paginate or warn |

---

## Extension Points

- Custom block types.
- Custom export formats.
- Custom page layouts.
- Custom template variables.
- Report automation (scheduled generation).
