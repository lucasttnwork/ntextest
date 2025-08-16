import React from 'react'
import { Message as MessageType } from '../stores/chatStore'
import { clsx } from 'clsx'
import { 
  UserIcon,
  SparklesIcon,
  DocumentTextIcon,
  PaintBrushIcon,
  ChartBarIcon,
  UserGroupIcon
} from '@heroicons/react/24/outline'

interface MessageProps {
  message: MessageType
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user'
  
  const getAgentIcon = (agentName?: string) => {
    if (!agentName) return SparklesIcon
    
    const agentIcons: Record<string, React.ComponentType<any>> = {
      'Copy Agent': DocumentTextIcon,
      'Design Agent': PaintBrushIcon,
      'Analytics Agent': ChartBarIcon,
      'Support Agent': UserGroupIcon,
      'Master Agent': SparklesIcon
    }
    
    return agentIcons[agentName] || SparklesIcon
  }
  
  const getAgentColor = (agentName?: string) => {
    if (!agentName) return '#8b5cf6'
    
    const agentColors: Record<string, string> = {
      'Copy Agent': '#10a37f',
      'Design Agent': '#19c37d',
      'Analytics Agent': '#f59e0b',
      'Support Agent': '#ef4444',
      'Master Agent': '#8b5cf6'
    }
    
    return agentColors[agentName] || '#8b5cf6'
  }

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString('pt-BR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const formatContent = (content: string) => {
    // Converter markdown básico para HTML
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="bg-chat-message px-1 py-0.5 rounded text-sm">$1</code>')
      .replace(/\n/g, '<br>')
  }

  return (
    <div className={clsx(
      "flex space-x-4 animate-fade-in",
      isUser ? "justify-end" : "justify-start"
    )}>
      {!isUser && (
        <div className="flex-shrink-0">
          <div 
            className="w-8 h-8 rounded-lg flex items-center justify-center text-white text-sm font-medium"
            style={{ backgroundColor: getAgentColor(message.agent) }}
          >
            {React.createElement(getAgentIcon(message.agent), { className: "w-5 h-5" })}
          </div>
        </div>
      )}
      
      <div className={clsx(
        "flex-1 max-w-3xl",
        isUser ? "text-right" : "text-left"
      )}>
        <div className={clsx(
          "inline-block px-4 py-3 rounded-2xl",
          isUser 
            ? "bg-primary-600 text-white" 
            : "bg-chat-message text-chat-text"
        )}>
          <div 
            className="prose prose-invert max-w-none"
            dangerouslySetInnerHTML={{ 
              __html: formatContent(message.content) 
            }}
          />
        </div>
        
        <div className={clsx(
          "flex items-center space-x-2 mt-2 text-xs text-chat-textSecondary",
          isUser ? "justify-end" : "justify-start"
        )}>
          {!isUser && message.agent && (
            <>
              <span className="px-2 py-1 rounded-full bg-chat-border text-chat-textSecondary">
                {message.agent}
              </span>
              <span>•</span>
            </>
          )}
          <span>{formatTimestamp(message.timestamp)}</span>
        </div>
      </div>
      
      {isUser && (
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <UserIcon className="w-5 h-5 text-white" />
          </div>
        </div>
      )}
    </div>
  )
}

export default Message
