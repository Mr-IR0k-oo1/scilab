import { useState, useRef } from 'react';

interface ImportDialogProps {
  onImport: (data: (string | number | null)[][], name: string) => void;
  onClose: () => void;
}

export default function ImportDialog({ onImport, onClose }: ImportDialogProps) {
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    setError(null);

    try {
      const text = await file.text();
      const lines = text.split('\n').filter((l) => l.trim());
      const data = lines.map((l) => {
        const vals = l.split(',').map((v) => {
          const trimmed = v.trim().replace(/^"|"$/g, '');
          if (trimmed === '') return null;
          const num = Number(trimmed);
          return isNaN(num) ? trimmed : num;
        });
        return vals;
      });
      onImport(data, name || file.name.replace(/\.[^/.]+$/, ''));
    } catch (err: any) {
      setError(err.message ?? 'Failed to parse file');
    }
    setLoading(false);
  };

  return (
    <div className="modal-overlay" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h2>Import Data</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <div className="form-group">
            <label>Dataset Name</label>
            <input
              type="text"
              className="form-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Auto-detected from filename"
            />
          </div>
          <div className="form-group">
            <label>File</label>
            <div className="file-dropzone" onClick={() => fileRef.current?.click()}>
              <input ref={fileRef} type="file" accept=".csv,.tsv,.xlsx,.xls,.json" hidden onChange={handleFile} />
              {loading ? <span>Loading...</span> : <span>Click to select CSV, Excel, or JSON file</span>}
            </div>
          </div>
          {error && <div className="form-error">{error}</div>}
        </div>
      </div>
    </div>
  );
}
