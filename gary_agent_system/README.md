# 🚀 Sistema Gary Bencivenga - Agente de Copywriting IA

Sistema completo e organizado para o agente Gary Bencivenga, especialista em copywriting profissional usando a metodologia comprovada de Gary Bencivenga com interface de chat moderna.

## 📁 Estrutura do Projeto

```
gary_agent_system/
├── agent_core/           # Núcleo do agente de IA
│   ├── agents/           # Implementações dos agentes Python
│   └── agno_agents/      # Sistema Agno com integrações
├── frontend/             # Interface web Next.js
│   ├── src/              # Código fonte React/TypeScript
│   └── gary-bencivenga-chat/ # Versão específica do chat
├── backend/              # API FastAPI
│   └── main.py           # Servidor principal
├── prompts/              # Prompts e configurações do agente
├── scripts/              # Scripts de automação e setup
├── docs/                 # Documentação completa
├── config/               # Configurações e schema do banco
│   └── sql/              # Scripts SQL
├── tests/                # Arquivos de teste e demonstração
└── docker-compose.yml    # Configuração Docker
```

## 🎯 Funcionalidades Principais

- 🤖 **Agente Especializado**: Gary Bencivenga com metodologia de 4 fases
- 💾 **Persistência Completa**: PostgreSQL para conversas e dados
- 🔍 **Busca Web Integrada**: Tavily API para pesquisa atualizada
- 📱 **Interface Moderna**: Next.js com ShadCN UI
- 🐳 **Docker Ready**: Ambiente containerizado completo
- ⚡ **Streaming**: Respostas em tempo real (futuro)

## 🚀 Início Rápido

### 1. Pré-requisitos

- **Docker & Docker Compose**
- **Python 3.10+**
- **Node.js 18+**
- **Git**

### 2. Configuração

```bash
# 1. Entrar no diretório
cd gary_agent_system

# 2. Configurar ambiente
cp config/config.env.example config/.env

# 3. Editar .env com suas chaves API
nano config/.env
```

### 3. Executar Sistema

```bash
# Opção 1: Script automatizado (recomendado)
python scripts/start_gary_system.py

# Ou manualmente:
# Terminal 1: Docker services
docker-compose up -d

# Terminal 2: Backend
cd backend && python -m uvicorn main:app --reload

# Terminal 3: Frontend
cd frontend && npm run dev
```

### 4. Acessar

- **🎨 Frontend**: http://localhost:3000
- **📡 Backend API**: http://localhost:8000
- **📚 Documentação API**: http://localhost:8000/docs
- **🗄️ PgAdmin**: http://localhost:8080

## 🔧 Configuração das APIs

Edite o arquivo `config/.env`:

```env
# OpenRouter (para IA)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_MODEL=x-ai/grok-code-fast-1

# Tavily (para busca web)
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ntex_db
DB_USER=ntex_user
DB_PASSWORD=ntex_password
```

## 📱 Como Usar

### Interface do Chat

1. **Barra Lateral**: Navegue entre conversas
2. **Nova Conversa**: Clique "+" para iniciar
3. **Busca Web**: Use 🌐 para pesquisa
4. **Mensagens**: Digite normalmente

### Metodologia Gary Bencivenga

O agente segue 4 fases comprovadas:

#### Fase 1: Pesquisa
- Coleta informações sobre projeto, público, concorrência

#### Fase 2: Ideação
- Matriz de ângulos persuasivos
- Banco de 25 headlines
- Arquitetura da peça

#### Fase 3: Rascunho
- Estrutura completa: Abertura → Aliança → Benefícios → Provas → Oferta → CTA
- Bullets de fascinação
- Cada parágrafo responde uma objeção

#### Fase 4: Lapidação
- Scorecard de qualidade (0-10)
- Regra dos 3 cortes
- Otimizações finais

## 🏗️ Desenvolvimento

### Estrutura Detalhada

```
├── agent_core/
│   ├── agents/copywriter_agent_bencivenga.py  # Agente principal
│   ├── agents/copywriter_agent.py             # Versão alternativa
│   ├── agents/Gary_Bencivenga_Base_Prompt.md  # Prompt base
│   └── agno_agents/                           # Sistema Agno
│       ├── gary_agent.py                      # Agente Agno
│       ├── chat_interface.py                  # Interface
│       └── config.py                          # Configurações
├── frontend/src/
│   ├── app/api/chat/                          # API routes
│   ├── components/                            # Componentes React
│   └── hooks/                                 # Hooks customizados
├── backend/
│   └── main.py                                # FastAPI server
├── prompts/
│   ├── Gary_Bencivenga_Agent.md              # Prompt principal
│   └── copywriter_examples.md                # Exemplos
└── scripts/
    ├── start_gary_system.py                  # Inicialização
    ├── setup_copywriter.sh                   # Setup
    └── copywriter_cli.py                     # CLI
```

## 🔧 Comandos Úteis

```bash
# Ver logs Docker
docker-compose logs -f

# Reiniciar serviços
docker-compose restart

# Parar sistema
docker-compose down

# Limpar volumes
docker-compose down -v

# Health check
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Problemas Comuns

**PostgreSQL não conecta:**
```bash
docker ps | grep postgres
docker logs ntex_postgres
```

**APIs não funcionam:**
- Verifique chaves no `.env`
- Teste APIs diretamente nos sites

**Frontend não carrega:**
```bash
cd frontend && rm -rf .next && npm run dev
```

## 📊 Monitoramento

- **Backend**: `GET /health`
- **Database**: Verificado no startup
- **Agent**: Status do Gary

## 🔒 Segurança

- Chaves API ficam no backend
- Frontend acessa apenas via API REST
- PostgreSQL em container isolado
- CORS configurado

## 📞 Suporte

Para dúvidas:

1. Verifique logs: `docker-compose logs -f`
2. Teste health checks
3. Consulte documentação em `docs/`
4. Abra issue no repositório

## 📝 Licença

Parte do ecossistema NTEX - Sistema de Conteúdo e Operações.

---

**🎯 Lembre-se**: "Novidade mata; fundamentos vendem." - Gary Bencivenga