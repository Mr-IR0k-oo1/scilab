interface CodePanelProps {
  code: string;
}

export default function CodePanel({ code }: CodePanelProps) {
  return (
    <div className="code-panel-view">
      <div className="code-panel-header">Generated Scilab Code</div>
      <pre className="code-panel-content">{code}</pre>
      <div className="code-panel-actions">
        <button className="toolbar-btn" onClick={() => navigator.clipboard.writeText(code)}>
          Copy Code
        </button>
      </div>
    </div>
  );
}
