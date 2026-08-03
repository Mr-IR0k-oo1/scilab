import { setStore } from '@/store/store';
import { api } from './api';

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
    const status = await api.request<ScilabStatus>('POST', '/api/scilab/start');
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
    await api.request<void>('POST', '/api/scilab/stop');
  } catch {}
  setStore({ scilabStatus: 'disconnected', scilabPid: null });
}

export async function executeScilabCode(code: string): Promise<ExecuteResult> {
  return api.request<ExecuteResult>('POST', '/api/scilab/execute', { code });
}

export async function getScilabStatus(): Promise<ScilabStatus | null> {
  try {
    return await api.request<ScilabStatus>('GET', '/api/scilab/status');
  } catch {
    return null;
  }
}

export async function syncScilabStatus(): Promise<void> {
  try {
    const status = await api.request<ScilabStatus>('GET', '/api/scilab/status');
    setStore({
      scilabStatus: status.running ? 'connected' : 'disconnected',
      scilabPid: status.pid ?? null,
    });
  } catch {
    setStore({ scilabStatus: 'disconnected', scilabPid: null });
  }
}

