import type { ReportBlock } from './ReportEditor';

const BLOCK_TYPES: { type: ReportBlock['type']; label: string; icon: string }[] = [
  { type: 'heading', label: 'Heading', icon: 'H' },
  { type: 'paragraph', label: 'Paragraph', icon: '¶' },
  { type: 'chart', label: 'Chart', icon: '◈' },
  { type: 'table', label: 'Table', icon: '▣' },
  { type: 'image', label: 'Image', icon: '▤' },
  { type: 'code', label: 'Code', icon: '<>' },
  { type: 'divider', label: 'Divider', icon: '—' },
  { type: 'page-break', label: 'Page Break', icon: '..' },
];

interface BlockPaletteProps {
  onAdd: (type: ReportBlock['type']) => void;
}

export default function BlockPalette({ onAdd }: BlockPaletteProps) {
  return (
    <div className="report-palette">
      <h3>Blocks</h3>
      {BLOCK_TYPES.map((bt) => (
        <button key={bt.type} className="palette-item" onClick={() => onAdd(bt.type)}>
          <span className="palette-icon">{bt.icon}</span>
          {bt.label}
        </button>
      ))}
    </div>
  );
}
