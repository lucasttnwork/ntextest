'use client';

import { useState, FormEvent } from 'react';
import { useChat } from '@/hooks/useChat';

// AI Elements Components
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import {
  Message,
  MessageContent,
  MessageAvatar,
} from '@/components/ai-elements/message';
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputSubmit,
} from '@/components/ai-elements/prompt-input';
import { Loader } from '@/components/ai-elements/loader';

// UI Components
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { ThemeToggle } from '@/components/theme-toggle';
import { Trash2, MessageSquare } from 'lucide-react';

interface ChatInterfaceProps {
  sessionId?: string;
  onSessionChange?: (sessionId: string) => void;
}

export function ChatInterface({ sessionId, onSessionChange }: ChatInterfaceProps) {
  const [inputValue, setInputValue] = useState('');
  const {
    messages,
    isLoading,
    error,
    currentSessionId,
    sendMessage,
    clearChat,
    messagesEndRef,
  } = useChat(sessionId);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const message = inputValue.trim();
    setInputValue('');

    await sendMessage(message, { stream: true });

    // Notify parent component of session change
    if (currentSessionId && onSessionChange) {
      onSessionChange(currentSessionId);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.ctrlKey && e.key === 'Enter') {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleClearChat = () => {
    clearChat();
    if (onSessionChange) {
      onSessionChange('');
    }
  };

  return (
    <div className="flex h-screen flex-col bg-background">
      {/* Header */}
      <div className="flex items-center justify-between border-b bg-background px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-primary" />
            <h1 className="text-lg font-semibold">Gary Bencivenga Agent</h1>
          </div>
          {currentSessionId && (
            <Badge variant="secondary" className="text-xs">
              Sessão {currentSessionId.slice(-8)}
            </Badge>
          )}
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button
            variant="outline"
            size="sm"
            onClick={handleClearChat}
            disabled={messages.length === 0}
            className="gap-2"
          >
            <Trash2 className="h-4 w-4" />
            Limpar
          </Button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden">
        {messages.length === 0 && !isLoading ? (
          <div className="flex h-full items-center justify-center">
            <div className="text-center space-y-6 max-w-lg mx-auto px-4">
              <div className="w-20 h-20 mx-auto bg-primary/10 rounded-full flex items-center justify-center">
                <MessageSquare className="h-10 w-10 text-primary" />
              </div>
              <div className="space-y-3">
                <h2 className="text-2xl font-bold">
                  Converse com Gary Bencivenga
                </h2>
                <p className="text-muted-foreground text-base leading-relaxed">
                  O maior copywriter vivo está aqui para ajudar você a criar
                  conteúdo persuasivo e de alta conversão com técnicas comprovadas.
                </p>
                <div className="pt-4">
                  <p className="text-sm text-muted-foreground">
                    💡 Experimente: &quot;Crie um anúncio para meu produto&quot;
                  </p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <Conversation>
            <ConversationContent>
              {messages.map((message) => (
                <Message
                  key={message.id}
                  from={message.role}
                  className="group"
                >
                  {message.role === 'assistant' && (
                    <MessageAvatar
                      src="/gary-avatar.svg"
                      name="Gary"
                      className="mt-1"
                    />
                  )}
                  <MessageContent>
                    <div className="prose prose-sm max-w-none">
                      {message.content.split('\n').map((line, i) => (
                        <p key={i} className={i > 0 ? 'mt-2' : ''}>
                          {line}
                        </p>
                      ))}
                      {isLoading && message.role === 'assistant' && message.id === messages[messages.length - 1]?.id && (
                        <span className="inline-block w-2 h-4 bg-primary animate-pulse ml-1" />
                      )}
                    </div>
                    {message.agent && (
                      <div className="mt-2 text-xs text-muted-foreground">
                        {message.agent}
                      </div>
                    )}
                  </MessageContent>
                  {message.role === 'user' && (
                    <MessageAvatar
                      src="/user-avatar.svg"
                      name="Você"
                      className="mt-1"
                    />
                  )}
                </Message>
              ))}

              {isLoading && (
                <Message from="assistant">
                  <MessageAvatar
                    src="/gary-avatar.png"
                    name="Gary"
                    className="mt-1"
                  />
                  <MessageContent>
                    <Loader />
                  </MessageContent>
                </Message>
              )}

              <div ref={messagesEndRef} />
            </ConversationContent>
            <ConversationScrollButton />
          </Conversation>
        )}
      </div>

      {/* Error Alert */}
      {error && (
        <div className="px-4 py-2">
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t bg-background p-4">
        <PromptInput onSubmit={handleSubmit}>
          <PromptInputTextarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Digite sua mensagem para Gary... (Ctrl+Enter para enviar)"
            disabled={isLoading}
            className="min-h-[48px] max-h-[120px]"
          />
          <PromptInputToolbar>
            <PromptInputSubmit
              status={isLoading ? 'submitted' : 'ready'}
              disabled={!inputValue.trim() || isLoading}
            />
          </PromptInputToolbar>
        </PromptInput>
      </div>
    </div>
  );
}
