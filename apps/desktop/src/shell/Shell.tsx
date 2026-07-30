import { useState, useEffect, useRef } from 'react';
import EcosystemShell from '@/ecosystem/EcosystemShell';
import WorkspaceView from '@/shell/WorkspaceView';
import { enterProject, getStore, subscribe, restoreSession, setStore } from '@/store/store';
import { syncScilabStatus } from '@/lib/scilab';
import type { FOSSEEProject } from '@/ecosystem/types';

export default function Shell() {
  const [ready, setReady] = useState(false);
  const [, forceUpdate] = useState(0);
  const restored = useRef(false);

  useEffect(() => {
    if (!restored.current) {
      restored.current = true;
      const session = restoreSession();
      if (session && session.inProject && session.project) {
        setStore({
          sidebarOpen: session.sidebarOpen ?? true,
          sidebarWidth: session.sidebarWidth ?? 250,
          bottomPanelOpen: session.bottomPanelOpen ?? false,
          bottomPanelHeight: session.bottomPanelHeight ?? 200,
          rightSidebarOpen: session.rightSidebarOpen ?? false,
          rightSidebarWidth: session.rightSidebarWidth ?? 300,
          theme: session.theme ?? 'dark',
          zoom: session.zoom ?? 1,
          consoleHistory: session.consoleHistory ?? [],
          scilabStatus: 'disconnected',
          scilabPid: null,
        });
        const p = session.project as FOSSEEProject;
        enterProject(p);
      }
    }
    syncScilabStatus();
    const interval = setInterval(syncScilabStatus, 5000);
    const t = setTimeout(() => setReady(true), 100);
    subscribe(() => forceUpdate((n) => n + 1));
    return () => { clearTimeout(t); clearInterval(interval); };
  }, []);

  const s = getStore();

  if (!ready) {
    return (
      <div className="shell-loading">
        <div className="shell-spinner" />
        <span>FOSSEE Engineering Workspace</span>
      </div>
    );
  }

  if (!s.inProject) {
    return <EcosystemShell onEnterProject={(project: FOSSEEProject) => enterProject(project)} />;
  }

  return <WorkspaceView />;
}
