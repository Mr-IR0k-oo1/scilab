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

async function invoke<T>(cmd: string, args?: Record<string, unknown>): Promise<T> {
  try {
    const mod = await import('@tauri-apps/api/core');
    return await (mod as any).invoke(cmd, args);
  } catch {
    throw new Error('Not running in Tauri');
  }
}

export async function readTextFile(path: string): Promise<string> {
  return invoke<string>('read_text_file', { path });
}

export async function writeTextFile(path: string, content: string): Promise<void> {
  return invoke<void>('write_text_file', { path, content });
}

export async function listDirectory(path: string): Promise<DirEntry[]> {
  return invoke<DirEntry[]>('list_directory', { path });
}

export async function createDirectory(path: string): Promise<void> {
  return invoke<void>('create_directory', { path });
}

export async function removeFile(path: string): Promise<void> {
  return invoke<void>('remove_file', { path });
}

export async function removeDirectory(path: string): Promise<void> {
  return invoke<void>('remove_directory', { path });
}

export async function fileExists(path: string): Promise<boolean> {
  return invoke<boolean>('file_exists', { path });
}

export async function pathInfo(path: string): Promise<PathInfo> {
  return invoke<PathInfo>('path_info', { path });
}

export async function getAppDataDir(): Promise<string> {
  return invoke<string>('get_app_data_dir');
}

export async function getDocumentsDir(): Promise<string> {
  return invoke<string>('get_documents_dir');
}

export async function getProjectDir(): Promise<string> {
  return invoke<string>('get_project_dir');
}

export interface CreateProjectOptions {
  name: string;
  tools: string[];
}

export async function createProjectBackend(options: CreateProjectOptions): Promise<string> {
  return invoke<string>('create_project', { name: options.name, tools: options.tools });
}

export async function listProjects(): Promise<DirEntry[]> {
  return invoke<DirEntry[]>('list_projects');
}

export async function renamePath(oldPath: string, newPath: string): Promise<void> {
  return invoke<void>('rename_path', { oldPath, newPath });
}

export async function updateProjectMetadata(name: string): Promise<void> {
  return invoke<void>('update_project_metadata', { name });
}

export async function deleteProjectBackend(name: string): Promise<void> {
  return invoke<void>('delete_project', { name });
}

export async function tryInvokeFs<T>(fn: () => Promise<T>): Promise<{ ok: true; value: T } | { ok: false; error: string }> {
  try {
    const value = await fn();
    return { ok: true, value };
  } catch (err) {
    return { ok: false, error: String(err) };
  }
}
