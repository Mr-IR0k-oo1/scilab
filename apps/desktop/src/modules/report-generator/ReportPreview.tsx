import type { ReportBlock } from './ReportEditor';

interface ReportPreviewProps {
  blocks: ReportBlock[];
  onUpdate: (id: string, props: Record<string, any>) => void;
  onRemove: (id: string) => void;
  onMove: (id: string, dir: 'up' | 'down') => void;
}

export default function ReportPreview({ blocks, onUpdate, onRemove, onMove }: ReportPreviewProps) {
  return (
    <div className="report-canvas">
      <div className="report-page">
        {blocks.map((block, i) => (
          <div key={block.id} className="report-block">
            <div className="report-block-controls">
              <button className="block-btn" onClick={() => onMove(block.id, 'up')} disabled={i === 0}>↑</button>
              <button className="block-btn" onClick={() => onMove(block.id, 'down')} disabled={i === blocks.length - 1}>↓</button>
              <button className="block-btn danger" onClick={() => onRemove(block.id)}>×</button>
            </div>
            <div className="report-block-content">
              {block.type === 'heading' && (
                <input
                  className={`report-heading level-${block.props.level ?? 1}`}
                  value={block.props.text ?? ''}
                  onChange={(e) => onUpdate(block.id, { ...block.props, text: e.target.value })}
                  style={{ fontSize: `${24 - (block.props.level ?? 1) * 2}px` }}
                />
              )}
              {block.type === 'paragraph' && (
                <textarea
                  className="report-paragraph"
                  value={block.props.text ?? ''}
                  onChange={(e) => onUpdate(block.id, { ...block.props, text: e.target.value })}
                />
              )}
              {block.type === 'divider' && <hr className="report-divider" />}
              {block.type === 'page-break' && <div className="report-page-break">.. Page Break</div>}
              {block.type === 'chart' && (
                <div className="report-chart-placeholder" style={{ height: block.props.height ?? 300 }}>
                  [ Chart: {block.props.chartType ?? 'line'} ]
                </div>
              )}
              {block.type === 'table' && (
                <table className="report-table">
                  <thead>
                    <tr>{(block.props.headers ?? []).map((h: string, i: number) => <th key={i}>{h}</th>)}</tr>
                  </thead>
                  <tbody>
                    {(block.props.rows ?? []).map((row: string[], ri: number) => (
                      <tr key={ri}>{row.map((cell: string, ci: number) => <td key={ci}>{cell}</td>)}</tr>
                    ))}
                  </tbody>
                </table>
              )}
              {block.type === 'image' && (
                <div className="report-image-placeholder">
                  {block.props.src ? <img src={block.props.src} alt={block.props.alt} /> : '[ Image ]'}
                </div>
              )}
              {block.type === 'code' && (
                <pre className="report-code">
                  <code>{block.props.code ?? ''}</code>
                </pre>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
