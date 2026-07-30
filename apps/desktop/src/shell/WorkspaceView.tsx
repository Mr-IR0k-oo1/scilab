import { useState, useEffect } from 'react';
import Platform from '@/platform/Platform';
import WorkspaceManager from '@/ecosystem/WorkspaceManager';
import { getStore, subscribe, toggleSidebar, toggleBottomPanel, leaveProject } from '@/store/store';
import { FOSSEE_TOOLS } from '@/ecosystem/ToolRegistry';

export default function WorkspaceView() {
  const [, forceUpdate] = useState(0);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const s = getStore();
  const tool = s.project ? FOSSEE_TOOLS[s.currentTool] : null;

  return (
    <div className="app">
      <header className="titlebar">
        <button className="titlebar-btn" onClick={leaveProject} title="Back to Ecosystem">
          ←
        </button>
        <span className="titlebar-logo" style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          {s.project?.name ?? 'Project'}
        </span>
        {tool && (
          <>
            <span className="titlebar-separator" />
            <span className="titlebar-btn active" style={{ cursor: 'default', color: tool.color }}>
              {tool.icon} {tool.name}
            </span>
          </>
        )}
        <div className="titlebar-spacer" />
        <button className="titlebar-btn" onClick={toggleSidebar} title="Toggle Sidebar (Ctrl+B)">
          ≡
        </button>
        <button className="titlebar-btn" onClick={toggleBottomPanel} title="Toggle Panel (Ctrl+J)">
          ▤
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
