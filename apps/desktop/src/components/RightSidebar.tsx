import { getStore } from '@/store/store';

export default function RightSidebar() {
  const s = getStore();

  const moduleInfo: Record<string, { label: string; desc: string; icon: string }> = {
    editor: { label: 'Script Editor', desc: 'Write and execute Scilab scripts (.sce, .sci)', icon: '<>' },
    gui: { label: 'GUI Builder', desc: 'Design Scilab GUIs with drag-and-drop widgets', icon: '▣' },
    viz: { label: 'Visualization', desc: 'Create charts and plots from data', icon: '◈' },
    data: { label: 'Data Studio', desc: 'Import, preview, transform, and analyze data', icon: '≡' },
    report: { label: 'Report Generator', desc: 'Create formatted reports with charts and tables', icon: '▤' },
    learn: { label: 'Learning Center', desc: 'Tutorials, examples, and Scilab reference', icon: '⌘' },
  };

  const info = moduleInfo[s.currentView];

  return (
    <div className="sidebar-right-content" style={{ padding: 12 }}>
      {info && (
        <div style={{ marginBottom: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
            <span style={{ fontSize: 18, opacity: 0.7 }}>{info.icon}</span>
            <h3 style={{ fontSize: 13, fontWeight: 600 }}>{info.label}</h3>
          </div>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>{info.desc}</p>
        </div>
      )}

      <div style={{ borderTop: '1px solid var(--border)', paddingTop: 12 }}>
        <h4 style={{ fontSize: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5, color: 'var(--text-muted)', marginBottom: 8 }}>
          Shortcuts
        </h4>
        {[
          { key: 'Ctrl+B', label: 'Toggle Sidebar' },
          { key: 'Ctrl+J', label: 'Toggle Bottom Panel' },
          { key: 'Ctrl+Enter', label: 'Run Script' },
          { key: 'Ctrl+Tab', label: 'Switch Tab' },
        ].map((sc) => (
          <div key={sc.key} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '3px 0', fontSize: 11 }}>
            <span style={{ color: 'var(--text-secondary)' }}>{sc.label}</span>
            <kbd style={{ padding: '1px 5px', background: 'var(--bg-alt)', border: '1px solid var(--border)', borderRadius: 3, fontSize: 10, color: 'var(--text-muted)' }}>{sc.key}</kbd>
          </div>
        ))}
      </div>

      {s.project && (
        <div style={{ borderTop: '1px solid var(--border)', paddingTop: 12, marginTop: 12 }}>
          <h4 style={{ fontSize: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 0.5, color: 'var(--text-muted)', marginBottom: 8 }}>
            Project
          </h4>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0' }}>
              <span>Name</span>
              <span style={{ color: 'var(--text)' }}>{s.project.name}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '2px 0' }}>
              <span>Tools</span>
              <span style={{ color: 'var(--text)' }}>{s.project.tools.length}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
