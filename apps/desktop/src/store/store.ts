import type { FOSSEEToolId, FOSSEEProject } from '@/ecosystem/types';

export interface Tab {
  id: string;
  title: string;
  module: string;
  data?: any;
  dirty?: boolean;
}

export interface Store {
  currentView: string;
  currentTool: FOSSEEToolId;
  tabs: Tab[];
  activeTab: string | null;
  sidebarOpen: boolean;
  sidebarWidth: number;
  bottomPanelOpen: boolean;
  bottomPanelHeight: number;
  rightSidebarOpen: boolean;
  rightSidebarWidth: number;
  project: FOSSEEProject | null;
  inProject: boolean;
  scilabStatus: 'connected' | 'disconnected' | 'connecting';
  scilabPid: number | null;
  theme: 'dark' | 'light';
  zoom: number;
  consoleHistory: string[];
  consoleInput: string;
}

type Listener = (s: Store) => void;

let listeners: Listener[] = [];
let store: Store = {
  currentView: 'editor',
  currentTool: 'scilab',
  tabs: [],
  activeTab: null,
  sidebarOpen: true,
  sidebarWidth: 250,
  bottomPanelOpen: false,
  bottomPanelHeight: 200,
  rightSidebarOpen: false,
  rightSidebarWidth: 300,
  project: null,
  inProject: false,
  scilabStatus: 'disconnected',
  scilabPid: null,
  theme: 'dark',
  zoom: 1,
  consoleHistory: [],
  consoleInput: '',
};

const SESSION_KEY = 'fossee-session';

function saveSession() {
  const { tabs, project, inProject, currentView, currentTool, theme, sidebarOpen, sidebarWidth, bottomPanelOpen, bottomPanelHeight, rightSidebarOpen, rightSidebarWidth, zoom, consoleHistory, scilabStatus } = store;
  const data = {
    project, inProject, currentView, currentTool, theme, sidebarOpen, sidebarWidth,
    bottomPanelOpen, bottomPanelHeight, rightSidebarOpen, rightSidebarWidth, zoom, consoleHistory,
    scilabStatus, scilabPid: null,
    tabs: tabs.filter(t => !t.dirty).map(t => ({ ...t, data: { ...t.data, content: undefined } })),
  };
  try { localStorage.setItem(SESSION_KEY, JSON.stringify(data)); } catch {}
}

export function getStore(): Store {
  return store;
}

export function setStore(update: Partial<Store>) {
  store = { ...store, ...update };
  listeners.forEach((l) => l(store));
  saveSession();
}

export function restoreSession(): Partial<Store> | null {
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch { return null; }
}

export function subscribe(listener: Listener) {
  listeners.push(listener);
  return () => {
    listeners = listeners.filter((l) => l !== listener);
  };
}

export function toggleSidebar() {
  setStore({ sidebarOpen: !store.sidebarOpen });
}

export function toggleBottomPanel() {
  setStore({ bottomPanelOpen: !store.bottomPanelOpen });
}

export function toggleRightSidebar() {
  setStore({ rightSidebarOpen: !store.rightSidebarOpen });
}

function emit() {
  listeners.forEach((l) => l(store));
  saveSession();
}

export function openTab(tab: Tab) {
  const existing = store.tabs.find((t) => t.id === tab.id);
  if (!existing) {
    store = { ...store, tabs: [...store.tabs, tab], activeTab: tab.id };
  } else {
    store = { ...store, activeTab: tab.id };
  }
  emit();
}

export function setTabData(tabId: string, data: Record<string, unknown>) {
  store = {
    ...store,
    tabs: store.tabs.map((t) => (t.id === tabId ? { ...t, data: { ...(t.data ?? {}), ...data } } : t)),
  };
  emit();
}

export function setTabDirty(tabId: string, dirty: boolean) {
  store = {
    ...store,
    tabs: store.tabs.map((t) => (t.id === tabId ? { ...t, dirty } : t)),
  };
  emit();
}

export function closeTab(id: string) {
  const idx = store.tabs.findIndex((t) => t.id === id);
  if (idx === -1) return;
  const newTabs = store.tabs.filter((t) => t.id !== id);
  let newActive = store.activeTab;
  if (store.activeTab === id) {
    newActive = newTabs[Math.min(idx, newTabs.length - 1)]?.id ?? null;
  }
  store = { ...store, tabs: newTabs, activeTab: newActive };
  emit();
}

export function resetTabs() {
  store = { ...store, tabs: [], activeTab: null };
  emit();
}

export function switchTool(toolId: FOSSEEToolId) {
  store = { ...store, currentTool: toolId, tabs: [], activeTab: null };
  emit();
}

export function enterProject(project: FOSSEEProject) {
  store = { ...store, project, inProject: true, tabs: [], activeTab: null };
  emit();
}

export function leaveProject() {
  store = { ...store, project: null, inProject: false, tabs: [], activeTab: null };
  emit();
}
