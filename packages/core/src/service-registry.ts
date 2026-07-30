import { Logger } from './logger.js';

export type ServiceState = 'registered' | 'initialized' | 'started' | 'stopped' | 'disposed';

export interface Service {
  readonly id: string;
  initialize(): Promise<void>;
  start(): Promise<void>;
  stop(): Promise<void>;
  dispose(): Promise<void>;
}

const logger = new Logger('service-registry');

export class ServiceRegistry {
  private services = new Map<string, Service>();
  private state = new Map<string, ServiceState>();

  register(service: Service): void {
    if (this.services.has(service.id)) {
      throw new Error(`Service already registered: ${service.id}`);
    }
    this.services.set(service.id, service);
    this.state.set(service.id, 'registered');
    logger.debug(`Registered service: ${service.id}`);
  }

  get<T extends Service>(id: string): T {
    const service = this.services.get(id);
    if (!service) {
      throw new Error(`Service not found: ${id}`);
    }
    return service as T;
  }

  getState(id: string): ServiceState {
    return this.state.get(id) ?? 'registered';
  }

  async initializeAll(): Promise<void> {
    for (const [id, service] of this.services) {
      if (this.state.get(id) === 'registered') {
        logger.info(`Initializing service: ${id}`);
        await service.initialize();
        this.state.set(id, 'initialized');
      }
    }
  }

  async startAll(): Promise<void> {
    for (const [id, service] of this.services) {
      if (this.state.get(id) === 'initialized') {
        logger.info(`Starting service: ${id}`);
        await service.start();
        this.state.set(id, 'started');
      }
    }
  }

  async stopAll(): Promise<void> {
    const entries = Array.from(this.services.entries()).reverse();
    for (const [id, service] of entries) {
      if (this.state.get(id) === 'started') {
        logger.info(`Stopping service: ${id}`);
        await service.stop();
        this.state.set(id, 'stopped');
      }
    }
  }

  async disposeAll(): Promise<void> {
    const entries = Array.from(this.services.entries()).reverse();
    for (const [id, service] of entries) {
      const s = this.state.get(id);
      if (s !== 'disposed' && s !== undefined) {
        if (s === 'started') await service.stop();
        logger.info(`Disposing service: ${id}`);
        await service.dispose();
        this.state.set(id, 'disposed');
      }
    }
  }

  getAll(): Map<string, Service> {
    return new Map(this.services);
  }
}
