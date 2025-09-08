'use client'

import { useState } from 'react'
import { useChat } from 'ai/react'

export default function ChatInterface() {
  const [sessionId] = useState(() => `session-${Date.now()}`)
  
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    body: {
      sessionId,
    },
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🤝 Gary Bencivenga
          </h1>
          <p className="text-lg text-gray-700 mb-4">
            O Mestre do Copywriting está aqui para ajudar você
          </p>
          <div className="inline-flex items-center justify-center px-4 py-2 bg-orange-100 text-orange-800 rounded-full text-sm font-medium">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
            Online
          </div>
        </div>

        {/* Chat Container */}
        <div className="bg-white rounded-2xl shadow-xl border">
          {/* Messages */}
          <div className="chat-container p-6">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gradient-to-r from-orange-400 to-amber-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-2xl">🧠</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Bem-vindo! Gary está pronto para te ajudar
                </h3>
                <p className="text-gray-600 mb-4">
                  Faça perguntas sobre copywriting, marketing ou qualquer coisa relacionada. Gary começará com uma sessão de descoberta.
                </p>
                <div className="text-sm text-gray-500">
                  Exemplos:
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-2 text-sm text-gray-600">
                  <div className="p-2 bg-gray-50 rounded-lg text-left">
                    "Quero criar copy para meu produto de fitness"
                  </div>
                  <div className="p-2 bg-gray-50 rounded-lg text-left">
                    "Me ajude a melhorar minhas conversões"
                  </div>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} message-animation`}
                  >
                    {message.role === 'assistant' && (
                      <div className="w-8 h-8 bg-gradient-to-r from-orange-400 to-amber-500 rounded-full mr-3 flex-shrink-0 flex items-center justify-center">
                        <span className="text-white text-sm">🧠</span>
                      </div>
                    )}
                    <div
                      className={`max-w-xl rounded-2xl px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <div 
                        className="text-sm leading-relaxed whitespace-pre-wrap"
                        dangerouslySetInnerHTML={{
                          __html: message.content.replace(/\n/g, '<br />')
                        }}
                      />
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start message-animation">
                    <div className="w-8 h-8 bg-gradient-to-r from-orange-400 to-amber-500 rounded-full mr-3 flex-shrink-0 flex items-center justify-center">
                      <span className="text-white text-sm">🧠</span>
                    </div>
                    <div className="bg-gray-100 rounded-2xl px-4 py-3">
                      <div className="flex items-center space-x-1">
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></span>
                        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Input */}
          <div className="border-t border-gray-200 p-6">
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <textarea
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Digite sua mensagem... (Ex: "Quero criar copy para meu produto de fitness para mulheres de 25-45 anos")"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
                  rows={3}
                  disabled={isLoading}
                />
              </div>
              <div className="flex items-end">
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="px-6 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white rounded-xl font-medium hover:from-orange-600 hover:to-amber-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
                >
                  <span>Enviar</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </form>
            
            <div className="mt-4 text-center text-xs text-gray-500">
              <p>💡 Gary vai começar com perguntas de descoberta para entender melhor sua necessidade</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}