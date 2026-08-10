import { useState, useEffect, useRef } from 'react';
import { getStore, setStore, subscribe } from '@/store/store';

type PanelTab = 'console' | 'variables' | 'output';

const RESPONSES: Record<string, string> = {
  sin: 'ans =  0.9093',
  cos: 'ans =  -0.4161',
  tan: 'ans =  1.5574',
  sqrt: 'ans =  3.1623',
  log: 'ans =  2.3026',
  disp: '',
  size: 'ans =  1.  100.',
  who: 'your variables are:\n\nans   x   y   z',
  zeros: 'ans =\n\n  0.  0.  0.\n  0.  0.  0.\n  0.  0.  0.',
  ones: 'ans =\n\n  1.  1.  1.\n  1.  1.  1.',
  rand: 'ans =\n\n  0.2113  0.6654  0.1256',
  plot: 'Graphical window opened.',
  histplot: 'Histogram plotted.',
  title: '',
  xlabel: '',
  ylabel: '',
  legend: '',
  clear: '',
  help: 'See https://help.scilab.org for documentation.',
  exit: '',
  quit: '',
};

function evalCommand(cmd: string): string {
  const trimmed = cmd.trim().toLowerCase();
  if (!trimmed) return '';
  if (trimmed === 'help') return 'ans =  \n\nAvailable commands: sin, cos, tan, sqrt, log, disp, who, zeros, ones, rand, plot, size, help, clear, exit';
  if (trimmed.startsWith('a=') || trimmed.startsWith('b=') || trimmed.startsWith('x=') || trimmed.startsWith('y=')) {
    const parts = trimmed.split('=');
    return `${parts[0].trim()} =  computed`;
  }
  for (const [key, resp] of Object.entries(RESPONSES)) {
    if (trimmed.includes(key)) return resp || '';
  }
  if (/^\d/.test(trimmed)) return `ans =  ${trimmed}`;
  return 'ans =  42';
}

export default function BottomPanel() {
  const [, forceUpdate] = useState(0);
  const [input, setInput] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const consoleRef = useRef<HTMLDivElement>(null);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  useEffect(() => {
    if (consoleRef.current) consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
  }, [history]);

  const s = getStore();
  const activeDataset = s.currentView === 'data' ? 'iris_dataset' : null;
  const varRows = [
    { name: 'ans', type: 'double', value: '42' },
    { name: 'x', type: 'double[1x100]', value: '0 0.0635 0.1269 ...' },
    { name: 'y', type: 'double[1x100]', value: '0 0.0634 0.1266 ...' },
    ...(activeDataset ? [{ name: 'data', type: 'double[150x5]', value: `[${activeDataset}]` }] : []),
  ];

  const executeCommand = (cmd: string) => {
    const trimmed = cmd.trim();
    if (!trimmed) return;
    const result = evalCommand(trimmed);
    const lines: string[] = [`--> ${trimmed}`];
    if (result) lines.push(...result.split('\n').map((l) => `    ${l}`));
    setHistory((prev) => [...prev, ...lines]);
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      executeCommand(input);
    }
  };

  const activeTab = s.activeBottomTab;
  const setActiveTab = (tab: PanelTab) => setStore({ activeBottomTab: tab });

  return (
    <div className="bottom-panel-content">
      <div className="bottom-panel-tabs">
        {([
          { id: 'console' as const, label: 'Console' },
          { id: 'variables' as const, label: 'Variables' },
          { id: 'output' as const, label: 'Output' },
        ]).map((tab) => (
          <button key={tab.id} className={`bp-tab ${activeTab === tab.id ? 'active' : ''}`} onClick={() => setActiveTab(tab.id)}>
            {tab.label}
          </button>
        ))}
        <div className="toolbar-spacer" />
        <button className="bp-close" onClick={() => setStore({ bottomPanelOpen: false })}>×</button>
      </div>
      <div className="bottom-panel-body">
        {activeTab === 'console' && (
          <div className="console" ref={consoleRef}>
            <div className="console-line" style={{ color: 'var(--accent)' }}>Scilab Console v0.1.0</div>
            <div className="console-line" style={{ color: 'var(--text-muted)' }}>Type Scilab commands or run scripts</div>
            {history.map((line, i) => (
              <div key={i} className={`console-line ${line.startsWith('-->') ? 'console-cmd' : ''}`}>{line}</div>
            ))}
            <div className="console-input-line">
              <span className="console-prompt">{'-->'}</span>
              <input className="console-input" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyDown} placeholder="Enter Scilab command..." autoFocus />
            </div>
          </div>
        )}
        {activeTab === 'variables' && (
          <div className="variables-panel">
            <table className="variables-table">
              <thead>
                <tr><th>Name</th><th>Type</th><th>Value</th></tr>
              </thead>
              <tbody>
                {varRows.map((row) => (
                  <tr key={row.name}>
                    <td><span className="var-name">{row.name}</span></td>
                    <td><span className="var-type">{row.type}</span></td>
                    <td>{row.value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {varRows.length === 0 && <div className="empty-state">No variables in workspace</div>}
          </div>
        )}
        {activeTab === 'output' && (
          <div className="output-pane">
            <pre className="output-content">{history.filter((l) => !l.startsWith('-->')).join('\n') || 'No output yet. Run a script to see results.'}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
