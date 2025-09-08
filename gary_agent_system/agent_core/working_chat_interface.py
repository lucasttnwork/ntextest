#!/usr/bin/env python3
"""
Interface de Chat para Agentes IA NTEX - Versão Funcional
Interface web similar ao ChatGPT para interagir com os agentes especializados
Integrada com sistema de memória Supabase
"""

import os
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any
from flask import Flask, render_template, request, jsonify, session, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv("NTEX_JWT_SECRET", "ntex_secret_key_2025")
CORS(app)

# Inicializar cliente Supabase
try:
    from supabase_client import get_supabase_client
    supabase_client = get_supabase_client()
    logger.info("Cliente Supabase inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar Supabase: {e}")
    supabase_client = None

# Importar agentes reais da arquitetura NTEX
try:
    from master_agent import NTEXMasterAgent
    from copy_agent import CopyAgent
    from design_agent import DesignAgent
    
    # Inicializar agentes reais
    master_agent = NTEXMasterAgent()
    copy_agent = CopyAgent()
    design_agent = DesignAgent()
    
    logger.info("Agentes reais da arquitetura NTEX carregados com sucesso")
    
except ImportError as e:
    logger.warning(f"Erro ao carregar agentes reais: {e}")
    logger.warning("Usando agentes simulados como fallback")
    
    # Fallback para agentes simulados
    class FallbackAgent:
        def __init__(self, name: str, capabilities: List[str]):
            self.name = name
            self.capabilities = capabilities
            self.status = "active"
        
        def process_message(self, message: str, context: Dict = None) -> Dict:
            """Processa mensagem e retorna resposta inteligente"""
            message_lower = message.lower()
            
            if self.name == "Copy Agent":
                return self._process_copy_request(message, message_lower)
            elif self.name == "Design Agent":
                return self._process_design_request(message, message_lower)
            else:
                return self._process_master_request(message, message_lower)
        
        def _process_copy_request(self, message: str, message_lower: str) -> Dict:
            """Processa solicitações de copy"""
            if any(word in message_lower for word in ['post', 'instagram', 'facebook', 'linkedin']):
                return {
                    "content": f"📝 **Copy para {message_lower.split()[0].title()} criado!**\n\n"
                              f"Baseado no seu pedido: '{message}'\n\n"
                              f"**Sugestão de Copy:**\n"
                              f"🚀 Transforme sua presença digital em resultados reais!\n\n"
                              f"💡 **Dica:** Foque no benefício principal para seu público-alvo.\n\n"
                              f"**Hashtags sugeridas:** #MarketingDigital #Resultados #Transformação\n\n"
                              f"Quer que eu refine algum aspecto específico?",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
            elif any(word in message_lower for word in ['anúncio', 'ad', 'publicidade']):
                return {
                    "content": f"📢 **Anúncio publicitário criado!**\n\n"
                              f"**Headline principal:** {message.title()}\n\n"
                              f"**Copy do anúncio:**\n"
                              f"Descubra como {message_lower.split()[0]} pode revolucionar seus resultados!\n\n"
                              f"✅ Benefícios claros\n"
                              f"🎯 Público-alvo definido\n"
                              f"💪 Call-to-action persuasivo\n\n"
                              f"Precisa de ajustes no tom ou público-alvo?",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "content": f"📝 **Copy Agent ativo!**\n\n"
                              f"Entendi sua solicitação: '{message}'\n\n"
                              f"**Como posso ajudar:**\n"
                              f"• Criação de posts para redes sociais\n"
                              f"• Redação de anúncios publicitários\n"
                              f"• Desenvolvimento de copy persuasivo\n"
                              f"• Otimização de textos para conversão\n\n"
                              f"Seja mais específico sobre o formato e objetivo desejado!",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
        
        def _process_design_request(self, message: str, message_lower: str) -> Dict:
            """Processa solicitações de design"""
            if any(word in message_lower for word in ['visual', 'imagem', 'template', 'layout']):
                return {
                    "content": f"🎨 **Design visual criado!**\n\n"
                              f"**Brief recebido:** {message}\n\n"
                              f"**Especificações do design:**\n"
                              f"🎯 **Estilo:** Moderno e profissional\n"
                              f"🌈 **Paleta:** Cores que transmitem confiança\n"
                              f"📐 **Layout:** Clean e focado na conversão\n"
                              f"🔤 **Tipografia:** Clara e legível\n\n"
                              f"**Elementos incluídos:**\n"
                              f"• Header impactante\n"
                              f"• Área de conteúdo bem estruturada\n"
                              f"• Call-to-action destacado\n"
                              f"• Footer com informações de contato\n\n"
                              f"Quer ajustar algum aspecto específico do design?",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "content": f"🎨 **Design Agent ativo!**\n\n"
                              f"Entendi sua solicitação: '{message}'\n\n"
                              f"**Como posso ajudar:**\n"
                              f"• Criação de templates visuais\n"
                              f"• Design de campanhas publicitárias\n"
                              f"• Desenvolvimento de identidade visual\n"
                              f"• Criação de materiais para redes sociais\n\n"
                              f"Especifique o tipo de design e público-alvo!",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
        
        def _process_master_request(self, message: str, message_lower: str) -> Dict:
            """Processa solicitações para o Master Agent"""
            if any(word in message_lower for word in ['campanha', 'estratégia', 'plano']):
                return {
                    "content": f"🤖 **Master Agent - Estratégia de Campanha!**\n\n"
                              f"**Análise da solicitação:** {message}\n\n"
                              f"**Plano estratégico:**\n"
                              f"1️⃣ **Fase de Pesquisa** - Análise de mercado e concorrência\n"
                              f"2️⃣ **Definição de Objetivos** - KPIs e métricas claras\n"
                              f"3️⃣ **Segmentação de Público** - Personas e jornada do cliente\n"
                              f"4️⃣ **Execução Multi-canal** - Coordenação entre agentes\n"
                              f"5️⃣ **Monitoramento** - Acompanhamento de resultados\n\n"
                              f"**Próximos passos:**\n"
                              f"• Quer que eu ative o Copy Agent para o conteúdo?\n"
                              f"• Ou prefere começar com o Design Agent?\n"
                              f"• Posso criar um cronograma detalhado da campanha!",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
            elif any(word in message_lower for word in ['olá', 'oi', 'hello', 'hi']):
                return {
                    "content": f"🤖 **Olá! Sou o Master Agent da NTEX!**\n\n"
                              f"**Como posso ajudar você hoje?**\n\n"
                              f"🎯 **Para estratégias:** Peça uma campanha ou plano\n"
                              f"📝 **Para conteúdo:** Solicite copy ou posts\n"
                              f"🎨 **Para design:** Peça templates ou visuais\n\n"
                              f"**Exemplos de comandos:**\n"
                              f"• 'Criar campanha de marketing digital'\n"
                              f"• 'Fazer post para Instagram sobre automação'\n"
                              f"• 'Criar design para campanha de vendas'\n\n"
                              f"O que você gostaria de fazer?",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "content": f"🤖 **Master Agent - Coordenador NTEX!**\n\n"
                              f"**Sua solicitação:** {message}\n\n"
                              f"**Como posso coordenar os agentes:**\n"
                              f"• **Copy Agent:** Para criação de conteúdo e copy\n"
                              f"• **Design Agent:** Para elementos visuais e templates\n"
                              f"• **Master Agent:** Para estratégia e coordenação\n\n"
                              f"**Sugestão:** Seja mais específico sobre o que precisa:\n"
                              f"• Tipo de conteúdo (post, anúncio, campanha)\n"
                              f"• Objetivo (vendas, engajamento, awareness)\n"
                              f"• Público-alvo (B2B, B2C, nicho específico)\n\n"
                              f"Como posso ajudar de forma mais direcionada?",
                    "agent": self.name,
                    "capabilities": self.capabilities,
                    "timestamp": datetime.now().isoformat()
                }
    
    # Inicializar agentes fallback
    master_agent = FallbackAgent("Master Agent", ["coordenação", "roteamento", "contexto", "estratégia"])
    copy_agent = FallbackAgent("Copy Agent", ["copywriting", "redes sociais", "anúncios", "conteúdo"])
    design_agent = FallbackAgent("Design Agent", ["design visual", "templates", "branding", "criatividade"])

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
                    log_data=log_data
                )
            except Exception as e:
                logger.error(f"Erro ao salvar log no Supabase: {e}")
        
        self.agent_history.append(log_data)
        return log_data
    
    def _process_copy_request(self, message: str, message_lower: str) -> Dict[str, Any]:
        """Processa solicitações de copy usando lógica inteligente"""
        if any(word in message_lower for word in ['post', 'instagram', 'facebook', 'linkedin']):
            return {
                "content": f"📝 **Copy para {message_lower.split()[0].title()} criado!**\n\n"
                          f"Baseado no seu pedido: '{message}'\n\n"
                          f"**Sugestão de Copy:**\n"
                          f"🚀 Transforme sua presença digital em resultados reais!\n\n"
                          f"💡 **Dica:** Foque no benefício principal para seu público-alvo.\n\n"
                          f"**Hashtags sugeridas:** #MarketingDigital #Resultados #Transformação\n\n"
                          f"Quer que eu refine algum aspecto específico?",
                "agent": "Copy Agent",
                "capabilities": ["copywriting", "redes sociais", "anúncios", "conteúdo"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in message_lower for word in ['anúncio', 'ad', 'publicidade']):
            return {
                "content": f"📢 **Anúncio publicitário criado!**\n\n"
                          f"**Headline principal:** {message.title()}\n\n"
                          f"**Copy do anúncio:**\n"
                          f"Descubra como {message_lower.split()[0]} pode revolucionar seus resultados!\n\n"
                          f"✅ Benefícios claros\n"
                          f"🎯 Público-alvo definido\n"
                          f"💪 Call-to-action persuasivo\n\n"
                          f"Precisa de ajustes no tom ou público-alvo?",
                "agent": "Copy Agent",
                "capabilities": ["copywriting", "redes sociais", "anúncios", "conteúdo"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "content": f"📝 **Copy Agent ativo!**\n\n"
                          f"Entendi sua solicitação: '{message}'\n\n"
                          f"**Como posso ajudar:**\n"
                          f"• Criação de posts para redes sociais\n"
                          f"• Redação de anúncios publicitários\n"
                          f"• Desenvolvimento de copy persuasivo\n"
                          f"• Otimização de textos para conversão\n\n"
                          f"Seja mais específico sobre o formato e objetivo desejado!",
                "agent": "Copy Agent",
                "capabilities": ["copywriting", "redes sociais", "anúncios", "conteúdo"],
                "timestamp": datetime.now().isoformat()
            }
    
    def _process_design_request(self, message: str, message_lower: str) -> Dict[str, Any]:
        """Processa solicitações de design usando lógica inteligente"""
        if any(word in message_lower for word in ['visual', 'imagem', 'template', 'layout']):
            return {
                "content": f"🎨 **Design visual criado!**\n\n"
                          f"**Brief recebido:** {message}\n\n"
                          f"**Especificações do design:**\n"
                          f"🎯 **Estilo:** Moderno e profissional\n"
                          f"🌈 **Paleta:** Cores que transmitem confiança\n"
                          f"📐 **Layout:** Clean e focado na conversão\n"
                          f"🔤 **Tipografia:** Clara e legível\n\n"
                          f"**Elementos incluídos:**\n"
                          f"• Header impactante\n"
                          f"• Área de conteúdo bem estruturada\n"
                          f"• Call-to-action destacado\n"
                          f"• Footer com informações de contato\n\n"
                          f"Quer ajustar algum aspecto específico do design?",
                "agent": "Design Agent",
                "capabilities": ["design visual", "templates", "branding", "criatividade"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "content": f"🎨 **Design Agent ativo!**\n\n"
                          f"Entendi sua solicitação: '{message}'\n\n"
                          f"**Como posso ajudar:**\n"
                          f"• Criação de templates visuais\n"
                          f"• Design de campanhas publicitárias\n"
                          f"• Desenvolvimento de identidade visual\n"
                          f"• Criação de materiais para redes sociais\n\n"
                          f"Especifique o tipo de design e público-alvo!",
                "agent": "Design Agent",
                "capabilities": ["design visual", "templates", "branding", "criatividade"],
                "timestamp": datetime.now().isoformat()
            }
    
    def _process_master_request(self, message: str, message_lower: str) -> Dict[str, Any]:
        """Processa solicitações para o Master Agent usando lógica inteligente"""
        if any(word in message_lower for word in ['campanha', 'estratégia', 'plano']):
            return {
                "content": f"🤖 **Master Agent - Estratégia de Campanha!**\n\n"
                          f"**Análise da solicitação:** {message}\n\n"
                          f"**Plano estratégico:**\n"
                          f"1️⃣ **Fase de Pesquisa** - Análise de mercado e concorrência\n"
                          f"2️⃣ **Definição de Objetivos** - KPIs e métricas claras\n"
                          f"3️⃣ **Segmentação de Público** - Personas e jornada do cliente\n"
                          f"4️⃣ **Execução Multi-canal** - Coordenação entre agentes\n"
                          f"5️⃣ **Monitoramento** - Acompanhamento de resultados\n\n"
                          f"**Próximos passos:**\n"
                          f"• Quer que eu ative o Copy Agent para o conteúdo?\n"
                          f"• Ou prefere começar com o Design Agent?\n"
                          f"• Posso criar um cronograma detalhado da campanha!",
                "agent": "Master Agent",
                "capabilities": ["coordenação", "roteamento", "contexto", "estratégia"],
                "timestamp": datetime.now().isoformat()
            }
        elif any(word in message_lower for word in ['olá', 'oi', 'hello', 'hi']):
            return {
                "content": f"🤖 **Olá! Sou o Master Agent da NTEX!**\n\n"
                          f"**Como posso ajudar você hoje?**\n\n"
                          f"🎯 **Para estratégias:** Peça uma campanha ou plano\n"
                          f"📝 **Para conteúdo:** Solicite copy ou posts\n"
                          f"🎨 **Para design:** Peça templates ou visuais\n\n"
                          f"**Exemplos de comandos:**\n"
                          f"• 'Criar campanha de marketing digital'\n"
                          f"• 'Fazer post para Instagram sobre automação'\n"
                          f"• 'Criar design para campanha de vendas'\n\n"
                          f"O que você gostaria de fazer?",
                "agent": "Master Agent",
                "capabilities": ["coordenação", "roteamento", "contexto", "estratégia"],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "content": f"🤖 **Master Agent - Coordenador NTEX!**\n\n"
                          f"**Sua solicitação:** {message}\n\n"
                          f"**Como posso coordenar os agentes:**\n"
                          f"• **Copy Agent:** Para criação de conteúdo e copy\n"
                          f"• **Design Agent:** Para elementos visuais e templates\n"
                          f"• **Master Agent:** Para estratégia e coordenação\n\n"
                          f"**Sugestão:** Seja mais específico sobre o que precisa:\n"
                          f"• Tipo de conteúdo (post, anúncio, campanha)\n"
                          f"• Objetivo (vendas, engajamento, awareness)\n"
                          f"• Público-alvo (B2B, B2C, nicho específico)\n\n"
                          f"Como posso ajudar de forma mais direcionada?",
                "agent": "Master Agent",
                "capabilities": ["coordenação", "roteamento", "contexto", "estratégia"],
                "timestamp": datetime.now().isoformat()
            }

# Sessões ativas
active_sessions: Dict[str, ChatSession] = {}

@app.route('/')
def home():
    """Página principal com interface de chat"""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint para chat com agentes"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id')
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in active_sessions:
            active_sessions[session_id] = ChatSession(session_id)
        
        chat_session = active_sessions[session_id]
        
        # Adicionar mensagem do usuário
        user_message = chat_session.add_message("user", message)
        
        # Determinar qual agente usar baseado no conteúdo usando lógica inteligente
        message_lower = message.lower()
        
        # Usar agentes reais se disponíveis, senão fallback para simulados
        if hasattr(master_agent, 'process_message'):
            # Agentes reais - usar roteamento inteligente
            if any(word in message_lower for word in ['instagram', 'post', 'rede social', 'copy', 'texto', 'anúncio']):
                agent_name = "Copy Agent"
                response = copy_agent.process_message(message)
            elif any(word in message_lower for word in ['design', 'visual', 'imagem', 'template', 'arte', 'branding']):
                agent_name = "Design Agent"
                response = design_agent.process_message(message)
            elif any(word in message_lower for word in ['campanha', 'estratégia', 'plano', 'coordenar']):
                agent_name = "Master Agent"
                response = master_agent.process_message(message)
            else:
                # Roteamento inteligente - deixar o Master Agent decidir
                agent_name = "Master Agent"
                response = master_agent.process_message(message)
        else:
            # Fallback para agentes simulados
            if any(word in message_lower for word in ['instagram', 'post', 'rede social', 'copy', 'texto']):
                agent_name = "Copy Agent"
                response = chat_session._process_copy_request(message, message_lower)
            elif any(word in message_lower for word in ['design', 'visual', 'imagem', 'template', 'arte']):
                agent_name = "Design Agent"
                response = chat_session._process_design_request(message, message_lower)
            elif any(word in message_lower for word in ['campanha', 'estratégia', 'plano']):
                agent_name = "Master Agent"
                response = chat_session._process_master_request(message, message_lower)
            else:
                agent_name = "Master Agent"
                response = chat_session._process_master_request(message, message_lower)
        
        # Adicionar resposta do agente
        agent_message = chat_session.add_message("assistant", response["content"], agent_name)
        
        # Adicionar log do agente
        chat_session.add_agent_log(
            agent_name=agent_name,
            message=f"Processando mensagem: {message[:50]}...",
            log_level="info",
            log_type="execution"
        )
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "response": response["content"],
            "agent": agent_name,
            "capabilities": response["capabilities"]
        })
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/sessions', methods=['GET'])
def list_sessions():
    """Lista todas as sessões ativas"""
    try:
        sessions = []
        for session_id, chat_session in active_sessions.items():
            if chat_session.messages:
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

@app.route('/api/agents/status', methods=['GET'])
def get_agents_status():
    """Retorna status dos agentes"""
    try:
        status = {
            "master_agent": {
                "status": master_agent.status,
                "name": master_agent.name,
                "capabilities": master_agent.capabilities
            },
            "copy_agent": {
                "status": copy_agent.status,
                "name": copy_agent.name,
                "capabilities": copy_agent.capabilities
            },
            "design_agent": {
                "status": design_agent.status,
                "name": design_agent.name,
                "capabilities": design_agent.capabilities
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
    print(f"🚀 Interface de Chat NTEX iniciando na porta {port}...")
    print(f"📱 Acesse: http://localhost:{port}")
    print("💡 Use /help para ver comandos disponíveis")
    app.run(host='0.0.0.0', port=port, debug=True)
