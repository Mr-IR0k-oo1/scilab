import { useState, useEffect, useCallback, useRef, type ReactNode } from 'react';
import { setStore, openTab, subscribe, getStore } from '@/store/store';
import { CodeRed, Csv, Document, PDF, Folder, FolderOpen } from '@react-symbols/icons';
import { listDirectory, createDirectory, removeFile, removeDirectory, renamePath } from '@/lib/fs';

interface FileNode {
  name: string;
  type: 'file' | 'folder';
  children?: FileNode[];
  path: string;
}

interface ContextMenu {
  x: number;
  y: number;
  node: FileNode;
}

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

interface SidebarProps {
  onOpenFile?: (path: string) => void;
}

function toFileNode(entry: { name: string; path: string; is_dir: boolean }): FileNode {
  return {
    name: entry.name,
    type: entry.is_dir ? 'folder' : 'file',
    path: entry.path,
    children: entry.is_dir ? [] : undefined,
  };
}

export default function Sidebar({ onOpenFile }: SidebarProps) {
  const [, forceUpdate] = useState(0);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [sidebarTab, setSidebarTab] = useState<'explorer' | 'search'>('explorer');
  const [searchQuery, setSearchQuery] = useState('');
  const [treeData, setTreeData] = useState<Record<string, FileNode[]>>({});
  const [ctxMenu, setCtxMenu] = useState<ContextMenu | null>(null);
  const [renaming, setRenaming] = useState<string | null>(null);
  const renameRef = useRef<HTMLInputElement>(null);
  const contextRef = useRef<HTMLDivElement>(null);

  useEffect(() => subscribe(() => forceUpdate((n) => n + 1)), []);

  useEffect(() => {
    const onClick = () => setCtxMenu(null);
    window.addEventListener('click', onClick);
    return () => window.removeEventListener('click', onClick);
  }, []);

  useEffect(() => {
    if (renaming && renameRef.current) {
      renameRef.current.focus();
      renameRef.current.select();
    }
  }, [renaming]);

  const s = getStore();
  const rootPath = s.inProject && s.project ? s.project.path : null;

  useEffect(() => {
    if (!rootPath) {
      setTreeData({});
      return;
    }
    loadDir(rootPath).then((entries) => {
      setTreeData((prev) => ({ ...prev, [rootPath]: entries }));
    });
  }, [rootPath]);

  const loadDir = async (dirPath: string): Promise<FileNode[]> => {
    try {
      const entries = await listDirectory(dirPath);
      return entries.map(toFileNode);
    } catch {
      return [];
    }
  };

  const refreshPath = async (path: string) => {
    const entries = await loadDir(path);
    setTreeData((prev) => ({ ...prev, [path]: entries }));
    const parent = path.substring(0, path.lastIndexOf('/'));
    if (parent && treeData[parent]) {
      const parentEntries = await loadDir(parent);
      setTreeData((prev) => ({ ...prev, [parent]: parentEntries }));
    }
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

  const openFile = (node: FileNode) => {
    onOpenFile?.(node.path);
    const ext = node.name.split('.').pop()?.toLowerCase();
    const moduleMap: Record<string, string> = {
      sce: 'editor', sci: 'editor', csv: 'data', xlsx: 'data', xls: 'data',
    };
    const mod = moduleMap[ext ?? ''] ?? 'editor';
    openTab({ id: 'file-' + node.path, title: node.name, module: mod, data: { filePath: node.path } });
    setStore({ currentView: mod as any });
  };

  const handleCtxMenu = (e: React.MouseEvent, node: FileNode) => {
    e.preventDefault();
    e.stopPropagation();
    setCtxMenu({ x: e.clientX, y: e.clientY, node });
  };

  const handleRenameSubmit = async (node: FileNode) => {
    if (!renaming) return;
    const newName = renaming.trim();
    setRenaming(null);
    if (!newName || newName === node.name) return;
    const parent = node.path.substring(0, node.path.lastIndexOf('/'));
    const newPath = parent + '/' + newName;
    try {
      await renamePath(node.path, newPath);
      const dir = node.type === 'folder' ? node.path : parent;
      await refreshPath(dir);
    } catch {}
  };

  const handleDelete = async (node: FileNode) => {
    setCtxMenu(null);
    const msg = `Delete "${node.name}"?`;
    if (!confirm(msg)) return;
    try {
      if (node.type === 'folder') {
        await removeDirectory(node.path);
      } else {
        await removeFile(node.path);
      }
      const parent = node.path.substring(0, node.path.lastIndexOf('/'));
      await refreshPath(parent);
    } catch {}
  };

  const handleNewFile = async (parentPath: string) => {
    setCtxMenu(null);
    const name = prompt('File name:');
    if (!name) return;
    const fullPath = parentPath + '/' + name;
    try {
      await import('@/lib/fs').then(m => m.writeTextFile(fullPath, ''));
      await refreshPath(parentPath);
    } catch {}
  };

  const handleNewFolder = async (parentPath: string) => {
    setCtxMenu(null);
    const name = prompt('Folder name:');
    if (!name) return;
    const fullPath = parentPath + '/' + name;
    try {
      await createDirectory(fullPath);
      await refreshPath(parentPath);
    } catch {}
  };

  const getParentPath = (path: string): string => {
    if (rootPath && path === rootPath) return rootPath;
    return path.substring(0, path.lastIndexOf('/'));
  };

  const renderNode = (node: FileNode, depth: number) => {
    const isExpanded = expanded.has(node.path);
    const hasChildren = node.type === 'folder';
    const children = hasChildren ? (treeData[node.path] ?? node.children ?? []) : [];
    const isRenaming = renaming === node.path;

    return (
      <div key={node.path}>
        <div
          className={`tree-node ${node.type}`}
          style={{ paddingLeft: 8 + depth * 16 }}
          onClick={() => hasChildren ? toggleExpand(node.path) : openFile(node)}
          onContextMenu={(e) => handleCtxMenu(e, node)}
        >
          <span className="tree-icon">
            {hasChildren
              ? (isExpanded ? <FolderOpen width={14} height={14} /> : <Folder width={14} height={14} />)
              : getFileIcon(node.name)}
          </span>
          {isRenaming ? (
            <input
              ref={renameRef}
              className="rename-input"
              defaultValue={node.name}
              onBlur={() => { setRenaming(null); }}
              onKeyDown={(e) => {
                if (e.key === 'Enter') { handleRenameSubmit(node); }
                if (e.key === 'Escape') { setRenaming(null); }
                e.stopPropagation();
              }}
              onClick={(e) => e.stopPropagation()}
            />
          ) : (
            <span className="tree-name">{node.name}</span>
          )}
        </div>
        {hasChildren && isExpanded && children.map((child) => renderNode(child, depth + 1))}
      </div>
    );
  };

  const flattenFiles = (nodes: FileNode[]): FileNode[] =>
    nodes.flatMap((n) => (n.type === 'folder' ? flattenFiles(n.children ?? []) : [n]));

  const rootNodes = rootPath ? treeData[rootPath] ?? [] : [];

  const allFiles = Object.values(treeData).flat();
  const searchResults = searchQuery
    ? flattenFiles(allFiles).filter((f) => f.name.toLowerCase().includes(searchQuery.toLowerCase()))
    : [];

  return (
    <aside className="sidebar">
      <div className="sidebar-tabs">
        <button className={`sidebar-tab ${sidebarTab === 'explorer' ? 'active' : ''}`} onClick={() => setSidebarTab('explorer')}>
          Explorer
        </button>
        <button className={`sidebar-tab ${sidebarTab === 'search' ? 'active' : ''}`} onClick={() => setSidebarTab('search')}>
          Search
        </button>
      </div>
      {sidebarTab === 'explorer' ? (
        <div className="sidebar-section">
          <div className="sidebar-header">
            <h3>Project Files</h3>
            <button className="icon-btn" title="New File" onClick={() => {
              const name = prompt('File name:');
              if (name && rootPath) {
                (async () => {
                  const fp = rootPath + '/' + name;
                  await import('@/lib/fs').then(m => m.writeTextFile(fp, ''));
                  await refreshPath(rootPath);
                  openTab({ id: 'file-' + fp, title: name, module: 'editor', data: { filePath: fp } });
                  setStore({ currentView: 'editor' });
                })();
              }
            }}>+</button>
          </div>
          <div className="sidebar-tree">
            {!rootPath ? (
              <div className="tree-empty">No project open</div>
            ) : rootNodes.length === 0 ? (
              <div className="tree-empty">Empty project</div>
            ) : (
              rootNodes.map((node) => renderNode(node, 0))
            )}
          </div>
        </div>
      ) : (
        <div className="sidebar-section">
          <h3>Search Files</h3>
          <div className="search-box">
            <input className="search-input" placeholder="Search files..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
          </div>
          {searchQuery && (
            <div className="sidebar-tree">
              {searchResults.length === 0 && <div className="tree-empty">No results</div>}
              {searchResults.map((f) => (
                <div key={f.path} className="tree-node file" onClick={() => openFile(f)}>
                  <span className="tree-icon">{getFileIcon(f.name)}</span>
                  <span className="tree-name">{f.name}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {ctxMenu && (
        <div
          ref={contextRef}
          className="context-menu"
          style={{ left: ctxMenu.x, top: ctxMenu.y, position: 'fixed' }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="context-menu-item" onClick={() => { setRenaming(ctxMenu.node.path); setCtxMenu(null); }}>Rename</div>
          <div className="context-menu-separator" />
          <div className="context-menu-item" onClick={() => handleNewFile(ctxMenu.node.type === 'folder' ? ctxMenu.node.path : getParentPath(ctxMenu.node.path))}>New File</div>
          <div className="context-menu-item" onClick={() => handleNewFolder(ctxMenu.node.type === 'folder' ? ctxMenu.node.path : getParentPath(ctxMenu.node.path))}>New Folder</div>
          <div className="context-menu-separator" />
          <div className="context-menu-item danger" onClick={() => handleDelete(ctxMenu.node)}>Delete</div>
        </div>
      )}
    </aside>
  );
}
