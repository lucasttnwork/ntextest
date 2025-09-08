# 🚀 Sistema Gary Bencivenga - Interface de Chat com IA

Interface completa para interagir com o agente Gary Bencivenga, especialista em copywriting usando a metodologia comprovada de Gary Bencivenga.

## 🎯 Visão Geral

Este sistema oferece uma interface de chat completa similar ao ChatGPT, mas especializada em copywriting profissional usando as técnicas de Gary Bencivenga. Inclui:

- 🤖 **Agente Especializado**: Gary Bencivenga com metodologia de 4 fases
- 💾 **Persistência de Conversas**: Todas as conversas salvas no PostgreSQL
- 🔍 **Busca Web**: Pesquisa na internet para informações atualizadas
- 📱 **Interface Responsiva**: Barra lateral para navegação entre conversas
- 🐳 **Docker Ready**: Ambiente completo com containers
- ⚡ **Streaming**: Respostas em tempo real (futuro)

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│                 │    │                 │    │                 │
│ • React/TS      │    │ • Python 3.10+  │    │ • Sessões       │
│ • ShadCN UI     │    │ • OpenRouter API│    │ • Mensagens     │
│ • AI Elements   │    │ • Tavily Search │    │ • Contexto      │
│ • Responsive    │    │ • PostgreSQL    │    │ • Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Início Rápido

### 1. Pré-requisitos

- **Docker & Docker Compose** (ou Docker Desktop)
- **Python 3.10+**
- **Node.js 18+**
- **Git**

### 2. Clonagem e Configuração

```bash
# 1. Clonar repositório
git clone <repository-url>
cd cerebro-ntex

# 2. Configurar ambiente
cp backend/.env.example backend/.env

# 3. Editar .env com suas chaves
nano backend/.env
```

### 3. Configuração das APIs

Edite o arquivo `backend/.env`:

```env
# OpenRouter (para IA)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_MODEL=x-ai/grok-code-fast-1

# Tavily (para busca web)
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx

# PostgreSQL (já configurado)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ntex_db
DB_USER=ntex_user
DB_PASSWORD=ntex_password
```

### 4. Iniciar Sistema Completo

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

### 5. Acessar o Sistema

- **🎨 Frontend**: http://localhost:3000
- **📡 Backend API**: http://localhost:8000
- **📚 Documentação API**: http://localhost:8000/docs
- **🗄️ PgAdmin**: http://localhost:8080 (admin@ntex.com / admin123)

## 📱 Como Usar

### Interface Principal

1. **Barra Lateral**: Navegue entre conversas anteriores
2. **Nova Conversa**: Clique no "+" para iniciar nova conversa
3. **Busca Web**: Use o botão 🌐 para pesquisa na internet
4. **Mensagens**: Digite suas solicitações normalmente

### Funcionalidades do Agente Gary

O agente responde seguindo a metodologia Bencivenga:

#### Fase 1: Pesquisa
- Faz perguntas específicas sobre o projeto
- Coleta informações sobre público, produto, concorrência

#### Fase 2: Ideaão
- Gera matriz de ângulos persuasivos
- Cria banco de 25 headlines
- Define arquitetura da peça

#### Fase 3: Rascunho
- Estrutura completa: Abertura → Aliança → Benefícios → Provas → Oferta → CTA
- Usa bullets de fascinação
- Cada parágrafo responde uma objeção

#### Fase 4: Lapidação
- Scorecard de qualidade (0-10)
- Regra dos 3 cortes
- Otimizações finais

### Exemplos de Uso

```
"Crie um anúncio para curso de marketing digital"

"Copie este anúncio: [colar anúncio concorrente]"

"Faça uma landing page para produto SaaS"

"Escreva um email de vendas para consultoria"
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente

```env
# Backend
PORT=8000
NTEX_JWT_SECRET=your-secret-key

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ntex_db
DB_USER=ntex_user
DB_PASSWORD=ntex_password

# OpenRouter
OPENROUTER_API_KEY=your-key
OPENROUTER_MODEL=x-ai/grok-code-fast-1
OPENROUTER_REFERER=https://ntex.com.br

# Tavily
TAVILY_API_KEY=your-key
```

### Comandos Úteis

```bash
# Ver logs do Docker
docker-compose logs -f

# Reiniciar serviços
docker-compose restart

# Parar tudo
docker-compose down

# Limpar volumes
docker-compose down -v

# Testar backend
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de conexão com PostgreSQL:**
```bash
# Verificar se container está rodando
docker ps | grep postgres

# Ver logs do container
docker logs ntex_postgres
```

**Erro nas APIs:**
- Verifique se as chaves estão corretas no `.env`
- Teste as APIs diretamente no site dos provedores

**Frontend não carrega:**
```bash
# Limpar cache Next.js
cd frontend && rm -rf .next && npm run dev
```

**Backend não inicia:**
```bash
# Instalar dependências
cd backend && pip install -r requirements.txt

# Verificar Python
python --version
```

## 📊 Monitoramento

### Health Checks

- **Backend**: `GET /health`
- **Database**: Verificado automaticamente no startup
- **Agent**: Status do Gary Bencivenga

### Logs

```bash
# Logs do backend
tail -f server.log

# Logs do Docker
docker-compose logs -f backend

# Logs do frontend (no browser console)
```

## 🔒 Segurança

- Todas as chaves de API ficam no servidor (backend)
- Frontend só acessa dados via API REST
- PostgreSQL roda em container isolado
- CORS configurado para desenvolvimento

## 🚧 Desenvolvimento

### Estrutura de Pastas

```
/
├── backend/           # FastAPI backend
│   ├── main.py       # Servidor principal
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # Next.js frontend
│   ├── src/
│   └── package.json
├── agents/           # Agentes Python
├── sql/             # Schema do banco
├── docker-compose.yml
└── scripts/         # Scripts de automação
```

### Próximas Funcionalidades

- [ ] Streaming de respostas em tempo real
- [ ] Upload de arquivos para análise
- [ ] Export de conversas em PDF
- [ ] Temas dark/light
- [ ] Notificações push
- [ ] Integração com ferramentas externas

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs do sistema
2. Teste os health checks
3. Consulte a documentação das APIs
4. Abra uma issue no repositório

## 📝 Licença

Este projeto é parte do ecossistema NTEX - Sistema de Conteúdo e Operações.

---

**🎯 Lembre-se**: "Novidade mata; fundamentos vendem." - Gary Bencivenga
