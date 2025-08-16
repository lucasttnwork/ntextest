import React, { useRef, useEffect } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/solid'
import { useChatStore } from '../stores/chatStore'
import Message from './Message'
import ChatInput from './ChatInput'
import { Bars3Icon } from '@heroicons/react/24/outline'

const ChatArea: React.FC = () => {
  const { 
    sessions, 
    currentSessionId, 
    sidebarOpen, 
    toggleSidebar 
  } = useChatStore()
  
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const currentSession = sessions.find(s => s.id === currentSessionId)

  // Auto-scroll para baixo
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [currentSession?.messages])

  if (!currentSession) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-chat-bg">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto">
            <span className="text-white font-bold text-2xl">N</span>
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-white mb-2">
              Bem-vindo ao NTEX
            </h2>
            <p className="text-chat-textSecondary text-lg max-w-md">
              Comece uma nova conversa para interagir com nossos agentes de IA especializados em marketing digital e automação.
            </p>
          </div>
          <div className="flex items-center justify-center space-x-4 text-sm text-chat-textSecondary">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-agent-copy rounded-full"></div>
              <span>Copy Agent</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-agent-design rounded-full"></div>
              <span>Design Agent</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-agent-master rounded-full"></div>
              <span>Master Agent</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col bg-chat-bg">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-chat-border bg-chat-bg">
        <div className="flex items-center space-x-3">
          {!sidebarOpen && (
            <button
              onClick={toggleSidebar}
              className="p-2 rounded-lg hover:bg-chat-message transition-colors duration-200"
            >
              <Bars3Icon className="w-5 h-5 text-chat-text" />
            </button>
          )}
          <div>
            <h2 className="text-lg font-semibold text-white">{currentSession.name}</h2>
            <p className="text-sm text-chat-textSecondary">
              {currentSession.messages.length} mensagens • 
              Criada em {currentSession.createdAt.toLocaleDateString('pt-BR')}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="flex -space-x-1">
            {['master', 'copy', 'design'].map((agentType) => (
              <div
                key={agentType}
                className="w-6 h-6 rounded-full border-2 border-chat-bg flex items-center justify-center text-xs font-medium text-white"
                style={{
                  backgroundColor: 
                    agentType === 'master' ? '#8b5cf6' :
                    agentType === 'copy' ? '#10a37f' : '#19c37d'
                }}
              >
                {agentType === 'master' ? 'M' : agentType === 'copy' ? 'C' : 'D'}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Área de mensagens */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        <div className="p-4 space-y-6">
          {currentSession.messages.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-12 h-12 bg-chat-message rounded-full flex items-center justify-center mx-auto mb-4">
                <PaperAirplaneIcon className="w-6 h-6 text-chat-textSecondary" />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">
                Comece a conversar
              </h3>
              <p className="text-chat-textSecondary max-w-md mx-auto">
                Digite sua mensagem abaixo para começar a interagir com os agentes NTEX. 
                Eles podem ajudar com copy, design, estratégias de marketing e muito mais.
              </p>
            </div>
          ) : (
            currentSession.messages.map((message) => (
              <Message key={message.id} message={message} />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input de chat */}
      <ChatInput sessionId={currentSession.id} />
    </div>
  )
}

export default ChatArea
