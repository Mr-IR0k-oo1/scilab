import { api } from './api';

export interface DirEntry {
  name: string;
  path: string;
  is_dir: boolean;
  size: number;
  modified: string;
}

export interface PathInfo {
  exists: boolean;
  is_dir: boolean;
  is_file: boolean;
  size: number;
  modified: string;
  extension: string | null;
}

export async function readTextFile(path: string): Promise<string> {
  const res = await api.request<{ content: string }>('GET', '/api/fs/file', { path });
  return res.content;
}

export async function writeTextFile(path: string, content: string): Promise<void> {
  await api.request<void>('PUT', '/api/fs/file', { path, content });
}

export async function listDirectory(path: string): Promise<DirEntry[]> {
  return api.request<DirEntry[]>('GET', '/api/fs/list', { path });
}

export async function createDirectory(path: string): Promise<void> {
  await api.request<void>('POST', '/api/fs/dir', { path });
}

export async function removeFile(path: string): Promise<void> {
  await api.request<void>('DELETE', '/api/fs/file', { path });
}

export async function removeDirectory(path: string): Promise<void> {
  await api.request<void>('DELETE', '/api/fs/dir', { path });
}

export async function fileExists(path: string): Promise<boolean> {
  const res = await api.request<{ exists: boolean }>('GET', '/api/fs/exists', { path });
  return res.exists;
}

export async function pathInfo(path: string): Promise<PathInfo> {
  return api.request<PathInfo>('GET', '/api/fs/info', { path });
}

export async function getAppDataDir(): Promise<string> {
  // Polyfill using project dir for now
  return getProjectDir();
}

export async function getDocumentsDir(): Promise<string> {
  // Polyfill using project dir for now
  return getProjectDir();
}

export async function getProjectDir(): Promise<string> {
  const res = await api.request<{ dir: string }>('GET', '/api/projects/dir');
  return res.dir;
}

export interface CreateProjectOptions {
  name: string;
  tools: string[];
}

export async function createProjectBackend(options: CreateProjectOptions): Promise<string> {
  const res = await api.request<{ name: string }>('POST', '/api/projects', {
    name: options.name,
    description: `Uses tools: ${options.tools.join(', ')}`
  });
  return res.name;
}

export async function listProjects(): Promise<DirEntry[]> {
  const projects = await api.request<any[]>('GET', '/api/projects');
  // Map project metadata to DirEntry shape for the frontend
  return projects.map((p) => ({
    name: p.name,
    path: p.name, // The backend handles paths by name for projects
    is_dir: true,
    size: 0,
    modified: p.updated_at ? new Date(p.updated_at * 1000).toISOString() : new Date().toISOString(),
  }));
}

export async function renamePath(oldPath: string, newPath: string): Promise<void> {
  await api.request<void>('POST', '/api/fs/rename', { old_path: oldPath, new_path: newPath });
}

export async function updateProjectMetadata(name: string): Promise<void> {
  await api.request<void>('PATCH', `/api/projects/${name}`, {
    name: name,
    updated_at: Date.now() / 1000,
  });
}

export async function deleteProjectBackend(name: string): Promise<void> {
  await api.request<void>('DELETE', `/api/projects/${name}`);
}

export async function tryInvokeFs<T>(fn: () => Promise<T>): Promise<{ ok: true; value: T } | { ok: false; error: string }> {
  try {
    const value = await fn();
    return { ok: true, value };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}

