import { create } from 'zustand'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  agent?: string
  metadata?: Record<string, any>
}

export interface ChatSession {
  id: string
  name: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}

export interface Agent {
  id: string
  name: string
  type: 'master' | 'copy' | 'design' | 'analytics' | 'support'
  status: 'active' | 'inactive' | 'processing'
  capabilities: string[]
  color: string
}

export interface ChatState {
  // Estado das sessões
  sessions: ChatSession[]
  currentSessionId: string | null
  
  // Estado dos agentes
  agents: Agent[]
  activeAgent: string | null
  
  // Estado da interface
  isLoading: boolean
  sidebarOpen: boolean
  
  // Ações
  createSession: () => void
  switchSession: (sessionId: string) => void
  addMessage: (sessionId: string, message: Omit<Message, 'id' | 'timestamp'>) => void
  updateAgentStatus: (agentId: string, status: Agent['status']) => void
  setLoading: (loading: boolean) => void
  toggleSidebar: () => void
}

const initialAgents: Agent[] = [
  {
    id: 'master',
    name: 'Master Agent',
    type: 'master',
    status: 'active',
    capabilities: ['coordenação', 'estratégia', 'roteamento'],
    color: '#8b5cf6'
  },
  {
    id: 'copy',
    name: 'Copy Agent',
    type: 'copy',
    status: 'active',
    capabilities: ['copywriting', 'redes sociais', 'anúncios'],
    color: '#10a37f'
  },
  {
    id: 'design',
    name: 'Design Agent',
    type: 'design',
    status: 'active',
    capabilities: ['design visual', 'templates', 'branding'],
    color: '#19c37d'
  },
  {
    id: 'analytics',
    name: 'Analytics Agent',
    type: 'analytics',
    status: 'active',
    capabilities: ['dashboards', 'relatórios', 'KPIs'],
    color: '#f59e0b'
  },
  {
    id: 'support',
    name: 'Support Agent',
    type: 'support',
    status: 'active',
    capabilities: ['atendimento', 'qualificação', 'propostas'],
    color: '#ef4444'
  }
]

export const useChatStore = create<ChatState>((set) => ({
  // Estado inicial
  sessions: [],
  currentSessionId: null,
  agents: initialAgents,
  activeAgent: null,
  isLoading: false,
  sidebarOpen: true,
  
  // Ações
  createSession: () => {
    const newSession: ChatSession = {
      id: crypto.randomUUID(),
      name: `Nova conversa ${new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}`,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date()
    }
    
    set((state) => ({
      sessions: [newSession, ...state.sessions],
      currentSessionId: newSession.id
    }))
  },
  
  switchSession: (sessionId: string) => {
    set({ currentSessionId: sessionId })
  },
  
  addMessage: (sessionId: string, message: Omit<Message, 'id' | 'timestamp'>) => {
    const newMessage: Message = {
      ...message,
      id: crypto.randomUUID(),
      timestamp: new Date()
    }
    
    set((state) => ({
      sessions: state.sessions.map(session => 
        session.id === sessionId 
          ? {
              ...session,
              messages: [...session.messages, newMessage],
              updatedAt: new Date()
            }
          : session
      )
    }))
  },
  
  updateAgentStatus: (agentId: string, status: Agent['status']) => {
    set((state) => ({
      agents: state.agents.map(agent =>
        agent.id === agentId ? { ...agent, status } : agent
      )
    }))
  },
  
  setLoading: (loading: boolean) => {
    set({ isLoading: loading })
  },
  
  toggleSidebar: () => {
    set((state) => ({ sidebarOpen: !state.sidebarOpen }))
  }
}))
