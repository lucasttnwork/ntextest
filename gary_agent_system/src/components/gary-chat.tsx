'use client';

import { useState, useEffect, useRef } from 'react';
import { useChat } from '@ai-sdk/react';
import { Copy, MessageSquare, Target, TrendingUp, Globe, Brain, Loader2, Circle } from 'lucide-react';
import { toast } from 'sonner';

// AI Elements imports
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import { Message, MessageContent, MessageAvatar } from '@/components/ai-elements/message';
import {
  PromptInput,
  PromptInputButton,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputTools,
} from '@/components/ai-elements/prompt-input';
import {
  Actions,
  Action,
} from '@/components/ai-elements/actions';
import { Response } from '@/components/ai-elements/response';
import { Loader } from '@/components/ai-elements/loader';
import {
  Sources,
  SourcesTrigger,
  SourcesContent,
  Source,
} from '@/components/ai-elements/sources';
import {
  Tool,
  ToolHeader,
  ToolContent,
  ToolInput,
  ToolOutput,
} from '@/components/ai-elements/tool';

type GaryMessage = {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  createdAt: Date;
  sources?: Array<{
    title: string;
    url: string;
    content?: string;
  }>;
  persona?: string;
  analysis?: string;
  recommendations?: string[];
};

export default function GaryChat() {
  const [webSearch, setWebSearch] = useState(false);
  const formRef = useRef<HTMLFormElement | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  
  const { messages, input, handleInputChange, handleSubmit, isLoading, error, reload } = useChat({
    api: '/api/gary',
    body: {
      webSearch
    },
    onFinish: (message) => {
      if (message.content) {
        toast.success('🎯 Gary Bencivenga analisou sua questão!');
      }
    },
    onError: (error) => {
      console.error('❌ Erro no Gary Chat:', error);
      toast.error('🚨 Ocorreu um erro. Tente novamente.');
    }
  });

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) {
      toast.error('🎯 Parceiro, você precisa digitar algo para o Gary analisar!');
      return;
    }
    handleSubmit(e);
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success('📝 Copy copiado com sucesso!');
    } catch (error) {
      toast.error('Erro ao copiar');
    }
  };

  // Autosize suave do textarea
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 240) + 'px';
  }, [input]);

  // Atalhos globais
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const meta = e.metaKey || e.ctrlKey;
      if (meta && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        textareaRef.current?.focus();
        return;
      }
      if (meta && e.key === 'Enter') {
        e.preventDefault();
        formRef.current?.requestSubmit();
        return;
      }
      if (e.key === 'Escape') {
        if (textareaRef.current && document.activeElement === textareaRef.current) {
          e.preventDefault();
          const ev = { target: { value: '' } } as any;
          handleInputChange(ev);
        }
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [handleInputChange]);

  const lastMessage = messages[messages.length - 1];
  const hasMessages = messages.length > 0;

  const GaryAvatar = () => (
    <div className="w-8 h-8 rounded-full flex items-center justify-center text-foreground font-bold text-sm shadow-lg bg-muted border border-border">
      G
    </div>
  );

  return (
    <div className="flex flex-col h-full min-h-0 bg-background">
      {/* Header */}
      <div className="bg-background border-b border-border px-4 sm:px-6 py-3">
        <div className="mx-auto max-w-3xl flex items-center justify-between">
          <div className="flex items-center gap-3">
            <GaryAvatar />
            <div>
              <h1 className="text-base sm:text-lg font-semibold text-foreground">Gary Bencivenga AI</h1>
              <div className="text-xs sm:text-sm text-muted-foreground flex items-center gap-2">
                {isLoading ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Pensando…</span>
                  </>
                ) : (
                  <>
                    <Circle className="w-3 h-3 text-emerald-500 fill-emerald-500" />
                    <span>Pronto</span>
                  </>
                )}
              </div>
            </div>
          </div>
          <div className="hidden sm:flex items-center space-x-2 text-xs text-muted-foreground">
            <Brain className="w-4 h-4" />
            <span>Powered by Grok</span>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 min-h-0 overflow-hidden">
        {hasMessages ? (
          <Conversation className="h-full">
            <ConversationContent className="h-full px-4 sm:px-6 py-6 overflow-y-auto">
              <div className="mx-auto w-full max-w-3xl">
                {messages.map((message) => (
                  <Message key={message.id} from={message.role as any}>
                    {message.role === 'user' ? (
                      <div className="flex justify-end">
                        <MessageContent className="max-w-[80%] bg-primary text-primary-foreground rounded-2xl px-4 py-3 shadow-sm transition-all hover:shadow-md">
                          <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                        </MessageContent>
                      </div>
                    ) : (
                      <div className="flex justify-start gap-3">
                        <MessageAvatar className="mt-1">
                          <GaryAvatar />
                        </MessageAvatar>
                        <div className="flex-1 max-w-[80%] space-y-3">
                          <MessageContent className="bg-muted text-foreground border border-border rounded-2xl px-4 py-3 shadow-sm transition-all hover:shadow-md">
                            <div className="whitespace-pre-wrap leading-relaxed">
                              {message.content}
                            </div>
                          </MessageContent>

                          <Actions className="justify-start">
                            <Action onClick={() => copyToClipboard(message.content)} variant="ghost" className="hover:bg-accent/60 active:scale-95 transition">
                              <Copy className="w-4 h-4" />
                            </Action>
                          </Actions>
                        </div>
                      </div>
                    )}
                  </Message>
                ))}

                {isLoading && (
                  <Message from="assistant">
                    <div className="flex justify-start gap-3">
                      <MessageAvatar>
                        <GaryAvatar />
                      </MessageAvatar>
                      <MessageContent className="bg-muted border border-border rounded-2xl px-4 py-3 shadow-sm">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <span className="w-2 h-2 rounded-full bg-foreground/60 animate-bounce" />
                          <span className="w-2 h-2 rounded-full bg-foreground/60 animate-bounce [animation-delay:120ms]" />
                          <span className="w-2 h-2 rounded-full bg-foreground/60 animate-bounce [animation-delay:240ms]" />
                        </div>
                      </MessageContent>
                    </div>
                  </Message>
                )}
              </div>
            </ConversationContent>
            <ConversationScrollButton />
          </Conversation>
        ) : (
          <div className="flex-1 flex items-center justify-center p-6">
            <div className="text-center max-w-2xl space-y-6">
              <div className="flex justify-center">
                <GaryAvatar />
              </div>
              <div className="space-y-2">
                <h2 className="text-2xl font-bold text-foreground">🎯 Bem-vindo ao Gary Bencivenga AI</h2>
                <p className="text-muted-foreground">
                  O maior copywriter do mundo está aqui para ajudar você. 
                  Peça para criar copy, analisar estratégias, desenvolver personas ou qualquer coisa relacionada a marketing e conversão.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-background border-t border-border px-4 sm:px-6 py-4">
        <form ref={formRef} onSubmit={handleFormSubmit} className="mx-auto max-w-3xl space-y-3">
          <PromptInput className="bg-input border-border">
            <PromptInputTools>
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="webSearch"
                  checked={webSearch}
                  onChange={(e) => { setWebSearch(e.target.checked); toast.message(e.target.checked ? 'Pesquisa na web ON' : 'Pesquisa na web OFF'); }}
                  className="rounded border-input text-foreground focus:ring-ring"
                />
                <label htmlFor="webSearch" className="text-sm text-muted-foreground flex items-center gap-1">
                  <Globe className="w-4 h-4" />
                  <span>Incluir pesquisa na web</span>
                </label>
              </div>
            </PromptInputTools>
            
            <div className="flex gap-2">
              <PromptInputTextarea
                ref={textareaRef as any}
                value={input}
                onChange={handleInputChange}
                placeholder="Digite sua mensagem para Gary..."
                disabled={isLoading}
                rows={3}
                className="min-h-[60px] transition-[height] duration-200 ease-in-out"
              />
              <PromptInputSubmit status={isLoading ? 'submitted' : 'ready'} disabled={!input.trim() || isLoading} />
            </div>
          </PromptInput>
        </form>
      </div>
    </div>
  );
}