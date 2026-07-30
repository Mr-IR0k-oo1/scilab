import { useState, useMemo } from 'react';
import type { Dataset } from './DataStudio';

interface DataPreviewProps {
  dataset: Dataset;
}

export default function DataPreview({ dataset }: DataPreviewProps) {
  const [sortKey, setSortKey] = useState<number | null>(null);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');

  const sortedRows = useMemo(() => {
    if (sortKey === null) return dataset.rows;
    return [...dataset.rows].sort((a, b) => {
      const va = a[sortKey] ?? '';
      const vb = b[sortKey] ?? '';
      const cmp = String(va).localeCompare(String(vb));
      return sortDir === 'asc' ? cmp : -cmp;
    });
  }, [dataset.rows, sortKey, sortDir]);

  const handleHeaderClick = (idx: number) => {
    if (sortKey === idx) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(idx);
      setSortDir('asc');
    }
  };

  return (
    <div className="data-preview">
      <div className="data-preview-info">
        <span>{dataset.rows.length} rows</span>
        <span> • </span>
        <span>{dataset.columns.length} columns</span>
        <span> • </span>
        <span>{dataset.name}</span>
      </div>
      <div className="data-grid-container">
        <table className="data-grid">
          <thead>
            <tr>
              <th className="grid-row-num">#</th>
              {dataset.columns.map((col, i) => (
                <th key={i} onClick={() => handleHeaderClick(i)} className="grid-header">
                  {col.name}
                  <span className="col-type">{col.type}</span>
                  {sortKey === i && <span className="sort-indicator">{sortDir === 'asc' ? ' ▲' : ' ▼'}</span>}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedRows.map((row, ri) => (
              <tr key={ri}>
                <td className="grid-row-num">{ri + 1}</td>
                {row.map((cell, ci) => (
                  <td key={ci} className="grid-cell">{cell ?? <span className="null-value">null</span>}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
