"""
Interface de Chat para Gary Bencivenga Agent
Interface simples usando framework Agno com PostgreSQL local
"""

import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Importar agente Gary
from gary_agent import get_gary_agent
from postgres_client import get_postgres_client

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("NTEX_JWT_SECRET", "ntex_secret_key_2025")
CORS(app)

# Inicializar agente Gary
gary_agent = get_gary_agent()

# Inicializar cliente PostgreSQL
try:
    postgres_client = get_postgres_client()
    logger.info("Cliente PostgreSQL inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar PostgreSQL: {e}")
    postgres_client = None

# Função para fetch seguro de metadados das sources
def fetch_source_metadata(url: str) -> Dict[str, str]:
    """Busca metadados de uma URL com timeout seguro"""
    try:
        headers = {
            'User-Agent': 'NTEX-Agent/1.0 (https://ntex.com.br)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        }

        response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
        response.raise_for_status()

        # Extrair título da página HTML
        import re
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else url

        # Extrair descrição meta
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', response.text, re.IGNORECASE)
        description = desc_match.group(1).strip() if desc_match else ""

        return {
            'title': title,
            'description': description
        }
    except Exception as e:
        logger.warning(f"Erro ao buscar metadados de {url}: {e}")
        return {
            'title': url,
            'description': ''
        }

# Função auxiliar para processar com Gary Agent
def process_with_gary_agent(message: str) -> Dict[str, Any]:
    """Processa mensagem com o agente Gary Bencivenga"""
    try:
        result = gary_agent.process_request(message)

        if result["success"]:
            return {
                "success": True,
                "response": result["response"],
                "agent": "Gary_Bencivenga_Agent"
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Erro desconhecido"),
                "agent": "Gary_Bencivenga_Agent"
            }
    except Exception as e:
        logger.error(f"Erro no Gary Agent: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent": "Gary_Bencivenga_Agent"
        }

# Schemas assumidos já existentes
class ChatSession:
    """Gerencia sessões de chat com memória persistente"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.agent_history: List[str] = []
        self.current_agent = None
        self.processing_status = "idle"
    
    def add_message(self, role: str, content: str, agent: str = None, metadata: Dict[str, Any] = None):
        """Adiciona mensagem à sessão"""
        message = {
            "id": len(self.messages) + 1,
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "metadata": metadata or {}
        }
        self.messages.append(message)
        
        # Salvar no PostgreSQL se disponível e a sessão for realmente do banco
        if postgres_client and self.session_id and not str(self.session_id).startswith("local_session_"):
            try:
                postgres_client.add_message(
                    session_id=self.session_id,
                    role=role,
                    content=content,
                    agent_name=agent,
                    metadata=metadata
                )
            except Exception as e:
                logger.error(f"Erro ao salvar mensagem no PostgreSQL: {e}")
        
        return message
    
    def add_agent_log(self, agent_name: str, message: str, log_level: str = "info", 
                      log_type: str = "execution", step_number: int = None, 
                      execution_time_ms: int = None, metadata: Dict = None):
        """Adiciona log de execução do agente"""
        log_data = {
            "agent_name": agent_name,
            "message": message,
            "log_level": log_level,
            "log_type": log_type,
            "step_number": step_number,
            "execution_time_ms": execution_time_ms,
            "metadata": metadata or {}
        }
        if postgres_client and self.session_id and not str(self.session_id).startswith("local_session_"):
            try:
                postgres_client.add_agent_log(
                    session_id=self.session_id,
                    log_data=log_data
                )
            except Exception as e:
                logger.error(f"Erro ao salvar log no PostgreSQL: {e}")
        self.agent_history.append(log_data)
        return log_data
        
    def add_agent_file(self, agent_name: str, file_name: str, file_type: str,
                       file_path: str, file_size: int = None, mime_type: str = None,
                       metadata: Dict = None):
        """Adiciona arquivo gerado pelo agente"""
        file_data = {
            "agent_name": agent_name,
            "file_name": file_name,
            "file_type": file_type,
            "file_path": file_path,
            "file_size": file_size,
            "mime_type": mime_type,
            "metadata": metadata or {}
        }
        if postgres_client and self.session_id:
            try:
                # PostgreSQL não implementa arquivos ainda - apenas log
                logger.info(f"Arquivo {file_name} registrado para {agent_name}")
            except Exception as e:
                logger.error(f"Erro ao registrar arquivo: {e}")
        return file_data
    
    def update_agent_context(self, agent_name: str, context_key: str, context_value: str,
                            context_type: str = "text", importance_score: int = 1,
                            expires_at: datetime = None):
        """Atualiza contexto do agente"""
        if postgres_client and self.session_id:
            try:
                # PostgreSQL não implementa contexto ainda - apenas log
                logger.info(f"Contexto atualizado para {agent_name}: {context_key}")
            except Exception as e:
                logger.error(f"Erro ao atualizar contexto: {e}")
    
    def get_context(self) -> str:
        """Retorna contexto da conversa para os agentes"""
        if postgres_client and self.session_id:
            try:
                context_result = postgres_client.get_session_context(self.session_id)
                if context_result["success"]:
                    return context_result["context"]
            except Exception as e:
                logger.error(f"Erro ao obter contexto do PostgreSQL: {e}")
        
        recent_messages = self.messages[-10:]
        context = []
        for msg in recent_messages:
            if msg["role"] == "user":
                context.append(f"Usuário: {msg['content']}")
            elif msg["role"] == "assistant":
                context.append(f"Agente {msg.get('agent', 'NTEX')}: {msg['content']}")
        return "\n".join(context)
    
    def get_agent_suggestions(self) -> List[str]:
        """Retorna sugestões de ações baseadas no contexto"""
        suggestions = [
            "Criar post Instagram",
            "Criar copy para anúncio",
            "Criar design visual",
            "Criar landing page",
            "Analisar performance",
            "Otimizar campanhas"
        ]
        
        # Personalizar sugestões baseado no contexto
        if any("instagram" in msg["content"].lower() for msg in self.messages[-3:]):
            suggestions.insert(0, "Criar post completo (copy + design)")
        
        if any("anúncio" in msg["content"].lower() or "ads" in msg["content"].lower() for msg in self.messages[-3:]):
            suggestions.insert(0, "Criar campanha completa")
        
        return suggestions[:5]

# Sessões ativas
active_sessions: Dict[str, ChatSession] = {}

@app.route('/')
def index():
    """Página principal do chat"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para processar mensagens do chat com Gary Agent"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')

        if not message:
            return jsonify({"error": "Mensagem vazia"}), 400

        # Criar ou recuperar sessão
        if not session_id:
            session_name = f"Conversa com Gary: {message[:50]}..."
            # Tentar criar sessão no Postgres primeiro
            if postgres_client:
                try:
                    session_result = postgres_client.create_chat_session(session_name)
                    if session_result.get("success") and session_result.get("session_id"):
                        session_id = session_result["session_id"]
                    else:
                        logger.warning("Não foi possível criar sessão no Postgres, usando sessão local")
                        session_id = f"local_session_{datetime.now().timestamp()}"
                except Exception as e:
                    logger.error(f"Erro ao criar sessão no Postgres: {e}")
                    session_id = f"local_session_{datetime.now().timestamp()}"
            else:
                session_id = f"local_session_{datetime.now().timestamp()}"

        if session_id not in active_sessions:
            active_sessions[session_id] = ChatSession(session_id)

        chat_session = active_sessions[session_id]

        # Adicionar mensagem do usuário
        chat_session.add_message("user", message)

        # Processar com Gary Agent
        result = process_with_gary_agent(message)

        if result["success"]:
            # Adicionar resposta do agente
            chat_session.add_message("assistant", result["response"], result["agent"])

            return jsonify({
                "success": True,
                "response": result["response"],
                "agent": result["agent"],
                "session_id": session_id
            })
        else:
            return jsonify({
                "success": False,
                "error": result["error"],
                "agent": result["agent"]
            }), 500

    except Exception as e:
        logger.error(f"Erro no endpoint de chat: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Endpoint para streaming de chat com deltas simples (SSE)."""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        web_search = data.get('webSearch', False)

        if not message:
            return jsonify({"error": "Mensagem vazia"}), 400

        # Criar sessão (DB se disponível, senão local)
        if not session_id:
            session_name = f"Streaming: {message[:50]}..."
            if postgres_client:
                try:
                    session_result = postgres_client.create_chat_session(session_name)
                    if session_result.get("success") and session_result.get("session_id"):
                        session_id = session_result["session_id"]
                    else:
                        logger.warning("Não foi possível criar sessão no Postgres, usando sessão local")
                        session_id = f"local_session_{datetime.now().timestamp()}"
                except Exception as e:
                    logger.error(f"Erro ao criar sessão no Postgres: {e}")
                    session_id = f"local_session_{datetime.now().timestamp()}"
            else:
                session_id = f"local_session_{datetime.now().timestamp()}"

        if session_id not in active_sessions:
            active_sessions[session_id] = ChatSession(session_id)

        chat_session = active_sessions[session_id]
        chat_session.add_message("user", message)

        def generate():
            try:
                # Executa o agente (com web_search habilitado no prompt indireto)
                prompt = message
                if web_search:
                    prompt = (
                        "[WEB_SEARCH ON] Se necessário, pesquise na web e incorpore fatos atuais com fontes.\n" +
                        message
                    )
                result = process_with_gary_agent(prompt)
                text = result.get("response", "")

                # Salvar resposta do assistente no DB se for sessão válida
                if result.get("success") and not str(session_id).startswith("local_session_"):
                    try:
                        postgres_client.add_message(
                            session_id=session_id,
                            role="assistant",
                            content=text,
                            agent_name=result.get("agent", "Gary_Bencivenga_Agent")
                        )
                    except Exception as e:
                        logger.error(f"Erro ao salvar resposta do assistente: {e}")

                # Stream de deltas simples
                chunk_size = 35
                for i in range(0, len(text), chunk_size):
                    delta = text[i:i+chunk_size]
                    yield f"data: {json.dumps({'type': 'delta', 'content': delta})}\n\n"

                # Extrair URLs e buscar metadados para popular Sources
                import re
                url_pattern = r"https?://[\w\-\.\/:?#=,&%+~]+"
                urls = re.findall(url_pattern, text)
                sources = []
                for u in urls:
                    metadata = fetch_source_metadata(u)
                    sources.append({
                        'title': metadata['title'],
                        'url': u,
                        'description': metadata['description']
                    })

                # Enviar fontes encontradas (se houver)
                if sources:
                    yield f"data: {json.dumps({'type': 'sources', 'sources': sources})}\n\n"

                # Finaliza
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            except Exception as e:
                logger.error(f"Erro no streaming: {e}")
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

        return Response(generate(), mimetype='text/plain')

    except Exception as e:
        logger.error(f"Erro no endpoint de streaming: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

# Função removida - agora usamos apenas process_with_gary_agent diretamente

# Funções dos agentes antigos removidas - agora usamos apenas Gary Agent


@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """Lista sessões de chat"""
    try:
        if postgres_client:
            result = postgres_client.list_chat_sessions(limit=50)
            if result["success"]:
                return jsonify(result["sessions"])
            else:
                return jsonify({"error": result["error"]}), 500
        else:
            # Retornar sessões locais
            sessions = []
            for session_id, chat_session in active_sessions.items():
                sessions.append({
                    "id": session_id,
                    "session_name": f"Conversa {session_id[-8:]}",
                    "status": "active",
                    "last_activity": chat_session.messages[-1]["timestamp"] if chat_session.messages else None
                })
            return jsonify(sessions)
            
    except Exception as e:
        logger.error(f"Erro ao listar sessões: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """Obtém detalhes de uma sessão específica"""
    try:
        if postgres_client:
            # Obter contexto completo
            context_result = postgres_client.get_session_context(session_id)
            if context_result["success"]:
                return jsonify(context_result["context"])
            else:
                return jsonify({"error": context_result["error"]}), 500
        else:
            # Retornar sessão local
            if session_id in active_sessions:
                chat_session = active_sessions[session_id]
                return jsonify({
                    "session_info": {
                        "id": session_id,
                        "status": "active",
                        "created_at": chat_session.messages[0]["timestamp"] if chat_session.messages else None
                    },
                    "recent_messages": chat_session.messages[-10:],
                    "agent_contexts": {}
                })
            else:
                return jsonify({"error": "Sessão não encontrada"}), 404
                
    except Exception as e:
        logger.error(f"Erro ao obter sessão: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/sessions/<session_id>/close', methods=['POST'])
def close_session(session_id):
    """Fecha uma sessão de chat"""
    try:
        # Remover sessão local
        if session_id in active_sessions:
            del active_sessions[session_id]
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Sessão não encontrada"}), 404
                
    except Exception as e:
        logger.error(f"Erro ao fechar sessão: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Retorna status dos agentes"""
    try:
        status = {
            "gary_agent": {
                "status": "active",
                "name": "Gary_Bencivenga_Agent",
                "capabilities": ["copywriting", "marketing", "persuasion"]
            },
            "agno_framework": {
                "status": "active" if gary_agent else "inactive",
                "capabilities": ["AI processing", "context awareness"]
            },
            "postgres": {
                "status": "active" if postgres_client else "inactive",
                "capabilities": ["data persistence", "session management"]
            }
        }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Erro ao obter status dos agentes: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)
