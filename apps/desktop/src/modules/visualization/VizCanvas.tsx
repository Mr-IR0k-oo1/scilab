import { useRef, useMemo } from 'react';

interface VizCanvasProps {
  config: {
    type: string;
    title: string;
    data: any[];
    xKey: string;
    yKey: string;
    theme: 'dark' | 'light';
  };
}

export default function VizCanvas({ config }: VizCanvasProps) {
  const svgRef = useRef<SVGSVGElement>(null);
  const width = 700;
  const height = 400;
  const pad = { top: 40, right: 20, bottom: 50, left: 60 };
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const isDark = config.theme === 'dark';
  const axisColor = isDark ? '#333' : '#ddd';
  const textColor = isDark ? '#888' : '#999';

  const { chartContent } = useMemo(() => {
    const data = config.data;
    const xs = data.map((d) => Number(d[config.xKey]));
    const ys = data.map((d) => Number(d[config.yKey]));
    const xMin = Math.min(...xs); const xMax = Math.max(...xs);
    const yMin = Math.min(...ys); const yMax = Math.max(...ys);
    const xR = xMax - xMin || 1; const yR = yMax - yMin || 1;

    const xS = (v: number) => pad.left + ((v - xMin) / xR) * innerW;
    const yS = (v: number) => pad.top + innerH - ((v - yMin) / yR) * innerH;
    const pts = data.map((d) => ({ x: xS(Number(d[config.xKey])), y: yS(Number(d[config.yKey])) }));

    let content: React.ReactNode = null;

    switch (config.type) {
      case 'line': {
        const d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ');
        content = <path d={d} fill="none" stroke="#4fc3f7" strokeWidth={2} />;
        break;
      }
      case 'scatter':
        content = pts.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={5} fill="#4fc3f7" opacity={0.8} />);
        break;
      case 'bar': {
        const bw = Math.max(4, innerW / data.length - 4);
        content = pts.map((p, i) => (
          <rect key={i} x={p.x - bw / 2} y={p.y} width={bw} height={pad.top + innerH - p.y} fill="#4fc3f7" opacity={0.8} rx={2} />
        ));
        break;
      }
      case 'histogram': {
        const bins = 10;
        const binW = innerW / bins;
        const values = data.map((d) => Number(d[config.yKey]));
        const min = Math.min(...values); const max = Math.max(...values);
        const range = max - min || 1;
        const hist = Array(bins).fill(0);
        values.forEach((v) => { hist[Math.min(bins - 1, Math.floor(((v - min) / range) * bins))]++; });
        const hMax = Math.max(...hist) || 1;
        content = hist.map((count, i) => (
          <rect key={i} x={pad.left + i * binW} y={pad.top + innerH - (count / hMax) * innerH} width={binW - 2} height={(count / hMax) * innerH} fill="#4fc3f7" opacity={0.8} rx={1} />
        ));
        break;
      }
      case 'heatmap': {
        const grid = 8;
        const cellW = innerW / grid, cellH = innerH / grid;
        const cells: React.ReactNode[] = [];
        for (let r = 0; r < grid; r++)
          for (let c = 0; c < grid; c++) {
            const val = Math.sin(r * 0.5) * Math.cos(c * 0.5) * 0.5 + 0.5;
            cells.push(<rect key={`${r}-${c}`} x={pad.left + c * cellW} y={pad.top + r * cellH} width={cellW} height={cellH} fill={`hsl(${200 - val * 200}, 70%, ${50 + val * 30}%)`} stroke={axisColor} strokeWidth={0.5} />);
          }
        content = cells;
        break;
      }
      case 'surface': {
        const g = 20;
        const pts3d: React.ReactNode[] = [];
        for (let i = 0; i < g; i++)
          for (let j = 0; j < g; j++) {
            const x = (i / g) * 2 - 1, y = (j / g) * 2 - 1;
            const z = Math.sin(Math.sqrt(x * x + y * y) * 3) * 0.5 + 0.5;
            pts3d.push(<circle key={`${i}-${j}`} cx={pad.left + (i / g) * innerW + (j / g) * 20} cy={pad.top + innerH / 2 - z * innerH * 0.4 + (j / g) * 15} r={2} fill={`hsl(${200 - z * 200}, 80%, ${40 + z * 40}%)`} />);
          }
        content = pts3d;
        break;
      }
      case 'sankey': {
        const ns = [
          { x: pad.left, y: pad.top + 50, w: 20, h: 80, label: 'Input' },
          { x: pad.left + innerW * 0.33, y: pad.top + 30, w: 20, h: 60, label: 'Process' },
          { x: pad.left + innerW * 0.33, y: pad.top + 130, w: 20, h: 60, label: 'Filter' },
          { x: pad.left + innerW * 0.66, y: pad.top + 20, w: 20, h: 70, label: 'Out 1' },
          { x: pad.left + innerW * 0.66, y: pad.top + 140, w: 20, h: 50, label: 'Out 2' },
          { x: pad.left + innerW, y: pad.top + 60, w: 20, h: 90, label: 'Result' },
        ];
        content = (
          <>
            {[[0,1],[0,2],[1,3],[1,4],[2,4],[3,5],[4,5]].map(([s, t], i) => (
              <path key={i} d={`M${ns[s].x + ns[s].w},${ns[s].y + ns[s].h / 2} C${(ns[s].x + ns[t].x) / 2},${ns[s].y + ns[s].h / 2} ${(ns[s].x + ns[t].x) / 2},${ns[t].y + ns[t].h / 2} ${ns[t].x},${ns[t].y + ns[t].h / 2}`} fill="none" stroke="#4fc3f7" strokeWidth={8} opacity={0.4} />
            ))}
            {ns.map((n, i) => (
              <g key={i}>
                <rect x={n.x} y={n.y} width={n.w} height={n.h} fill="#1a237e" stroke="#4fc3f7" rx={2} />
                <text x={n.x + n.w + 4} y={n.y + n.h / 2 + 4} fill={textColor} fontSize={10}>{n.label}</text>
              </g>
            ))}
          </>
        );
        break;
      }
      case 'network': {
        const nd = [
          { x: pad.left + innerW * 0.5, y: pad.top + innerH * 0.2 },
          { x: pad.left + innerW * 0.2, y: pad.top + innerH * 0.5 },
          { x: pad.left + innerW * 0.8, y: pad.top + innerH * 0.5 },
          { x: pad.left + innerW * 0.35, y: pad.top + innerH * 0.8 },
          { x: pad.left + innerW * 0.65, y: pad.top + innerH * 0.8 },
        ];
        content = (
          <>
            {[[0,1],[0,2],[1,3],[2,4],[3,4],[1,2]].map(([s, t], i) => (
              <line key={i} x1={nd[s].x} y1={nd[s].y} x2={nd[t].x} y2={nd[t].y} stroke="#4fc3f7" strokeWidth={1} opacity={0.5} />
            ))}
            {nd.map((n, i) => <circle key={i} cx={n.x} cy={n.y} r={12} fill="#1a237e" stroke="#4fc3f7" strokeWidth={2} />)}
          </>
        );
        break;
      }
      case 'radar': {
        const cats = ['Speed', 'Power', 'Accuracy', 'Range', 'Cost'];
        const vals = [85, 70, 90, 60, 75];
        const cx = pad.left + innerW / 2, cy = pad.top + innerH / 2;
        const r = Math.min(innerW, innerH) / 2 - 20;
        const aStep = (2 * Math.PI) / cats.length;
        const pts2 = cats.map((_, i) => ({ x: cx + r * Math.cos(-Math.PI / 2 + i * aStep), y: cy + r * Math.sin(-Math.PI / 2 + i * aStep) }));
        const dataPts = cats.map((_, i) => ({ x: cx + (vals[i] / 100) * r * Math.cos(-Math.PI / 2 + i * aStep), y: cy + (vals[i] / 100) * r * Math.sin(-Math.PI / 2 + i * aStep) }));
        content = (
          <>
            {pts2.map((p, i) => <line key={i} x1={cx} y1={cy} x2={p.x} y2={p.y} stroke={axisColor} strokeWidth={1} />)}
            {[0.25, 0.5, 0.75, 1].map((lv) => (
              <polygon key={lv} points={pts2.map((p) => `${cx + (p.x - cx) * lv},${cy + (p.y - cy) * lv}`).join(' ')} fill="none" stroke={axisColor} strokeWidth={0.5} />
            ))}
            <polygon points={dataPts.map((p) => `${p.x},${p.y}`).join(' ')} fill="#4fc3f7" fillOpacity={0.3} stroke="#4fc3f7" strokeWidth={2} />
            {dataPts.map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={4} fill="#4fc3f7" />)}
            {pts2.map((p, i) => <text key={i} x={p.x} y={p.y + (p.y < cy ? -10 : 14)} textAnchor="middle" fill={textColor} fontSize={10}>{cats[i]}</text>)}
          </>
        );
        break;
      }
      case 'gauge': {
        const cx = pad.left + innerW / 2, cy = pad.top + innerH - 30;
        const rG = Math.min(innerW, innerH) / 2 - 20;
        const value = 67;
        const angle = (-135 + (value / 100) * 270) * (Math.PI / 180);
        content = (
          <>
            <path d={`M ${cx - rG},${cy} A ${rG},${rG} 0 1,1 ${cx + rG},${cy}`} fill="none" stroke="#333" strokeWidth={20} />
            <path d={`M ${cx - rG},${cy} A ${rG},${rG} 0 0,1 ${cx + rG * Math.cos(angle)},${cy + rG * Math.sin(angle)}`} fill="none" stroke="#4fc3f7" strokeWidth={20} />
            <line x1={cx} y1={cy} x2={cx + (rG - 10) * Math.cos(angle)} y2={cy + (rG - 10) * Math.sin(angle)} stroke="#fff" strokeWidth={3} />
            <circle cx={cx} cy={cy} r={5} fill="#fff" />
            <text x={cx} y={cy + 5} textAnchor="middle" fill={textColor} fontSize={24} fontWeight="bold">{value}</text>
            <text x={cx} y={cy + 25} textAnchor="middle" fill={textColor} fontSize={12}>%</text>
          </>
        );
        break;
      }
      case 'waterfall': {
        const cats = ['Revenue', 'Cost', 'Tax', 'Profit'];
        const vals = [100, -40, -20, 40];
        let cum = 0;
        const bw2 = Math.min(40, innerW / cats.length - 8);
        content = cats.map((cat, i) => {
          const isTotal = i === cats.length - 1;
          const m = Math.max(...vals.map(Math.abs)) || 1;
          const startY = isTotal ? pad.top + innerH : pad.top + innerH - (cum / m) * innerH;
          const hVal = (Math.abs(vals[i]) / m) * innerH;
          const barY = vals[i] > 0 ? startY - hVal : startY;
          cum += vals[i];
          return (
            <g key={i}>
              <rect x={pad.left + i * (innerW / cats.length) + (innerW / cats.length - bw2) / 2} y={barY} width={bw2} height={hVal} fill={vals[i] > 0 ? '#4fc3f7' : '#ef5350'} opacity={0.8} rx={2} />
              <text x={pad.left + i * (innerW / cats.length) + (innerW / cats.length) / 2} y={pad.top + innerH + 16} textAnchor="middle" fill={textColor} fontSize={10}>{cat}</text>
            </g>
          );
        });
        break;
      }
    }

    return { chartContent: content };
  }, [config]);

  const bgColor = isDark ? '#1a1a2e' : '#fff';

  return (
    <div className="viz-canvas" style={{ background: bgColor, borderRadius: 6 }}>
      <svg ref={svgRef} width={width} height={height}>
        <rect width={width} height={height} fill={bgColor} />
        <text x={width / 2} y={24} textAnchor="middle" fill={isDark ? '#e0e0e0' : '#333'} fontSize={14} fontWeight="bold">
          {config.title}
        </text>
        {!['gauge', 'radar', 'sankey', 'network'].includes(config.type) && (
          <>
            <line x1={pad.left} y1={pad.top + innerH} x2={pad.left + innerW} y2={pad.top + innerH} stroke={axisColor} />
            <line x1={pad.left} y1={pad.top} x2={pad.left} y2={pad.top + innerH} stroke={axisColor} />
          </>
        )}
        {chartContent}
      </svg>
    </div>
  );
}
