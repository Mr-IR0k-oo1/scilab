import { useState } from 'react';
import BlockPalette from './BlockPalette';
import ReportPreview from './ReportPreview';

export interface ReportBlock {
  id: string;
  type: 'heading' | 'paragraph' | 'chart' | 'table' | 'image' | 'code' | 'divider' | 'page-break';
  props: Record<string, any>;
}

let blockCounter = 0;

function generateHTML(blocks: ReportBlock[]): string {
  let html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Report</title>';
  html += '<style>body{font-family:sans-serif;max-width:800px;margin:40px auto;padding:0 20px;line-height:1.6}h1,h2,h3{color:#333}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:8px}pre{background:#1a1a2e;color:#abb2bf;padding:12px;border-radius:4px;overflow-x:auto}.page-break{page-break-after:always}hr{border:none;border-top:1px solid #ddd}</style></head><body>';
  for (const b of blocks) {
    switch (b.type) {
      case 'heading': html += `<h${b.props.level ?? 1}>${b.props.text ?? ''}</h${b.props.level ?? 1}>`; break;
      case 'paragraph': html += `<p>${(b.props.text ?? '').replace(/\n/g, '<br>')}</p>`; break;
      case 'divider': html += '<hr>'; break;
      case 'page-break': html += '<div class="page-break"></div>'; break;
      case 'table': html += '<table><thead><tr>' + (b.props.headers ?? []).map((h: string) => `<th>${h}</th>`).join('') + '</tr></thead><tbody>' + (b.props.rows ?? []).map((row: string[]) => '<tr>' + row.map((c: string) => `<td>${c}</td>`).join('') + '</tr>').join('') + '</tbody></table>'; break;
      case 'code': html += `<pre><code>${b.props.code ?? ''}</code></pre>`; break;
      case 'chart': html += `<div style="height:${b.props.height ?? 300}px;background:#f5f5f5;display:flex;align-items:center;justify-content:center;color:#999;border:1px solid #ddd;border-radius:4px">[${b.props.chartType ?? 'line'} chart]</div>`; break;
      case 'image': html += b.props.src ? `<img src="${b.props.src}" alt="${b.props.alt ?? ''}" style="max-width:100%">` : '<div style="padding:40px;background:#f5f5f5;text-align:center;color:#999">[Image]</div>'; break;
    }
  }
  html += '</body></html>';
  return html;
}

export default function ReportEditor() {
  const [blocks, setBlocks] = useState<ReportBlock[]>([
    { id: 'b-1', type: 'heading', props: { text: 'Report Title', level: 1 } },
    { id: 'b-2', type: 'paragraph', props: { text: 'This is an auto-generated report from Scilab Studio.' } },
  ]);
  const [message, setMessage] = useState('');

  const addBlock = (type: ReportBlock['type']) => {
    const defaults: Record<string, any> = {
      heading: { text: 'New Heading', level: 2 },
      paragraph: { text: 'New paragraph text...' },
      chart: { chartType: 'line', height: 300 },
      table: { headers: ['Col 1', 'Col 2'], rows: [['Val 1', 'Val 2']] },
      image: { src: '', alt: '' },
      code: { code: '// Scilab code', language: 'scilab' },
      divider: { style: 'solid' },
      'page-break': {},
    };
    setBlocks((prev) => [...prev, { id: `block-${++blockCounter}`, type, props: defaults[type] ?? {} }]);
  };

  const updateBlock = (id: string, props: Record<string, any>) => {
    setBlocks((prev) => prev.map((b) => b.id === id ? { ...b, props } : b));
  };

  const removeBlock = (id: string) => {
    setBlocks((prev) => prev.filter((b) => b.id !== id));
  };

  const moveBlock = (id: string, dir: 'up' | 'down') => {
    const idx = blocks.findIndex((b) => b.id === id);
    if (idx < 0) return;
    const newIdx = dir === 'up' ? idx - 1 : idx + 1;
    if (newIdx < 0 || newIdx >= blocks.length) return;
    const next = [...blocks];
    [next[idx], next[newIdx]] = [next[newIdx], next[idx]];
    setBlocks(next);
  };

  const handleExportHTML = () => {
    const html = generateHTML(blocks);
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'report.html'; a.click();
    URL.revokeObjectURL(url);
    setMessage('Report exported as HTML');
    setTimeout(() => setMessage(''), 3000);
  };

  const handleExportPDF = () => {
    const printWindow = window.open('', '_blank');
    if (printWindow) {
      printWindow.document.write(generateHTML(blocks));
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => printWindow.print(), 500);
      setMessage('PDF export opened in print dialog');
      setTimeout(() => setMessage(''), 3000);
    }
  };

  return (
    <div className="report-editor">
      <div className="report-toolbar">
        <button className="toolbar-btn run-btn" onClick={handleExportHTML}>Export HTML</button>
        <button className="toolbar-btn" onClick={handleExportPDF}>Export PDF</button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn" onClick={() => setBlocks([])}>Clear</button>
        {message && <span className="report-message">{message}</span>}
      </div>
      <div className="report-body">
        <BlockPalette onAdd={addBlock} />
        <ReportPreview blocks={blocks} onUpdate={updateBlock} onRemove={removeBlock} onMove={moveBlock} />
      </div>
    </div>
  );
}
