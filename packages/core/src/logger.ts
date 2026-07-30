export type LogLevel = 'trace' | 'debug' | 'info' | 'warn' | 'error';

const LEVEL_PRIORITY: Record<LogLevel, number> = {
  trace: 0,
  debug: 1,
  info: 2,
  warn: 3,
  error: 4
};

export interface LogEntry {
  level: LogLevel;
  message: string;
  data?: object;
  timestamp: string;
  source: string;
}

export class Logger {
  private minLevel: LogLevel = 'info';
  private source: string;

  constructor(source: string) {
    this.source = source;
  }

  setLevel(level: LogLevel): void {
    this.minLevel = level;
  }

  trace(message: string, data?: object): void {
    this.log('trace', message, data);
  }

  debug(message: string, data?: object): void {
    this.log('debug', message, data);
  }

  info(message: string, data?: object): void {
    this.log('info', message, data);
  }

  warn(message: string, data?: object): void {
    this.log('warn', message, data);
  }

  error(message: string, data?: object): void {
    this.log('error', message, data);
  }

  private log(level: LogLevel, message: string, data?: object): void {
    if (LEVEL_PRIORITY[level] < LEVEL_PRIORITY[this.minLevel]) {
      return;
    }

    const entry: LogEntry = {
      level,
      message,
      data,
      timestamp: new Date().toISOString(),
      source: this.source
    };

    const prefix = `[${entry.timestamp}] [${level.toUpperCase()}] [${this.source}]`;

    switch (level) {
      case 'error':
        console.error(prefix, message, data ?? '');
        break;
      case 'warn':
        console.warn(prefix, message, data ?? '');
        break;
      default:
        console.log(prefix, message, data ?? '');
    }
  }
}
