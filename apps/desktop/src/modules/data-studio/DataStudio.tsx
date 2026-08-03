import { useState, useCallback, useMemo } from 'react';
import DataPreview from './DataPreview';
import TransformEditor from './TransformEditor';
import StatsPanel from './StatsPanel';
import ImportDialog from './ImportDialog';
import { getStore, setDatasets } from '@/store/store';
import type { Dataset } from '@/store/store';

export type { Dataset };
export interface TransformStep {
  id: string;
  type: string;
  config: Record<string, any>;
  enabled: boolean;
}

let dsCounter = 0;

function applyTransforms(rows: (string | number | null)[][], transforms: TransformStep[], columns: { name: string; type: string; nullable: boolean }[]): (string | number | null)[][] {
  let result = rows.map((r) => [...r]);
  const colNames = columns.map((c) => c.name);

  for (const step of transforms) {
    if (!step.enabled) continue;
    const c = step.config;

    switch (step.type) {
      case 'filter': {
        const ci = colNames.indexOf(c.column);
        if (ci === -1) break;
        const val = c.value;
        result = result.filter((r) => {
          const cell = r[ci];
          const num = Number(cell);
          const cellVal = isNaN(num) ? String(cell ?? '') : num;
          const filterVal = isNaN(Number(val)) ? val : Number(val);
          switch (c.op) {
            case 'equals': return cellVal === filterVal;
            case 'contains': return String(cellVal).toLowerCase().includes(String(filterVal).toLowerCase());
            case 'gt': return typeof cellVal === 'number' && typeof filterVal === 'number' && cellVal > filterVal;
            case 'lt': return typeof cellVal === 'number' && typeof filterVal === 'number' && cellVal < filterVal;
            case 'gte': return typeof cellVal === 'number' && typeof filterVal === 'number' && cellVal >= filterVal;
            case 'lte': return typeof cellVal === 'number' && typeof filterVal === 'number' && cellVal <= filterVal;
            default: return true;
          }
        });
        break;
      }
      case 'sort': {
        const ci = colNames.indexOf(c.column);
        if (ci === -1) break;
        const dir = c.direction === 'desc' ? -1 : 1;
        result.sort((a, b) => {
          const av = a[ci], bv = b[ci];
          if (av === bv) return 0;
          if (av === null) return 1;
          if (bv === null) return -1;
          return av < bv ? -dir : dir;
        });
        break;
      }
      case 'select': {
        const indices = (c.columns ?? []).map((n: string) => colNames.indexOf(n)).filter((i: number) => i !== -1);
        result = result.map((r) => indices.map((i: number) => r[i]));
        break;
      }
      case 'rename': {
        const ci = colNames.indexOf(c.column);
        if (ci !== -1 && c.newName) colNames[ci] = c.newName;
        break;
      }
      case 'dropna': {
        if (c.column) {
          const ci = colNames.indexOf(c.column);
          if (ci !== -1) result = result.filter((r) => r[ci] !== null && r[ci] !== '');
        } else {
          result = result.filter((r) => r.some((v) => v !== null && v !== ''));
        }
        break;
      }
      case 'fillna': {
        const fillVal = c.value ?? '';
        if (c.column) {
          const ci = colNames.indexOf(c.column);
          if (ci !== -1) result = result.map((r) => r[ci] === null || r[ci] === '' ? [...r.slice(0, ci), fillVal, ...r.slice(ci + 1)] : r);
        } else {
          result = result.map((r) => r.map((v) => v === null || v === '' ? fillVal : v));
        }
        break;
      }
      case 'deduplicate': {
        if (c.column) {
          const ci = colNames.indexOf(c.column);
          if (ci !== -1) {
            const seen = new Set<string>();
            result = result.filter((r) => { const k = String(r[ci]); if (seen.has(k)) return false; seen.add(k); return true; });
          }
        } else {
          const seen = new Set<string>();
          result = result.filter((r) => { const k = JSON.stringify(r); if (seen.has(k)) return false; seen.add(k); return true; });
        }
        break;
      }
      case 'cast': {
        const ci = colNames.indexOf(c.column);
        if (ci === -1) break;
        result = result.map((r) => {
          if (r[ci] === null) return r;
          const val = c.dtype === 'number' ? Number(r[ci]) : String(r[ci]);
          return [...r.slice(0, ci), isNaN(val as number) && c.dtype === 'number' ? r[ci] : val, ...r.slice(ci + 1)];
        });
        break;
      }
      case 'aggregate': {
        const gci = colNames.indexOf(c.groupBy);
        if (gci === -1) break;
        const groups = new Map<string, (string | number | null)[][]>();
        result.forEach((r) => { const k = String(r[gci]); if (!groups.has(k)) groups.set(k, []); groups.get(k)!.push(r); });
        result = Array.from(groups.entries()).map(([k, rows]) => {
          const vals = rows.map((r) => Number(r[gci])).filter((v) => !isNaN(v));
          switch (c.fn) {
            case 'sum': return [k, vals.reduce((a, b) => a + b, 0)];
            case 'mean': return [k, vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : 0];
            case 'min': return [k, vals.length ? Math.min(...vals) : 0];
            case 'max': return [k, vals.length ? Math.max(...vals) : 0];
            default: return [k, rows.length];
          }
        });
        break;
      }
      case 'derive': {
        if (!c.newColumn || !c.expression) break;
        result = result.map((r) => {
          try {
            const scope = Object.fromEntries(colNames.map((n, i) => [n, Number(r[i]) ?? 0]));
            const val = new Function(...Object.keys(scope), `return ${c.expression}`)(...Object.values(scope));
            return [...r, isNaN(val) ? null : val];
          } catch { return [...r, null]; }
        });
        break;
      }
    }
  }

  return result;
}

function toCSV(columns: { name: string }[], rows: (string | number | null)[][]): string {
  return [columns.map((c) => c.name).join(','), ...rows.map((r) => r.map((v) => {
    const s = String(v ?? '');
    return s.includes(',') || s.includes('"') || s.includes('\n') ? `"${s.replace(/"/g, '""')}"` : s;
  }).join(','))].join('\n');
}

function toXLSX(columns: { name: string }[], rows: (string | number | null)[][]): Blob {
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
 <Styles>
  <Style ss:ID="header"><Font ss:Bold="1"/></Style>
 </Styles>
 <Worksheet ss:Name="Data">
  <Table>
   <Row>${columns.map((c) => `<Cell ss:StyleID="header"><Data ss:Type="String">${c.name}</Data></Cell>`).join('')}</Row>
${rows.map((r) => `   <Row>${r.map((v) => `<Cell><Data ss:Type="${typeof v === 'number' ? 'Number' : 'String'}">${String(v ?? '')}</Data></Cell>`).join('')}</Row>`).join('\n')}
  </Table>
 </Worksheet>
</Workbook>`;
  return new Blob([xml], { type: 'application/vnd.ms-excel' });
}

export default function DataStudio() {
  const datasets = getStore().datasets;
  const [activeDatasetId, setActiveDatasetId] = useState<string | null>(null);
  const [showImport, setShowImport] = useState(false);
  const [transforms, setTransforms] = useState<TransformStep[]>([]);
  const [activeTab, setActiveTab] = useState<'preview' | 'transforms' | 'stats'>('preview');

  const activeDataset = datasets.find((d) => d.id === activeDatasetId) ?? null;

  const transformedRows = useMemo(() => {
    if (!activeDataset) return [];
    return applyTransforms(activeDataset.rows, transforms, activeDataset.columns);
  }, [activeDataset, transforms]);

  const transformedColumns = useMemo(() => {
    if (!activeDataset) return [];
    const cols = [...activeDataset.columns];
    for (const step of transforms) {
      if (!step.enabled) continue;
      if (step.type === 'rename' && step.config.column && step.config.newName) {
        const ci = cols.findIndex((c) => c.name === step.config.column);
        if (ci !== -1) cols[ci] = { ...cols[ci], name: step.config.newName };
      }
      if (step.type === 'select' && step.config.columns) {
        return step.config.columns.map((n: string) => cols.find((c) => c.name === n)).filter(Boolean) as typeof cols;
      }
      if (step.type === 'derive' && step.config.newColumn) {
        cols.push({ name: step.config.newColumn, type: 'number', nullable: true });
      }
    }
    return cols;
  }, [activeDataset, transforms]);

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
    setDatasets([...getStore().datasets, ds]);
    setActiveDatasetId(id);
    setShowImport(false);
  }, []);

  const addTransform = (type: string) => {
    const step: TransformStep = { id: `step-${Date.now()}`, type, config: {}, enabled: true };
    setTransforms((prev) => [...prev, step]);
  };

  const toggleStep = (id: string) => {
    setTransforms((prev) => prev.map((s) => s.id === id ? { ...s, enabled: !s.enabled } : s));
  };

  const removeStep = (id: string) => {
    setTransforms((prev) => prev.filter((s) => s.id !== id));
  };

  const updateConfig = (id: string, config: Record<string, any>) => {
    setTransforms((prev) => prev.map((s) => s.id === id ? { ...s, config } : s));
  };

  const download = (blob: Blob, filename: string) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  };

  const previewDataset = activeDataset ? { ...activeDataset, columns: transformedColumns, rows: transformedRows } : null;

  return (
    <div className="data-studio">
      <div className="data-toolbar">
        <button className="toolbar-btn" onClick={() => setShowImport(true)}>
          + Import Data
        </button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn" disabled={!activeDataset} onClick={() => {
          if (!activeDataset) return;
          download(new Blob([toCSV(transformedColumns, transformedRows)], { type: 'text/csv' }), `${activeDataset.name}.csv`);
        }}>Export CSV</button>
        <button className="toolbar-btn" disabled={!activeDataset} onClick={() => {
          if (!activeDataset) return;
          download(toXLSX(transformedColumns, transformedRows), `${activeDataset.name}.xls`);
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
              onClick={() => { setActiveDatasetId(ds.id); setTransforms([]); }}
            >
              <span className="data-ds-icon">▤</span>
              <span className="data-ds-name">{ds.name}</span>
              <span className="data-ds-info">{ds.rows.length} rows</span>
            </div>
          ))}
        </div>
        <div className="data-main">
          {previewDataset ? (
            <>
              <div className="data-tabs">
                {(['preview', 'transforms', 'stats'] as const).map((tab) => (
                  <button key={tab} className={`data-tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </div>
              <div className="data-content">
                {activeTab === 'preview' && <DataPreview dataset={previewDataset} />}
                {activeTab === 'transforms' && (
                  <TransformEditor
                    transforms={transforms}
                    onAdd={addTransform}
                    onToggle={toggleStep}
                    onRemove={removeStep}
                    onUpdateConfig={updateConfig}
                    columnNames={activeDataset?.columns.map((c) => c.name) ?? []}
                  />
                )}
                {activeTab === 'stats' && <StatsPanel dataset={previewDataset} />}
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
