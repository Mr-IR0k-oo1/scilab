import { useState, useRef, useCallback } from 'react';
import type { Widget, WidgetType } from '@scilab-studio/widgets';
import { WIDGET_DEFINITIONS } from '@scilab-studio/widgets';
import Inspector from './Inspector';
import Palette from './Palette';
import CodePanel from './CodePanel';

let widgetCounter = 0;

export default function GuiBuilder() {
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [dragging, setDragging] = useState<{ id: string; offsetX: number; offsetY: number } | null>(null);
  const [resizing, setResizing] = useState<{ id: string; handle: string; startX: number; startY: number; origW: number; origH: number; origX: number; origY: number } | null>(null);
  const [showCode, setShowCode] = useState(false);
  const [snapToGrid, setSnapToGrid] = useState(true);
  const gridSize = 10;
  const canvasRef = useRef<HTMLDivElement>(null);

  const selectedWidget = widgets.find((w) => w.id === selectedId) ?? null;

  const snap = (v: number) => snapToGrid ? Math.round(v / gridSize) * gridSize : v;

  const addWidget = useCallback((type: WidgetType) => {
    const def = WIDGET_DEFINITIONS.find((d) => d.type === type)!;
    const newWidget: Widget = {
      id: `widget-${++widgetCounter}`,
      type,
      x: snap(20 + (widgetCounter % 5) * 30),
      y: snap(20 + (widgetCounter % 5) * 30),
      width: def.defaultWidth,
      height: def.defaultHeight,
      props: { label: def.label },
    };
    setWidgets((prev) => [...prev, newWidget]);
    setSelectedId(newWidget.id);
  }, [snapToGrid]);

  const updateWidget = useCallback((id: string, updates: Partial<Widget>) => {
    setWidgets((prev) => prev.map((w) => w.id === id ? { ...w, ...updates } : w));
  }, []);

  const deleteWidget = useCallback((id: string) => {
    setWidgets((prev) => prev.filter((w) => w.id !== id));
    setSelectedId((prev) => prev === id ? null : prev);
  }, []);

  const handleCanvasMouseDown = (e: React.MouseEvent) => {
    if (e.target === canvasRef.current) setSelectedId(null);
  };

  const handleWidgetMouseDown = (e: React.MouseEvent, widget: Widget) => {
    e.stopPropagation();
    setSelectedId(widget.id);
    const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
    setDragging({
      id: widget.id,
      offsetX: e.clientX - rect.left,
      offsetY: e.clientY - rect.top,
    });
  };

  const handleResizeMouseDown = (e: React.MouseEvent, widget: Widget, handle: string) => {
    e.stopPropagation();
    setSelectedId(widget.id);
    setResizing({
      id: widget.id, handle,
      startX: e.clientX, startY: e.clientY,
      origW: widget.width, origH: widget.height,
      origX: widget.x, origY: widget.y,
    });
  };

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (dragging) {
      const cr = canvasRef.current?.getBoundingClientRect();
      if (!cr) return;
      const x = snap(Math.max(0, e.clientX - cr.left - dragging.offsetX));
      const y = snap(Math.max(0, e.clientY - cr.top - dragging.offsetY));
      updateWidget(dragging.id, { x, y });
    }
    if (resizing) {
      const dx = e.clientX - resizing.startX;
      const dy = e.clientY - resizing.startY;
      let w = resizing.origW, h = resizing.origH, x = resizing.origX, y = resizing.origY;
      if (resizing.handle.includes('e')) w = Math.max(40, resizing.origW + dx);
      if (resizing.handle.includes('s')) h = Math.max(20, resizing.origH + dy);
      if (resizing.handle.includes('w')) { w = Math.max(40, resizing.origW - dx); x = resizing.origX + (resizing.origW - w); }
      if (resizing.handle.includes('n')) { h = Math.max(20, resizing.origH - dy); y = resizing.origY + (resizing.origH - h); }
      updateWidget(resizing.id, { width: Math.round(w), height: Math.round(h), x: Math.round(x), y: Math.round(y) });
    }
  }, [dragging, resizing, updateWidget, snapToGrid]);

  const handleMouseUp = useCallback(() => { setDragging(null); setResizing(null); }, []);

  const generateCode = () => {
    let code = `function main_gui()\n`;
    code += `    fig = figure("position", [100, 100, 800, 600], "figure_name", "Main GUI");\n\n`;
    for (const w of widgets) {
      const style = widgetTypeToStyle(w.type);
      code += `    uicontrol(fig, "style", "${style}", "string", "${w.props.label ?? ''}", "position", [${w.x}, ${w.y}, ${w.width}, ${w.height}]);\n`;
    }
    code += `\nendfunction\n`;
    return code;
  };

  return (
    <div className="gui-builder">
      <div className="gui-toolbar">
        <button className="toolbar-btn" onClick={() => setShowCode(!showCode)}>
          {showCode ? 'Canvas' : 'Code'}
        </button>
        <button className={`toolbar-btn ${snapToGrid ? 'active' : ''}`} onClick={() => setSnapToGrid(!snapToGrid)}>
          Snap {gridSize}px
        </button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn" onClick={() => setWidgets([])}>Clear</button>
      </div>
      <div className="gui-body">
        <Palette onAdd={addWidget} />
        {showCode ? (
          <CodePanel code={generateCode()} />
        ) : (
          <div
            className="gui-canvas-container"
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            <div ref={canvasRef} className="gui-canvas" onMouseDown={handleCanvasMouseDown}>
              {widgets.map((widget) => {
                const isSelected = widget.id === selectedId;
                return (
                  <div
                    key={widget.id}
                    className={`gui-widget ${isSelected ? 'selected' : ''}`}
                    style={{
                      left: widget.x,
                      top: widget.y,
                      width: widget.width,
                      height: widget.height,
                      backgroundColor: widget.props.backgroundColor,
                      color: widget.props.textColor,
                      border: widget.props.border,
                      fontSize: widget.props.fontSize ? `${widget.props.fontSize}px` : undefined,
                    }}
                    onMouseDown={(e) => handleWidgetMouseDown(e, widget)}
                  >
                    <div className="gui-widget-content">
                      {widget.type === 'button' && <button className="gui-button">{widget.props.label ?? 'Button'}</button>}
                      {widget.type === 'label' && <span className="gui-label">{widget.props.label ?? 'Label'}</span>}
                      {widget.type === 'text-field' && <input className="gui-input" placeholder={widget.props.label ?? 'Text'} readOnly />}
                      {widget.type === 'slider' && <input type="range" className="gui-slider" readOnly />}
                      {widget.type === 'checkbox' && (
                        <label className="gui-checkbox"><input type="checkbox" readOnly /> {widget.props.label ?? 'Check'}</label>
                      )}
                      {widget.type === 'dropdown' && (
                        <select className="gui-select" disabled>
                          <option>{widget.props.label ?? 'Option 1'}</option>
                          <option>Option 2</option>
                        </select>
                      )}
                      {widget.type === 'image' && (
                        <div className="gui-image-placeholder">
                          <span>🖼 {widget.props.label ?? 'Image Preview'}</span>
                        </div>
                      )}
                      {widget.type === 'table' && (
                        <table className="gui-table-placeholder">
                          <thead>
                            <tr><th>Col 1</th><th>Col 2</th></tr>
                          </thead>
                          <tbody>
                            <tr><td>Val A</td><td>Val B</td></tr>
                            <tr><td>Val C</td><td>Val D</td></tr>
                          </tbody>
                        </table>
                      )}
                      {widget.type === 'plot' && <div className="gui-plot">[ Plot Area ]</div>}
                      {widget.type === 'panel' && <div className="gui-panel">{widget.props.label ?? 'Panel'}</div>}
                    </div>
                    {isSelected && ['n','s','e','w','ne','nw','se','sw'].map((h) => (
                      <div key={h} className={`resize-handle ${h}`} onMouseDown={(e) => handleResizeMouseDown(e, widget, h)} />
                    ))}
                  </div>
                );
              })}
            </div>
          </div>
        )}
        <Inspector widget={selectedWidget} onUpdate={(u) => selectedId && updateWidget(selectedId, u)} onDelete={() => selectedId && deleteWidget(selectedId)} />
      </div>
    </div>
  );
}

function widgetTypeToStyle(type: WidgetType): string {
  const map: Record<string, string> = {
    button: 'pushbutton', label: 'text', 'text-field': 'edit',
    slider: 'slider', checkbox: 'checkbox', dropdown: 'popupmenu',
    image: 'image', table: 'table', plot: 'axes', panel: 'frame',
  };
  return map[type] ?? 'pushbutton';
}
