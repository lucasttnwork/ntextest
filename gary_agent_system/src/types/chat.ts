export interface Source {
  title: string;
  url: string;
  description: string;
}

// UIMessage format from AI SDK
export interface UIMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  createdAt: Date;
  parts?: any[];
  sources?: Source[];
  reasoning?: string;
  toolCalls?: any[];
}

// Legacy format for backward compatibility
export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  agent?: string;
  sources?: Source[];
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
