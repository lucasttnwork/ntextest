#!/usr/bin/env bash
set -euo pipefail

LOGFILE="test_ai_elements.log"
SESSION_ID="test-session-1"

BACKEND_CMD="python3 '/Users/lucasttn/Documents/Documents/Cérebro NTEX/agno_agents/chat_interface.py'"
FRONTEND_DIR="/Users/lucasttn/Documents/Documents/Cérebro NTEX/agno_agents"


echo "Starting test run at $(date)" | tee -a "$LOGFILE" 

# Iniciar backend
echo "Starting backend..." | tee -a "$LOGFILE" 
$BACKEND_CMD &> "$LOGFILE.backend" &
BACKEND_PID=$!

# Wait backend ficar pronto (checa status de agentes)
echo "Waiting for backend to respond..." | tee -a "$LOGFILE" 
for i in {1..60}; do
  if curl -sS http://127.0.0.1:5003/api/agents/status >/dev/null 2>&1; then
    echo "Backend ready." | tee -a "$LOGFILE" 
    break
  fi
  sleep 1
done

# Iniciar frontend
echo "Starting frontend..." | tee -a "$LOGFILE" 
cd "$FRONTEND_DIR" 
npm install --silent
npm run dev > "$LOGFILE.frontend" 2>&1 &
FRONTEND_PID=$!

# Voltar para o diretório original
cd - >/dev/null

# Esperar o frontend iniciar
echo "Esperando frontend iniciar..." | tee -a "$LOGFILE" 
sleep 5

# Cenários de teste
echo "Test Gary prompt..." | tee -a "$LOGFILE" 
curl -sS -X POST -H "Content-Type: application/json" -d "{\"message\":\"Gary, crie uma copy sobre automação de marketing\",\"session_id\":\"$SESSION_ID\"}" http://127.0.0.1:5003/api/chat | tee -a "$LOGFILE"

echo "Test Copy (Instagram post)..." | tee -a "$LOGFILE" 
curl -sS -X POST -H "Content-Type: application/json" -d "{\"message\":\"Criar post para Instagram sobre automação de marketing\",\"session_id\":\"$SESSION_ID\"}" http://127.0.0.1:5003/api/chat | tee -a "$LOGFILE"

echo "Test Design..." | tee -a "$LOGFILE" 
curl -sS -X POST -H "Content-Type: application/json" -d "{\"message\":\"Criar design para campanha\",\"session_id\":\"$SESSION_ID\"}" http://127.0.0.1:5003/api/chat | tee -a "$LOGFILE"

# Encerramento
echo "Testes concluídos. Logs em $LOGFILE" | tee -a "$LOGFILE"

# Opcional: manter serviços ativos para inspeção, descomente para encerrar
# sleep 600
# kill $BACKEND_PID || true
# kill $FRONTEND_PID || true
