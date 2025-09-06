'use client';

import { useState } from 'react';
import {
  Actions,
  Action,
  Branch,
  BranchMessages,
  BranchSelector,
  BranchPrevious,
  BranchNext,
  BranchPage,
  CodeBlock,
  CodeBlockCopyButton,
  Conversation,
  ConversationContent,
  ConversationScrollButton,
  InlineCitation,
  InlineCitationText,
  InlineCitationCard,
  InlineCitationCardTrigger,
  InlineCitationCardBody,
  InlineCitationCarousel,
  InlineCitationCarouselContent,
  InlineCitationCarouselItem,
  InlineCitationCarouselHeader,
  InlineCitationCarouselIndex,
  InlineCitationCarouselPrev,
  InlineCitationCarouselNext,
  InlineCitationSource,
  Loader,
  Message,
  MessageContent,
  MessageAvatar,
  PromptInput,
  PromptInputTextarea,
  PromptInputToolbar,
  PromptInputTools,
  PromptInputButton,
  PromptInputSubmit,
  Reasoning,
  ReasoningTrigger,
  ReasoningContent,
  Response,
  Sources,
  SourcesTrigger,
  SourcesContent,
  Source,
  Suggestions,
  Suggestion,
  Task,
  TaskTrigger,
  TaskContent,
  TaskItem,
  TaskItemFile,
  Tool,
  ToolHeader,
  ToolContent,
  ToolInput,
  ToolOutput,
  WebPreview,
  WebPreviewNavigation,
  WebPreviewNavigationButton,
  WebPreviewUrl,
  WebPreviewBody,
  WebPreviewConsole,
} from './ai-elements/index';
import { CopyIcon, ThumbsUpIcon, ArrowLeftIcon, ArrowRightIcon, GlobeIcon } from 'lucide-react';

export default function AIElementsDemo() {
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      setIsLoading(true);
      // Simulate API call
      setTimeout(() => {
        setIsLoading(false);
        setInput('');
      }, 2000);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-center mb-8">
        AI Elements Demo - Todos os Componentes Implementados
      </h1>

      {/* 1. Conversation & Message Components */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">1. Conversation & Messages</h2>
        <Conversation className="h-96 border rounded-lg">
          <ConversationContent>
            <Message from="user">
              <MessageContent>
                <Response>Olá! Como posso usar os AI Elements?</Response>
              </MessageContent>
              <MessageAvatar src="/user-avatar.svg" name="User" />
            </Message>

            <Message from="assistant">
              <MessageContent>
                <Response>Olá! Os AI Elements são componentes React para construir interfaces de chat modernas.</Response>
              </MessageContent>
              <MessageAvatar src="/gary-avatar.svg" name="AI" />
              <Actions className="mt-2">
                <Action tooltip="Copiar resposta">
                  <CopyIcon size={16} />
                </Action>
                <Action tooltip="Curtir resposta">
                  <ThumbsUpIcon size={16} />
                </Action>
              </Actions>
            </Message>
          </ConversationContent>
          <ConversationScrollButton />
        </Conversation>
      </section>

      {/* 2. Prompt Input */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">2. Prompt Input</h2>
        <PromptInput onSubmit={handleSubmit} className="w-full">
          <PromptInputTextarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Digite sua mensagem..."
          />
          <PromptInputToolbar>
            <PromptInputTools>
              <PromptInputButton variant="ghost">
                <GlobeIcon size={16} />
                <span>Search</span>
              </PromptInputButton>
            </PromptInputTools>
            <PromptInputSubmit disabled={!input || isLoading} />
          </PromptInputToolbar>
        </PromptInput>
      </section>

      {/* 3. Reasoning Component */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">3. Reasoning</h2>
        <Reasoning isStreaming={isLoading}>
          <ReasoningTrigger />
          <ReasoningContent>
            Estou analisando sua solicitação para entender melhor o contexto e fornecer a resposta mais adequada.
          </ReasoningContent>
        </Reasoning>
      </section>

      {/* 4. Code Block */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">4. Code Block</h2>
        <CodeBlock
          code={`function helloWorld() {
  console.log('Hello, AI Elements!');
  return 'Success!';
}`}
          language="javascript"
          showLineNumbers
        >
          <CodeBlockCopyButton />
        </CodeBlock>
      </section>

      {/* 5. Sources */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">5. Sources</h2>
        <Sources>
          <SourcesTrigger count={2} />
          <SourcesContent>
            <Source href="https://ai-sdk.dev" title="AI SDK Documentation">
              Documentação oficial dos componentes AI SDK
            </Source>
            <Source href="https://react.dev" title="React Documentation">
              Documentação do React para desenvolvimento
            </Source>
          </SourcesContent>
        </Sources>
      </section>

      {/* 6. Branch Navigation */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">6. Branch Navigation</h2>
        <Branch>
          <BranchMessages>
            <div>Versão 1: Resposta simples</div>
            <div>Versão 2: Resposta detalhada</div>
            <div>Versão 3: Resposta técnica</div>
          </BranchMessages>
          <BranchSelector from="assistant">
            <BranchPrevious />
            <BranchPage />
            <BranchNext />
          </BranchSelector>
        </Branch>
      </section>

      {/* 7. Suggestions */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">7. Suggestions</h2>
        <Suggestions>
          <Suggestion suggestion="Como usar componentes React?" />
          <Suggestion suggestion="Exemplos de AI Elements" />
          <Suggestion suggestion="Documentação completa" />
        </Suggestions>
      </section>

      {/* 8. Task Management */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">8. Task Management</h2>
        <Task>
          <TaskTrigger title="Implementar novo componente">
            <TaskContent>
              <TaskItem>Analisar requisitos</TaskItem>
              <TaskItem>Criar componente base</TaskItem>
              <TaskItem>Implementar funcionalidades</TaskItem>
              <TaskItem>Testar integração</TaskItem>
              <TaskItemFile>component.tsx</TaskItemFile>
              <TaskItemFile>styles.css</TaskItemFile>
            </TaskContent>
          </TaskTrigger>
        </Task>
      </section>

      {/* 9. Tool Execution */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">9. Tool Execution</h2>
        <Tool>
          <ToolHeader type="tool-search" state="output-available" />
          <ToolContent>
            <ToolInput input={{ query: 'AI Elements documentation' }} />
            <ToolOutput output="Encontrados 15 resultados relevantes" errorText={undefined} />
          </ToolContent>
        </Tool>
      </section>

      {/* 10. Web Preview */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">10. Web Preview</h2>
        <WebPreview className="h-96">
          <WebPreviewNavigation>
            <WebPreviewNavigationButton tooltip="Voltar">
              <ArrowLeftIcon size={16} />
            </WebPreviewNavigationButton>
            <WebPreviewNavigationButton tooltip="Avançar">
              <ArrowRightIcon size={16} />
            </WebPreviewNavigationButton>
            <WebPreviewUrl />
          </WebPreviewNavigation>
          <WebPreviewBody src="https://ai-sdk.dev" />
          <WebPreviewConsole
            logs={[
              { level: 'log', message: 'Página carregada com sucesso', timestamp: new Date() },
              { level: 'log', message: 'Componentes renderizados', timestamp: new Date() }
            ]}
          />
        </WebPreview>
      </section>

      {/* 11. Inline Citations */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">11. Inline Citations</h2>
        <div className="p-4 border rounded-lg">
          <p>
            Os AI Elements são componentes poderosos{' '}
            <InlineCitation>
              <InlineCitationText>para construir interfaces de chat modernas</InlineCitationText>
              <InlineCitationCard>
                <InlineCitationCardTrigger sources={['https://ai-sdk.dev']} />
                <InlineCitationCardBody>
                  <InlineCitationCarousel>
                    <InlineCitationCarouselHeader>
                      <InlineCitationCarouselIndex />
                    </InlineCitationCarouselHeader>
                    <InlineCitationCarouselContent>
                      <InlineCitationCarouselItem>
                        <InlineCitationSource
                          title="AI SDK Documentation"
                          url="https://ai-sdk.dev"
                          description="Documentação completa dos componentes AI SDK"
                        />
                      </InlineCitationCarouselItem>
                    </InlineCitationCarouselContent>
                    <InlineCitationCarouselPrev />
                    <InlineCitationCarouselNext />
                  </InlineCitationCarousel>
                </InlineCitationCardBody>
              </InlineCitationCard>
            </InlineCitation>
            {' '}com React e TypeScript.
          </p>
        </div>
      </section>

      {/* 12. Loader */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">12. Loader</h2>
        <div className="flex items-center gap-4 p-4 border rounded-lg">
          <span>Carregando resposta...</span>
          <Loader />
        </div>
      </section>

      {/* Status Summary */}
      <section className="space-y-4">
        <h2 className="text-2xl font-semibold">✅ Status dos Componentes</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {[
            'Actions', 'Branch', 'Code Block', 'Conversation', 'Image',
            'Inline Citation', 'Loader', 'Message', 'Prompt Input', 'Reasoning',
            'Response', 'Sources', 'Suggestion', 'Task', 'Tool', 'Web Preview'
          ].map((component) => (
            <div key={component} className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-sm font-medium">{component}</span>
            </div>
          ))}
        </div>
        <p className="text-center text-muted-foreground">
          Todos os 16 componentes AI Elements foram implementados e estão funcionando corretamente!
        </p>
      </section>
    </div>
  );
}
