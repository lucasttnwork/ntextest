import { useState, useCallback, useRef, useEffect } from 'react';
import { ChatMessage } from '@/types/chat';
import { ntexApi } from '@/services/api';

export function useChat(sessionId?: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentSessionId, setCurrentSessionId] = useState<string | undefined>(sessionId);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Send message to Gary Agent
  const sendMessage = useCallback(async (message: string, options?: { webSearch?: boolean; stream?: boolean }) => {
    if (!message.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Add user message immediately
      const userMessage: ChatMessage = {
        id: Date.now(),
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage]);

      if (options?.stream) {
        const baseId = Date.now() + 1;
        setMessages(prev => [
          ...prev,
          {
            id: baseId,
            role: 'assistant',
            content: '',
            timestamp: new Date().toISOString(),
          },
        ]);

        try {
          for await (const evt of ntexApi.streamMessage(message, currentSessionId, options?.webSearch)) {
            if (evt.type === 'delta' && typeof evt.content === 'string') {
              setMessages(prev => prev.map(m => m.id === baseId ? { ...m, content: (m.content || '') + evt.content } : m));
            } else if (evt.type === 'sources' && evt.sources && Array.isArray(evt.sources)) {
              setMessages(prev => prev.map(m => m.id === baseId ? { ...m, sources: evt.sources } : m));
            } else if (evt.type === 'complete') {
              break;
            } else if (evt.type === 'error') {
              setError(evt.error || 'Erro no streaming');
              break;
            }
          }
        } catch (e) {
          console.error('Streaming error:', e);
        }
      } else {
        // Send to API
        const response = await ntexApi.sendMessage(message, currentSessionId, options?.webSearch);

        if (response.success) {
          // Set session ID if it's a new session
          if (response.session_id && !currentSessionId) {
            setCurrentSessionId(response.session_id);
          }

          // Add assistant response
          const assistantMessage: ChatMessage = {
            id: Date.now() + 1,
            role: 'assistant',
            content: response.response || '',
            timestamp: new Date().toISOString(),
            agent: response.agent,
          };

          setMessages(prev => [...prev, assistantMessage]);
        } else {
          setError(response.error || 'Erro ao enviar mensagem');
        }
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Erro de conexão. Verifique se o backend está rodando.');
    } finally {
      setIsLoading(false);
    }
  }, [currentSessionId]);

  // Clear chat
  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  // Load existing session
  const loadSession = useCallback(async (sessionId: string) => {
    try {
      const sessionData = await ntexApi.getSession(sessionId);
      if (sessionData.recent_messages && Array.isArray(sessionData.recent_messages)) {
        setMessages(sessionData.recent_messages as ChatMessage[]);
        setCurrentSessionId(sessionId);
      }
    } catch (err) {
      console.error('Error loading session:', err);
      setError('Erro ao carregar sessão');
    }
  }, []);

  // Load session if sessionId is provided
  useEffect(() => {
    if (sessionId && !messages.length) {
      loadSession(sessionId);
    }
  }, [sessionId, loadSession, messages.length]);

  return {
    messages,
    isLoading,
    error,
    currentSessionId,
    sendMessage,
    clearChat,
    loadSession,
    messagesEndRef,
  };
}
