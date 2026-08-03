export interface ApiTransport {
  request<T>(method: string, path: string, body?: any): Promise<T>;
}

export class FetchTransport implements ApiTransport {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8747';
  }

  async request<T>(method: string, path: string, body?: any): Promise<T> {
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (body !== undefined) {
      if (method === 'GET' || method === 'DELETE') {
        const params = new URLSearchParams(body as Record<string, string>);
        path += '?' + params.toString();
      } else {
        options.body = JSON.stringify(body);
      }
    }

    const response = await fetch(`${this.baseUrl}${path}`, options);
    
    if (!response.ok) {
      let errorDetail = response.statusText;
      try {
        const errorData = await response.json();
        if (errorData.detail) errorDetail = errorData.detail;
      } catch (e) {
        // Ignored
      }
      throw new Error(`API error: ${errorDetail}`);
    }

    return response.json();
  }
}

export const api = new FetchTransport();
