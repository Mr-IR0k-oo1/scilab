import { useState, useEffect } from 'react';
import { getStore, subscribe } from '@/store/store';

async function tryInvoke(cmd: string, args?: any): Promise<any> {
  try {
    const mod = await import('@tauri-apps/api/core');
    return await (mod as any).invoke(cmd, args);
  } catch {
    return null;
  }
}

export default function StatusBar() {
  const [, forceUpdate] = useState(0);

  useEffect(() => {
    const unsub = subscribe(() => forceUpdate((n) => n + 1));
    tryInvoke('scilab_status').then((status) => {
      if (status) {
        forceUpdate((n) => n + 1);
      }
    });
    return unsub;
  }, []);

  const s = getStore();

  return (
    <footer className="statusbar">
      <span className="statusbar-item">FOSSEE Engineering Workspace v0.1.0</span>
      {s.project && (
        <>
          <span className="statusbar-separator">|</span>
          <span className="statusbar-item">{s.project.name}</span>
          <span className="statusbar-separator">|</span>
          <span className="statusbar-item">{s.project.tools.length} tool{s.project.tools.length > 1 ? 's' : ''}</span>
        </>
      )}
      <span className="statusbar-spacer" />
      <span className={`statusbar-item status-${s.scilabStatus === 'connected' ? 'connected' : 'disconnected'}`}>
        Scilab: {s.scilabStatus === 'connected' ? 'Connected' : 'Disconnected'}
      </span>
    </footer>
  );
}
