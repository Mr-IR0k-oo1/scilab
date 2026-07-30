import { useState, useEffect, type ReactNode } from 'react';
import { getStore, subscribe, setStore, switchTool, leaveProject, openTab } from '@/store/store';
import { getTool, FOSSEE_TOOLS } from '@/ecosystem/ToolRegistry';
import type { WorkspaceFile } from './types';
import { CodeRed, Csv, Document, PDF, Folder, FolderOpen } from '@react-symbols/icons';
import { listDirectory } from '@/lib/fs';

const FILE_ICONS: Record<string, ReactNode> = {
  sce: <CodeRed width={14} height={14} />,
  sci: <CodeRed width={14} height={14} />,
  csv: <Csv width={14} height={14} />,
  xlsx: <Document width={14} height={14} />,
  xls: <Document width={14} height={14} />,
  pdf: <PDF width={14} height={14} />,
};

function getFileIcon(name: string): ReactNode {
  const ext = name.split('.').pop()?.toLowerCase();
  return ext && ext in FILE_ICONS ? FILE_ICONS[ext] : <Document width={14} height={14} />;
}

function toWorkspaceFile(entry: { name: string; path: string; is_dir: boolean }): WorkspaceFile {
  return {
    name: entry.name,
    type: entry.is_dir ? 'folder' : 'file',
    path: entry.path,
    children: entry.is_dir ? [] : undefined,
  };
}

interface ToolModule {
  id: string;
  label: string;
  icon: string;
}

const TOOL_MODULES: Record<string, ToolModule[]> = {
  scilab: [
    { id: 'editor', label: 'Editor', icon: '<>' },
    { id: 'gui', label: 'GUI', icon: '▣' },
    { id: 'viz', label: 'Viz', icon: '◈' },
    { id: 'data', label: 'Data', icon: '≡' },
    { id: 'report', label: 'Report', icon: '▤' },
    { id: 'learn', label: 'Learn', icon: '⌘' },
  ],
  xcos: [
    { id: 'viz', label: 'Model', icon: '◈' },
    { id: 'data', label: 'Data', icon: '≡' },
    { id: 'report', label: 'Report', icon: '▤' },
  ],
  esim: [
    { id: 'viz', label: 'Schematic', icon: '◎' },
    { id: 'report', label: 'Report', icon: '▤' },
  ],
  openmodelica: [
    { id: 'editor', label: 'Modelica', icon: '<>' },
    { id: 'viz', label: 'Simulation', icon: '◈' },
    { id: 'data', label: 'Data', icon: '≡' },
    { id: 'report', label: 'Report', icon: '▤' },
  ],
};

export default function WorkspaceManager() {
  const [, forceUpdate] = useState(0);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [treeData, setTreeData] = useState<Record<string, WorkspaceFile[]>>({});

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const s = getStore();
  if (!s.project) return null;

  const rootPath = s.project.path;
  const tool = getTool(s.currentTool);
  const modules = TOOL_MODULES[s.currentTool] ?? [];

  useEffect(() => {
    if (!rootPath) return;
    loadDir(rootPath).then((entries) => {
      setTreeData((prev) => ({ ...prev, [rootPath]: entries }));
    });
  }, [rootPath]);

  const loadDir = async (dirPath: string): Promise<WorkspaceFile[]> => {
    try {
      const entries = await listDirectory(dirPath);
      return entries.map(toWorkspaceFile);
    } catch {
      return [];
    }
  };

  const switchModule = (id: string) => {
    const mod = modules.find((m) => m.id === id);
    openTab({ id, title: mod?.label ?? id, module: id });
    setStore({ currentView: id });
  };

  const toggleExpand = async (path: string) => {
    const next = new Set(expanded);
    if (next.has(path)) {
      next.delete(path);
      setExpanded(next);
      return;
    }
    next.add(path);
    setExpanded(next);

    if (!treeData[path]) {
      const children = await loadDir(path);
      setTreeData((prev) => ({ ...prev, [path]: children }));
    }
  };

  const renderNode = (node: WorkspaceFile, depth: number) => {
    const isExpanded = expanded.has(node.path);
    const isFolder = node.type === 'folder';
    const name = node.name;
    const ext = name.split('.').pop()?.toLowerCase();
    const children = isFolder ? (treeData[node.path] ?? node.children ?? []) : [];
    return (
      <div key={node.path}>
        <div
          className="tree-node"
          style={{ paddingLeft: 8 + depth * 16 }}
          onClick={() => isFolder ? toggleExpand(node.path) : openFile(name, node.path)}
        >
          <span className="tree-icon">
            {isFolder
              ? (isExpanded ? <FolderOpen width={14} height={14} /> : <Folder width={14} height={14} />)
              : getFileIcon(name)}
          </span>
          <span className="tree-name">{name}</span>
        </div>
        {isFolder && isExpanded && children.map((child) => renderNode(child, depth + 1))}
      </div>
    );
  };

  const openFile = (name: string, filePath: string) => {
    const ext = name.split('.').pop()?.toLowerCase();
    const moduleMap: Record<string, string> = {
      sce: 'editor', sci: 'editor', csv: 'data', xlsx: 'data', xls: 'data',
    };
    const mod = moduleMap[ext ?? ''] ?? 'editor';
    openTab({ id: 'file-' + filePath, title: name, module: mod, data: { filePath } });
    setStore({ currentView: mod });
  };

  const handleSwitchTool = (e: React.ChangeEvent<HTMLSelectElement>) => {
    switchTool(e.target.value as any);
  };

  return (
    <div className="sidebar">
      <div className="sidebar-section">
        <div className="sidebar-header" style={{ padding: '8px 12px', display: 'flex', flexDirection: 'column', gap: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <h3 style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              {s.project.name}
            </h3>
            <button className="icon-btn" onClick={leaveProject} title="Close Project">×</button>
          </div>
          <select
            className="tool-select"
            value={s.currentTool}
            onChange={handleSwitchTool}
            style={{
              width: '100%', padding: '4px 8px', background: 'var(--bg-app)',
              color: 'var(--text)', border: '1px solid var(--border)',
              borderRadius: 'var(--radius)', fontSize: 12, outline: 'none',
            }}
          >
            {s.project.tools.map((tid) => {
              const t = FOSSEE_TOOLS[tid];
              return <option key={tid} value={tid}>{t?.name ?? tid}</option>;
            })}
          </select>
        </div>
      </div>

      <div className="sidebar-tabs" style={{ display: 'flex', borderBottom: '1px solid var(--border)' }}>
        {modules.map((m) => (
          <button
            key={m.id}
            className="sidebar-tab"
            style={{
              flex: 1, padding: '6px 8px', background: 'none', border: 'none',
              borderBottom: `2px solid ${s.currentView === m.id ? 'var(--accent)' : 'transparent'}`,
              color: s.currentView === m.id ? 'var(--accent)' : 'var(--text-muted)',
              fontSize: 11, fontWeight: 500, cursor: 'pointer', textAlign: 'center',
            }}
            onClick={() => switchModule(m.id)}
          >
            {m.icon} {m.label}
          </button>
        ))}
      </div>

      <div className="sidebar-tree">
        {(treeData[rootPath] ?? []).map((node) => renderNode(node, 0))}
      </div>
    </div>
  );
}
