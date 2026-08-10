import { useEffect, useState, type ReactNode } from 'react';
import {
  Blocks,
  ChartColumn,
  ChevronDown,
  ChevronRight,
  Code2,
  File,
  FileSpreadsheet,
  FileText,
  Folder,
  FolderOpen,
  GraduationCap,
  PanelTop,
  Table2,
  X,
} from 'lucide-react';
import { getStore, leaveProject, openTab, setStore, subscribe, switchTool } from '@/store/store';
import { FOSSEE_TOOLS, getTool } from '@/ecosystem/ToolRegistry';
import type { WorkspaceFile } from './types';
import { listDirectory } from '@/lib/fs';

const FILE_ICONS: Record<string, ReactNode> = {
  sce: <Code2 size={14} />,
  sci: <Code2 size={14} />,
  csv: <FileSpreadsheet size={14} />,
  xlsx: <FileSpreadsheet size={14} />,
  xls: <FileSpreadsheet size={14} />,
  pdf: <FileText size={14} />,
};

const MODULE_ICONS: Record<string, ReactNode> = {
  editor: <Code2 size={14} />,
  gui: <Blocks size={14} />,
  viz: <ChartColumn size={14} />,
  data: <Table2 size={14} />,
  report: <FileText size={14} />,
  learn: <GraduationCap size={14} />,
};

function getFileIcon(name: string): ReactNode {
  const ext = name.split('.').pop()?.toLowerCase();
  return ext && ext in FILE_ICONS ? FILE_ICONS[ext] : <File size={14} />;
}

function toWorkspaceFile(entry: { name: string; path: string; is_dir: boolean }): WorkspaceFile {
  return {
    name: entry.name,
    type: entry.is_dir ? 'folder' : 'file',
    path: entry.path,
    children: entry.is_dir ? [] : undefined,
  };
}

async function loadWorkspaceDir(dirPath: string): Promise<WorkspaceFile[]> {
  try {
    const entries = await listDirectory(dirPath);
    return entries.map(toWorkspaceFile);
  } catch {
    return [];
  }
}

interface ToolModule {
  id: string;
  label: string;
}

const TOOL_MODULES: Record<string, ToolModule[]> = {
  scilab: [
    { id: 'editor', label: 'Editor' },
    { id: 'gui', label: 'GUI' },
    { id: 'viz', label: 'Viz' },
    { id: 'data', label: 'Data' },
    { id: 'report', label: 'Report' },
    { id: 'learn', label: 'Learn' },
  ],
  xcos: [
    { id: 'viz', label: 'Model' },
    { id: 'data', label: 'Data' },
    { id: 'report', label: 'Report' },
  ],
  esim: [
    { id: 'viz', label: 'Schematic' },
    { id: 'report', label: 'Report' },
  ],
  openmodelica: [
    { id: 'editor', label: 'Modelica' },
    { id: 'viz', label: 'Simulation' },
    { id: 'data', label: 'Data' },
    { id: 'report', label: 'Report' },
  ],
};

export default function WorkspaceManager() {
  const [, forceUpdate] = useState(0);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [treeData, setTreeData] = useState<Record<string, WorkspaceFile[]>>({});

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  const s = getStore();
  const rootPath = s.project?.path;
  const tool = getTool(s.currentTool);
  const modules = TOOL_MODULES[s.currentTool] ?? [];

  useEffect(() => {
    if (!rootPath) return;
    loadWorkspaceDir(rootPath).then((entries) => {
      setTreeData((prev) => ({ ...prev, [rootPath]: entries }));
    });
  }, [rootPath]);

  if (!s.project || !rootPath) return null;

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
      const children = await loadWorkspaceDir(path);
      setTreeData((prev) => ({ ...prev, [path]: children }));
    }
  };

  const openFile = (name: string, filePath: string) => {
    const ext = name.split('.').pop()?.toLowerCase();
    const moduleMap: Record<string, string> = {
      sce: 'editor',
      sci: 'editor',
      csv: 'data',
      xlsx: 'data',
      xls: 'data',
    };
    const mod = moduleMap[ext ?? ''] ?? 'editor';
    openTab({ id: 'file-' + filePath, title: name, module: mod, data: { filePath } });
    setStore({ currentView: mod });
  };

  const renderNode = (node: WorkspaceFile, depth: number) => {
    const isExpanded = expanded.has(node.path);
    const isFolder = node.type === 'folder';
    const children = isFolder ? (treeData[node.path] ?? node.children ?? []) : [];

    return (
      <div key={node.path}>
        <button
          className="tree-node"
          style={{ paddingLeft: 8 + depth * 14 }}
          onClick={() => isFolder ? toggleExpand(node.path) : openFile(node.name, node.path)}
          title={node.path}
        >
          <span className="tree-caret">
            {isFolder ? (isExpanded ? <ChevronDown size={13} /> : <ChevronRight size={13} />) : null}
          </span>
          <span className="tree-icon">
            {isFolder ? (isExpanded ? <FolderOpen size={14} /> : <Folder size={14} />) : getFileIcon(node.name)}
          </span>
          <span className="tree-name">{node.name}</span>
        </button>
        {isFolder && isExpanded && children.map((child) => renderNode(child, depth + 1))}
      </div>
    );
  };

  return (
    <div className="project-panel">
      <div className="project-panel-header">
        <div className="project-panel-title">
          <PanelTop size={14} />
          <span>{s.project.name}</span>
        </div>
        <button className="icon-btn" onClick={leaveProject} title="Close project" aria-label="Close project">
          <X size={14} />
        </button>
      </div>

      <label className="tool-switcher">
        <span>Runtime</span>
        <select className="tool-select" value={s.currentTool} onChange={(e) => switchTool(e.target.value as any)}>
          {s.project.tools.map((tid) => {
            const t = FOSSEE_TOOLS[tid];
            return <option key={tid} value={tid}>{t?.name ?? tid}</option>;
          })}
        </select>
      </label>

      <div className="module-strip" aria-label={`${tool.name} modules`}>
        {modules.map((m) => (
          <button key={m.id} className={`module-pill ${s.currentView === m.id ? 'active' : ''}`} onClick={() => switchModule(m.id)}>
            {MODULE_ICONS[m.id]}
            <span>{m.label}</span>
          </button>
        ))}
      </div>

      <div className="sidebar-section-title">Files</div>
      <div className="sidebar-tree">
        {(treeData[rootPath] ?? []).map((node) => renderNode(node, 0))}
      </div>
    </div>
  );
}
