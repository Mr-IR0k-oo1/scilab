import {
  Bot,
  ChartColumn,
  Code2,
  Command,
  FileText,
  GraduationCap,
  LayoutPanelLeft,
  PanelBottom,
  PanelsTopLeft,
  Table2,
} from 'lucide-react';
import { getStore, openTab, setStore } from '@/store/store';

interface ActivityRailProps {
  onCommandPalette: () => void;
}

const MODULES = [
  { id: 'editor', label: 'Editor', icon: Code2 },
  { id: 'gui', label: 'GUI Builder', icon: PanelsTopLeft },
  { id: 'viz', label: 'Visualization', icon: ChartColumn },
  { id: 'data', label: 'Data Studio', icon: Table2 },
  { id: 'report', label: 'Reports', icon: FileText },
  { id: 'learn', label: 'Learning', icon: GraduationCap },
];

export default function ActivityRail({ onCommandPalette }: ActivityRailProps) {
  const s = getStore();

  const switchModule = (id: string, label: string) => {
    openTab({ id, title: label, module: id });
    setStore({ currentView: id });
  };

  return (
    <nav className="activity-rail" aria-label="Workbench">
      <button className="activity-btn" onClick={() => setStore({ sidebarOpen: !s.sidebarOpen })} title="Toggle left panel">
        <LayoutPanelLeft size={17} />
      </button>
      <button className="activity-btn command" onClick={onCommandPalette} title="Command palette">
        <Command size={17} />
      </button>
      <div className="activity-separator" />
      {MODULES.map((item) => {
        const Icon = item.icon;
        return (
          <button
            key={item.id}
            className={`activity-btn ${s.currentView === item.id ? 'active' : ''}`}
            onClick={() => switchModule(item.id, item.label)}
            title={item.label}
            aria-label={item.label}
          >
            <Icon size={17} />
          </button>
        );
      })}
      <div className="activity-spacer" />
      <button className={`activity-btn ${s.rightSidebarOpen ? 'active' : ''}`} onClick={() => setStore({ rightSidebarOpen: !s.rightSidebarOpen })} title="Assistant">
        <Bot size={17} />
      </button>
      <button className={`activity-btn ${s.bottomPanelOpen ? 'active' : ''}`} onClick={() => setStore({ bottomPanelOpen: !s.bottomPanelOpen })} title="Toggle bottom panel">
        <PanelBottom size={17} />
      </button>
    </nav>
  );
}
