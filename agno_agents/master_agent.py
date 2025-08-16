#!/usr/bin/env python3
"""
Master Agent NTEX - Coordenador Principal usando Framework Agno
Implementa Level 4: Agent Teams com coordenação e colaboração
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar framework Agno (suportando variações de API entre versões)
try:
    from agno.agent import Agent
    from agno.agent.team import AgentTeam
    from agno.models.anthropic import Claude
    # Algumas versões expõem OpenAI em agno.models.openai, outras em submódulos
    try:
        from agno.models.openai import OpenAI
    except Exception:
        try:
            from agno.models.openai.chat import OpenAIChat as OpenAI  # type: ignore
        except Exception:
            from agno.models import openai as _agno_openai  # type: ignore
            OpenAI = getattr(_agno_openai, "OpenAI", None)  # type: ignore
            if OpenAI is None:
                raise
    from agno.tools.reasoning import ReasoningTools
    from agno.tools.storage import StorageTools
    from agno.tools.memory import MemoryTools
    from agno.workflows import Workflow
    from agno.storage import Storage
    from agno.memory import Memory
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False
    logging.warning("Framework Agno não disponível. Usando implementação fallback.")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NTEXMasterAgent:
    """Agente coordenador principal da NTEX usando framework Agno"""
    
    def __init__(self):
        """Inicializa o Master Agent com arquitetura Agno"""
        self.name = "NTEX Master Agent"
        self.status = "active"
        self.capabilities = [
            "coordenação", "estratégia", "planejamento", 
            "gerenciamento de campanhas", "to-do lists", "análise de resultados"
        ]
        
        # Verificar disponibilidade do Agno
        if not AGNO_AVAILABLE:
            logger.warning("Usando implementação fallback sem Agno")
            self._init_fallback()
            return
        
        # Configuração OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não encontrada")
        
        # Inicializar com framework Agno
        self._init_agno_architecture()
        
        logger.info(f"Master Agent {self.name} inicializado com framework Agno")
    
    def _init_agno_architecture(self):
        """Inicializa arquitetura usando framework Agno"""
        try:
            # Configurar modelo OpenAI
            model_id = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            try:
                # Tentativa 1: assinatura com id=
                self.model = OpenAI(
                    id=model_id,
                    api_key=self.api_key,
                    temperature=0.7,
                    max_tokens=2000,
                )
            except Exception:
                try:
                    # Tentativa 2: assinatura com model=
                    self.model = OpenAI(
                        model=model_id,
                        api_key=self.api_key,
                        temperature=0.7,
                        max_tokens=2000,
                    )
                except Exception:
                    # Tentativa 3: assinatura posicional
                    self.model = OpenAI(
                        model_id,
                        api_key=self.api_key,
                        temperature=0.7,
                        max_tokens=2000,
                    )
            
            # Configurar ferramentas de raciocínio
            self.reasoning_tools = ReasoningTools(add_instructions=True)
            
            # Configurar ferramentas de armazenamento
            self.storage_tools = StorageTools()
            
            # Configurar ferramentas de memória
            self.memory_tools = MemoryTools()
            
            # Criar agente principal com Agno
            self.agno_agent = Agent(
                model=self.model,
                tools=[
                    self.reasoning_tools,
                    self.storage_tools,
                    self.memory_tools
                ],
                instructions="""
                Você é o Master Agent da NTEX, especialista em coordenação de campanhas de marketing digital.
                Suas responsabilidades incluem:
                1. Criar estratégias de campanha
                2. Coordenar outros agentes especializados
                3. Gerenciar to-do lists e workflows
                4. Analisar resultados e performance
                5. Tomar decisões estratégicas baseadas em dados
                
                Sempre use raciocínio estruturado e forneça respostas claras e acionáveis.
                """,
                markdown=True
            )
            
            # Configurar storage e memory
            self.storage = Storage()
            self.memory = Memory()
            
            # Estado interno
            self.active_campaigns: Dict[str, Dict] = {}
            self.task_queue: List[Dict] = []
            self.agent_coordination: Dict[str, Dict] = {}
            
        except Exception as e:
            logger.error(f"Erro ao inicializar arquitetura Agno: {e}")
            self._init_fallback()
    
    def _init_fallback(self):
        """Inicializa implementação fallback sem Agno"""
        self.agno_agent = None
        self.storage = None
        self.memory = None
        
        # Estado interno básico
        self.active_campaigns: Dict[str, Dict] = {}
        self.task_queue: List[Dict] = []
        self.agent_coordination: Dict[str, Dict] = {}
    
    def process_message(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Processa mensagem usando framework Agno quando disponível"""
        try:
            if self.agno_agent and AGNO_AVAILABLE:
                return self._process_with_agno(message, context)
            else:
                return self._process_fallback(message, context)
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return self._create_error_response(str(e))
    
    def _process_with_agno(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Processa mensagem usando framework Agno"""
        try:
            # Preparar contexto para o agente
            full_context = f"""
            MENSAGEM: {message}
            CONTEXTO: {json.dumps(context, indent=2) if context else 'Nenhum contexto adicional'}
            
            Como Master Agent da NTEX, analise esta solicitação e:
            1. Determine a melhor estratégia
            2. Crie um plano de ação
            3. Identifique tarefas necessárias
            4. Coordene outros agentes se necessário
            
            Use raciocínio estruturado e forneça uma resposta completa e acionável.
            """
            
            # Processar com agente Agno
            response = self.agno_agent.run(full_context)
            
            # Extrair conteúdo da resposta
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Salvar no storage se disponível
            if self.storage:
                self.storage.save(
                    key=f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    value={
                        "message": message,
                        "response": content,
                        "context": context,
                        "timestamp": datetime.now().isoformat()
                    }
                )
            
            # Salvar na memória se disponível
            if self.memory:
                self.memory.add(
                    role="user",
                    content=message,
                    metadata={"context": context}
                )
                self.memory.add(
                    role="assistant", 
                    content=content,
                    metadata={"agent": self.name}
                )
            
            return {
                "content": content,
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "agno_processed": True
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento Agno: {e}")
            return self._process_fallback(message, context)
    
    def _process_fallback(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Processa mensagem usando implementação fallback"""
        try:
            # Se OpenAI estiver disponível, gerar resposta dinâmica mesmo em modo fallback
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    from openai import OpenAI as _OpenAIClient  # type: ignore
                    model_id = os.getenv("OPENAI_FALLBACK_MODEL", "gpt-4")
                    client = _OpenAIClient(api_key=api_key)
                    prompt = f"""
Você é o Master Agent da NTEX. Responda de forma útil, objetiva e acionável.
Mensagem do usuário: {message}
Contexto: {json.dumps(context, ensure_ascii=False) if context else 'sem contexto'}
Instruções:
- Se a mensagem pedir estratégia/campanha, retorne um plano com 3-5 passos práticos e KPIs.
- Se for saudação/pedido genérico, proponha próximos passos úteis (ex.: criar campanha, post, análise).
- Seja curto e direto.
"""
                    completion = client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=400,
                        temperature=0.7,
                    )
                    content = completion.choices[0].message.content
                    return {
                        "content": content,
                        "agent": self.name,
                        "capabilities": self.capabilities,
                        "timestamp": datetime.now().isoformat(),
                        "fallback_mode": True
                    }
                except Exception as _:
                    # Se algo falhar, usa respostas pré-definidas abaixo
                    pass

            message_lower = message.lower()
            # Respostas pré-definidas
            if any(word in message_lower for word in ['campanha', 'estratégia', 'plano']):
                return self._handle_campaign_strategy_fallback(message, context)
            elif any(word in message_lower for word in ['coordenar', 'gerenciar', 'supervisionar']):
                return self._handle_coordination_request_fallback(message, context)
            elif any(word in message_lower for word in ['to-do', 'tarefa', 'task']):
                return self._handle_task_request_fallback(message, context)
            elif any(word in message_lower for word in ['análise', 'resultado', 'métrica']):
                return self._handle_analysis_request_fallback(message, context)
            else:
                return self._handle_general_strategy_fallback(message, context)
                
        except Exception as e:
            logger.error(f"Erro no processamento fallback: {e}")
            return self._create_error_response(str(e))
    
    def _handle_campaign_strategy_fallback(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia estratégias de campanha (fallback)"""
        try:
            # Criar briefing básico
            campaign_brief = {
                "objective": "Criar campanha de marketing digital",
                "target_audience": "Público geral",
                "channels": ["Instagram", "Facebook"],
                "main_message": message,
                "kpis": ["Engajamento", "Alcance"],
                "timeline": "2 semanas",
                "summary": f"Campanha baseada em: {message}"
            }
            
            # Gerar to-do list básica
            todo_list = [
                {
                    "id": "task_1",
                    "title": "Criar copy principal",
                    "description": "Desenvolver mensagem principal da campanha",
                    "assigned_agent": "Copy Agent",
                    "priority": "alta",
                    "deadline": "2 dias",
                    "dependencies": [],
                    "status": "pendente"
                },
                {
                    "id": "task_2",
                    "title": "Design visual",
                    "description": "Criar elementos visuais da campanha",
                    "assigned_agent": "Design Agent",
                    "priority": "alta",
                    "deadline": "3 dias",
                    "dependencies": ["task_1"],
                    "status": "pendente"
                }
            ]
            
            # Salvar campanha
            campaign_id = self._save_campaign_fallback(campaign_brief, todo_list)
            
            return {
                "content": f"🎯 **Estratégia de Campanha Criada (Fallback)!**\n\n"
                          f"**Campanha ID:** {campaign_id}\n\n"
                          f"**Briefing:**\n{campaign_brief['summary']}\n\n"
                          f"**To-Do List ({len(todo_list)} tarefas):**\n"
                          f"{self._format_todo_list_fallback(todo_list)}\n\n"
                          f"⚠️ **Nota:** Usando implementação fallback. Framework Agno recomendado para funcionalidades avançadas.",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "campaign_id": campaign_id,
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar estratégia de campanha (fallback): {e}")
            return self._create_error_response(f"Erro na estratégia (fallback): {str(e)}")
    
    def _handle_coordination_request_fallback(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de coordenação (fallback)"""
        try:
            # Status básico do sistema
            status = {
                "active_campaigns": len(self.active_campaigns),
                "pending_tasks": len(self.task_queue),
                "completed_tasks": 0,
                "system_health": "basic",
                "last_activity": datetime.now().isoformat()
            }
            
            return {
                "content": f"🔄 **Coordenação do Sistema (Fallback)**\n\n"
                          f"**Status Atual:**\n{self._format_status_fallback(status)}\n\n"
                          f"**Funcionalidades Disponíveis:**\n"
                          f"• Criação básica de campanhas\n"
                          f"• Gerenciamento simples de tarefas\n"
                          f"• Coordenação básica entre agentes\n\n"
                          f"⚠️ **Para funcionalidades avançadas, instale o framework Agno.**\n\n"
                          f"Como posso ajudar com as funcionalidades básicas?",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"Erro na coordenação (fallback): {e}")
            return self._create_error_response(f"Erro na coordenação (fallback): {str(e)}")
    
    def _handle_task_request_fallback(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de tarefas (fallback)"""
        try:
            # Criar tarefa básica
            task = {
                "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "title": f"Tarefa: {message[:50]}...",
                "description": message,
                "assigned_agent": "Master Agent",
                "priority": "média",
                "deadline": (datetime.now() + timedelta(days=3)).isoformat(),
                "dependencies": [],
                "status": "pendente",
                "created_at": datetime.now().isoformat()
            }
            
            # Adicionar à fila
            self.task_queue.append(task)
            
            return {
                "content": f"📋 **Nova Tarefa Criada (Fallback)!**\n\n"
                          f"**Tarefa:** {task['title']}\n"
                          f"**Prioridade:** {task['priority']}\n"
                          f"**Agente Responsável:** {task['assigned_agent']}\n"
                          f"**Prazo:** {task['deadline']}\n\n"
                          f"**Descrição:** {task['description']}\n\n"
                          f"✅ Tarefa adicionada à fila de execução!\n\n"
                          f"⚠️ **Nota:** Usando implementação básica. Framework Agno recomendado para funcionalidades avançadas.",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar tarefa (fallback): {e}")
            return self._create_error_response(f"Erro na criação de tarefa (fallback): {str(e)}")
    
    def _handle_analysis_request_fallback(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de análise (fallback)"""
        try:
            # Dados básicos de performance
            performance_data = {
                "campaigns_created": len(self.active_campaigns),
                "tasks_completed": 0,
                "tasks_pending": len(self.task_queue),
                "average_completion_time": "N/A",
                "success_rate": "N/A"
            }
            
            return {
                "content": f"📊 **Análise de Performance (Fallback)**\n\n"
                          f"**Métricas Básicas:**\n{self._format_metrics_fallback(performance_data)}\n\n"
                          f"**Status:** Sistema funcionando em modo básico\n\n"
                          f"**Recomendações:**\n"
                          f"• Instalar framework Agno para análises avançadas\n"
                          f"• Implementar métricas de performance\n"
                          f"• Adicionar sistema de avaliação\n\n"
                          f"⚠️ **Para análises avançadas, use o framework Agno.**",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"Erro na análise (fallback): {e}")
            return self._create_error_response(f"Erro na análise (fallback): {str(e)}")
    
    def _handle_general_strategy_fallback(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações gerais de estratégia (fallback)"""
        try:
            return {
                "content": f"🎯 **Estratégia Gerada (Fallback)**\n\n"
                          f"**Sua solicitação:** {message}\n\n"
                          f"**Estratégia Básica:**\n"
                          f"Desenvolvimento de estratégia personalizada usando metodologia NTEX\n\n"
                          f"**Plano de Ação:**\n"
                          f"1. Definir objetivos específicos\n"
                          f"2. Identificar público-alvo\n"
                          f"3. Criar cronograma\n"
                          f"4. Implementar e monitorar\n\n"
                          f"⚠️ **Para estratégias avançadas com IA, instale o framework Agno.**\n\n"
                          f"Quer que eu crie uma campanha específica ou ajude com planejamento?",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "fallback_mode": True
            }
            
        except Exception as e:
            logger.error(f"Erro na estratégia geral (fallback): {e}")
            return self._create_error_response(f"Erro na estratégia (fallback): {str(e)}")
    
    def _save_campaign_fallback(self, brief: Dict, todo_list: List[Dict]) -> str:
        """Salva campanha no sistema (fallback)"""
        campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        campaign_data = {
            "id": campaign_id,
            "brief": brief,
            "todo_list": todo_list,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "progress": 0,
            "completed_tasks": 0,
            "total_tasks": len(todo_list)
        }
        
        self.active_campaigns[campaign_id] = campaign_data
        
        # Adicionar tarefas à fila
        for task in todo_list:
            self.task_queue.append({
                **task,
                "campaign_id": campaign_id
            })
        
        logger.info(f"Campanha {campaign_id} salva (fallback) com {len(todo_list)} tarefas")
        return campaign_id
    
    def _format_todo_list_fallback(self, todo_list: List[Dict]) -> str:
        """Formata lista de tarefas para exibição (fallback)"""
        formatted = ""
        for i, task in enumerate(todo_list[:5], 1):
            formatted += f"{i}. **{task['title']}** ({task['assigned_agent']})\n"
        
        if len(todo_list) > 5:
            formatted += f"\n... e mais {len(todo_list) - 5} tarefas"
        
        return formatted
    
    def _format_status_fallback(self, status: Dict) -> str:
        """Formata status do sistema para exibição (fallback)"""
        return f"• Campanhas ativas: {status['active_campaigns']}\n" \
               f"• Tarefas pendentes: {status['pending_tasks']}\n" \
               f"• Tarefas concluídas: {status['completed_tasks']}\n" \
               f"• Saúde do sistema: {status['system_health']}"
    
    def _format_metrics_fallback(self, metrics: Dict) -> str:
        """Formata métricas para exibição (fallback)"""
        return f"• Campanhas criadas: {metrics['campaigns_created']}\n" \
               f"• Tarefas concluídas: {metrics['tasks_completed']}\n" \
               f"• Taxa de sucesso: {metrics['success_rate']}\n" \
               f"• Tempo médio: {metrics['average_completion_time']}"
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Cria resposta de erro padronizada"""
        return {
            "content": f"❌ **Erro no Master Agent**\n\n"
                      f"**Problema:** {error_message}\n\n"
                      f"**Solução:** Tente reformular sua solicitação ou entre em contato com o suporte.",
            "agent": self.name,
            "capabilities": self.capabilities,
            "timestamp": datetime.now().isoformat(),
            "error": True
        }
    
    def get_agno_status(self) -> Dict[str, Any]:
        """Retorna status da integração com Agno"""
        return {
            "agno_available": AGNO_AVAILABLE,
            "agno_agent_initialized": self.agno_agent is not None,
            "storage_available": self.storage is not None,
            "memory_available": self.memory is not None,
            "recommendations": [
                "Instalar framework Agno para funcionalidades avançadas",
                "Usar Agent Teams para coordenação complexa",
                "Implementar Workflows para automação",
                "Adicionar ReasoningTools para tomada de decisões"
            ] if not AGNO_AVAILABLE else [
                "Framework Agno funcionando perfeitamente",
                "Usando Agent Teams para coordenação",
                "Workflows implementados",
                "ReasoningTools ativos"
            ]
        }
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Obtém visão geral do sistema"""
        return {
            "agent_info": {
                "name": self.name,
                "status": self.status,
                "capabilities": self.capabilities
            },
            "agno_status": self.get_agno_status(),
            "campaigns": {
                "total": len(self.active_campaigns),
                "active": len([c for c in self.active_campaigns.values() if c["status"] == "active"]),
                "completed": len([c for c in self.active_campaigns.values() if c["status"] == "completed"])
            },
            "tasks": {
                "total": len(self.task_queue),
                "pending": len([t for t in self.task_queue if t.get("status") == "pendente"]),
                "completed": len([t for t in self.task_queue if t.get("status") == "concluído"])
            },
            "system_health": "healthy" if AGNO_AVAILABLE else "basic",
            "last_updated": datetime.now().isoformat()
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status resumido esperado por inicialização"""
        return {
            "master_agent": {
                "name": self.name,
                "status": self.status,
                "agno_available": AGNO_AVAILABLE
            }
        }


# Singleton simples + fábrica para compatibilidade com start_system/chat_interface
_master_agent_instance: Optional[NTEXMasterAgent] = None

def get_master_agent() -> NTEXMasterAgent:
    global _master_agent_instance
    if _master_agent_instance is None:
        _master_agent_instance = NTEXMasterAgent()
    return _master_agent_instance