import { useState, useEffect, useCallback, ReactNode } from 'react';
import StatusBar from '@/components/StatusBar';
import MenuBar from '@/components/MenuBar';
import Sidebar from '@/components/Sidebar';
import BottomPanel from '@/components/BottomPanel';
import RightSidebar from '@/components/RightSidebar';
import Assistant from '@/components/Assistant';
import ActivityRail from '@/components/ActivityRail';
import CommandPalette from '@/components/CommandPalette';
import Layout from '@/platform/Layout';
import GuiBuilder from '@/modules/gui-builder/GuiBuilder';
import VizStudio from '@/modules/visualization/VizStudio';
import DataStudio from '@/modules/data-studio/DataStudio';
import ReportEditor from '@/modules/report-generator/ReportEditor';
import LearningCenter from '@/modules/learning-center/LearningCenter';
import ScriptEditor from '@/components/ScriptEditor';
import Tabs from '@/components/Tabs';
import { getStore, subscribe, openTab, setStore } from '@/store/store';

const MODULES: Record<string, { label: string; component: React.FC }> = {
  editor: { label: 'Script Editor', component: ScriptEditor },
  gui: { label: 'GUI Builder', component: GuiBuilder },
  viz: { label: 'Visualization Studio', component: VizStudio },
  data: { label: 'Data Studio', component: DataStudio },
  report: { label: 'Report Generator', component: ReportEditor },
  learn: { label: 'Learning Center', component: LearningCenter },
};

function WelcomeScreen({ onSwitch }: { onSwitch: (id: string) => void }) {
  return (
    <main className="editor-area">
      <div className="welcome-screen">
        <h1>Open Engineering Workspace</h1>
        <p>Select a module to begin</p>
        <div className="welcome-actions">
          {Object.entries(MODULES).map(([id, mod]) => (
            <button key={id} className="welcome-btn" onClick={() => onSwitch(id)}>
              {mod.label}
            </button>
          ))}
        </div>
      </div>
    </main>
  );
}

interface PlatformProps {
  rightSidebarContent?: 'default' | 'assistant' | 'none';
  sidebar?: ReactNode;
}

export default function Platform({ rightSidebarContent = 'assistant', sidebar }: PlatformProps) {
  const [commandOpen, setCommandOpen] = useState(false);
  const [, forceUpdate] = useState(0);
  const s = getStore();

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'b') { e.preventDefault(); setStore({ sidebarOpen: !getStore().sidebarOpen }); }
      if ((e.ctrlKey || e.metaKey) && e.key === 'j') { e.preventDefault(); setStore({ bottomPanelOpen: !getStore().bottomPanelOpen }); }
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key.toLowerCase() === 'p') { e.preventDefault(); setCommandOpen(true); }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'p') { e.preventDefault(); setCommandOpen(true); }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  const switchModule = useCallback((id: string) => {
    const mod = MODULES[id];
    if (!mod) return;
    openTab({ id, title: mod.label, module: id });
    setStore({ currentView: id });
  }, []);

  const activeModule = s.activeTab ? MODULES[s.activeTab] : null;
  const ActiveComponent = activeModule?.component ?? (() => <WelcomeScreen onSwitch={switchModule} />);

  const rightContent = rightSidebarContent === 'none' ? null : rightSidebarContent === 'assistant' ? <Assistant /> : <RightSidebar />;

  return (
    <div className="app workbench" style={{ zoom: s.zoom }}>
      <MenuBar />
      <div className="workbench-frame">
        <ActivityRail onCommandPalette={() => setCommandOpen(true)} />
        <Layout
          sidebar={sidebar ?? (
            <Sidebar
              onOpenFile={(path) => {
                const ext = path.split('.').pop()?.toLowerCase();
                if (ext === 'sci' || ext === 'sce') switchModule('editor');
                else if (ext === 'csv' || ext === 'xlsx' || ext === 'xls') switchModule('data');
              }}
            />
          )}
          main={
            <div className="editor-area" key={s.activeTab ?? 'welcome'}>
              <Tabs />
              <div className="editor-content">
                <ActiveComponent />
              </div>
            </div>
          }
          rightSidebar={s.rightSidebarOpen ? rightContent : null}
          bottomPanel={s.bottomPanelOpen ? <BottomPanel /> : null}
        />
      </div>
      <StatusBar />
      <CommandPalette open={commandOpen} onClose={() => setCommandOpen(false)} />
    </div>
  );
}
