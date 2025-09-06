# Testes Manuais NTEX - Chat Enhancements

## Pré-requisitos
- Backend rodando: `cd agno_agents && python chat_interface.py` (porta 5003)
- Frontend rodando: `cd frontend && npm run dev` (porta 3000)
- PostgreSQL rodando localmente com schema criado

## Testes de Streaming SSE

### 1. Teste básico de streaming
```bash
curl -s -N -X POST http://localhost:5003/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Crie um anúncio simples para produto de limpeza"}'
```

**Saída esperada:**
- Eventos SSE com `type: "delta"` contendo pedaços do texto
- Evento final `type: "complete"`
- Sem duplicação de conteúdo

### 2. Teste com busca web
```bash
curl -s -N -X POST http://localhost:5003/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Quais são as tendências de marketing digital em 2024?", "webSearch": true}'
```

**Saída esperada:**
- Eventos SSE com deltas
- Evento `type: "sources"` com URLs encontradas e metadados
- Sources com title e description populados

### 3. Teste de erro
```bash
curl -s -N -X POST http://localhost:5003/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":""}'
```

**Saída esperada:**
- Evento `type: "error"` com mensagem de erro

## Testes de Persistência

### 4. Verificar criação de sessão
```bash
# Testar criação de sessão
python3 -c "
from agno_agents.postgres_client import get_postgres_client
client = get_postgres_client()
result = client.create_chat_session('Teste de sessão')
print('Sessão criada:', result)
client.disconnect()
"
```

### 5. Verificar mensagens salvas
```bash
# Após enviar mensagem via curl, verificar DB
python3 -c "
from agno_agents.postgres_client import get_postgres_client
client = get_postgres_client()
result = client.list_chat_sessions(5)
print('Sessões encontradas:', len(result.get('sessions', [])))
if result.get('sessions'):
    session_id = result['sessions'][0]['session_id']
    context = client.get_session_context(session_id)
    print('Mensagens da sessão:', context)
client.disconnect()
"
```

## Testes de Frontend

### 6. Teste de streaming no browser
1. Abrir http://localhost:3000
2. Digitar mensagem e enviar
3. Verificar:
   - Streaming de texto em tempo real
   - Caret piscante durante streaming
   - Sources aparecem quando URLs são encontradas
   - Atalho Ctrl+Enter funciona

### 7. Teste de sources no frontend
1. Enviar mensagem que contenha URLs
2. Verificar se sources aparecem com títulos corretos
3. Clicar nas sources para verificar links

## Validações de Performance

### 8. Teste de timeout das sources
```bash
curl -s -N -X POST http://localhost:5003/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Visite http://httpbin.org/delay/10 para teste"}'
```

**Saída esperada:**
- Streaming funciona mesmo com URL lenta
- Sources aparecem com fallback (URL como título)

## Logs e Debugging

### 9. Verificar logs do backend
```bash
tail -f /Users/lucasttn/Documents/Documents/Cérebro\ NTEX/server.log
```

### 10. Teste de concorrência
```bash
# Testar múltiplas requisições simultâneas
for i in {1..3}; do
  curl -s -X POST http://localhost:5003/api/chat/stream \
    -H "Content-Type: application/json" \
    -d "{\"message\":\"Teste $i\"}" &
done
```

## Checklist de Validação

- [ ] Streaming funciona sem duplicação
- [ ] Sources são populadas com metadados
- [ ] Frontend exibe sources corretamente
- [ ] Sessões são criadas no DB
- [ ] Mensagens são persistidas
- [ ] Atalho Ctrl+Enter funciona
- [ ] Caret pisca durante streaming
- [ ] Build passa sem warnings
- [ ] Timeout de 3s nas sources funciona
- [ ] Tratamento de erros adequado
