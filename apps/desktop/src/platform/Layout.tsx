import { useEffect, useState } from 'react';
import { getStore, subscribe, setStore } from '@/store/store';

interface LayoutProps {
  sidebar: React.ReactNode;
  main: React.ReactNode;
  rightSidebar: React.ReactNode;
  bottomPanel: React.ReactNode;
}

export default function Layout({ sidebar, main, rightSidebar, bottomPanel }: LayoutProps) {
  const [, forceUpdate] = useState(0);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const s = getStore();

  return (
    <div className="layout">
      {s.sidebarOpen && sidebar && (
        <aside className="sidebar" style={{ width: s.sidebarWidth }}>
          <div
            className="resize-handle-x"
            onMouseDown={(e) => {
              const start = e.clientX;
              const startW = s.sidebarWidth;
              const onMove = (ev: MouseEvent) => {
                setStore({ sidebarWidth: Math.max(150, Math.min(400, startW + ev.clientX - start)) });
              };
              const onUp = () => { window.removeEventListener('mousemove', onMove); window.removeEventListener('mouseup', onUp); };
              window.addEventListener('mousemove', onMove);
              window.addEventListener('mouseup', onUp);
            }}
          />
          {sidebar}
        </aside>
      )}
      <div className="layout-main">
        {main}
      </div>
      {s.rightSidebarOpen && rightSidebar && (
        <aside className="sidebar-right" style={{ width: s.rightSidebarWidth }}>
          <div
            className="resize-handle-x left"
            onMouseDown={(e) => {
              const start = e.clientX;
              const startW = s.rightSidebarWidth;
              const onMove = (ev: MouseEvent) => {
                setStore({ rightSidebarWidth: Math.max(200, Math.min(500, startW - (ev.clientX - start))) });
              };
              const onUp = () => { window.removeEventListener('mousemove', onMove); window.removeEventListener('mouseup', onUp); };
              window.addEventListener('mousemove', onMove);
              window.addEventListener('mouseup', onUp);
            }}
          />
          {rightSidebar}
        </aside>
      )}
      {s.bottomPanelOpen && bottomPanel && (
        <div className="bottom-panel" style={{ height: s.bottomPanelHeight }}>
          <div
            className="resize-handle-y"
            onMouseDown={(e) => {
              const start = e.clientY;
              const startH = s.bottomPanelHeight;
              const onMove = (ev: MouseEvent) => {
                setStore({ bottomPanelHeight: Math.max(100, Math.min(400, startH - (ev.clientY - start))) });
              };
              const onUp = () => { window.removeEventListener('mousemove', onMove); window.removeEventListener('mouseup', onUp); };
              window.addEventListener('mousemove', onMove);
              window.addEventListener('mouseup', onUp);
            }}
          />
          {bottomPanel}
        </div>
      )}
    </div>
  );
}
