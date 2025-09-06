export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  agent?: string;
  metadata?: Record<string, unknown>;
}

export interface ChatSession {
  id: string;
  session_name: string;
  status: 'active' | 'closed';
  last_activity?: string;
  messages?: ChatMessage[];
}

export interface ChatResponse {
  success: boolean;
  response?: string;
  agent?: string;
  session_id?: string;
  error?: string;
}

export interface AgentStatus {
  status: 'active' | 'inactive';
  name: string;
  capabilities: string[];
}
