import { Logger } from '@scilab-studio/core';

export interface ExecuteResult {
  output: string;
  variables: Record<string, any>;
  error?: string;
  success: boolean;
}

export interface RuntimeStatus {
  state: 'not-running' | 'starting' | 'ready' | 'running' | 'idle';
  version?: string;
  pid?: number;
}

const API_BASE = 'http://localhost:8000';

export class ScilabBridge {
  private logger = new Logger('scilab-bridge');
  private status: RuntimeStatus = { state: 'not-running' };

  private async fetchApi(endpoint: string, options?: RequestInit): Promise<any> {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    if (!res.ok) {
      throw new Error(`API error: ${res.statusText}`);
    }
    return res.json();
  }

  async start(): Promise<void> {
    this.logger.info('Starting Scilab process...');
    this.status = { state: 'starting' };

    try {
      const res = await this.fetchApi('/api/scilab/start', { method: 'POST' });
      this.status = { state: 'ready', version: res.version, pid: res.pid };
      this.logger.info('Scilab ready');
    } catch (e: any) {
      this.status = { state: 'not-running' };
      this.logger.error('Failed to start scilab', e);
      throw e;
    }
  }

  async stop(): Promise<void> {
    this.logger.info('Stopping Scilab process...');
    try {
      await this.fetchApi('/api/scilab/stop', { method: 'POST' });
    } catch (e: any) {
      this.logger.error('Failed to stop', e);
    }
    this.status = { state: 'not-running' };
  }

  async execute(code: string, _timeout = 30000): Promise<ExecuteResult> {
    if (this.status.state !== 'ready' && this.status.state !== 'idle') {
      throw new Error('Scilab is not ready');
    }

    this.status.state = 'running';
    this.logger.debug('Executing code', { code: code.substring(0, 100) });

    try {
      const result = await this.fetchApi('/api/scilab/execute', {
        method: 'POST',
        body: JSON.stringify({ code }),
      });
      this.status.state = 'idle';
      
      if (!result.variables) {
        result.variables = {};
      }
      
      return result;
    } catch (e: any) {
      this.status.state = 'idle';
      throw e;
    }
  }

  async evaluate(expression: string): Promise<any> {
    const result = await this.execute(`disp(${expression})`);
    return result;
  }

  async getStatus(): Promise<RuntimeStatus> {
    try {
      const res = await this.fetchApi('/api/scilab/status', { method: 'GET' });
      if (res.running) {
        this.status = { state: 'idle', version: res.version, pid: res.pid };
      } else {
        this.status = { state: 'not-running' };
      }
    } catch (e: any) {
      this.logger.error('Failed to get status', e);
      this.status = { state: 'not-running' };
    }
    return { ...this.status };
  }

  async ping(): Promise<boolean> {
    const status = await this.getStatus();
    return status.state !== 'not-running';
  }
}

