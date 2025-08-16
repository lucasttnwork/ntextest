#!/usr/bin/env python3
"""
Configuração do Framework Agno para Agentes NTEX
Implementa arquitetura otimizada com Agent Teams e Workflows
"""

import os
import logging
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgnoConfig:
    """Configuração centralizada para o framework Agno"""
    
    def __init__(self):
        """Inicializa configuração do Agno"""
        self.agno_available = self._check_agno_availability()
        
        if self.agno_available:
            self._init_agno_config()
        else:
            logger.warning("Framework Agno não disponível. Usando configuração fallback.")
            self._init_fallback_config()
    
    def _check_agno_availability(self) -> bool:
        """Verifica se o framework Agno está disponível"""
        try:
            import agno
            logger.info(f"Framework Agno disponível: versão {agno.__version__}")
            return True
        except ImportError:
            logger.warning("Framework Agno não encontrado. Execute: pip install agno")
            return False
    
    def _init_agno_config(self):
        """Inicializa configuração para framework Agno"""
        # Configurações de modelo
        self.models = {
            "openai": {
                "gpt-4": {
                    "id": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "api_key": os.getenv("OPENAI_API_KEY")
                },
                "gpt-5": {
                    "id": "gpt-5",
                    "temperature": 0.8,
                    "max_tokens": 4000,
                    "api_key": os.getenv("OPENAI_API_KEY")
                }
            },
            "anthropic": {
                "claude-3-sonnet": {
                    "id": "claude-3-sonnet-20240229",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "api_key": os.getenv("ANTHROPIC_API_KEY")
                }
            }
        }
        
        # Configurações de ferramentas
        self.tools = {
            "reasoning": {
                "enabled": True,
                "add_instructions": True,
                "reasoning_model": "chain-of-thought"
            },
            "storage": {
                "enabled": True,
                "driver": "memory",  # memory, file, database
                "persistence": True
            },
            "memory": {
                "enabled": True,
                "max_messages": 100,
                "summarization": True
            }
        }
        
        # Configurações de Agent Teams
        self.agent_teams = {
            "enabled": True,
            "coordination": "hierarchical",  # hierarchical, collaborative, autonomous
            "communication": "structured",   # structured, natural, hybrid
            "decision_making": "consensus"   # consensus, leader, voting
        }
        
        # Configurações de Workflows
        self.workflows = {
            "enabled": True,
            "execution": "deterministic",  # deterministic, probabilistic, adaptive
            "state_management": True,
            "error_handling": "retry",      # retry, fallback, abort
            "monitoring": True
        }
        
        # Configurações de performance
        self.performance = {
            "max_concurrent_agents": 5,
            "timeout_seconds": 30,
            "retry_attempts": 3,
            "cache_enabled": True
        }
        
        logger.info("Configuração Agno inicializada com sucesso")
    
    def _init_fallback_config(self):
        """Inicializa configuração fallback sem Agno"""
        self.models = {
            "openai": {
                "gpt-4": {
                    "id": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "api_key": os.getenv("OPENAI_API_KEY")
                }
            }
        }
        
        self.tools = {
            "reasoning": {"enabled": False},
            "storage": {"enabled": False},
            "memory": {"enabled": False}
        }
        
        self.agent_teams = {"enabled": False}
        self.workflows = {"enabled": False}
        self.performance = {"max_concurrent_agents": 1}
        
        logger.info("Configuração fallback inicializada")
    
    def get_model_config(self, provider: str, model_name: str) -> Optional[Dict[str, Any]]:
        """Obtém configuração de modelo específico"""
        return self.models.get(provider, {}).get(model_name)
    
    def get_tool_config(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Obtém configuração de ferramenta específica"""
        return self.tools.get(tool_name)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Verifica se uma funcionalidade está habilitada"""
        feature_map = {
            "agent_teams": self.agent_teams.get("enabled", False),
            "workflows": self.workflows.get("enabled", False),
            "reasoning": self.tools.get("reasoning", {}).get("enabled", False),
            "storage": self.tools.get("storage", {}).get("enabled", False),
            "memory": self.tools.get("memory", {}).get("enabled", False)
        }
        return feature_map.get(feature, False)
    
    def get_agno_agent_config(self, agent_type: str) -> Dict[str, Any]:
        """Obtém configuração específica para tipo de agente"""
        base_config = {
            "model": self.models["openai"]["gpt-4"],
            "tools": [],
            "instructions": "",
            "markdown": True
        }
        
        if agent_type == "master":
            base_config.update({
                "tools": ["reasoning", "storage", "memory"] if self.agno_available else [],
                "instructions": """
                Você é o Master Agent da NTEX, especialista em coordenação de campanhas de marketing digital.
                Suas responsabilidades incluem:
                1. Criar estratégias de campanha
                2. Coordenar outros agentes especializados
                3. Gerenciar to-do lists e workflows
                4. Analisar resultados e performance
                5. Tomar decisões estratégicas baseadas em dados
                
                Sempre use raciocínio estruturado e forneça respostas claras e acionáveis.
                """
            })
        
        elif agent_type == "copy":
            base_config.update({
                "tools": ["reasoning"] if self.agno_available else [],
                "instructions": """
                Você é o Copy Agent da NTEX, especialista em copywriting e criação de conteúdo.
                Suas responsabilidades incluem:
                1. Criar copy para redes sociais
                2. Desenvolver anúncios publicitários
                3. Escrever emails e newsletters
                4. Criar landing pages
                5. Otimizar conteúdo para conversão
                
                Sempre use tom profissional, confiável e inovador, focado em resultados.
                """
            })
        
        elif agent_type == "design":
            base_config.update({
                "tools": ["reasoning"] if self.agno_available else [],
                "instructions": """
                Você é o Design Agent da NTEX, especialista em design visual e criatividade.
                Suas responsabilidades incluem:
                1. Criar designs para redes sociais
                2. Desenvolver elementos visuais para anúncios
                3. Criar identidade visual e branding
                4. Design de landing pages e websites
                5. Desenvolver templates reutilizáveis
                
                Sempre use estilo moderno, limpo e profissional, focado em engajamento e conversão.
                """
            })
        
        return base_config
    
    def get_workflow_config(self, workflow_type: str) -> Dict[str, Any]:
        """Obtém configuração específica para tipo de workflow"""
        base_config = {
            "execution": self.workflows.get("execution", "deterministic"),
            "state_management": self.workflows.get("state_management", True),
            "error_handling": self.workflows.get("error_handling", "retry"),
            "monitoring": self.workflows.get("monitoring", True)
        }
        
        if workflow_type == "campaign_creation":
            base_config.update({
                "steps": [
                    "briefing_creation",
                    "strategy_development",
                    "task_allocation",
                    "agent_coordination",
                    "execution_monitoring"
                ],
                "dependencies": {
                    "strategy_development": ["briefing_creation"],
                    "task_allocation": ["strategy_development"],
                    "agent_coordination": ["task_allocation"],
                    "execution_monitoring": ["agent_coordination"]
                }
            })
        
        elif workflow_type == "content_creation":
            base_config.update({
                "steps": [
                    "content_brief",
                    "copy_creation",
                    "design_creation",
                    "review_approval",
                    "publication"
                ],
                "dependencies": {
                    "copy_creation": ["content_brief"],
                    "design_creation": ["content_brief"],
                    "review_approval": ["copy_creation", "design_creation"],
                    "publication": ["review_approval"]
                }
            })
        
        return base_config
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Obtém configuração de performance"""
        return self.performance
    
    def validate_config(self) -> Dict[str, Any]:
        """Valida configuração atual"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        # Verificar API keys
        if not os.getenv("OPENAI_API_KEY"):
            validation_result["errors"].append("OPENAI_API_KEY não encontrada")
            validation_result["valid"] = False
        
        # Verificar funcionalidades Agno
        if not self.agno_available:
            validation_result["warnings"].append("Framework Agno não disponível")
            validation_result["recommendations"].append("Instalar Agno: pip install agno")
        
        # Verificar configurações de modelo
        for provider, models in self.models.items():
            for model_name, config in models.items():
                if not config.get("api_key"):
                    validation_result["warnings"].append(f"API key não configurada para {provider}/{model_name}")
        
        # Verificar ferramentas
        for tool_name, config in self.tools.items():
            if config.get("enabled") and not self.agno_available:
                validation_result["warnings"].append(f"Ferramenta {tool_name} habilitada mas Agno não disponível")
        
        return validation_result
    
    def get_installation_guide(self) -> str:
        """Retorna guia de instalação do Agno"""
        return """
        🚀 INSTALAÇÃO DO FRAMEWORK AGNO
        
        Para habilitar todas as funcionalidades avançadas:
        
        1. Instalar Agno:
           pip install agno
        
        2. Configurar variáveis de ambiente:
           export OPENAI_API_KEY="sua_chave_aqui"
           export ANTHROPIC_API_KEY="sua_chave_aqui"  # Opcional
        
        3. Verificar instalação:
           python -c "import agno; print(f'Agno {agno.__version__} instalado')"
        
        4. Reiniciar sistema de agentes
        
        📚 Documentação: https://docs.agno.com
        """
    
    def get_upgrade_path(self) -> Dict[str, Any]:
        """Retorna caminho de upgrade para funcionalidades avançadas"""
        current_level = 1 if not self.agno_available else 3
        
        upgrade_path = {
            "current_level": current_level,
            "next_level": current_level + 1,
            "steps": [],
            "benefits": []
        }
        
        if current_level == 1:
            upgrade_path["steps"] = [
                "Instalar framework Agno",
                "Configurar Agent com ReasoningTools",
                "Implementar Storage e Memory"
            ]
            upgrade_path["benefits"] = [
                "Agentes com raciocínio estruturado",
                "Memória persistente entre sessões",
                "Armazenamento de dados e contexto"
            ]
        
        elif current_level == 3:
            upgrade_path["steps"] = [
                "Implementar Agent Teams",
                "Configurar coordenação hierárquica",
                "Adicionar comunicação estruturada"
            ]
            upgrade_path["benefits"] = [
                "Coordenação automática entre agentes",
                "Tomada de decisões colaborativa",
                "Workflows determinísticos"
            ]
        
        elif current_level == 4:
            upgrade_path["steps"] = [
                "Implementar Workflows avançados",
                "Adicionar monitoramento em tempo real",
                "Configurar avaliação automática"
            ]
            upgrade_path["benefits"] = [
                "Automação completa de processos",
                "Monitoramento de performance",
                "Melhoria contínua dos agentes"
            ]
        
        return upgrade_path

# Instância global da configuração
agno_config = AgnoConfig()

def get_agno_config() -> AgnoConfig:
    """Retorna instância global da configuração Agno"""
    return agno_config
