import { ChatSession, ChatResponse, AgentStatus } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class NTEXApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async sendMessage(message: string, sessionId?: string, webSearch?: boolean): Promise<ChatResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
          webSearch,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getSessions(): Promise<ChatSession[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/sessions`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching sessions:', error);
      throw error;
    }
  }

  async getSession(sessionId: string): Promise<Record<string, unknown>> {
    try {
      const response = await fetch(`${this.baseUrl}/api/sessions/${sessionId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching session:', error);
      throw error;
    }
  }

  async closeSession(sessionId: string): Promise<{ success: boolean }> {
    try {
      const response = await fetch(`${this.baseUrl}/api/sessions/${sessionId}/close`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error closing session:', error);
      throw error;
    }
  }

  async getAgentsStatus(): Promise<Record<string, AgentStatus>> {
    try {
      const response = await fetch(`${this.baseUrl}/api/agents/status`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching agents status:', error);
      throw error;
    }
  }

  // Streaming endpoint (for future implementation)
  async *streamMessage(message: string, sessionId?: string, webSearch?: boolean) {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          session_id: sessionId,
          webSearch,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data.trim()) {
              try {
                const parsed = JSON.parse(data);
                yield parsed;
              } catch {
                console.warn('Failed to parse SSE data:', data);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error streaming message:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const ntexApi = new NTEXApiService();
export default ntexApi;
