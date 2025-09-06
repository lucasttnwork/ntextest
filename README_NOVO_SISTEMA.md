# Sistema NTEX - Gary Bencivenga Agent

## 📋 Visão Geral
Sistema simplificado focado no agente Gary Bencivenga usando framework Agno e banco PostgreSQL local.

## 🏗️ Arquitetura
- **Frontend**: Removido (projeto backend-only)
- **Backend**: Flask + PostgreSQL 
- **Agente**: Gary Bencivenga com Agno
- **Banco**: PostgreSQL via Docker

## 🚀 Como Usar

### 1. Iniciar Banco de Dados
```bash
cd /Users/lucasttn/Documents/Documents/Cérebro\ NTEX
docker-compose up -d
```

### 2. Instalar Dependências
```bash
cd agno_agents
python3 -m pip install -r requirements.txt
```

### 3. Iniciar Backend
```bash
cd agno_agents
python3 chat_interface.py
```

### 4. Testar API
```bash
curl -X POST http://localhost:5003/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Crie uma copy para Instagram sobre marketing digital"}'
```

## 📡 Endpoints Disponíveis

- `POST /api/chat` - Conversar com Gary
- `GET /api/sessions` - Listar sessões
- `GET /api/agents/status` - Status dos agentes

## 🤖 Como Usar o Gary

O agente responde a qualquer mensagem enviada para `/api/chat`. Exemplos:

```json
{
  "message": "Crie uma headline persuasiva para um curso de copywriting",
  "session_id": "optional_session_id"
}
```

## 🗃️ Banco de Dados

### Acesso ao PgAdmin
- URL: http://localhost:8080
- Email: admin@ntex.com
- Senha: admin123

### Conexão Direta PostgreSQL
- Host: localhost
- Porta: 5432
- Banco: ntex_db
- Usuário: ntex_user
- Senha: ntex_password

## 📝 Configuração

### Arquivo .env
```env
OPENAI_API_KEY=sua_chave_openai_aqui
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ntex_db
POSTGRES_USER=ntex_user
POSTGRES_PASSWORD=ntex_password
```

## 🔧 Desenvolvimento

### Arquivos Principais
- `gary_agent.py` - Agente Gary Bencivenga
- `chat_interface.py` - API Flask
- `postgres_client.py` - Cliente PostgreSQL
- `docker-compose.yml` - Configuração Docker
- `sql/init.sql` - Schema do banco

### Dependências
- agno>=1.8.0
- psycopg2-binary>=2.9.0
- flask>=2.3.0
- openai>=1.0.0

## 🧪 Testes

### Testar Agente Gary
```bash
cd agno_agents
python3 -c "from gary_agent import get_gary_agent; agent = get_gary_agent(); print(agent.process_request('Teste'))"
```

### Testar PostgreSQL
```bash
cd agno_agents
python3 -c "from postgres_client import get_postgres_client; client = get_postgres_client(); print('Conectado!' if client.connection else 'Erro')"
```

## 📊 Monitoramento

### Logs
Os logs são salvos no console e no banco de dados PostgreSQL.

### Status dos Agentes
```
GET /api/agents/status
```

## 🔄 Próximos Passos

1. **Adicionar UI**: Implementar interface web para conversar com Gary
2. **Streaming**: Adicionar suporte a respostas em tempo real
3. **Contextos**: Implementar memória conversacional avançada
4. **Templates**: Adicionar templates de prompts para Gary
