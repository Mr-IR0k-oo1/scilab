import { useState } from 'react';

interface ChartConfig {
  type: string;
  title: string;
  data: any[];
  xKey: string;
  yKey: string;
  theme: 'dark' | 'light';
}

const CHART_TYPES = [
  { id: 'line', label: 'Line', icon: '◜' },
  { id: 'scatter', label: 'Scatter', icon: '○' },
  { id: 'bar', label: 'Bar', icon: '▯' },
  { id: 'surface', label: 'Surface', icon: '◘' },
  { id: 'heatmap', label: 'Heatmap', icon: '▤' },
  { id: 'sankey', label: 'Sankey', icon: '↗' },
  { id: 'network', label: 'Network', icon: '◉' },
  { id: 'radar', label: 'Radar', icon: '◎' },
  { id: 'gauge', label: 'Gauge', icon: '◠' },
  { id: 'histogram', label: 'Histogram', icon: '▨' },
  { id: 'waterfall', label: 'Waterfall', icon: '▬' },
];

import VizCanvas from './VizCanvas';
import VizToolbar from './VizToolbar';
import VizConfig from './VizConfig';

export default function VizStudio() {
  const [chartType, setChartType] = useState('line');
  const [config, setConfig] = useState<ChartConfig>({
    type: 'line', title: 'Chart Title',
    data: [
      { x: 1, y: 10 }, { x: 2, y: 25 }, { x: 3, y: 15 },
      { x: 4, y: 30 }, { x: 5, y: 20 }, { x: 6, y: 35 },
    ],
    xKey: 'x', yKey: 'y', theme: 'dark',
  });

  return (
    <div className="viz-studio">
      <VizToolbar chartType={chartType} onChartTypeChange={setChartType} chartTypes={CHART_TYPES} />
      <div className="viz-body">
        <div className="viz-canvas-area">
          <VizCanvas config={{ ...config, type: chartType }} />
        </div>
        <VizConfig config={config} onChange={setConfig} />
      </div>
    </div>
  );
}
