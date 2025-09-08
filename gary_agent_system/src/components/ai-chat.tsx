'use client';

import { Fragment, useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { GlobeIcon, RefreshCcwIcon, CopyIcon, Menu, X } from 'lucide-react';

// Import AI Elements components correctly
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
  Suggestions,
  Suggestion,
} from '@/components/ai-elements/suggestion';
import {
  Sources,
  SourcesTrigger,
  SourcesContent,
  Source,
} from '@/components/ai-elements/sources';
import {
  Reasoning,
  ReasoningTrigger,
  ReasoningContent,
} from '@/components/ai-elements/reasoning';
import {
  Tool,
  ToolHeader,
  ToolContent,
  ToolInput,
  ToolOutput,
} from '@/components/ai-elements/tool';
import { ChatSidebar } from '@/components/chat-sidebar';
import { Button } from '@/components/ui/button';

const ChatBotDemo = () => {
  const [input, setInput] = useState('');
  const [webSearch, setWebSearch] = useState(false);
  const [thinkingBullets, setThinkingBullets] = useState<string[]>([]);
  const [currentTool, setCurrentTool] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const {
    messages,
    aiMessages,
    sendMessage,
    isLoading,
    currentSessionId,
    loadSession,
    clearChat
  } = useChat();

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      // gerar pensamento crítico básico baseado no prompt do usuário
      const bullets = [
        `Contexto: ${input.slice(0, 120)}`,
        'Objetivo: gerar resposta clara e persuasiva',
        'Foco: abordar intenção do usuário com CTA quando aplicável',
        'Riscos: evitar afirmações não verificadas'
      ];
      setThinkingBullets(bullets);
      if (webSearch) setCurrentTool('web-search');

      // enviar mensagem usando AI SDK (stream gerenciado pelo hook)
      sendMessage(input, { webSearch });
      setInput('');
    }
  };

  const handleRegenerate = () => {
    // Por enquanto, apenas limpa a entrada para nova mensagem
    setInput('');
  };

  const handleSessionSelect = (sessionId: string) => {
    loadSession();
    setSidebarOpen(false);
  };

  const handleNewChat = () => {
    clearChat();
    setInput('');
    setSidebarOpen(false);
  };

  return (
    <div className="flex h-full bg-background">
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-80 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}>
        <ChatSidebar
          currentSessionId={currentSessionId}
          onSessionSelect={handleSessionSelect}
          onNewChat={handleNewChat}
        />
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 min-h-0">
        {/* Mobile header */}
        <div className="lg:hidden flex items-center justify-between p-4 border-b border-border">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setSidebarOpen(true)}
            className="text-muted-foreground hover:text-foreground"
          >
            <Menu className="h-5 w-5" />
          </Button>
          <h1 className="text-lg font-semibold text-foreground">
            Gary Bencivenga
          </h1>
          <div className="w-9" /> {/* Spacer for centering */}
        </div>

        <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-4 lg:p-6 min-h-0 overflow-hidden">
        {/* Reasoning Component */}
        {/* Reasoning: aparece quando está carregando ou quando há pensamento do Gary */}
        {isLoading && (
          <Reasoning isStreaming={true} open={true} defaultOpen={true} className="mb-4">
            <ReasoningTrigger />
            <ReasoningContent>
              {thinkingBullets.length > 0 ? thinkingBullets.join('\n') : 'Gary Bencivenga está analisando sua solicitação com sua expertise incomparável...'}
            </ReasoningContent>
          </Reasoning>
        )}

        {/* Tool Execution Visualization */}
        {currentTool === 'web-search' && isLoading && (
          <Tool className="mb-4">
            <ToolHeader type="tool-web-search" state="input-streaming" />
            <ToolContent>
              <ToolInput input={{ query: input, engine: 'perplexity' }} />
              <ToolOutput output="Gary está pesquisando informações atualizadas para criar um copy ainda mais poderoso..." errorText={undefined} />
            </ToolContent>
          </Tool>
        )}

        <Conversation>
          <ConversationContent>
            {aiMessages.map((message) => (
              <Message from={message.role} key={message.id}>
                <MessageAvatar
                  src={message.role === 'user' ? '/user-avatar.svg' : '/gary-avatar.svg'}
                  name={message.role === 'user' ? 'Você' : 'Gary'}
                />
                <MessageContent>
                  {message.parts?.map((part: any, i: number) => {
                    switch (part.type) {
                      case 'text':
                        return (
                          <Response key={`${message.id}-${i}`}>
                            {('text' in part && (part as any).text) || ''}
                          </Response>
                        );
                      case 'reasoning':
                        return (
                          <Reasoning
                            key={`${message.id}-${i}`}
                            className="w-full"
                            isStreaming={isLoading && i === (message.parts?.length || 1) - 1 && message.id === aiMessages.at(-1)?.id}
                          >
                            <ReasoningTrigger />
                            <ReasoningContent>{('text' in part && (part as any).text) || ''}</ReasoningContent>
                          </Reasoning>
                        );
                      case 'source-url':
                        // fontes são renderizadas abaixo em bloco único
                        return null;
                      default:
                        return null;
                    }
                  })}

                  {/* Sources (lista única por mensagem) */}
                  {message.role === 'assistant' && message.parts?.some((p: any) => p.type === 'source-url') && (
                    <Sources className="mt-2">
                      <SourcesTrigger count={message.parts.filter((p: any) => p.type === 'source-url').length} />
                      <SourcesContent>
                        {message.parts
                          .filter((p: any) => p.type === 'source-url')
                          .map((p: any, idx: number) => (
                            <Source key={`${message.id}-src-${idx}`} href={p.url} title={p.url}>
                              {p.url}
                            </Source>
                          ))}
                      </SourcesContent>
                    </Sources>
                  )}
                </MessageContent>
                {/* Actions for assistant messages (última mensagem) */}
                {message.role === 'assistant' && message.id === aiMessages.at(-1)?.id && (
                  <Actions className="mt-2">
                    <Action
                      onClick={() => setInput('')}
                      tooltip="Regenerar resposta"
                      label="Retry"
                    >
                      <RefreshCcwIcon className="size-3" />
                    </Action>
                    <Action
                      onClick={() => {
                        const text = (() => {
                          const p = message.parts?.find((p: any) => p.type === 'text');
                          return p && 'text' in p ? (p as any).text : '';
                        })();
                        navigator.clipboard.writeText(text);
                      }}
                      tooltip="Copiar resposta"
                      label="Copy"
                    >
                      <CopyIcon className="size-3" />
                    </Action>
                  </Actions>
                )}
              </Message>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="px-4 py-2">
                <Loader />
              </div>
            )}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>


        {/* Suggestions Component */}
        <Suggestions className="mt-4">
          <Suggestion suggestion="Como criar um anúncio que converte?" />
          <Suggestion suggestion="Técnicas de headline que vendem" />
          <Suggestion suggestion="Copy para página de vendas" />
          <Suggestion suggestion="Análise de público-alvo para copy" />
          <Suggestion suggestion="Estratégias de urgência e escassez" />
        </Suggestions>

        <PromptInput onSubmit={handleFormSubmit} className="mt-4">
          <PromptInputTextarea
            onChange={(e) => setInput(e.target.value)}
            value={input}
            placeholder="Digite sua mensagem para Gary..."
          />
          <PromptInputToolbar>
            <PromptInputTools>
              <PromptInputButton
                variant={webSearch ? 'default' : 'ghost'}
                onClick={() => setWebSearch(!webSearch)}
              >
                <GlobeIcon size={16} />
                <span>Search</span>
              </PromptInputButton>
            </PromptInputTools>
            <PromptInputSubmit disabled={!input || isLoading} />
          </PromptInputToolbar>
        </PromptInput>
        </div>
      </div>
    </div>
  );
};

export default ChatBotDemo;