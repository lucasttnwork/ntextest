"""
Interface de Chat para Agentes IA NTEX
Interface web similar ao ChatGPT para interagir com os agentes especializados
Integrada com sistema de memória Supabase
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from flask import Flask, render_template, request, jsonify, session, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Importar agentes
from master_agent import get_master_agent
from copy_agent import get_copy_agent
from design_agent import get_design_agent
from supabase_client import get_supabase_client

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("NTEX_JWT_SECRET", "ntex_secret_key_2025")
CORS(app)

# Inicializar agentes
master_agent = get_master_agent()
copy_agent = get_copy_agent()
design_agent = get_design_agent()

# Inicializar cliente Supabase
try:
    supabase_client = get_supabase_client()
    logger.info("Cliente Supabase inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar Supabase: {e}")
    supabase_client = None

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
        
        # Salvar no Supabase se disponível
        if supabase_client and self.session_id:
            try:
                supabase_client.add_message(
                    session_id=self.session_id,
                    role=role,
                    content=content,
                    agent_name=agent,
                    metadata=metadata
                )
            except Exception as e:
                logger.error(f"Erro ao salvar mensagem no Supabase: {e}")
        
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
        
        # Salvar no Supabase se disponível
        if supabase_client and self.session_id:
            try:
                supabase_client.add_agent_log(
                    session_id=self.session_id,
                    **log_data
                )
            except Exception as e:
                logger.error(f"Erro ao salvar log no Supabase: {e}")
        
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
        
        # Salvar no Supabase se disponível
        if supabase_client and self.session_id:
            try:
                supabase_client.add_agent_file(
                    session_id=self.session_id,
                    **file_data
                )
            except Exception as e:
                logger.error(f"Erro ao salvar arquivo no Supabase: {e}")
        
        return file_data
    
    def update_agent_context(self, agent_name: str, context_key: str, context_value: str,
                            context_type: str = "text", importance_score: int = 1,
                            expires_at: datetime = None):
        """Atualiza contexto do agente"""
        if supabase_client and self.session_id:
            try:
                supabase_client.update_agent_context(
                    session_id=self.session_id,
                    agent_name=agent_name,
                    context_key=context_key,
                    context_value=context_value,
                    context_type=context_type,
                    importance_score=importance_score,
                    expires_at=expires_at
                )
            except Exception as e:
                logger.error(f"Erro ao atualizar contexto no Supabase: {e}")
    
    def get_context(self) -> str:
        """Retorna contexto da conversa para os agentes"""
        if supabase_client and self.session_id:
            try:
                context_result = supabase_client.get_session_context(self.session_id)
                if context_result["success"]:
                    return context_result["context"]
            except Exception as e:
                logger.error(f"Erro ao obter contexto do Supabase: {e}")
        
        # Fallback para contexto local
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
    """Endpoint para processar mensagens do chat"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({"error": "Mensagem vazia"}), 400
        
        # Criar ou recuperar sessão
        if not session_id:
            session_name = f"Conversa sobre {message[:50]}..."
            if supabase_client:
                session_result = supabase_client.create_chat_session(session_name)
                if session_result["success"]:
                    session_id = session_result["session_id"]
                else:
                    logger.error(f"Erro ao criar sessão: {session_result['error']}")
                    session_id = f"local_session_{datetime.now().timestamp()}"
            else:
                session_id = f"local_session_{datetime.now().timestamp()}"
        
        if session_id not in active_sessions:
            active_sessions[session_id] = ChatSession(session_id)
        
        chat_session = active_sessions[session_id]
        
        # Adicionar mensagem do usuário
        chat_session.add_message("user", message)
        
        # Processar com agente mestre
        response = process_with_master_agent(chat_session, message)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erro no endpoint de chat: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Endpoint para streaming de chat com logs em tempo real"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({"error": "Mensagem vazia"}), 400
        
        # Criar ou recuperar sessão
        if not session_id:
            session_name = f"Conversa sobre {message[:50]}..."
            if supabase_client:
                session_result = supabase_client.create_chat_session(session_name)
                if session_result["success"]:
                    session_id = session_result["session_id"]
                else:
                    session_id = f"local_session_{datetime.now().timestamp()}"
            else:
                session_id = f"local_session_{datetime.now().timestamp()}"
        
        if session_id not in active_sessions:
            active_sessions[session_id] = ChatSession(session_id)
        
        chat_session = active_sessions[session_id]
        
        # Adicionar mensagem do usuário
        chat_session.add_message("user", message)
        
        def generate():
            """Gerador para streaming de resposta"""
            try:
                # Iniciar processo do agente
                yield f"data: {json.dumps({'type': 'agent_start', 'agent': 'NTEX_Master_Agent'})}\n\n"
                
                # Simular processo do Copy Agent
                yield f"data: {json.dumps({'type': 'agent_process', 'agent': 'Copy_Agent', 'status': 'starting'})}\n\n"
                
                # Log de pensamento
                chat_session.add_agent_log(
                    "Copy_Agent", 
                    "Analisando pedido do usuário para criar post sobre automação de marketing",
                    log_type="thinking"
                )
                yield f"data: {json.dumps({'type': 'agent_thought', 'agent': 'Copy_Agent', 'thought': 'Analisando pedido do usuário...'})}\n\n"
                
                # Simular passos de execução
                steps = [
                    "Analisando objetivo: Gerar engajamento e leads",
                    "Definindo público-alvo: Empreendedores B2B",
                    "Gerando copy persuasivo..."
                ]
                
                for i, step in enumerate(steps):
                    chat_session.add_agent_log(
                        "Copy_Agent", 
                        step, 
                        log_type="execution", 
                        step_number=i+1
                    )
                    yield f"data: {json.dumps({'type': 'agent_step', 'agent': 'Copy_Agent', 'step': step, 'step_number': i+1})}\n\n"
                    yield f"data: {json.dumps({'type': 'agent_log', 'agent': 'Copy_Agent', 'log': step})}\n\n"
                
                # Simular resultado
                result = "✅ Post para Instagram criado com sucesso!\n\n📝 Copy gerado com técnicas de copywriting para B2B\n🎨 Design visual moderno e engajante"
                
                yield f"data: {json.dumps({'type': 'agent_result', 'agent': 'Copy_Agent', 'result': result})}\n\n"
                
                # Finalizar
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                
            except Exception as e:
                logger.error(f"Erro no streaming: {e}")
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/plain')
        
    except Exception as e:
        logger.error(f"Erro no endpoint de streaming: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

def process_with_master_agent(chat_session: ChatSession, message: str) -> Dict[str, Any]:
    """Processa mensagem com agente mestre"""
    try:
        # Adicionar log de início
        chat_session.add_agent_log(
            "NTEX_Master_Agent",
            f"Iniciando processamento da mensagem: {message[:100]}...",
            log_type="execution"
        )
        
        # Determinar tipo de tarefa
        task_type = determine_task_type(message)
        
        # Rotear para agente especializado
        if "instagram" in message.lower() or "post" in message.lower():
            agent_name = "Copy_Agent"
            agent_response = process_with_copy_agent(chat_session, message)
        elif "design" in message.lower() or "visual" in message.lower():
            agent_name = "Design_Agent"
            agent_response = process_with_design_agent(chat_session, message)
        else:
            agent_name = "NTEX_Master_Agent"
            agent_response = process_with_master_agent_logic(chat_session, message)
        
        # Adicionar resposta do agente
        chat_session.add_message("assistant", agent_response, agent_name)
        
        # Adicionar log de conclusão
        chat_session.add_agent_log(
            agent_name,
            "Processamento concluído com sucesso",
            log_type="result"
        )
        
        return {
            "success": True,
            "response": agent_response,
            "agent": agent_name,
            "session_id": chat_session.session_id
        }
        
    except Exception as e:
        logger.error(f"Erro no processamento com agente mestre: {e}")
        chat_session.add_agent_log(
            "NTEX_Master_Agent",
            f"Erro no processamento: {str(e)}",
            log_level="error"
        )
        return {
            "success": False,
            "error": f"Erro no processamento: {str(e)}"
        }

def determine_task_type(message: str) -> str:
    """Determina o tipo de tarefa baseado na mensagem"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["instagram", "post", "rede social"]):
        return "social_media"
    elif any(word in message_lower for word in ["anúncio", "ads", "publicidade"]):
        return "advertising"
    elif any(word in message_lower for word in ["design", "visual", "arte"]):
        return "design"
    elif any(word in message_lower for word in ["campanha", "estratégia"]):
        return "campaign"
    else:
        return "general"

def process_with_copy_agent(chat_session: ChatSession, message: str) -> str:
    """Processa com agente de copy"""
    try:
        chat_session.add_agent_log(
            "Copy_Agent",
            "Iniciando criação de copy",
            log_type="execution"
        )
        
        # Simular processo de criação de copy
        chat_session.add_agent_log(
            "Copy_Agent",
            "Analisando objetivo e público-alvo",
            log_type="execution",
            step_number=1
        )
        
        chat_session.add_agent_log(
            "Copy_Agent",
            "Aplicando técnicas de copywriting para B2B",
            log_type="execution",
            step_number=2
        )
        
        # Gerar resposta
        response = """✅ **Copy para Instagram criado com sucesso!**

📝 **Copy:**
"Transforme seu marketing em uma máquina de vendas! 🚀

A automação não é só sobre tecnologia - é sobre liberar seu tempo para o que realmente importa: estratégia e criatividade.

💡 Dica: Comece pequeno. Automatize uma tarefa por vez e veja a diferença.

#MarketingDigital #Automação #Eficiência #Vendas"

🎯 **Público-alvo:** Empreendedores B2B interessados em automação
📊 **Objetivo:** Gerar engajamento e leads qualificados
✨ **Tom de voz:** Profissional, mas acessível e motivador"""

        chat_session.add_agent_log(
            "Copy_Agent",
            "Copy gerado com sucesso",
            log_type="result"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Erro no agente de copy: {e}")
        return f"❌ Erro ao criar copy: {str(e)}"

def process_with_design_agent(chat_session: ChatSession, message: str) -> str:
    """Processa com agente de design"""
    try:
        chat_session.add_agent_log(
            "Design_Agent",
            "Iniciando criação de design",
            log_type="execution"
        )
        
        # Simular processo de criação de design
        chat_session.add_agent_log(
            "Design_Agent",
            "Analisando brief e requisitos visuais",
            log_type="execution",
            step_number=1
        )
        
        chat_session.add_agent_log(
            "Design_Agent",
            "Criando layout com princípios de design para redes sociais",
            log_type="execution",
            step_number=2
        )
        
        # Gerar resposta
        response = """🎨 **Design visual criado com sucesso!**

✨ **Características do design:**
• **Paleta de cores:** Gradiente azul-verde (#19c37d → #0ea5e9)
• **Tipografia:** Fonte moderna e legível
• **Layout:** Clean e minimalista
• **Elementos:** Ícones simples e ícones de ação
• **Formato:** Otimizado para Instagram (1080x1080px)

🎯 **Aplicações:**
• Post principal do Instagram
• Story destacado
• Avatar de perfil
• Template para futuros posts

📁 **Arquivos gerados:**
• post_instagram_design.png (1080x1080px)
• post_instagram_design_story.png (1080x1920px)
• post_instagram_design_avatar.png (400x400px)"""

        chat_session.add_agent_log(
            "Design_Agent",
            "Design criado com sucesso",
            log_type="result"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Erro no agente de design: {e}")
        return f"❌ Erro ao criar design: {str(e)}"

def process_with_master_agent_logic(chat_session: ChatSession, message: str) -> str:
    """Processa com lógica do agente mestre"""
    try:
        chat_session.add_agent_log(
            "NTEX_Master_Agent",
            "Processando solicitação geral",
            log_type="execution"
        )
        
        # Gerar resposta baseada no contexto
        response = """🤖 **Agente Mestre NTEX ativo!**

Entendi sua solicitação. Como posso ajudá-lo especificamente?

**Opções disponíveis:**
📱 **Criar post Instagram** - Copy + design para redes sociais
📢 **Criar anúncio** - Copy persuasivo para campanhas
🎨 **Criar design** - Elementos visuais e templates
🚀 **Criar campanha** - Estratégia completa de marketing
📊 **Analisar performance** - Métricas e otimizações

**Exemplos de comandos:**
• "Criar post para Instagram sobre automação de marketing"
• "Criar anúncio para Google Ads focado em CEOs"
• "Criar design para story do Instagram"
• "Criar campanha completa para LinkedIn"

Digite sua solicitação específica e eu direcionarei para o agente especializado mais adequado! 🎯"""

        chat_session.add_agent_log(
            "NTEX_Master_Agent",
            "Resposta geral gerada com sucesso",
            log_type="result"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Erro na lógica do agente mestre: {e}")
        return f"❌ Erro no processamento: {str(e)}"

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """Lista sessões de chat"""
    try:
        if supabase_client:
            result = supabase_client.list_chat_sessions(limit=50)
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
        if supabase_client:
            # Obter contexto completo
            context_result = supabase_client.get_session_context(session_id)
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
        if supabase_client:
            result = supabase_client.close_session(session_id)
            if result["success"]:
                return jsonify({"success": True})
            else:
                return jsonify({"error": result["error"]}), 500
        else:
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
            "master_agent": {
                "status": "active",
                "name": "NTEX_Master_Agent",
                "capabilities": ["coordenação", "roteamento", "contexto"]
            },
            "copy_agent": {
                "status": "active",
                "name": "Copy_Agent",
                "capabilities": ["copywriting", "redes sociais", "anúncios"]
            },
            "design_agent": {
                "status": "active",
                "name": "Design_Agent",
                "capabilities": ["design visual", "templates", "branding"]
            },
            "supabase": {
                "status": "active" if supabase_client else "inactive",
                "capabilities": ["memória persistente", "logs", "contexto"]
            }
        }
        
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"Erro ao obter status dos agentes: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)
