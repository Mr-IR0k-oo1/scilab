import { useState, useRef, useCallback } from 'react';
import DataPreview from './DataPreview';
import TransformEditor from './TransformEditor';
import StatsPanel from './StatsPanel';
import ImportDialog from './ImportDialog';

export interface Dataset {
  id: string;
  name: string;
  source: string;
  columns: { name: string; type: string; nullable: boolean }[];
  rows: (string | number | null)[][];
}

export interface TransformStep {
  id: string;
  type: string;
  config: Record<string, any>;
  enabled: boolean;
}

let dsCounter = 0;

export default function DataStudio() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [activeDatasetId, setActiveDatasetId] = useState<string | null>(null);
  const [showImport, setShowImport] = useState(false);
  const [transforms, setTransforms] = useState<TransformStep[]>([]);
  const [activeTab, setActiveTab] = useState<'preview' | 'transforms' | 'stats'>('preview');

  const activeDataset = datasets.find((d) => d.id === activeDatasetId) ?? null;

  const handleImport = useCallback((data: (string | number | null)[][], name: string) => {
    const id = `ds-${++dsCounter}`;
    const columns = (data[0] ?? []).map((_, i) => ({
      name: `Column ${i + 1}`,
      type: 'string' as const,
      nullable: false,
    }));
    const ds: Dataset = {
      id, name, source: 'import',
      columns,
      rows: data.slice(0, 1000),
    };
    setDatasets((prev) => [...prev, ds]);
    setActiveDatasetId(id);
    setShowImport(false);
  }, []);

  const addTransform = (type: string) => {
    const step: TransformStep = {
      id: `step-${Date.now()}`,
      type,
      config: {},
      enabled: true,
    };
    setTransforms((prev) => [...prev, step]);
  };

  const toggleStep = (id: string) => {
    setTransforms((prev) => prev.map((s) => s.id === id ? { ...s, enabled: !s.enabled } : s));
  };

  const removeStep = (id: string) => {
    setTransforms((prev) => prev.filter((s) => s.id !== id));
  };

  return (
    <div className="data-studio">
      <div className="data-toolbar">
        <button className="toolbar-btn" onClick={() => setShowImport(true)}>
          + Import Data
        </button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn" disabled={!activeDataset} onClick={() => {
          if (!activeDataset) return;
          const csv = [activeDataset.columns.map((c) => c.name).join(','), ...activeDataset.rows.map((r) => r.join(','))].join('\n');
          const blob = new Blob([csv], { type: 'text/csv' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href = url; a.download = `${activeDataset.name}.csv`; a.click();
          URL.revokeObjectURL(url);
        }}>Export CSV</button>
        <button className="toolbar-btn" disabled={!activeDataset} onClick={() => {
          if (!activeDataset) return;
          const csv = [activeDataset.columns.map((c) => c.name).join(','), ...activeDataset.rows.map((r) => r.join(','))].join('\n');
          const blob = new Blob([csv], { type: 'text/csv' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href = url; a.download = `${activeDataset.name}.csv`; a.click();
          URL.revokeObjectURL(url);
        }}>Export Excel</button>
      </div>
      <div className="data-body">
        <div className="data-sidebar">
          <h3>Datasets</h3>
          {datasets.length === 0 && <div className="tree-empty">No datasets imported</div>}
          {datasets.map((ds) => (
            <div
              key={ds.id}
              className={`data-dataset-item ${activeDatasetId === ds.id ? 'active' : ''}`}
              onClick={() => setActiveDatasetId(ds.id)}
            >
              <span className="data-ds-icon">▤</span>
              <span className="data-ds-name">{ds.name}</span>
              <span className="data-ds-info">{ds.rows.length} rows</span>
            </div>
          ))}
        </div>
        <div className="data-main">
          {activeDataset ? (
            <>
              <div className="data-tabs">
                {(['preview', 'transforms', 'stats'] as const).map((tab) => (
                  <button key={tab} className={`data-tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </div>
              <div className="data-content">
                {activeTab === 'preview' && <DataPreview dataset={activeDataset} />}
                {activeTab === 'transforms' && (
                  <TransformEditor
                    transforms={transforms}
                    onAdd={addTransform}
                    onToggle={toggleStep}
                    onRemove={removeStep}
                  />
                )}
                {activeTab === 'stats' && <StatsPanel dataset={activeDataset} />}
              </div>
            </>
          ) : (
            <div className="data-empty">
              <h2>Data Studio</h2>
              <p>Import a CSV, Excel, or JSON file to get started</p>
              <button className="welcome-btn" onClick={() => setShowImport(true)}>Import Data</button>
            </div>
          )}
        </div>
      </div>
      {showImport && <ImportDialog onImport={handleImport} onClose={() => setShowImport(false)} />}
    </div>
  );
}
