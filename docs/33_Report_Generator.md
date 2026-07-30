# Scilab Studio — Report Generator Specification

**Version:** 1.0.0
**Status:** Normative
**Last Updated:** 2026-07-27

This document specifies the Report Generator: visual report builder, block types, template system, and export formats. For the Report Generator feature overview, see [Feature Modules §2.5](05_Feature_Modules.md).

---

## 1. Architecture

### 1.1 Report Builder Components

```
Report Generator
├── Report Canvas (WYSIWYG editor)
│   ├── Page layout (A4/Letter)
│   ├── Block editor
│   ├── Drag-and-drop reordering
│   └── Resize handles
├── Block Palette (left sidebar)
│   ├── Text blocks (heading, paragraph)
│   ├── Data blocks (chart, table, image)
│   ├── Code blocks
│   └── Layout blocks (divider, pagebreak)
├── Property Inspector (right sidebar)
│   ├── Block properties
│   ├── Style properties
│   └── Data bindings
├── Template Manager
│   ├── Built-in templates
│   ├── Custom templates
│   └── Import/export
└── Export Engine
    ├── PDF renderer (Rust crate: printpdf)
    ├── HTML renderer
    └── LaTeX renderer (v0.2)
```

---

## 2. Report Block Types

### 2.1 Text Blocks

#### Heading

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | string | `"Heading"` | Heading text |
| `level` | number | `1` | Heading level (1–6) |
| `fontSize` | number | auto | Font size (pt), auto from level |
| `fontColor` | string | `"#000000"` | Text color |
| `fontFamily` | string | `"sans-serif"` | Font family |
| `align` | string | `"left"` | `"left"` \| `"center"` \| `"right"` |

**Auto font sizes:** H1=24pt, H2=20pt, H3=16pt, H4=14pt, H5=12pt, H6=11pt.

#### Paragraph

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | string | `"Paragraph text..."` | Content (supports basic markdown) |
| `fontSize` | number | `11` | Font size (pt) |
| `fontColor` | string | `"#000000"` | Text color |
| `lineHeight` | number | `1.5` | Line height multiplier |
| `align` | string | `"left"` | `"left"` \| `"center"` \| `"right"` \| `"justify"` |

### 2.2 Data Blocks

#### Chart

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `chartId` | string? | `null` | Linked Visualization Studio chart |
| `chartType` | string | `"line"` | Chart type (if not linked) |
| `data` | ChartData? | `null` | Inline data (if not linked) |
| `width` | number | `100%` | Width (% of page or px) |
| `height` | number | `300` | Height (px) |
| `showTitle` | boolean | `true` | Show chart title |
| `showLegend` | boolean | `true` | Show legend |

**Behavior:**
- If linked to a Visualization Studio chart, the chart is rendered at the block's dimensions.
- If inline data is provided, a new chart is rendered with the specified type and data.
- Charts update in the report preview when the source data changes.

#### Table

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | string? | `null` | Linked dataset ID |
| `headers` | string[] | `[]` | Column headers |
| `rows` | (string\|number)[][] | `[]` | Inline data rows |
| `showHeader` | boolean | `true` | Show header row |
| `showGrid` | boolean | `true` | Show grid lines |
| `headerStyle` | object | `{}` | Header styling |
| `cellStyle` | object | `{}` | Cell styling |
| `altRowColor` | string | `"#f5f5f5"` | Alternating row color |

**Behavior:**
- If linked to a Data Studio dataset, the table renders the first 100 rows.
- If inline rows are provided, those are rendered directly.
- Table content is paginated across pages if it exceeds one page.

#### Image

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `src` | string | `""` | Image path (relative to project or URL) |
| `alt` | string | `""` | Alt text |
| `width` | number | `100%` | Width |
| `height` | number | auto | Height (maintains aspect ratio) |
| `align` | string | `"center"` | `"left"` \| `"center"` \| `"right"` |

### 2.3 Code Blocks

#### Code

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `code` | string | `""` | Code content |
| `language` | string | `"scilab"` | Language for syntax highlighting |
| `showLineNumbers` | boolean | `false` | Show line numbers |
| `fontSize` | number | `10` | Font size (pt) |
| `wrap` | boolean | `false` | Wrap long lines |
| `maxHeight` | number | `400` | Max height before scroll |

### 2.4 Layout Blocks

#### Divider

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `style` | string | `"solid"` | `"solid"` \| `"dashed"` \| `"dotted"` |
| `color` | string | `"#cccccc"` | Line color |
| `thickness` | number | `1` | Line thickness (px) |
| `margin` | number | `16` | Vertical margin (px) |

#### Page Break

No properties. Forces a page break at this position.

---

## 3. Page Layout

### 3.1 Page Sizes

| Size | Dimensions (pt) | Margins |
|------|-----------------|---------|
| A4 | 595 × 842 | 72pt (1 inch) all sides |
| Letter | 612 × 792 | 72pt all sides |
| Legal | 612 × 1008 | 72pt all sides |
| Custom | User-defined | User-defined |

### 3.2 Page Properties

```typescript
interface PageLayout {
  size: "A4" | "Letter" | "Legal" | "Custom";
  width?: number;        // Custom width in pt
  height?: number;       // Custom height in pt
  margins: {
    top: number;         // Default 72
    right: number;
    bottom: number;
    left: number;
  };
  orientation: "portrait" | "landscape";
}
```

### 3.3 Header/Footer

Reports can optionally include headers and footers:

```typescript
interface HeaderFooter {
  enabled: boolean;
  content?: string;       // Static text or template variables
  fontSize: number;       // Default 9
  fontColor: string;      // Default "#666666"
  align: "left" | "center" | "right";
  showOnFirstPage: boolean;  // Default true
}

// Template variables: {{title}}, {{date}}, {{page}}, {{totalPages}}
```

---

## 4. Template System

### 4.1 Built-in Templates

| Template | Description |
|----------|-------------|
| `blank` | Empty report |
| `lab-report` | Title, abstract, methods, results, conclusion sections |
| `project-report` | Executive summary, data, analysis, recommendations |
| `data-analysis` | Data overview, statistics, visualizations, summary |
| `presentation` | Large text, minimal layout, slide-like pages |

### 4.2 Template Schema

```typescript
interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  thumbnail?: string;       // Base64 or file path
  page: PageLayout;
  blocks: ReportBlock[];
  styles: {
    heading: { fontFamily, fontSize, fontColor, marginBottom };
    paragraph: { fontFamily, fontSize, lineHeight, marginBottom };
    code: { fontFamily, fontSize, backgroundColor, padding };
  };
  header?: HeaderFooter;
  footer?: HeaderFooter;
}
```

### 4.3 Custom Templates

Users can save any report as a template:
1. Open the report in the Report Generator.
2. Click Save As Template.
3. Provide a name and description.
4. The template is saved to `~/.scilab-studio/templates/`.

---

## 5. Export Formats

### 5.1 PDF

- Rendered via the Rust `printpdf` crate.
- Supports all block types, images, and styled text.
- Page breaks are honored.
- Images are embedded at their original resolution.
- Fonts are embedded (subsetting for file size).

**Export options:**

```typescript
interface PdfExportOptions {
  pageSize: "A4" | "Letter" | "Custom";
  orientation: "portrait" | "landscape";
  margins: { top, right, bottom, left };
  includeHeader: boolean;
  includeFooter: boolean;
  compression: boolean;       // Default true
  imageQuality: number;       // 0.1–1.0, default 0.92
}
```

### 5.2 HTML

- Rendered as a self-contained HTML file.
- All styles are inlined (no external CSS).
- Images are base64-embedded.
- Responsive layout (works in any browser).

**Export options:**

```typescript
interface HtmlExportOptions {
  standalone: boolean;        // Self-contained HTML (default true)
  darkMode: boolean;          // Include dark mode styles
  interactive: boolean;       // Enable chart tooltips (default true)
}
```

### 5.3 LaTeX (v0.2)

- Rendered as a `.tex` file.
- Uses standard LaTeX packages.
- Can be compiled to PDF with `pdflatex`.

---

## 6. Report Generation Flow

```
1. User clicks "Generate Report"
2. Platform validates all data bindings
3. Data is fetched (from Scilab, imported files, inline)
4. Charts are rendered at block dimensions
5. Tables are paginated
6. Text is flowed through pages
7. Page breaks are inserted
8. Headers/footers are added
9. Output is written to `reports/<name>_v<version>.<format>`
10. Notification shown: "Report generated: <filename>"
11. Option to open in system viewer
```

---

## 7. Data Binding

### 7.1 Binding Sources

| Source | Syntax | Description |
|--------|--------|-------------|
| Scilab Variable | `scilab:variableName` | Live variable value |
| Dataset | `dataset:datasetId` | Imported dataset |
| Chart | `chart:chartId` | Visualization Studio chart |
| Static | (literal value) | Fixed text/number |
| Template Variable | `{{variableName}}` | Filled at generation time |

### 7.2 Auto-Fill Variables

| Variable | Value |
|----------|-------|
| `{{title}}` | Report title from project settings |
| `{{date}}` | Current date (YYYY-MM-DD) |
| `{{time}}` | Current time (HH:MM) |
| `{{author}}` | Project author name |
| `{{project}}` | Project name |
| `{{version}}` | Report version |
| `{{page}}` | Current page number |
| `{{totalPages}}` | Total page count |
