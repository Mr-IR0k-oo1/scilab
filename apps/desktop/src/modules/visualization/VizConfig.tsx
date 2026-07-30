import { useRef } from 'react';

interface VizConfigProps {
  config: {
    type: string;
    title: string;
    data: any[];
    xKey: string;
    yKey: string;
    theme: 'dark' | 'light';
  };
  onChange: (config: any) => void;
}

export default function VizConfig({ config, onChange }: VizConfigProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);

  const setSvgRef = (el: SVGSVGElement | null) => {
    svgRef.current = el;
  };

  const exportSVG = () => {
    if (!svgRef.current) return;
    const svg = svgRef.current;
    const clone = svg.cloneNode(true) as SVGSVGElement;
    const xmlns = 'http://www.w3.org/2000/svg';
    if (!clone.getAttribute('xmlns')) clone.setAttribute('xmlns', xmlns);
    const serializer = new XMLSerializer();
    const str = serializer.serializeToString(clone);
    const blob = new Blob([str], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${config.title || 'chart'}.svg`; a.click();
    URL.revokeObjectURL(url);
  };

  const exportPNG = () => {
    if (!svgRef.current) return;
    const svg = svgRef.current;
    const clone = svg.cloneNode(true) as SVGSVGElement;
    const xmlns = 'http://www.w3.org/2000/svg';
    if (!clone.getAttribute('xmlns')) clone.setAttribute('xmlns', xmlns);
    const serializer = new XMLSerializer();
    const str = serializer.serializeToString(clone);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();
    const blob = new Blob([str], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    img.onload = () => {
      canvas.width = svg.clientWidth * 2;
      canvas.height = svg.clientHeight * 2;
      ctx!.scale(2, 2);
      ctx!.fillStyle = config.theme === 'dark' ? '#1a1a2e' : '#fff';
      ctx!.fillRect(0, 0, canvas.width, canvas.height);
      ctx!.drawImage(img, 0, 0);
      canvas.toBlob((b) => {
        if (b) {
          const pngUrl = URL.createObjectURL(b);
          const a = document.createElement('a');
          a.href = pngUrl; a.download = `${config.title || 'chart'}.png`; a.click();
          URL.revokeObjectURL(pngUrl);
        }
      });
      URL.revokeObjectURL(url);
    };
    img.src = url;
  };

  return (
    <aside className="viz-config">
      <div className="viz-config-section">
        <h3>General</h3>
        <div className="inspector-group">
          <label>Title</label>
          <input type="text" value={config.title} onChange={(e) => onChange({ ...config, title: e.target.value })} />
        </div>
        <div className="inspector-group">
          <label>Theme</label>
          <select value={config.theme} onChange={(e) => onChange({ ...config, theme: e.target.value })} className="inspector-select">
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </div>
      </div>
      <div className="viz-config-section">
        <h3>Axes</h3>
        <div className="inspector-group">
          <label>X Axis</label>
          <input type="text" value={config.xKey} onChange={(e) => onChange({ ...config, xKey: e.target.value })} />
        </div>
        <div className="inspector-group">
          <label>Y Axis</label>
          <input type="text" value={config.yKey} onChange={(e) => onChange({ ...config, yKey: e.target.value })} />
        </div>
      </div>
      <div className="viz-config-section">
        <h3>Export</h3>
        <div className="viz-config-actions">
          <button className="toolbar-btn" onClick={exportPNG}>Export PNG</button>
          <button className="toolbar-btn" onClick={exportSVG}>Export SVG</button>
        </div>
      </div>
      <div style={{ display: 'none' }}>
        <svg ref={setSvgRef} />
      </div>
    </aside>
  );
}
