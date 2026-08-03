import type { TransformStep } from './DataStudio';

interface TransformEditorProps {
  transforms: TransformStep[];
  onAdd: (type: string) => void;
  onToggle: (id: string) => void;
  onRemove: (id: string) => void;
  onUpdateConfig: (id: string, config: Record<string, any>) => void;
  columnNames: string[];
}

const TRANSFORM_TYPES = [
  { id: 'filter', label: 'Filter Rows' },
  { id: 'sort', label: 'Sort' },
  { id: 'select', label: 'Select Columns' },
  { id: 'rename', label: 'Rename Column' },
  { id: 'dropna', label: 'Drop Nulls' },
  { id: 'fillna', label: 'Fill Nulls' },
  { id: 'deduplicate', label: 'Remove Duplicates' },
  { id: 'cast', label: 'Change Type' },
  { id: 'aggregate', label: 'Aggregate' },
  { id: 'derive', label: 'Add Computed Column' },
];

function TransformConfig({ step, onUpdate, columnNames }: { step: TransformStep; onUpdate: (c: Record<string, any>) => void; columnNames: string[] }) {
  const c = step.config;

  switch (step.type) {
    case 'filter':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">Column</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <select value={c.op ?? 'contains'} onChange={(e) => onUpdate({ ...c, op: e.target.value })} className="transform-input">
            <option value="contains">contains</option>
            <option value="equals">equals</option>
            <option value="gt">greater than</option>
            <option value="lt">less than</option>
            <option value="gte">≥</option>
            <option value="lte">≤</option>
          </select>
          <input className="transform-input" placeholder="Value" value={c.value ?? ''} onChange={(e) => onUpdate({ ...c, value: e.target.value })} />
        </div>
      );
    case 'sort':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">Column</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <select value={c.direction ?? 'asc'} onChange={(e) => onUpdate({ ...c, direction: e.target.value })} className="transform-input">
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>
      );
    case 'select':
      return (
        <div className="transform-config-row">
          <input className="transform-input" placeholder="Comma-separated columns" value={(c.columns ?? []).join(', ')} onChange={(e) => onUpdate({ ...c, columns: e.target.value.split(',').map((s: string) => s.trim()).filter(Boolean) })} />
        </div>
      );
    case 'rename':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">Column</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <input className="transform-input" placeholder="New name" value={c.newName ?? ''} onChange={(e) => onUpdate({ ...c, newName: e.target.value })} />
        </div>
      );
    case 'dropna':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">All columns</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
        </div>
      );
    case 'fillna':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">All columns</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <input className="transform-input" placeholder="Fill value" value={c.value ?? ''} onChange={(e) => onUpdate({ ...c, value: e.target.value })} />
        </div>
      );
    case 'deduplicate':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">All columns</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
        </div>
      );
    case 'cast':
      return (
        <div className="transform-config-row">
          <select value={c.column ?? ''} onChange={(e) => onUpdate({ ...c, column: e.target.value })} className="transform-input">
            <option value="">Column</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <select value={c.dtype ?? 'number'} onChange={(e) => onUpdate({ ...c, dtype: e.target.value })} className="transform-input">
            <option value="number">Number</option>
            <option value="string">String</option>
          </select>
        </div>
      );
    case 'aggregate':
      return (
        <div className="transform-config-row">
          <select value={c.groupBy ?? ''} onChange={(e) => onUpdate({ ...c, groupBy: e.target.value })} className="transform-input">
            <option value="">Group by</option>
            {columnNames.map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <select value={c.fn ?? 'count'} onChange={(e) => onUpdate({ ...c, fn: e.target.value })} className="transform-input">
            <option value="count">Count</option>
            <option value="sum">Sum</option>
            <option value="mean">Mean</option>
            <option value="min">Min</option>
            <option value="max">Max</option>
          </select>
        </div>
      );
    case 'derive':
      return (
        <div className="transform-config-row">
          <input className="transform-input" placeholder="New column name" value={c.newColumn ?? ''} onChange={(e) => onUpdate({ ...c, newColumn: e.target.value })} />
          <input className="transform-input" placeholder="Expression (e.g. col1 + col2)" value={c.expression ?? ''} onChange={(e) => onUpdate({ ...c, expression: e.target.value })} />
        </div>
      );
    default:
      return null;
  }
}

export default function TransformEditor({ transforms, onAdd, onToggle, onRemove, onUpdateConfig, columnNames }: TransformEditorProps) {
  return (
    <div className="transform-editor">
      <div className="transform-toolbar">
        <select
          className="transform-select"
          value=""
          onChange={(e) => { if (e.target.value) onAdd(e.target.value); }}
        >
          <option value="" disabled>Add transform step...</option>
          {TRANSFORM_TYPES.map((t) => (
            <option key={t.id} value={t.id}>{t.label}</option>
          ))}
        </select>
      </div>
      <div className="transform-pipeline">
        {transforms.length === 0 && (
          <div className="transform-empty">
            No transform steps. Add one to start building a pipeline.
          </div>
        )}
        {transforms.map((step, i) => (
          <div key={step.id} className={`transform-step ${!step.enabled ? 'disabled' : ''}`}>
            <div className="transform-step-header">
              <span className="transform-step-num">{i + 1}</span>
              <span className="transform-step-type">{TRANSFORM_TYPES.find((t) => t.id === step.type)?.label ?? step.type}</span>
              <div className="transform-step-actions">
                <button className="transform-btn" onClick={() => onToggle(step.id)}>
                  {step.enabled ? '#' : '·'}
                </button>
                <button className="transform-btn danger" onClick={() => onRemove(step.id)}>×</button>
              </div>
            </div>
            <div className="transform-step-config">
              <TransformConfig step={step} onUpdate={(c) => onUpdateConfig(step.id, c)} columnNames={columnNames} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
