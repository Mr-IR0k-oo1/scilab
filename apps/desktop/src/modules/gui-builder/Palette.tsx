import type { WidgetType } from '@scilab-studio/widgets';
import { WIDGET_DEFINITIONS } from '@scilab-studio/widgets';

interface PaletteProps {
  onAdd: (type: WidgetType) => void;
}

export default function Palette({ onAdd }: PaletteProps) {
  return (
    <div className="gui-palette">
      <h3>Widgets</h3>
      {WIDGET_DEFINITIONS.map((def) => (
        <button key={def.type} className="palette-item" onClick={() => onAdd(def.type)}>
          <span className="palette-icon">{def.icon}</span>
          {def.label}
        </button>
      ))}
    </div>
  );
}
