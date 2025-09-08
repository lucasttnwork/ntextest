# AI Elements - Componentes Completos

Este projeto implementa **todos os componentes** da biblioteca AI Elements conforme documentado em [https://ai-sdk.dev/elements/components](https://ai-sdk.dev/elements/components).

## 📦 Componentes Implementados

### ✅ Foundation Components (Base)
- **Actions** - Botões de ação para respostas
- **Conversation** - Container principal da conversa
- **Message** - Componente de mensagem individual
- **PromptInput** - Campo de entrada para prompts
- **Response** - Renderização de respostas com markdown

### ✅ Interactive Elements (Interativos)
- **Branch** - Navegação entre versões de resposta
- **Suggestions** - Sugestões rápidas de entrada
- **Sources** - Lista de fontes consultadas
- **Task** - Gerenciamento de tarefas
- **Tool** - Execução e visualização de ferramentas

### ✅ Content Enhancement (Conteúdo)
- **Code Block** - Blocos de código com syntax highlighting
- **Image** - Exibição de imagens geradas
- **Inline Citation** - Citações inline com tooltips
- **Reasoning** - Processo de raciocínio passo-a-passo
- **Web Preview** - Visualização de páginas web

### ✅ Utility Components (Utilitários)
- **Loader** - Indicadores de carregamento animados

## 🚀 Como Usar

### Importação Completa
```tsx
import {
  Actions,
  Action,
  Conversation,
  Message,
  PromptInput,
  // ... todos os componentes
} from '@/components/ai-elements';
```

### Exemplo Básico de Chat
```tsx
import {
  Conversation,
  ConversationContent,
  Message,
  MessageContent,
  PromptInput,
  Response
} from '@/components/ai-elements';

function ChatInterface() {
  return (
    <Conversation>
      <ConversationContent>
        <Message from="user">
          <MessageContent>
            <Response>Olá, como posso ajudar?</Response>
          </MessageContent>
        </Message>
        <Message from="assistant">
          <MessageContent>
            <Response>Estou aqui para ajudar!</Response>
          </MessageContent>
        </Message>
      </ConversationContent>

      <PromptInput onSubmit={handleSubmit}>
        <PromptInputTextarea placeholder="Digite sua mensagem..." />
        <PromptInputToolbar>
          <PromptInputSubmit />
        </PromptInputToolbar>
      </PromptInput>
    </Conversation>
  );
}
```

### Exemplo com Reasoning
```tsx
import { Reasoning, ReasoningTrigger, ReasoningContent } from '@/components/ai-elements';

function ThinkingProcess() {
  return (
    <Reasoning isStreaming={true}>
      <ReasoningTrigger />
      <ReasoningContent>
        Estou analisando sua solicitação e processando a resposta...
      </ReasoningContent>
    </Reasoning>
  );
}
```

### Exemplo com Code Block
```tsx
import { CodeBlock, CodeBlockCopyButton } from '@/components/ai-elements';

function CodeExample() {
  return (
    <CodeBlock
      code={`function hello() { return 'world'; }`}
      language="javascript"
      showLineNumbers
    >
      <CodeBlockCopyButton />
    </CodeBlock>
  );
}
```

### Exemplo com Sources
```tsx
import { Sources, SourcesTrigger, SourcesContent, Source } from '@/components/ai-elements';

function SourcesExample() {
  return (
    <Sources>
      <SourcesTrigger count={2} />
      <SourcesContent>
        <Source href="https://example.com" title="Fonte 1" />
        <Source href="https://example2.com" title="Fonte 2" />
      </SourcesContent>
    </Sources>
  );
}
```

## 🎨 Personalização

Todos os componentes suportam:
- **Classes CSS customizadas** via prop `className`
- **Themes** (light/dark mode)
- **Responsive design**
- **Acessibilidade** (ARIA attributes, keyboard navigation)

## 📚 Documentação Detalhada

Cada componente possui documentação completa com:
- API completa
- Exemplos de uso
- Props disponíveis
- Casos de uso recomendados

## 🧪 Demonstração

Para ver todos os componentes funcionando, importe o componente de demonstração:

```tsx
import AIElementsDemo from '@/components/ai-elements-demo';
```

## ✅ Status da Implementação

| Componente | Status | Descrição |
|------------|--------|-----------|
| Actions | ✅ | Botões de ação implementados |
| Branch | ✅ | Navegação entre branches funcionando |
| Code Block | ✅ | Syntax highlighting e cópia funcionando |
| Conversation | ✅ | Container de conversa completo |
| Image | ✅ | Exibição de imagens base64 |
| Inline Citation | ✅ | Citações com tooltips e carrossel |
| Loader | ✅ | Animações de carregamento |
| Message | ✅ | Mensagens com avatares |
| Prompt Input | ✅ | Input completo com toolbar |
| Reasoning | ✅ | Processo de raciocínio expansível |
| Response | ✅ | Renderização com markdown |
| Sources | ✅ | Lista de fontes consultadas |
| Suggestion | ✅ | Sugestões rápidas |
| Task | ✅ | Gerenciamento de tarefas |
| Tool | ✅ | Execução de ferramentas |
| Web Preview | ✅ | Preview de páginas web |

**Total: 16 componentes implementados e funcionando!** 🎉

## 🔧 Desenvolvimento

Para adicionar novos componentes:
1. Criar arquivo em `src/components/ai-elements/`
2. Seguir padrões de nomenclatura da documentação
3. Adicionar ao arquivo `index.ts`
4. Atualizar demonstração se necessário

## 📖 Referências

- [Documentação Oficial AI Elements](https://ai-sdk.dev/elements/components)
- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org)
