import type { Service, ServiceRegistry } from './service-registry.js';
import { Logger } from './logger.js';

export interface ModuleManifest {
  id: string;
  name: string;
  version: string;
  description: string;
  entry: ModuleFactory;
}

export type ModuleFactory = (context: ModuleContext) => Service;

export interface ModuleContext {
  logger: Logger;
}

const logger = new Logger('module-loader');

export class ModuleLoader {
  private manifests = new Map<string, ModuleManifest>();
  private registry: ServiceRegistry;

  constructor(registry: ServiceRegistry) {
    this.registry = registry;
  }

  register(manifest: ModuleManifest): void {
    if (this.manifests.has(manifest.id)) {
      throw new Error(`Module already registered: ${manifest.id}`);
    }
    this.manifests.set(manifest.id, manifest);
    logger.debug(`Registered module: ${manifest.id} v${manifest.version}`);
  }

  async loadAll(): Promise<void> {
    for (const [id, manifest] of this.manifests) {
      logger.info(`Loading module: ${id}`);
      const context: ModuleContext = {
        logger: new Logger(id),
      };
      const service = manifest.entry(context);
      this.registry.register(service);
    }

    await this.registry.initializeAll();
    await this.registry.startAll();
  }

  getManifest(id: string): ModuleManifest | undefined {
    return this.manifests.get(id);
  }

  list(): ModuleManifest[] {
    return Array.from(this.manifests.values());
  }
}
