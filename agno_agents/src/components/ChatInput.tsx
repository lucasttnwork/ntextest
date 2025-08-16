import React, { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/solid'
import { useChatStore } from '../stores/chatStore'
import { sendMessageToBackend } from '../services/chatService'

interface ChatInputProps {
  sessionId: string
}

const ChatInput: React.FC<ChatInputProps> = ({ sessionId }) => {
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const { addMessage, setLoading } = useChatStore()

  // Auto-resize do textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px'
    }
  }, [message])

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault()
    
    if (!message.trim() || isLoading) return

    const userMessage = message.trim()
    setMessage('')
    setIsLoading(true)
    setLoading(true)

    // Adicionar mensagem do usuário
    addMessage(sessionId, {
      role: 'user',
      content: userMessage
    })

    try {
      // Enviar para o backend
      const response = await sendMessageToBackend(userMessage, sessionId)
      
      if (response.success && response.response) {
        // Adicionar resposta do agente
        addMessage(sessionId, {
          role: 'assistant',
          content: response.response,
          agent: response.agent,
          metadata: {
            agent: response.agent,
            capabilities: response.capabilities
          }
        })
      } else {
        // Adicionar mensagem de erro
        addMessage(sessionId, {
          role: 'assistant',
          content: `❌ Erro: ${response.error || 'Falha na comunicação com o agente'}`,
          agent: 'NTEX_System'
        })
      }
    } catch (error) {
      console.error('Erro no chat:', error)
      addMessage(sessionId, {
        role: 'assistant',
        content: '❌ Erro de conexão com o servidor',
        agent: 'NTEX_System'
      })
    } finally {
      setIsLoading(false)
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-chat-border bg-chat-bg p-4">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative">
          <div className="relative bg-chat-message border border-chat-border rounded-2xl shadow-lg">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Digite sua mensagem..."
              className="w-full bg-transparent text-chat-text placeholder-chat-textSecondary resize-none outline-none px-4 py-3 pr-12 min-h-[44px] max-h-[120px]"
              rows={1}
              disabled={isLoading}
            />
            
            <button
              type="submit"
              disabled={!message.trim() || isLoading}
              className={`
                absolute right-2 bottom-2 p-2 rounded-lg transition-all duration-200
                ${message.trim() && !isLoading
                  ? 'bg-primary-600 hover:bg-primary-700 text-white'
                  : 'bg-chat-border text-chat-textSecondary cursor-not-allowed'
                }
              `}
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <PaperAirplaneIcon className="w-5 h-5" />
              )}
            </button>
          </div>
          
          {/* Dicas de uso */}
          <div className="mt-3 text-center">
            <p className="text-xs text-chat-textSecondary">
              💡 Dica: Use Shift+Enter para nova linha • 
              Digite "ajuda" para ver comandos disponíveis
            </p>
          </div>
        </div>
      </form>
    </div>
  )
}

export default ChatInput
