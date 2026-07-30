import type { Service } from '@scilab-studio/core';
import { Logger, EventBus, Storage } from '@scilab-studio/core';
import { join, basename } from 'path-browserify';

export interface ProjectMetadata {
  name: string;
  path: string;
  createdAt: string;
  updatedAt: string;
  version: string;
}

export interface ProjectData {
  metadata: ProjectMetadata;
  files: Record<string, unknown>;
}

const logger = new Logger('workspace');

export class WorkspaceService implements Service {
  readonly id = 'workspace';

  private currentProject: ProjectData | null = null;
  private recentProjects: string[] = [];
  private eventBus: EventBus;
  private storage: Storage;

  constructor(eventBus: EventBus, storage: Storage) {
    this.eventBus = eventBus;
    this.storage = storage;
  }

  async initialize(): Promise<void> {
    const recent = await this.storage.get<string[]>('recentProjects');
    if (recent) {
      this.recentProjects = recent;
    }
  }

  async start(): Promise<void> {
    logger.info('Workspace service started');
  }

  async stop(): Promise<void> {
    if (this.currentProject) {
      await this.saveProject();
    }
  }

  async dispose(): Promise<void> {
    this.currentProject = null;
  }

  async createProject(name: string, parentPath: string): Promise<ProjectData> {
    const projectPath = join(parentPath, name);
    const now = new Date().toISOString();

    const project: ProjectData = {
      metadata: {
        name,
        path: projectPath,
        createdAt: now,
        updatedAt: now,
        version: '1.0.0',
      },
      files: {},
    };

    this.currentProject = project;
    this.addToRecent(projectPath);

    this.eventBus.emit('project:created', project.metadata);
    logger.info(`Created project: ${name} at ${projectPath}`);

    return project;
  }

  async openProject(projectPath: string): Promise<ProjectData> {
    // In real implementation, reads .scstudio file from disk via Tauri
    const project: ProjectData = {
      metadata: {
        name: basename(projectPath),
        path: projectPath,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        version: '1.0.0',
      },
      files: {},
    };

    this.currentProject = project;
    this.addToRecent(projectPath);

    this.eventBus.emit('project:opened', project.metadata);
    logger.info(`Opened project: ${projectPath}`);

    return project;
  }

  async saveProject(): Promise<void> {
    if (!this.currentProject) return;

    this.currentProject.metadata.updatedAt = new Date().toISOString();
    this.eventBus.emit('project:saved', this.currentProject.metadata);
    logger.info(`Saved project: ${this.currentProject.metadata.name}`);
  }

  closeProject(): void {
    if (this.currentProject) {
      const name = this.currentProject.metadata.name;
      this.currentProject = null;
      this.eventBus.emit('project:closed', { name });
      logger.info(`Closed project: ${name}`);
    }
  }

  getCurrentProject(): ProjectData | null {
    return this.currentProject;
  }

  getRecentProjects(): string[] {
    return [...this.recentProjects];
  }

  private addToRecent(path: string): void {
    this.recentProjects = this.recentProjects.filter((p) => p !== path);
    this.recentProjects.unshift(path);
    if (this.recentProjects.length > 10) {
      this.recentProjects = this.recentProjects.slice(0, 10);
    }
    this.storage.set('recentProjects', this.recentProjects);
  }
}
