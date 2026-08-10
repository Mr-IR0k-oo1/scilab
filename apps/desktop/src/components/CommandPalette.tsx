import { useEffect, useMemo, useRef, useState } from 'react';
import {
  Bot,
  ChartColumn,
  Code2,
  FileText,
  GraduationCap,
  LayoutPanelLeft,
  PanelBottom,
  PanelsTopLeft,
  Play,
  Search,
  Table2,
  Terminal,
} from 'lucide-react';
import { getStore, openTab, setStore } from '@/store/store';

interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
}

const COMMANDS = [
  { id: 'editor', title: 'Open Script Editor', hint: 'Module', icon: Code2, run: () => switchModule('editor', 'Script Editor') },
  { id: 'gui', title: 'Open GUI Builder', hint: 'Module', icon: PanelsTopLeft, run: () => switchModule('gui', 'GUI Builder') },
  { id: 'viz', title: 'Open Visualization Studio', hint: 'Module', icon: ChartColumn, run: () => switchModule('viz', 'Visualization Studio') },
  { id: 'data', title: 'Open Data Studio', hint: 'Module', icon: Table2, run: () => switchModule('data', 'Data Studio') },
  { id: 'report', title: 'Open Report Generator', hint: 'Module', icon: FileText, run: () => switchModule('report', 'Report Generator') },
  { id: 'learn', title: 'Open Learning Center', hint: 'Module', icon: GraduationCap, run: () => switchModule('learn', 'Learning Center') },
  { id: 'run-script', title: 'Run Active Script', hint: 'Scilab', icon: Play, run: () => document.dispatchEvent(new CustomEvent('app:run-script')) },
  { id: 'toggle-sidebar', title: 'Toggle Left Panel', hint: 'View', icon: LayoutPanelLeft, run: () => setStore({ sidebarOpen: !getStore().sidebarOpen }) },
  { id: 'toggle-bottom', title: 'Toggle Bottom Panel', hint: 'View', icon: PanelBottom, run: () => setStore({ bottomPanelOpen: !getStore().bottomPanelOpen }) },
  { id: 'toggle-assistant', title: 'Toggle Assistant', hint: 'View', icon: Bot, run: () => setStore({ rightSidebarOpen: !getStore().rightSidebarOpen }) },
  { id: 'start-engine', title: 'Start Scilab Engine', hint: 'Runtime', icon: Terminal, run: () => document.dispatchEvent(new CustomEvent('scilab:start')) },
];

function switchModule(id: string, title: string) {
  openTab({ id, title, module: id });
  setStore({ currentView: id });
}

export default function CommandPalette({ open, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return COMMANDS;
    return COMMANDS.filter((command) => `${command.title} ${command.hint}`.toLowerCase().includes(q));
  }, [query]);

  useEffect(() => {
    if (!open) return;
    setQuery('');
    setActiveIndex(0);
    requestAnimationFrame(() => inputRef.current?.focus());
  }, [open]);

  useEffect(() => {
    if (activeIndex >= filtered.length) setActiveIndex(0);
  }, [activeIndex, filtered.length]);

  if (!open) return null;

  const run = (index: number) => {
    const command = filtered[index];
    if (!command) return;
    command.run();
    onClose();
  };

  return (
    <div className="command-overlay" onMouseDown={onClose}>
      <div className="command-panel" role="dialog" aria-label="Command palette" onMouseDown={(e) => e.stopPropagation()}>
        <div className="command-input-row">
          <Search size={16} />
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Escape') onClose();
              if (e.key === 'ArrowDown') {
                e.preventDefault();
                setActiveIndex((i) => Math.min(filtered.length - 1, i + 1));
              }
              if (e.key === 'ArrowUp') {
                e.preventDefault();
                setActiveIndex((i) => Math.max(0, i - 1));
              }
              if (e.key === 'Enter') run(activeIndex);
            }}
            placeholder="Search commands, views, and tools"
          />
        </div>
        <div className="command-list">
          {filtered.map((command, index) => {
            const Icon = command.icon;
            return (
              <button
                key={command.id}
                className={`command-item ${index === activeIndex ? 'active' : ''}`}
                onMouseEnter={() => setActiveIndex(index)}
                onClick={() => run(index)}
              >
                <Icon size={16} />
                <span>{command.title}</span>
                <small>{command.hint}</small>
              </button>
            );
          })}
          {filtered.length === 0 && <div className="command-empty">No commands found</div>}
        </div>
      </div>
    </div>
  );
}
