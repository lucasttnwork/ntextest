import { useState, useCallback, useRef, useEffect } from 'react';
import { useChat as useAIChat } from '@ai-sdk/react';

export function useChat(sessionId?: string) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // AI SDK chat hook
  const ai = useAIChat({
    api: '/api/gary' as any,
  } as any);

  // Scroll to bottom when new AI messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [ai.messages, scrollToBottom]);

  // Adapter: sendMessage wrapper
  const sendMessage = useCallback(
    async (message: string, options?: { webSearch?: boolean }) => {
      if (!message.trim()) return;
      await ai.sendMessage(
        { text: message },
        { body: { webSearch: !!options?.webSearch, sessionId } }
      );
    },
    [ai, sessionId]
  );

  // Adapter: expose minimal legacy-compatible shape
  const legacyMessages = (ai.messages as any[]).map((m, idx) => ({
    id: idx + 1,
    role: m.role === 'system' ? 'assistant' : (m.role as 'user' | 'assistant'),
    content: m.content as unknown as string,
    timestamp: new Date().toISOString(),
    sources: (m as any).sources,
    metadata: { reasoning: (m as any).parts?.find((p: any) => p.type === 'reasoning')?.text },
  }));

  return {
    // legacy
    messages: legacyMessages,
    isLoading: (ai as any).isLoading,
    error: (ai as any).error?.message || null,
    currentSessionId: sessionId,
    sendMessage,
    clearChat: ai.stop,
    loadSession: async () => {},
    messagesEndRef,
    // ai native
    aiMessages: ai.messages,
  };
}
