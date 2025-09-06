# NTEX Frontend - Gary Bencivenga Agent

## 🎯 Visão Geral

Interface frontend moderna para o sistema NTEX, construída com Next.js, TypeScript, AI SDK 5 e AI Elements. Permite interação direta com o Gary Bencivenga Agent através de uma interface de chat intuitiva.

## 🚀 Tecnologias Utilizadas

- **Next.js 14** - Framework React com App Router
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização utilitária
- **AI SDK 5** - Framework para integração com modelos de IA
- **AI Elements** - Componentes de UI para interfaces de IA
- **shadcn/ui** - Biblioteca de componentes acessíveis
- **Lucide React** - Ícones modernos

## 🏗️ Arquitetura

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx      # Layout principal
│   │   └── page.tsx        # Página inicial
│   ├── components/         # Componentes React
│   │   ├── ChatInterface.tsx # Interface principal do chat
│   │   └── ai-elements/    # Componentes AI Elements
│   ├── hooks/              # Hooks customizados
│   │   └── useChat.ts      # Hook para gerenciamento do chat
│   ├── services/           # Serviços de API
│   │   └── api.ts          # Cliente para API Flask
│   ├── types/              # Tipos TypeScript
│   │   └── chat.ts         # Tipos do chat
│   └── lib/                # Utilitários
│       └── utils.ts        # Funções utilitárias
```

## 🎨 Componentes Principais

### ChatInterface
Componente principal que integra:
- **Conversation**: Container principal do chat
- **Message**: Mensagens individuais com avatares
- **PromptInput**: Campo de entrada com submit
- **Loader**: Indicador de carregamento
- Estados de loading e error handling

### useChat Hook
Gerencia o estado do chat:
- Envio de mensagens
- Recebimento de respostas
- Gerenciamento de sessões
- Estados de loading e erro

### NTEXApiService
Cliente para integração com backend Flask:
- `sendMessage()`: Enviar mensagens para Gary
- `getSessions()`: Listar sessões
- `getSession()`: Obter detalhes de sessão
- `closeSession()`: Fechar sessão

## 🔧 Como Executar

### Pré-requisitos
- Node.js 18+
- Backend NTEX rodando (Flask + PostgreSQL)

### Instalação
```bash
cd frontend
npm install
```

### Configuração
1. **Variáveis de Ambiente**:
   ```bash
   cp .env.example .env.local
   ```

   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:5003
   ```

2. **Executar Frontend**:
   ```bash
   npm run dev
   ```

   Acesse: http://localhost:3000

### Executar Sistema Completo
```bash
# Terminal 1: Banco de dados
cd /Users/lucasttn/Documents/Documents/Cérebro\ NTEX
docker-compose up -d

# Terminal 2: Backend Flask
cd agno_agents
python3 chat_interface.py

# Terminal 3: Frontend Next.js
cd frontend
npm run dev
```

## 🎯 Funcionalidades Implementadas

### ✅ Interface de Chat
- Conversação em tempo real com Gary Bencivenga
- Interface responsiva mobile-first
- Avatares personalizados
- Tema claro/escuro automático

### ✅ Gerenciamento de Estado
- Hook customizado `useChat`
- Estados de loading e erro
- Scroll automático para novas mensagens
- Limpeza de chat

### ✅ Integração com Backend
- API REST completa
- Tratamento de erros
- Sessões persistentes
- Streaming de respostas (preparado)

### ✅ UX Moderna
- Componentes AI Elements
- Animações suaves
- Loading states
- Error handling intuitivo

## 🔄 API Endpoints Utilizados

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/chat` | POST | Enviar mensagem para Gary |
| `/api/sessions` | GET | Listar sessões |
| `/api/sessions/:id` | GET | Obter sessão específica |
| `/api/sessions/:id/close` | POST | Fechar sessão |
| `/api/agents/status` | GET | Status dos agentes |

## 📱 Interface Responsiva

- **Desktop**: Layout completo com sidebar opcional
- **Tablet**: Interface adaptada
- **Mobile**: Interface touch-friendly

## 🎨 Personalização

### Tema
- Baseado em Tailwind CSS
- Variáveis CSS customizáveis
- Suporte a dark mode

### Componentes
- AI Elements customizáveis
- shadcn/ui consistente
- Ícones Lucide React

## 🐛 Debugging

### Logs
- Console do navegador para erros frontend
- Logs do backend Flask
- Network tab para requests API

### Troubleshooting
1. **Erro de conexão**: Verificar se backend está rodando
2. **CORS errors**: Verificar configurações Flask
3. **Build errors**: Verificar dependências instaladas

## 📊 Performance

- **Lazy loading**: Componentes carregados sob demanda
- **Code splitting**: Bundle otimizado
- **Caching**: API responses cacheadas
- **Optimistic UI**: Updates imediatos

## 🔐 Segurança

- Variáveis de ambiente para configuração
- Validação de inputs
- Sanitização de dados
- Error boundaries

## 🚀 Próximos Passos

- [ ] Implementar streaming em tempo real
- [ ] Adicionar histórico de conversas
- [ ] Suporte a múltiplas sessões simultâneas
- [ ] Integração com autenticação
- [ ] Notificações push
- [ ] Export de conversas

---

**🎯 Status**: ✅ **Frontend Completo e Funcional**

O frontend está totalmente integrado com o backend existente e pronto para uso em produção.
