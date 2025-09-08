# 🚀 NTEX - Interface Moderna de Agentes IA

Interface React moderna e minimalista para os agentes de IA da NTEX, inspirada no design do ChatGPT com estilo Apple.

## ✨ Características

- **Interface Moderna**: Design limpo e minimalista estilo Apple
- **React 18 + TypeScript**: Stack moderna e robusta
- **Tailwind CSS**: Estilização utilitária e responsiva
- **Zustand**: Gerenciamento de estado simples e eficiente
- **Heroicons**: Ícones consistentes e bonitos
- **Responsivo**: Funciona perfeitamente em desktop e mobile

## 🛠️ Stack Tecnológica

- **Frontend**: React 18 + TypeScript 5.3 + Vite
- **Estilização**: Tailwind CSS 3.4 + Headless UI
- **Estado**: Zustand + React Hooks
- **Ícones**: Heroicons (Outline + Solid)
- **Build**: Vite (rápido e moderno)

## 📦 Instalação

### 1. Instalar dependências
```bash
npm install
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 3. Iniciar servidor de desenvolvimento
```bash
npm run dev
```

A interface estará disponível em: http://localhost:3000

## 🏗️ Estrutura do Projeto

```
src/
├── components/          # Componentes React
│   ├── Sidebar.tsx     # Barra lateral com navegação
│   ├── ChatArea.tsx    # Área principal do chat
│   ├── Message.tsx     # Componente de mensagem
│   └── ChatInput.tsx   # Input para envio de mensagens
├── stores/             # Gerenciamento de estado
│   └── chatStore.ts    # Store Zustand para chat
├── services/           # Serviços de API
│   └── chatService.ts  # Comunicação com backend
├── App.tsx             # Componente principal
└── main.tsx            # Ponto de entrada
```

## 🔧 Configuração

### Backend Flask
A interface se comunica com o servidor Flask existente na porta 5003. Certifique-se de que está rodando:

```bash
cd agno_agents
python3 working_chat_interface.py
```

### Proxy de Desenvolvimento
O Vite está configurado para fazer proxy das chamadas `/api` para o Flask:

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5003',
      changeOrigin: true
    }
  }
}
```

## 🎨 Personalização

### Cores e Tema
Edite `tailwind.config.js` para personalizar:

```javascript
theme: {
  extend: {
    colors: {
      primary: { /* suas cores */ },
      chat: { /* cores do chat */ },
      agent: { /* cores dos agentes */ }
    }
  }
}
```

### Componentes
Todos os componentes são modulares e podem ser facilmente customizados:

- **Sidebar**: Navegação e ações rápidas
- **ChatArea**: Área principal de conversação
- **Message**: Exibição de mensagens
- **ChatInput**: Input de texto

## 🚀 Deploy

### Build de Produção
```bash
npm run build
```

### Preview da Build
```bash
npm run preview
```

## 📱 Responsividade

A interface é totalmente responsiva e funciona em:

- **Desktop**: Layout completo com sidebar
- **Tablet**: Sidebar colapsável
- **Mobile**: Interface otimizada para touch

## 🔌 Integração com Agentes

A interface se integra com a arquitetura de agentes existente:

- **Master Agent**: Coordenação e estratégia
- **Copy Agent**: Criação de conteúdo
- **Design Agent**: Elementos visuais
- **Analytics Agent**: Dashboards e relatórios
- **Support Agent**: Atendimento e suporte

## 🐛 Troubleshooting

### Problemas Comuns

1. **Porta 3000 ocupada**
   ```bash
   # Usar outra porta
   npm run dev -- --port 3001
   ```

2. **Erro de CORS**
   - Verificar se o Flask está rodando na porta 5003
   - Confirmar configuração do proxy no Vite

3. **Dependências não encontradas**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

## 📚 Recursos Adicionais

- **Hot Reload**: Mudanças refletem instantaneamente
- **TypeScript**: Tipagem estática para melhor desenvolvimento
- **ESLint**: Linting automático de código
- **DevTools**: Integração com Redux DevTools para debug

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é parte do sistema NTEX e segue as mesmas diretrizes de licenciamento.

---

**Desenvolvido com ❤️ pela equipe NTEX**
