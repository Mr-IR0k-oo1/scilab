import { setStore } from '@/store/store';

async function invoke<T>(cmd: string, args?: Record<string, unknown>): Promise<T> {
  try {
    const mod = await import('@tauri-apps/api/core');
    return await (mod as any).invoke(cmd, args);
  } catch {
    throw new Error('Not running in Tauri');
  }
}

export interface ScilabStatus {
  running: boolean;
  version?: string | null;
  pid?: number | null;
}

export interface ExecuteResult {
  output: string;
  error?: string | null;
  success: boolean;
}

export async function startScilab(): Promise<ScilabStatus> {
  try {
    const status = await invoke<ScilabStatus>('start_scilab');
    if (status.running) {
      setStore({ scilabStatus: 'connected', scilabPid: status.pid ?? null });
    }
    return status;
  } catch {
    setStore({ scilabStatus: 'disconnected', scilabPid: null });
    throw new Error('Scilab is not installed or not found in PATH');
  }
}

export async function stopScilab(): Promise<void> {
  try {
    await invoke<void>('stop_scilab');
  } catch {}
  setStore({ scilabStatus: 'disconnected', scilabPid: null });
}

export async function executeScilabCode(code: string): Promise<ExecuteResult> {
  return invoke<ExecuteResult>('execute_code', { code });
}

export async function getScilabStatus(): Promise<ScilabStatus | null> {
  try {
    return await invoke<ScilabStatus>('scilab_status');
  } catch {
    return null;
  }
}

export async function syncScilabStatus(): Promise<void> {
  try {
    const status = await invoke<ScilabStatus>('scilab_status');
    setStore({
      scilabStatus: status.running ? 'connected' : 'disconnected',
      scilabPid: status.pid ?? null,
    });
  } catch {
    setStore({ scilabStatus: 'disconnected', scilabPid: null });
  }
}
