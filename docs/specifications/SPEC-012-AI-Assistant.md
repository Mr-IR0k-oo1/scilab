# SPEC-012 — AI Assistant

## Purpose

Provide context-aware coding assistance within Scilab Studio. Help users write Scilab code, understand errors, and learn best practices.

---

## Capabilities

### Code Completion
- Suggest function names, variable names, keywords.
- Context-aware: knows which functions are available in the current Scilab version.
- Shows function signatures and parameter hints.

### Error Explanation
- When Scilab returns an error, the AI explains what went wrong.
- Suggests fixes based on the error message and code context.
- Links to relevant documentation.

### Code Generation
- Generate Scilab code from natural language descriptions.
- Generate boilerplate code (loops, functions, GUI layouts).
- Generate test cases for user functions.

### Documentation
- Auto-generate function documentation from code.
- Explain what existing code does (inline comments).
- Suggest variable names and code structure improvements.

### Learning
- Answer questions about Scilab syntax and functions.
- Explain engineering concepts in context.
- Suggest next steps based on what the user is building.

---

## Interaction Model

### Inline Suggestions
- As the user types, suggestions appear as ghost text.
- Press Tab to accept, Escape to dismiss.
- Arrow keys to cycle through suggestions.

### Chat Panel
- Side panel for conversational interaction.
- User asks questions, AI responds with code and explanations.
- Code blocks can be inserted directly into the editor.
- Conversation history preserved per project.

### Error Inline
- When an error occurs, an inline message appears below the error line.
- "Explain" button opens the AI chat with the error context.
- "Fix" button applies the suggested fix (with user confirmation).

---

## Context Sources

| Source | How Used |
|--------|----------|
| Current file | Code context for completions and explanations |
| Open files | Cross-file references |
| Scilab version | Available functions and syntax |
| Project settings | Module-specific knowledge |
| Error history | Pattern detection |
| User coding style | Personalized suggestions |

---

## Privacy

- All AI processing happens locally on the user's machine.
- No code is sent to external servers.
- No telemetry or usage tracking.
- AI models are bundled with the application (or downloaded separately with explicit consent).

---

## Model

### Local Model (v0.3)
- Small language model bundled with the application.
- Runs on CPU (no GPU required).
- Optimized for Scilab-specific completions.
- ~500MB download.

### Enhanced Model (v0.4)
- Larger model with better understanding.
- Optional GPU acceleration.
- ~2GB download.
- User choice: local (private) vs enhanced (better quality).

---

## Configuration

```jsonc
{
  "ai": {
    "enabled": true,
    "model": "local",              // "local" | "enhanced" | "off"
    "suggestions": true,           // Inline code completions
    "errorExplanation": true,      // Explain errors inline
    "codeGeneration": true,        // Natural language → code
    "chatHistory": true,           // Preserve conversation per project
    "maxTokens": 500,              // Max tokens per suggestion
    "temperature": 0.3             // Creativity level (0–1)
  }
}
```

---

## UI

### Inline Suggestions
- Ghost text in editor (dimmed, semi-transparent).
- Tab to accept, Escape to dismiss.
- Up/Down to cycle alternatives.
- Ctrl+Space to trigger manually.

### Chat Panel
- Toggle with Ctrl+Shift+A / Cmd+Shift+A.
- Split view: editor on left, chat on right.
- Messages with code blocks.
- "Insert" button to add code to editor.
- "Copy" button for code blocks.
- Clear conversation button.

### Error Inline
- Appears below error line in editor.
- Yellow warning background.
- "Explain" and "Fix" buttons.
- Dismissable.

---

## Constraints

| Constraint | Value |
|------------|-------|
| Local model size | ~500MB |
| Suggestion latency | < 500ms |
| Chat response latency | < 2s |
| Max conversation history | 100 messages |
| Max code context | 10,000 tokens |
| GPU requirement | None (CPU only for local model) |

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| Model not downloaded | Show download prompt, disable AI features |
| Model load fails | Show error, fall back to basic completions |
| Suggestion timeout | Show "AI busy" indicator, continue without |
| Model out of memory | Reduce context window, retry |
| Invalid suggestion | User dismisses, no side effects |

---

## Extension Points

- Custom AI models (user-provided).
- Custom completion sources.
- Custom chat plugins.
- Integration with external AI services (opt-in).
- Domain-specific models (control systems, signal processing).
