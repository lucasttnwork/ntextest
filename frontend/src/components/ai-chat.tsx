'use client';

import { Fragment } from 'react';
import { useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { GlobeIcon, RefreshCcwIcon, CopyIcon } from 'lucide-react';

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
  Reasoning,
  ReasoningTrigger,
  ReasoningContent,
} from '@/components/ai-elements/reasoning';
import {
  Sources,
  SourcesTrigger,
  SourcesContent,
  Source,
} from '@/components/ai-elements/sources';
import {
  Suggestions,
  Suggestion,
} from '@/components/ai-elements/suggestion';
import {
  Tool,
  ToolHeader,
  ToolContent,
  ToolInput,
  ToolOutput,
} from '@/components/ai-elements/tool';

const ChatBotDemo = () => {
  const [input, setInput] = useState('');
  const [webSearch, setWebSearch] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [currentTool, setCurrentTool] = useState<string | null>(null);
  const { messages, sendMessage, isLoading } = useChat();

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      setIsThinking(true);
      if (webSearch) setCurrentTool('web-search');
      // habilita streaming + webSearch
      sendMessage(input, { webSearch, stream: true });
      setInput('');
      // Simulate thinking delay
      setTimeout(() => {
        setIsThinking(false);
        setCurrentTool(null);
      }, 3000);
    }
  };

  const handleRegenerate = () => {
    // Por enquanto, apenas limpa a entrada para nova mensagem
    setInput('');
  };

  return (
    <div className="max-w-4xl mx-auto p-6 relative size-full h-screen">
      <div className="flex flex-col h-full">
        {/* Reasoning Component */}
        <Reasoning isStreaming={isThinking} className="mb-4">
          <ReasoningTrigger />
          <ReasoningContent>
            Analisando sua solicitação e preparando a melhor resposta baseada nas técnicas de copywriting de Gary Bencivenga...
          </ReasoningContent>
        </Reasoning>

        {/* Tool Execution Visualization */}
        {currentTool === 'web-search' && (
          <Tool className="mb-4">
            <ToolHeader type="tool-web-search" state="input-streaming" />
            <ToolContent>
              <ToolInput input={{ query: input, engine: 'tavily' }} />
              <ToolOutput output="Executando busca na web..." errorText={undefined} />
            </ToolContent>
          </Tool>
        )}

        <Conversation className="h-full">
          <ConversationContent>
            {messages.map((message) => (
              <Fragment key={message.id}>
                <Message from={message.role}>
                  <MessageAvatar
                    src={message.role === 'user' ? '/user-avatar.svg' : '/gary-avatar.svg'}
                    name={message.role === 'user' ? 'Você' : 'Gary'}
                  />
                  <MessageContent>
                    <Response>
                      {message.content || 'Mensagem sem conteúdo'}
                    </Response>
                  </MessageContent>
                </Message>
                {message.role === 'assistant' && message.id === messages.at(-1)?.id && (
                  <Actions className="mt-2">
                    <Action
                      onClick={handleRegenerate}
                      tooltip="Regenerar resposta"
                      label="Retry"
                    >
                      <RefreshCcwIcon className="size-3" />
                    </Action>
                    <Action
                      onClick={() =>
                        navigator.clipboard.writeText(message.content || '')
                      }
                      tooltip="Copiar resposta"
                      label="Copy"
                    >
                      <CopyIcon className="size-3" />
                    </Action>
                  </Actions>
                )}
                {message.role === 'assistant' && message.sources && message.sources.length > 0 && (
                  <Sources className="mt-2">
                    <SourcesTrigger count={message.sources.length} />
                    <SourcesContent>
                      {message.sources.map((s: any, idx: number) => (
                        <Source key={idx} href={s.url} title={s.title}>
                          {s.description || s.url}
                        </Source>
                      ))}
                    </SourcesContent>
                  </Sources>
                )}
              </Fragment>
            ))}
            {isLoading && (
              <div className="px-4 py-2">
                <Loader />
              </div>
            )}
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>

        {/* Sources (placeholder; será populado quando houver URLs reais) */}
        {messages.length > 0 && (
          <Sources className="mt-4">
            <SourcesTrigger count={0} />
            <SourcesContent />
          </Sources>
        )}

        {/* Suggestions Component */}
        <Suggestions className="mt-4">
          <Suggestion suggestion="Como criar um anúncio persuasivo?" />
          <Suggestion suggestion="Técnicas de headline poderosas" />
          <Suggestion suggestion="Copy para landing page" />
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
  );
};

export default ChatBotDemo;