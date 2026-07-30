import { useState, useEffect } from 'react';
import { getStore, subscribe, closeTab, openTab, setStore } from '@/store/store';

export default function Tabs() {
  const [, forceUpdate] = useState(0);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const s = getStore();

  if (s.tabs.length === 0) return null;

  return (
    <div className="tab-bar">
      {s.tabs.map((tab) => (
        <div
          key={tab.id}
          className={`tab-item ${s.activeTab === tab.id ? 'active' : ''}`}
          onMouseDown={() => {
            setStore({ currentView: tab.module as any, activeTab: tab.id });
          }}
        >
          <span className="tab-title">{tab.title}</span>
          {tab.dirty && <span className="tab-dirty">·</span>}
          <button
            className="tab-close"
            onMouseDown={(e) => {
              e.stopPropagation();
              closeTab(tab.id);
            }}
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
