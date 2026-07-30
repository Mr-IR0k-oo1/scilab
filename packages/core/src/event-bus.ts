export type EventHandler = (data: any) => void;

export interface Disposable {
  dispose(): void;
}

export class EventBus {
  private handlers = new Map<string, Set<EventHandler>>();

  on(event: string, handler: EventHandler): Disposable {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);

    return {
      dispose: () => {
        this.handlers.get(event)?.delete(handler);
      }
    };
  }

  emit(event: string, data?: any): void {
    const handlers = this.handlers.get(event);
    if (handlers) {
      for (const handler of handlers) {
        try {
          handler(data);
        } catch (error) {
          console.error(`Event handler error for "${event}":`, error);
        }
      }
    }
  }

  off(event: string, handler: EventHandler): void {
    this.handlers.get(event)?.delete(handler);
  }

  removeAll(): void {
    this.handlers.clear();
  }
}
