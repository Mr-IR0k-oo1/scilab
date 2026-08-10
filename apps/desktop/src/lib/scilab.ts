import { setStore } from '@/store/store';
import { api } from './api';

export interface ScilabStatusResponse {
  installed: boolean;
  executable: string | null;
  version: string | null;
  status: string;
  session_state: string;
}

export interface ExecuteResultResponse {
  id: string;
  command: string;
  success: boolean;
  stdout: string;
  stderr: string;
  exit_code: number | null;
  duration_ms: number;
  status: string;
  truncated: boolean;
}

export interface ExecuteResult {
  output: string;
  error?: string | null;
  success: boolean;
  execution_id?: string;
  duration_ms?: number;
}

export async function getScilabStatus(): Promise<ScilabStatusResponse | null> {
  try {
    return await api.request<ScilabStatusResponse>('GET', '/scilab/status');
  } catch {
    return null;
  }
}

export async function startScilab(): Promise<ScilabStatusResponse> {
  try {
    const status = await api.request<ScilabStatusResponse>('POST', '/scilab/start');
    const isRunning = status.status === 'running' || status.session_state === 'RUNNING';
    setStore({
      scilabStatus: isRunning ? 'connected' : 'disconnected',
    });
    return status;
  } catch (err: any) {
    setStore({ scilabStatus: 'disconnected' });
    throw new Error(err.message || 'Scilab is not installed or not found in PATH');
  }
}

export async function stopScilab(): Promise<void> {
  try {
    await api.request<void>('POST', '/scilab/stop');
  } catch {}
  setStore({ scilabStatus: 'disconnected', scilabPid: null });
}

export async function executeScilabCode(code: string): Promise<ExecuteResult> {
  try {
    const res = await api.request<ExecuteResultResponse>('POST', '/scilab/execute', { command: code });
    return {
      output: res.stdout || '',
      error: res.stderr || null,
      success: res.success,
      execution_id: res.id,
      duration_ms: res.duration_ms,
    };
  } catch (err: any) {
    return {
      output: '',
      error: err.message || 'Execution failed',
      success: false,
    };
  }
}

export async function executeScilabScript(path: string): Promise<ExecuteResult> {
  try {
    const res = await api.request<ExecuteResultResponse>('POST', '/scilab/execute-script', { path });
    return {
      output: res.stdout || '',
      error: res.stderr || null,
      success: res.success,
      execution_id: res.id,
      duration_ms: res.duration_ms,
    };
  } catch (err: any) {
    return {
      output: '',
      error: err.message || 'Script execution failed',
      success: false,
    };
  }
}

export async function syncScilabStatus(): Promise<void> {
  try {
    const status = await api.request<ScilabStatusResponse>('GET', '/scilab/status');
    const isRunning = status.status === 'running' || status.session_state === 'RUNNING';
    setStore({
      scilabStatus: isRunning ? 'connected' : 'disconnected',
    });
  } catch {
    setStore({ scilabStatus: 'disconnected', scilabPid: null });
  }
}
