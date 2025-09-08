#!/usr/bin/env python3
"""
Gary Bencivenga Agent - Sistema simples com Agno
Agente especialista em copywriting usando framework Agno
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GaryBencivengaAgent:
    """Agente Gary Bencivenga usando framework Agno"""
    
    def __init__(self):
        """Inicializa o agente Gary Bencivenga"""
        self.name = "Gary_Bencivenga_Agent"
        
        # Carregar prompt
        self.prompt_text = self._load_prompt()
        
        # Configuração OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não encontrada no .env")
        
        # Configurar ferramentas de busca web
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        tools = []
        if tavily_api_key:
            tools.append(TavilyTools(api_key=tavily_api_key))

        # Inicializar agente Agno com GPT-5-mini
        self.agent = Agent(
            model=OpenAIChat(id="gpt-5-mini"),
            instructions=self._get_instructions(),
            tools=tools,
            markdown=True,
            add_datetime_to_instructions=True,
            show_tool_calls=True
        )
        
        logger.info("Gary Bencivenga Agent inicializado com Agno")
    
    def _load_prompt(self) -> str:
        """Carrega o prompt do Gary Bencivenga"""
        prompt_path = Path(__file__).parent.parent / 'prompts' / 'Gary_Bencivenga_Agent.md'
        try:
            return prompt_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Erro ao carregar prompt: {e}")
            return "Você é Gary Bencivenga, especialista em copywriting."
    
    def _get_instructions(self) -> str:
        """Retorna as instruções completas para o agente"""
        base_instructions = f"""
        Você é Gary Bencivenga, o maior copywriter vivo da história.
        
        SEU BACKGROUND:
        {self.prompt_text}
        
        SUA MISSÃO:
        - Criar copywriting de alta conversão
        - Usar técnicas comprovadas de marketing direto
        - Focar em headlines persuasivas e calls-to-action poderosos
        - Sempre pensar em termos de benefícios para o cliente
        
        DIRETRIZES DE COMUNICAÇÃO:
        - Seja direto e persuasivo
        - Use linguagem simples mas poderosa
        - Foque em resultados mensuráveis
        - Sempre termine com uma call-to-action clara
        
        Quando receber uma solicitação, analise o contexto e crie copy baseado nas técnicas de Gary Bencivenga.
        """
        
        return base_instructions
    
    def process_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Processa uma solicitação usando o Agno Agent"""
        try:
            # Preparar prompt completo
            full_prompt = f"""
            SOLICITAÇÃO: {message}
            
            CONTEXTO ADICIONAL: {context or 'Nenhum contexto adicional'}
            
            Como Gary Bencivenga, crie uma resposta baseada nas suas técnicas de copywriting.
            Foque em:
            1. Headline forte
            2. Benefícios claros
            3. Prova social quando aplicável
            4. Call-to-action persuasivo
            """
            
            # Usar Agno para processar
            response = self.agent.run(full_prompt)
            
            return {
                "success": True,
                "response": response.content if hasattr(response, 'content') else str(response),
                "agent": self.name,
                "processed_with": "Agno Agent"
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }

def get_gary_agent() -> GaryBencivengaAgent:
    """Factory para obter o agente Gary"""
    return GaryBencivengaAgent()

# Teste do agente
if __name__ == "__main__":
    try:
        agent = get_gary_agent()
        result = agent.process_request("Crie um anúncio para um curso de copywriting")
        print("✅ Gary Agent funcionando!")
        print(f"Resposta: {result['response'][:200]}...")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
