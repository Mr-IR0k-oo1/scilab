export interface Command {
  id: string;
  label: string;
  category: string;
  execute: (...args: any[]) => Promise<any> | any;
  undo?: (...args: any[]) => Promise<any> | any;
}

interface HistoryEntry {
  commandId: string;
  args: any[];
  result: any;
}

export class CommandSystem {
  private commands = new Map<string, Command>();
  private history: HistoryEntry[] = [];
  private historyIndex = -1;
  private maxHistory = 100;

  register(command: Command): void {
    this.commands.set(command.id, command);
  }

  get(id: string): Command | undefined {
    return this.commands.get(id);
  }

  getAll(): Command[] {
    return Array.from(this.commands.values());
  }

  async execute(id: string, ...args: any[]): Promise<any> {
    const command = this.commands.get(id);
    if (!command) {
      throw new Error(`Command not found: ${id}`);
    }

    const result = await command.execute(...args);

    if (command.undo) {
      this.history.splice(this.historyIndex + 1);
      this.history.push({ commandId: id, args, result });
      if (this.history.length > this.maxHistory) {
        this.history.shift();
      }
      this.historyIndex = this.history.length - 1;
    }

    return result;
  }

  async undo(): Promise<void> {
    if (this.historyIndex < 0) return;

    const entry = this.history[this.historyIndex];
    const command = this.commands.get(entry.commandId);

    if (command?.undo) {
      await command.undo(...entry.args);
    }

    this.historyIndex--;
  }

  async redo(): Promise<void> {
    if (this.historyIndex >= this.history.length - 1) return;

    this.historyIndex++;
    const entry = this.history[this.historyIndex];
    const command = this.commands.get(entry.commandId);

    if (command) {
      await command.execute(...entry.args);
    }
  }

  canUndo(): boolean {
    return this.historyIndex >= 0;
  }

  canRedo(): boolean {
    return this.historyIndex < this.history.length - 1;
  }
}
