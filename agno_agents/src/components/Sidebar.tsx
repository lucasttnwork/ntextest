import React from 'react'
import { 
  PlusIcon, 
  ChatBubbleLeftRightIcon,
  DocumentTextIcon,
  PaintBrushIcon,
  ChartBarIcon,
  UserGroupIcon,
  Cog6ToothIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'
import { useChatStore } from '../stores/chatStore'
import { clsx } from 'clsx'

const Sidebar: React.FC = () => {
  const { 
    sessions, 
    currentSessionId, 
    createSession, 
    switchSession,
    agents,
    sidebarOpen 
  } = useChatStore()

  const quickActions = [
    {
      icon: DocumentTextIcon,
      label: 'Criar post Instagram',
      action: () => handleQuickAction('Criar post para Instagram sobre automação de marketing'),
      color: 'text-agent-copy'
    },
    {
      icon: PaintBrushIcon,
      label: 'Criar design',
      action: () => handleQuickAction('Criar design visual para campanha de marketing'),
      color: 'text-agent-design'
    },
    {
      icon: ChartBarIcon,
      label: 'Criar campanha',
      action: () => handleQuickAction('Criar campanha completa de marketing digital'),
      color: 'text-agent-master'
    },
    {
      icon: UserGroupIcon,
      label: 'Análise de público',
      action: () => handleQuickAction('Analisar público-alvo para campanha B2B'),
      color: 'text-agent-analytics'
    }
  ]

  const handleQuickAction = (message: string) => {
    if (!currentSessionId) {
      createSession()
    }
    // TODO: Implementar envio automático da mensagem
    console.log('Quick action:', message)
  }

  if (!sidebarOpen) return null

  return (
    <div className="w-80 bg-chat-sidebar border-r border-chat-border flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-chat-border">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">N</span>
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">NTEX</h1>
            <p className="text-chat-textSecondary text-xs">Agentes IA</p>
          </div>
        </div>
      </div>

      {/* Nova conversa */}
      <div className="p-4">
        <button
          onClick={createSession}
          className="w-full flex items-center justify-center space-x-2 bg-chat-message hover:bg-chat-border transition-colors duration-200 text-white rounded-lg px-4 py-3 border border-chat-border"
        >
          <PlusIcon className="w-5 h-5" />
          <span>Nova conversa</span>
        </button>
      </div>

      {/* Sessões ativas */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        <div className="px-4 pb-4">
          <h3 className="text-chat-textSecondary text-xs font-medium uppercase tracking-wider mb-3">
            Conversas ativas
          </h3>
          {sessions.length === 0 ? (
            <p className="text-chat-textSecondary text-sm text-center py-8">
              Nenhuma conversa ainda
            </p>
          ) : (
            <div className="space-y-1">
              {sessions.map((session) => (
                <button
                  key={session.id}
                  onClick={() => switchSession(session.id)}
                  className={clsx(
                    "w-full text-left px-3 py-2 rounded-lg text-sm transition-colors duration-200",
                    currentSessionId === session.id
                      ? "bg-chat-message text-white"
                      : "text-chat-textSecondary hover:bg-chat-message/50 hover:text-white"
                  )}
                >
                  <div className="flex items-center space-x-2">
                    <ChatBubbleLeftRightIcon className="w-4 h-4" />
                    <span className="truncate">{session.name}</span>
                  </div>
                  {session.messages.length > 0 && (
                    <p className="text-xs text-chat-textSecondary mt-1 truncate">
                      {session.messages[session.messages.length - 1].content.substring(0, 30)}...
                    </p>
                  )}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Ações rápidas */}
      <div className="p-4 border-t border-chat-border">
        <h3 className="text-chat-textSecondary text-xs font-medium uppercase tracking-wider mb-3">
          Ações rápidas
        </h3>
        <div className="space-y-2">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={action.action}
              className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm text-chat-textSecondary hover:bg-chat-message hover:text-white transition-colors duration-200"
            >
              <action.icon className={clsx("w-4 h-4", action.color)} />
              <span>{action.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Status dos agentes */}
      <div className="p-4 border-t border-chat-border">
        <h3 className="text-chat-textSecondary text-xs font-medium uppercase tracking-wider mb-3">
          Status dos agentes
        </h3>
        <div className="space-y-2">
          {agents.map((agent) => (
            <div key={agent.id} className="flex items-center justify-between px-3 py-2 rounded-lg bg-chat-message/30">
              <div className="flex items-center space-x-2">
                <div 
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: agent.color }}
                />
                <span className="text-sm text-white">{agent.name}</span>
              </div>
              <div className={clsx(
                "text-xs px-2 py-1 rounded-full",
                agent.status === 'active' && "bg-green-500/20 text-green-400",
                agent.status === 'processing' && "bg-yellow-500/20 text-yellow-400",
                agent.status === 'inactive' && "bg-red-500/20 text-red-400"
              )}>
                {agent.status === 'active' && 'Ativo'}
                {agent.status === 'processing' && 'Processando'}
                {agent.status === 'inactive' && 'Inativo'}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-chat-border">
        <div className="flex items-center justify-between">
          <button className="flex items-center space-x-2 text-chat-textSecondary hover:text-white transition-colors duration-200">
            <Cog6ToothIcon className="w-4 h-4" />
            <span className="text-sm">Configurações</span>
          </button>
          <button className="flex items-center space-x-2 text-chat-textSecondary hover:text-white transition-colors duration-200">
            <InformationCircleIcon className="w-4 h-4" />
            <span className="text-sm">Ajuda</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Sidebar
