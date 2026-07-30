type ConfigValue = string | number | boolean | object;
type ConfigChangeListener = (key: string, value: any) => void;

export class Configuration {
  private store = new Map<string, ConfigValue>();
  private listeners = new Map<string, Set<ConfigChangeListener>>();

  get<T>(key: string): T | undefined {
    return this.store.get(key) as T | undefined;
  }

  set(key: string, value: ConfigValue): void {
    const old = this.store.get(key);
    this.store.set(key, value);

    if (old !== value) {
      this.notify(key, value);
    }
  }

  has(key: string): boolean {
    return this.store.has(key);
  }

  delete(key: string): void {
    this.store.delete(key);
  }

  onDidChange(key: string, handler: ConfigChangeListener): { dispose(): void } {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }
    this.listeners.get(key)!.add(handler);

    return {
      dispose: () => {
        this.listeners.get(key)?.delete(handler);
      }
    };
  }

  private notify(key: string, value: any): void {
    const handlers = this.listeners.get(key);
    if (handlers) {
      for (const handler of handlers) {
        try {
          handler(key, value);
        } catch (error) {
          console.error(`Config listener error for "${key}":`, error);
        }
      }
    }
  }

  load(data: Record<string, any>): void {
    for (const [key, value] of Object.entries(data)) {
      this.store.set(key, value);
    }
  }

  toJSON(): Record<string, any> {
    const result: Record<string, any> = {};
    for (const [key, value] of this.store) {
      result[key] = value;
    }
    return result;
  }
}
