import { openTab, setStore, getStore } from '@/store/store';

interface ToolbarProps {
  onModuleSwitch?: (id: string) => void;
}

const MODULES = [
  { id: 'editor', label: 'Editor', icon: '<>' },
  { id: 'gui', label: 'GUI', icon: '▣' },
  { id: 'viz', label: 'Viz', icon: '◈' },
  { id: 'data', label: 'Data', icon: '≡' },
  { id: 'report', label: 'Report', icon: '▤' },
  { id: 'learn', label: 'Learn', icon: '⌘' },
];

export default function Toolbar({ onModuleSwitch }: ToolbarProps) {
  const switchMod = (id: string) => {
    const mod = MODULES.find((m) => m.id === id);
    if (!mod) return;
    openTab({ id, title: mod.label, module: id });
    setStore({ currentView: id as any });
    onModuleSwitch?.(id);
  };

  const handleRun = () => {
    const s = getStore();
    if (s.currentView !== 'editor') {
      switchMod('editor');
    }
    document.dispatchEvent(new CustomEvent('app:run-script'));
  };

  return (
    <div className="toolbar">
      {MODULES.map((m) => (
        <button key={m.id} className="toolbar-btn" onClick={() => switchMod(m.id)} title={m.label}>
          {m.icon} {m.label}
        </button>
      ))}
      <div className="toolbar-separator" />
      <button className="toolbar-btn run-btn" onClick={handleRun} title="Run Script (Ctrl+Enter)">▸ Run</button>
      <div className="toolbar-spacer" />
    </div>
  );
}
