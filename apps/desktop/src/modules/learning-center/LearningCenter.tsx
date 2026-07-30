import { useState } from 'react';
import ExampleCard from '@/modules/learning-center/ExampleCard';
import TutorialPanel from '@/modules/learning-center/TutorialPanel';
import ReferenceView from '@/modules/learning-center/ReferenceView';
import { openTab, setStore } from '@/store/store';

const EXAMPLES = [
  { id: 'hello-world', title: 'Hello World', category: 'Getting Started', difficulty: 'Beginner', duration: '5 min', description: 'Your first Scilab script' },
  { id: 'import-csv', title: 'Import CSV', category: 'Data Analysis', difficulty: 'Beginner', duration: '10 min', description: 'Load and analyze CSV data' },
  { id: 'line-chart', title: 'Line Chart', category: 'Visualization', difficulty: 'Beginner', duration: '10 min', description: 'Create a basic line chart' },
  { id: 'gui-basics', title: 'Basic GUI', category: 'GUI Design', difficulty: 'Beginner', duration: '15 min', description: 'Build a simple GUI' },
  { id: 'data-stats', title: 'Data Statistics', category: 'Data Analysis', difficulty: 'Beginner', duration: '15 min', description: 'Compute descriptive statistics' },
  { id: 'transform-pipeline', title: 'Transform Pipeline', category: 'Data Analysis', difficulty: 'Intermediate', duration: '20 min', description: 'Build a data transform pipeline' },
  { id: 'multi-series', title: 'Multi-Series Chart', category: 'Visualization', difficulty: 'Intermediate', duration: '15 min', description: 'Compare multiple data series' },
  { id: 'heatmap', title: 'Heatmap', category: 'Visualization', difficulty: 'Intermediate', duration: '15 min', description: 'Visualize matrix data as heatmap' },
  { id: 'gui-callbacks', title: 'GUI with Callbacks', category: 'GUI Design', difficulty: 'Intermediate', duration: '25 min', description: 'Add event callbacks to GUI' },
  { id: 'signal-fft', title: 'Signal FFT', category: 'Signal Processing', difficulty: 'Intermediate', duration: '20 min', description: 'Compute FFT of a signal' },
  { id: 'bode-plot', title: 'Bode Plot', category: 'Control Systems', difficulty: 'Advanced', duration: '25 min', description: 'Analyze system frequency response' },
  { id: 'ode-solver', title: 'ODE Solver', category: 'Numerical Methods', difficulty: 'Advanced', duration: '30 min', description: 'Solve differential equations' },
  { id: 'lab-report', title: 'Lab Report', category: 'Reports', difficulty: 'Intermediate', duration: '20 min', description: 'Create a formatted lab report' },
];

const CATEGORIES = ['All', 'Getting Started', 'Data Analysis', 'Visualization', 'GUI Design', 'Signal Processing', 'Control Systems', 'Numerical Methods', 'Reports'];

const REFERENCE_CATEGORIES = [
  { name: 'Basic', functions: ['disp', 'who', 'clear', 'size', 'type', 'exists'] },
  { name: 'Matrices', functions: ['zeros', 'ones', 'rand', 'eye', 'diag', 'triu', 'tril'] },
  { name: 'Plotting', functions: ['plot', 'scatter', 'bar', 'histplot', 'title', 'xlabel', 'ylabel', 'legend'] },
  { name: 'Data', functions: ['csvRead', 'csvWrite', 'xlsRead', 'savemat', 'loadmat'] },
  { name: 'Signal', functions: ['fft', 'ifft', 'filter', 'correl', 'psd'] },
  { name: 'Control', functions: ['tf', 'ss', 'bode', 'nyquist', 'rlocus', 'step', 'impulse'] },
  { name: 'Numerical', functions: ['ode', 'interp', 'spline', 'intg', 'fsolve'] },
  { name: 'Statistics', functions: ['mean', 'median', 'stdev', 'histc', 'corr', 'reglin'] },
];

const MODULE_MAP: Record<string, string> = {
  'hello-world': 'editor',
  'import-csv': 'data',
  'line-chart': 'viz',
  'gui-basics': 'gui',
  'data-stats': 'data',
  'transform-pipeline': 'data',
  'multi-series': 'viz',
  'heatmap': 'viz',
  'gui-callbacks': 'gui',
  'signal-fft': 'viz',
  'bode-plot': 'viz',
  'ode-solver': 'editor',
  'lab-report': 'report',
};

export default function LearningCenter() {
  const [activeTab, setActiveTab] = useState<'examples' | 'tutorials' | 'reference'>('examples');
  const [category, setCategory] = useState('All');
  const [search, setSearch] = useState('');

  const openExample = (id: string) => {
    const mod = MODULE_MAP[id] ?? 'editor';
    const ex = EXAMPLES.find((e) => e.id === id);
    openTab({ id: 'ex-' + id, title: ex?.title ?? 'Example', module: mod });
    setStore({ currentView: mod as any });
  };

  const filtered = EXAMPLES.filter((e) => {
    if (category !== 'All' && e.category !== category) return false;
    if (search && !e.title.toLowerCase().includes(search.toLowerCase()) && !e.description.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="learning-center">
      <div className="lc-toolbar">
        <div className="lc-tabs">
          {(['examples', 'tutorials', 'reference'] as const).map((tab) => (
            <button key={tab} className={`lc-tab ${activeTab === tab ? 'active' : ''}`} onClick={() => setActiveTab(tab)}>
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
      </div>
      {activeTab === 'examples' && (
        <div className="lc-content">
          <div className="lc-search-bar">
            <input className="lc-search-input" placeholder="Search examples..." value={search} onChange={(e) => setSearch(e.target.value)} />
            <div className="lc-categories">
              {CATEGORIES.map((c) => (
                <button key={c} className={`lc-cat-btn ${category === c ? 'active' : ''}`} onClick={() => setCategory(c)}>{c}</button>
              ))}
            </div>
          </div>
          <div className="lc-examples-grid">
            {filtered.map((ex) => (
              <ExampleCard key={ex.id} example={ex} onOpen={() => openExample(ex.id)} />
            ))}
          </div>
        </div>
      )}
      {activeTab === 'tutorials' && <TutorialPanel />}
      {activeTab === 'reference' && <ReferenceView categories={REFERENCE_CATEGORIES} />}
    </div>
  );
}
