import { useState, useRef, useEffect } from 'react';
import { toggleSidebar, toggleBottomPanel, openTab, resetTabs, setStore, getStore, subscribe } from '@/store/store';

interface MenuAction {
  label: string;
  shortcut?: string;
  action?: () => void;
  disabled?: boolean;
  separator?: boolean;
}

interface MenuDef {
  label: string;
  items: MenuAction[];
}

export default function MenuBar() {
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const [, forceUpdate] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpenMenu(null);
    };
    window.addEventListener('mousedown', handler);
    return () => window.removeEventListener('mousedown', handler);
  }, []);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const switchMod = (id: string, label: string) => {
    openTab({ id, title: label, module: id });
    setStore({ currentView: id as any });
  };

  const menus: MenuDef[] = [
    {
      label: 'File',
      items: [
        { label: 'New Project', shortcut: 'Ctrl+N', action: () => setStore({ project: { version: '1.0', name: 'Untitled', path: '/Untitled', tools: ['scilab'], created: new Date().toISOString(), modified: new Date().toISOString() } }) },
        { label: 'Open Project', shortcut: 'Ctrl+O', action: () => {} },
        { label: 'Save', shortcut: 'Ctrl+S', action: () => {} },
        { label: 'Save As...', shortcut: 'Ctrl+Shift+S', action: () => {} },
        { label: '', separator: true },
        { label: 'Recent Projects', disabled: true },
        { label: '', separator: true },
        { label: 'Exit', action: () => window.close() },
      ],
    },
    {
      label: 'Edit',
      items: [
        { label: 'Undo', shortcut: 'Ctrl+Z', action: () => document.dispatchEvent(new CustomEvent('app:undo')) },
        { label: 'Redo', shortcut: 'Ctrl+Shift+Z', action: () => document.dispatchEvent(new CustomEvent('app:redo')) },
        { label: '', separator: true },
        { label: 'Cut', shortcut: 'Ctrl+X', action: () => {} },
        { label: 'Copy', shortcut: 'Ctrl+C', action: () => {} },
        { label: 'Paste', shortcut: 'Ctrl+V', action: () => {} },
        { label: '', separator: true },
        { label: 'Find', shortcut: 'Ctrl+F', action: () => {} },
        { label: 'Replace', shortcut: 'Ctrl+H', action: () => {} },
      ],
    },
    {
      label: 'View',
      items: [
        { label: 'Toggle Sidebar', shortcut: 'Ctrl+B', action: toggleSidebar },
        { label: 'Toggle Bottom Panel', shortcut: 'Ctrl+J', action: toggleBottomPanel },
        { label: '', separator: true },
        { label: 'Zoom In', shortcut: 'Ctrl+=', action: () => setStore({ zoom: Math.min(2, getStore().zoom + 0.1) }) },
        { label: 'Zoom Out', shortcut: 'Ctrl+-', action: () => setStore({ zoom: Math.max(0.5, getStore().zoom - 0.1) }) },
        { label: 'Reset Zoom', shortcut: 'Ctrl+0', action: () => setStore({ zoom: 1 }) },
        { label: '', separator: true },
        { label: 'Script Editor', action: () => switchMod('editor', 'Script Editor') },
        { label: 'GUI Builder', action: () => switchMod('gui', 'GUI Builder') },
        { label: 'Visualization', action: () => switchMod('viz', 'Visualization Studio') },
        { label: 'Data Studio', action: () => switchMod('data', 'Data Studio') },
        { label: 'Reports', action: () => switchMod('report', 'Report Generator') },
        { label: 'Learning Center', action: () => switchMod('learn', 'Learning Center') },
      ],
    },
    {
      label: 'Scilab',
      items: [
        { label: 'Start Engine', action: () => document.dispatchEvent(new CustomEvent('scilab:start')) },
        { label: 'Stop Engine', action: () => document.dispatchEvent(new CustomEvent('scilab:stop')) },
        { label: 'Restart Engine', action: () => {
          document.dispatchEvent(new CustomEvent('scilab:stop'));
          setTimeout(() => document.dispatchEvent(new CustomEvent('scilab:start')), 500);
        }},
        { label: '', separator: true },
        { label: 'Clear Console', action: () => setStore({ consoleHistory: [] }) },
        { label: 'Abort Execution', shortcut: 'Ctrl+C', action: () => {} },
      ],
    },
    {
      label: 'Help',
      items: [
        { label: 'Documentation', action: () => switchMod('learn', 'Learning Center') },
        { label: 'Learning Center', action: () => switchMod('learn', 'Learning Center') },
        { label: '', separator: true },
        { label: 'About Scilab Studio', action: () => alert('Scilab Studio v0.1.0\n\nThe Open Engineering Development Platform') },
      ],
    },
  ];

  return (
    <nav className="menubar" ref={ref}>
      {menus.map((menu) => (
        <div key={menu.label} className="menu-container">
          <span
            className={`menubar-item ${openMenu === menu.label ? 'active' : ''}`}
            onMouseDown={() => setOpenMenu(openMenu === menu.label ? null : menu.label)}
            onMouseEnter={() => openMenu && setOpenMenu(menu.label)}
          >
            {menu.label}
          </span>
          {openMenu === menu.label && (
            <div className="menu-dropdown">
              {menu.items.map((item, i) =>
                item.separator ? (
                  <div key={i} className="menu-separator" />
                ) : (
                  <button
                    key={i}
                    className="menu-item"
                    disabled={item.disabled}
                    onClick={() => {
                      item.action?.();
                      setOpenMenu(null);
                    }}
                  >
                    <span>{item.label}</span>
                    {item.shortcut && <span className="menu-shortcut">{item.shortcut}</span>}
                  </button>
                )
              )}
            </div>
          )}
        </div>
      ))}
    </nav>
  );
}
