import { useMemo } from 'react';
import type { Dataset } from './DataStudio';

interface StatsPanelProps {
  dataset: Dataset;
}

export default function StatsPanel({ dataset }: StatsPanelProps) {
  const stats = useMemo(() => {
    return dataset.columns.map((col, ci) => {
      const values = dataset.rows.map((r) => r[ci]).filter((v) => v !== null);
      const nums = values.filter((v) => typeof v === 'number') as number[];
      const strings = values.filter((v) => typeof v === 'string') as string[];

      return {
        name: col.name,
        type: col.type,
        total: dataset.rows.length,
        nonNull: values.length,
        nullCount: dataset.rows.length - values.length,
        numeric: nums.length > 0 ? {
          min: Math.min(...nums),
          max: Math.max(...nums),
          mean: nums.reduce((a, b) => a + b, 0) / nums.length,
          median: [...nums].sort((a, b) => a - b)[Math.floor(nums.length / 2)],
        } : null,
        string: strings.length > 0 ? {
          uniqueCount: new Set(strings).size,
          avgLength: strings.reduce((a, b) => a + b.length, 0) / strings.length,
        } : null,
      };
    });
  }, [dataset]);

  return (
    <div className="stats-panel">
      <div className="stats-summary">
        <div className="stat-card">
          <span className="stat-value">{dataset.rows.length}</span>
          <span className="stat-label">Rows</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{dataset.columns.length}</span>
          <span className="stat-label">Columns</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{dataset.rows.reduce((s, r) => s + r.filter((c) => c === null).length, 0)}</span>
          <span className="stat-label">Nulls</span>
        </div>
      </div>
      <table className="stats-table">
        <thead>
          <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Non-null</th>
            <th>Nulls</th>
            <th>Min</th>
            <th>Max</th>
            <th>Mean</th>
            <th>Median</th>
            <th>Unique</th>
          </tr>
        </thead>
        <tbody>
          {stats.map((s) => (
            <tr key={s.name}>
              <td className="stats-col-name">{s.name}</td>
              <td><span className="col-type">{s.type}</span></td>
              <td>{s.nonNull}</td>
              <td>{s.nullCount}</td>
              <td>{s.numeric?.min.toFixed(2) ?? '—'}</td>
              <td>{s.numeric?.max.toFixed(2) ?? '—'}</td>
              <td>{s.numeric?.mean.toFixed(2) ?? '—'}</td>
              <td>{s.numeric?.median.toFixed(2) ?? '—'}</td>
              <td>{s.string?.uniqueCount ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
