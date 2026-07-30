import { useState, useRef, useEffect } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const WELCOME_MSG = 'Ask me anything about Scilab — syntax, plotting, data analysis, or debugging.';

const RESPONSES: Record<string, string> = {
  plot: 'Use `plot(x, y)` for 2D line plots. Add `scatter(x, y)` for scatter points. Customize with `title()`, `xlabel()`, `ylabel()`, and `legend()`.',
  matrix: 'Create matrices with `zeros(m,n)`, `ones(m,n)`, `rand(m,n)`, or `eye(n)`. Index with `A(i,j)`. Use `size(A)` to get dimensions.',
  csv: 'Import CSV data with `csvRead("file.csv")`. Returns a matrix. Use `csvWrite(data, "out.csv")` to export.',
  fft: 'Compute FFT with `fft(signal)`. Get frequency axis: `f = (0:N-1)*(fs/N)`. Plot magnitude with `plot(f, abs(fft(signal)))`.',
  ode: 'Solve ODEs with `ode(y0, t0, t, f)`. Define a function for the derivative: `function dy = f(t, y)`. Returns solution matrix.',
  filter: 'Design filters with `filter(b, a, signal)` for IIR/FIR. Use `ffilt()` for frequency sampling. Check `help filter` for details.',
  gui: 'Build GUIs with `uicontrol()`. Create figure: `f = figure()`. Add button: `uicontrol(f, "style", "pushbutton", "string", "Click")`.',
  stats: 'Compute `mean(x)`, `median(x)`, `stdev(x)`, `corr(x,y)`, `reglin(x,y)` for linear regression.',
};

function generateResponse(input: string): string {
  const lower = input.toLowerCase();
  for (const [key, resp] of Object.entries(RESPONSES)) {
    if (lower.includes(key)) return resp;
  }
  if (lower.includes('hello') || lower.includes('hi')) return 'Hello! How can I help you with Scilab today?';
  if (lower.includes('thank')) return "You're welcome! Let me know if you need anything else.";
  if (lower.includes('help') || lower.includes('?')) return 'I can help with: plotting, matrices, CSV import/export, FFT, ODE solving, filter design, GUI building, and statistics. Try asking about any of these!';
  return `I'm not sure about "${input}". Try asking about: plot, matrix, csv, fft, ode, filter, gui, or stats.`;
}

export default function Assistant() {
  const [messages, setMessages] = useState<Message[]>([{ role: 'assistant', content: WELCOME_MSG }]);
  const [input, setInput] = useState('');
  const [thinking, setThinking] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, thinking]);

  const send = () => {
    const text = input.trim();
    if (!text) return;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: text }]);
    setThinking(true);
    setTimeout(() => {
      setMessages((prev) => [...prev, { role: 'assistant', content: generateResponse(text) }]);
      setThinking(false);
    }, 600 + Math.random() * 600);
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  };

  return (
    <div className="assistant-panel">
      <div className="assistant-header">
        <span className="assistant-logo">G</span>
        Grok Assistant
      </div>
      <div className="assistant-messages">
        {messages.length === 1 && (
          <div className="assistant-empty">
            <div className="assistant-empty-icon">+</div>
            <h3>Scilab Assistant</h3>
            <p>Ask about plotting, matrices, data import, signal processing, or anything Scilab-related.</p>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`assistant-msg ${m.role}`}>
            <div className="assistant-msg-avatar">{m.role === 'assistant' ? 'G' : 'U'}</div>
            <div className="assistant-msg-bubble">
              {m.content.split('\n').map((p, j) => (
                p.startsWith('  ') || p.startsWith('`') ? (
                  <pre key={j}><code>{p}</code></pre>
                ) : (
                  <p key={j}>{p}</p>
                )
              ))}
            </div>
          </div>
        ))}
        {thinking && (
          <div className="assistant-msg assistant">
            <div className="assistant-msg-avatar">G</div>
            <div className="assistant-msg-bubble" style={{ opacity: 0.6 }}>Thinking...</div>
          </div>
        )}
        <div ref={endRef} />
      </div>
      <div className="assistant-input-area">
        <textarea
          className="assistant-input"
          placeholder="Ask about Scilab..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          rows={1}
        />
        <button className="assistant-send-btn" onClick={send} disabled={!input.trim() || thinking}>→</button>
      </div>
    </div>
  );
}
