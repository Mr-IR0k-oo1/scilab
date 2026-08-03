import { useState, useEffect } from 'react';
import { getStore, subscribe, setStore } from '@/store/store';
import { syncScilabStatus } from '@/lib/scilab';
import { api } from '@/lib/api';

export default function StatusBar() {
  const [, forceUpdate] = useState(0);

  useEffect(() => {
    const unsub = subscribe(() => forceUpdate((n) => n + 1));
    
    let isSubscribed = true;
    const syncBackendStatus = async () => {
      try {
        const res = await api.request<{ status: string }>('GET', '/api/health');
        if (res.status === 'ok') {
          setStore({ backendStatus: 'online' });
          await syncScilabStatus();
        } else {
          setStore({ backendStatus: 'offline', scilabStatus: 'disconnected' });
        }
      } catch (e) {
        setStore({ backendStatus: 'offline', scilabStatus: 'disconnected' });
      }
    };

    // Initial sync
    syncBackendStatus();
    
    // Poll every 5 seconds
    const interval = setInterval(() => {
      if (isSubscribed) {
        syncBackendStatus();
      }
    }, 5000);

    return () => {
      isSubscribed = false;
      clearInterval(interval);
      unsub();
    };
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
      <span className={`statusbar-item status-${s.backendStatus === 'online' ? 'connected' : 'disconnected'}`}>
        Backend: {s.backendStatus === 'online' ? 'Online' : 'Offline'}
      </span>
      <span className="statusbar-separator">|</span>
      <span className={`statusbar-item status-${s.scilabStatus === 'connected' ? 'connected' : 'disconnected'}`}>
        Scilab: {s.scilabStatus === 'connected' ? 'Connected' : 'Disconnected'}
      </span>
    </footer>
  );
}
