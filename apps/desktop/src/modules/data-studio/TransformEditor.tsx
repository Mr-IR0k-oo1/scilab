import type { TransformStep } from './DataStudio';

interface TransformEditorProps {
  transforms: TransformStep[];
  onAdd: (type: string) => void;
  onToggle: (id: string) => void;
  onRemove: (id: string) => void;
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

export default function TransformEditor({ transforms, onAdd, onToggle, onRemove }: TransformEditorProps) {
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
              <input className="transform-input" placeholder="Configure parameters..." />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
