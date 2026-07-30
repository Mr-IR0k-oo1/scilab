import { useState, useRef, useEffect, useCallback } from 'react';
import { getStore, subscribe, setTabData, setTabDirty } from '@/store/store';
import { readTextFile, writeTextFile } from '@/lib/fs';
import { startScilab, stopScilab, executeScilabCode } from '@/lib/scilab';
import { updateProjectMetadata } from '@/lib/fs';

export default function ScriptEditor() {
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [running, setRunning] = useState(false);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [fileName, setFileName] = useState('');
  const [filePath, setFilePath] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const outputRef = useRef<HTMLPreElement>(null);
  const codeRef = useRef(code);
  codeRef.current = code;

  useEffect(() => {
    if (outputRef.current) outputRef.current.scrollTop = outputRef.current.scrollHeight;
  }, [output]);

  useEffect(() => {
    const unsub = subscribe(() => {
      const s = getStore();
      const activeTab = s.tabs.find((t) => t.id === s.activeTab);
      if (activeTab && activeTab.module === 'editor') {
        const fp = activeTab.data?.filePath as string | undefined;
        if (fp && fp !== filePath) {
          setFileName(activeTab.title);
          setFilePath(fp);
          loadFile(fp);
        } else if (!fp && !filePath) {
          setFileName(activeTab.title);
          setCode(typeof activeTab.data?.content === 'string' ? activeTab.data.content : '');
        }
      }
    });
    return unsub;
  }, [filePath]);

  const loadFile = async (fp: string) => {
    setLoading(true);
    try {
      const content = await readTextFile(fp);
      setCode(content);
      setTabData('file-' + fp, { content });
    } catch {
      setCode('// Error loading file\n');
    }
    setLoading(false);
  };

  const handleChange = (value: string) => {
    setCode(value);
    const s = getStore();
    if (s.activeTab) {
      setTabDirty(s.activeTab, true);
    }
  };

  const handleSave = useCallback(async () => {
    if (!filePath) return;
    setSaving(true);
    try {
      await writeTextFile(filePath, codeRef.current);
      if (getStore().activeTab) {
        setTabDirty(getStore().activeTab!, false);
      }
      const s = getStore();
      if (s.project) {
        updateProjectMetadata(s.project.name).catch(() => {});
      }
    } catch (e) {
      setOutput((prev) => prev + `> Save failed: ${e}\n`);
    }
    setSaving(false);
  }, [filePath]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        handleSave();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [handleSave]);

  const log = (msg: string) => setOutput((prev) => prev + msg + '\n');

  const handleStart = async () => {
    try {
      await startScilab();
      log('> Scilab started');
    } catch (e) {
      log(`> ${e}`);
    }
  };

  const handleStop = async () => {
    try {
      await stopScilab();
      log('> Scilab stopped');
    } catch {
      log('> Failed to stop Scilab');
    }
  };

  const handleRun = async () => {
    const s = getStore();
    if (s.scilabStatus !== 'connected') {
      log('> Scilab is not running. Start it first.');
      return;
    }
    setRunning(true);
    log('> Executing...');
    try {
      const result = await executeScilabCode(code);
      if (result.output) log(result.output);
      if (result.error) log(`> Error: ${result.error}`);
    } catch (e) {
      log(`> Execution failed: ${e}`);
    }
    setRunning(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleRun();
    }
    if (e.key === 'Tab') {
      e.preventDefault();
      const ta = textareaRef.current;
      if (ta) {
        const start = ta.selectionStart;
        const end = ta.selectionEnd;
        setCode(code.substring(0, start) + '  ' + code.substring(end));
        setTimeout(() => { ta.selectionStart = ta.selectionEnd = start + 2; }, 0);
      }
    }
  };

  const clearOutput = () => setOutput('');

  return (
    <div className="script-editor">
      <div className="editor-toolbar">
        <span className="editor-filename" title={filePath ?? undefined}>
          {fileName || 'Untitled'}
          {getStore().tabs.find((t) => t.id === getStore().activeTab)?.dirty ? ' ●' : ''}
        </span>
        <span className="toolbar-separator" />
        <button className="toolbar-btn" onClick={handleSave} disabled={saving || !filePath}>
          {saving ? 'Saving...' : 'Save (Ctrl+S)'}
        </button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn" onClick={handleStart} disabled={getStore().scilabStatus === 'connected'}>Start Scilab</button>
        <button className="toolbar-btn" onClick={handleStop} disabled={getStore().scilabStatus !== 'connected'}>Stop</button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn run-btn" onClick={handleRun} disabled={running || getStore().scilabStatus !== 'connected'}>
          {running ? 'Running...' : 'Run (Ctrl+Enter)'}
        </button>
        <div className="toolbar-separator" />
        <button className="toolbar-btn" onClick={clearOutput}>Clear Output</button>
        <span className="toolbar-spacer" />
        {loading && <span className="status-indicator">Loading...</span>}
        {getStore().scilabPid && <span className="status-indicator running">PID {getStore().scilabPid}</span>}
        {getStore().scilabStatus !== 'connected' && <span className="status-indicator stopped">Disconnected</span>}
      </div>
      <div className="editor-panels">
        <div className="code-panel">
          <textarea
            ref={textareaRef}
            className="code-textarea"
            value={code}
            onChange={(e) => handleChange(e.target.value)}
            onKeyDown={handleKeyDown}
            spellCheck={false}
          />
        </div>
        <div className="output-panel">
          <div className="output-header">Output</div>
          <pre ref={outputRef} className="output-content">{output || 'Output will appear here'}</pre>
        </div>
      </div>
    </div>
  );
}
