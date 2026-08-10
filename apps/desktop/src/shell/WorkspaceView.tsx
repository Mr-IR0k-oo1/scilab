import { useEffect, useState } from 'react';
import { Bot, Command, PanelBottom, PanelLeft } from 'lucide-react';
import Platform from '@/platform/Platform';
import WorkspaceManager from '@/ecosystem/WorkspaceManager';
import { getStore, setStore, subscribe, toggleBottomPanel, toggleSidebar } from '@/store/store';
import { FOSSEE_TOOLS } from '@/ecosystem/ToolRegistry';

export default function WorkspaceView() {
  const [, forceUpdate] = useState(0);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const s = getStore();
  const tool = s.project ? FOSSEE_TOOLS[s.currentTool] : null;

  const openCommandPalette = () => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'p', ctrlKey: true }));
  };

  return (
    <div className="app">
      <header className="titlebar">
        <span className="titlebar-logo">Scilab Studio</span>
        {tool && (
          <>
            <span className="titlebar-separator" />
            <span className="titlebar-project">{s.project?.name ?? 'Project'}</span>
            <span className="titlebar-tool" style={{ color: tool.color }}>{tool.name}</span>
          </>
        )}
        <div className="titlebar-spacer" />
        <button className="titlebar-command" onClick={openCommandPalette} title="Command Palette (Ctrl+P)">
          <Command size={14} />
          <span>Search commands</span>
          <kbd>Ctrl P</kbd>
        </button>
        <button className="titlebar-btn" onClick={toggleSidebar} title="Toggle Sidebar (Ctrl+B)" aria-label="Toggle sidebar">
          <PanelLeft size={15} />
        </button>
        <button className="titlebar-btn" onClick={toggleBottomPanel} title="Toggle Panel (Ctrl+J)" aria-label="Toggle bottom panel">
          <PanelBottom size={15} />
        </button>
        <button className="titlebar-btn" onClick={() => setStore({ rightSidebarOpen: !s.rightSidebarOpen })} title="Toggle Assistant" aria-label="Toggle assistant">
          <Bot size={15} />
        </button>
        <div className="titlebar-scilab">
          <span className={`titlebar-dot ${s.scilabStatus === 'connected' ? '' : 'disconnected'}`} />
          {tool?.name ?? 'Scilab'}
        </div>
      </header>
      <Platform sidebar={<WorkspaceManager />} />
    </div>
  );
}
