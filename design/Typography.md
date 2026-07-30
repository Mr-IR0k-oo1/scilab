# Typography

## Font Family

```css
--ss-font-family: 'Inter', system-ui, -apple-system, sans-serif;
--ss-font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
```

## Type Scale

| Token | Size | Weight | Line Height | Use |
|-------|------|--------|-------------|-----|
| `text-2xs` | 10px | 400 | 14px | Footnotes, badges |
| `text-xs` | 11px | 400 | 16px | Code snippets, metadata |
| `text-sm` | 12px | 400 | 16px | Small labels, hints |
| `text-md` | 13px | 400 | 20px | Body text, UI labels |
| `text-lg` | 14px | 400 | 20px | Primary text |
| `text-xl` | 16px | 500 | 24px | Subheadings |
| `text-2xl` | 18px | 600 | 28px | Section headings |
| `text-3xl` | 20px | 600 | 32px | Page titles |
| `text-4xl` | 24px | 600 | 36px | Hero headings |

## Usage

```css
/* Body text */
body {
  font-family: var(--ss-font-family);
  font-size: var(--ss-text-lg);
  line-height: 1.5;
}

/* Code */
code {
  font-family: var(--ss-font-mono);
  font-size: var(--ss-text-sm);
}

/* Section heading */
h2 {
  font-size: var(--ss-text-2xl);
  font-weight: 600;
  line-height: 1.3;
}
```

## Rules

- Never go below 10px. Text smaller than 10px is unreadable.
- Use `font-weight: 500` for labels, `600` for headings.
- Monospace font for code, terminal, and data values.
- Consistent line height: 1.4 for body, 1.2 for headings.
