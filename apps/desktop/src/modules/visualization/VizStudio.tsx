import { useState, useMemo } from 'react';
import { getStore } from '@/store/store';
import type { Dataset } from '@/store/store';

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

const SAMPLE_DATA = [
  { x: 1, y: 10 }, { x: 2, y: 25 }, { x: 3, y: 15 },
  { x: 4, y: 30 }, { x: 5, y: 20 }, { x: 6, y: 35 },
];

import VizCanvas from './VizCanvas';
import VizToolbar from './VizToolbar';
import VizConfig from './VizConfig';

export default function VizStudio() {
  const datasets = getStore().datasets;
  const [chartType, setChartType] = useState('line');
  const [selectedDatasetId, setSelectedDatasetId] = useState<string>('');
  const [xCol, setXCol] = useState('x');
  const [yCol, setYCol] = useState('y');
  const [config, setConfig] = useState<ChartConfig>({
    type: 'line', title: 'Chart Title',
    data: SAMPLE_DATA,
    xKey: 'x', yKey: 'y', theme: 'dark',
  });

  const selectedDataset = datasets.find((d) => d.id === selectedDatasetId);

  const chartData = useMemo(() => {
    if (!selectedDataset) return SAMPLE_DATA;
    return selectedDataset.rows.map((row) => {
      const obj: Record<string, any> = {};
      selectedDataset.columns.forEach((col, i) => {
        obj[col.name] = row[i];
      });
      return obj;
    }).slice(0, 200);
  }, [selectedDataset]);

  const columnNames = selectedDataset?.columns.map((c) => c.name) ?? ['x', 'y'];

  const handleDatasetChange = (id: string) => {
    setSelectedDatasetId(id);
    const ds = datasets.find((d) => d.id === id);
    if (ds && ds.columns.length >= 2) {
      const numCol = ds.columns.find((c) => c.type === 'number')?.name ?? ds.columns[0].name;
      const numCols = ds.columns.filter((c) => c.type === 'number' || !isNaN(Number(ds.rows[0]?.[ds.columns.indexOf(c)])));
      const yColName = numCols.length > 1 ? numCols[1].name : numCols[0]?.name ?? ds.columns[1].name;
      setXCol(numCol);
      setYCol(yColName);
      setConfig((prev) => ({ ...prev, xKey: numCol, yKey: yColName }));
    }
  };

  const handleConfigChange = (newConfig: Partial<ChartConfig>) => {
    setConfig((prev) => ({ ...prev, ...newConfig }));
  };

  return (
    <div className="viz-studio">
      <VizToolbar chartType={chartType} onChartTypeChange={setChartType} chartTypes={CHART_TYPES} />
      <div className="viz-body">
        <div className="viz-canvas-area">
          {datasets.length > 0 && (
            <div className="viz-data-source">
              <label>Data Source</label>
              <select value={selectedDatasetId} onChange={(e) => handleDatasetChange(e.target.value)} className="toolbar-select">
                <option value="">Sample Data</option>
                {datasets.map((ds) => (
                  <option key={ds.id} value={ds.id}>{ds.name} ({ds.rows.length} rows)</option>
                ))}
              </select>
              {selectedDataset && (
                <>
                  <select value={xCol} onChange={(e) => { setXCol(e.target.value); setConfig((prev) => ({ ...prev, xKey: e.target.value })); }} className="toolbar-select">
                    {columnNames.map((n) => <option key={n} value={n}>X: {n}</option>)}
                  </select>
                  <select value={yCol} onChange={(e) => { setYCol(e.target.value); setConfig((prev) => ({ ...prev, yKey: e.target.value })); }} className="toolbar-select">
                    {columnNames.map((n) => <option key={n} value={n}>Y: {n}</option>)}
                  </select>
                </>
              )}
            </div>
          )}
          <VizCanvas config={{ ...config, type: chartType, data: chartData, xKey: xCol, yKey: yCol }} />
        </div>
        <VizConfig config={{ ...config, data: chartData, xKey: xCol, yKey: yCol }} onChange={handleConfigChange} />
      </div>
    </div>
  );
}
