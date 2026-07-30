import { useState } from 'react';
import type { Widget } from '@scilab-studio/widgets';

interface InspectorProps {
  widget: Widget | null;
  onUpdate: (updates: Partial<Widget>) => void;
  onDelete: () => void;
}

type InspectorTab = 'properties' | 'layout' | 'appearance' | 'events';

export default function Inspector({ widget, onUpdate, onDelete }: InspectorProps) {
  const [tab, setTab] = useState<InspectorTab>('properties');

  if (!widget) {
    return (
      <aside className="inspector">
        <div className="inspector-header">Properties</div>
        <div className="inspector-empty">No widget selected</div>
      </aside>
    );
  }

  return (
    <aside className="inspector">
      <div className="inspector-header">
        Properties
        <button className="inspector-delete" onClick={onDelete}>Delete</button>
      </div>
      <div className="inspector-tabs">
        {(['properties', 'layout', 'appearance', 'events'] as const).map((t) => (
          <button key={t} className={`inspector-tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>
      <div className="inspector-body">
        {tab === 'layout' && (
          <>
            <div className="inspector-group"><label>X</label><input type="number" value={widget.x} onChange={(e) => onUpdate({ x: Number(e.target.value) })} /></div>
            <div className="inspector-group"><label>Y</label><input type="number" value={widget.y} onChange={(e) => onUpdate({ y: Number(e.target.value) })} /></div>
            <div className="inspector-group"><label>Width</label><input type="number" value={widget.width} onChange={(e) => onUpdate({ width: Number(e.target.value) })} /></div>
            <div className="inspector-group"><label>Height</label><input type="number" value={widget.height} onChange={(e) => onUpdate({ height: Number(e.target.value) })} /></div>
          </>
        )}
        {tab === 'properties' && (
          <>
            <div className="inspector-group"><label>Type</label><span className="inspector-value">{widget.type}</span></div>
            <div className="inspector-group"><label>Label</label><input type="text" value={widget.props.label ?? ''} onChange={(e) => onUpdate({ props: { ...widget.props, label: e.target.value } })} /></div>
          </>
        )}
        {tab === 'appearance' && (
          <>
            <div className="inspector-group"><label>Bg Color</label><input type="text" value={widget.props.backgroundColor ?? '#f0f0f0'} onChange={(e) => onUpdate({ props: { ...widget.props, backgroundColor: e.target.value } })} placeholder="#f0f0f0" /></div>
            <div className="inspector-group"><label>Text Color</label><input type="text" value={widget.props.textColor ?? '#333333'} onChange={(e) => onUpdate({ props: { ...widget.props, textColor: e.target.value } })} placeholder="#333333" /></div>
            <div className="inspector-group"><label>Font Size</label><input type="number" value={widget.props.fontSize ?? 13} onChange={(e) => onUpdate({ props: { ...widget.props, fontSize: String(e.target.value) } })} min={8} max={48} /></div>
            <div className="inspector-group"><label>Border</label><input type="text" value={widget.props.border ?? '1px solid #ccc'} onChange={(e) => onUpdate({ props: { ...widget.props, border: e.target.value } })} placeholder="1px solid #ccc" /></div>
          </>
        )}
        {tab === 'events' && (
          <>
            <div className="inspector-group"><label>onClick</label><input type="text" value={widget.props.onClick ?? ''} onChange={(e) => onUpdate({ props: { ...widget.props, onClick: e.target.value } })} placeholder="callback_function" /></div>
            <div className="inspector-group"><label>onChange</label><input type="text" value={widget.props.onChange ?? ''} onChange={(e) => onUpdate({ props: { ...widget.props, onChange: e.target.value } })} placeholder="callback_function" /></div>
            <div className="inspector-group"><label>onFocus</label><input type="text" value={widget.props.onFocus ?? ''} onChange={(e) => onUpdate({ props: { ...widget.props, onFocus: e.target.value } })} placeholder="callback_function" /></div>
          </>
        )}
      </div>
    </aside>
  );
}
