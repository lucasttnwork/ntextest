#!/usr/bin/env python3
"""
NTEX Copywriter Agent - Agente de IA especializado em copywriting
================================================================

Este agente é projetado para:
- Criar copy de alta qualidade seguindo as diretrizes NTEX
- Realizar pesquisas na internet para informações atualizadas
- Gerar textos longos com capacidade de 128k tokens via OpenRouter
- Usar modelo Grok da xAI para máxima performance
- Manter consistência com o tom de voz da marca

Autor: NTEX (Lucas)
Versão: 2.0.0 - OpenRouter + Grok + 128k tokens
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importações de IA
try:
    import requests
    from tavily import TavilyClient
except ImportError:
    logger.error("Bibliotecas necessárias não instaladas. Instale com: pip install requests tavily-python")
    exit(1)

class NTEXCopywriterAgent:
    """
    Agente de copywriting especializado NTEX
    """
    
    def __init__(self):
        self.setup_clients()
        self.load_prompts()
        self.conversation_history = []
        
    def setup_clients(self):
        """Configura clientes de API"""
        # OpenRouter Configuration
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if not self.openrouter_key:
            raise ValueError("OPENROUTER_API_KEY não encontrada no .env")
        
        self.openrouter_url = "https://openrouter.ai/api/v1"
        self.model_name = os.getenv("OPENROUTER_MODEL", "x-ai/grok-code-fast-1")  # Grok modelo principal
        
        # Headers para OpenRouter
        self.openrouter_headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "https://ntex.com.br"),  # Sua URL
            "X-Title": os.getenv("OPENROUTER_TITLE", "NTEX Copywriter Agent"),
            "Content-Type": "application/json"
        }
        
        # Tavily (busca na web)
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        if self.tavily_key:
            self.tavily_client = TavilyClient(api_key=self.tavily_key)
            self.search_enabled = True
        else:
            logger.warning("TAVILY_API_KEY não encontrada - busca na web desabilitada")
            self.search_enabled = False
    
    def load_prompts(self):
        """Carrega prompts do sistema NTEX"""
        prompts_path = Path("/Users/lucasttn/Documents/Documents/Cérebro NTEX/prompts")
        
        self.system_prompt = """Você é o NTEX-Copywriter, um agente de IA especializado em copywriting da NTEX.

CARACTERÍSTICAS DO TOM NTEX:
- Direto, punchy, zero buzzwords
- Frases curtas e objetivas  
- Valor primeiro, sempre
- Sem metáforas ou jargões corporativos
- Foco em resultados e benefícios claros

DIRETRIZES DE COPY NTEX:
1. Comece com o valor/resultado principal
2. Use linguagem simples e acessível
3. Seja específico com números e exemplos
4. Estrutura: Problema → Solução → Resultado
5. Call-to-action claro e único

CAPACIDADES:
- Criar copy para ads, emails, landing pages, posts sociais
- Pesquisar informações atualizadas na internet
- Gerar textos longos (até 128k tokens)
- Adaptar tom para diferentes públicos
- Otimizar para SEO e conversão

REGRAS:
- Sempre mantenha o tom NTEX
- Pesquise quando não tiver informações suficientes
- Seja criativo mas baseado em dados
- Revise e aprimore antes de entregar"""

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Realiza busca na web usando Tavily"""
        if not self.search_enabled:
            return []
        
        try:
            response = self.tavily_client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
                include_raw_content=True
            )
            return response.get('results', [])
        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            return []
    
    async def generate_copy(self, 
                          prompt: str, 
                          copy_type: str = "social_post",
                          target_audience: str = "",
                          tone: str = "ntex",
                          max_tokens: int = 4000,
                          include_research: bool = True) -> Dict[str, Any]:
        """
        Gera copy com base no prompt e parâmetros
        
        Args:
            prompt: Descrição do que precisa ser criado
            copy_type: Tipo de copy (social_post, email, landing_page, ad_copy, etc)
            target_audience: Público-alvo
            tone: Tom da mensagem (ntex, formal, casual, urgente)
            max_tokens: Máximo de tokens para gerar
            include_research: Se deve pesquisar na web antes de criar
        
        Returns:
            Dict com copy gerado, sugestões e metadados
        """
        
        # Busca na web se necessário
        research_data = []
        if include_research and self.search_enabled:
            search_query = f"{prompt} {target_audience} marketing copy best practices 2025"
            research_data = await self.search_web(search_query)
        
        # Constrói prompt completo
        full_prompt = self.build_copy_prompt(
            user_prompt=prompt,
            copy_type=copy_type,
            target_audience=target_audience,
            tone=tone,
            research_data=research_data
        )
        
        # Gera copy com OpenRouter e Grok (128k tokens)
        try:
            # Prepara payload para OpenRouter
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                "max_tokens": min(max_tokens, 128000),  # Limite de 128k tokens
                "temperature": 0.7,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
                "stream": False
            }
            
            # Faz requisição para OpenRouter
            response = requests.post(
                f"{self.openrouter_url}/chat/completions",
                headers=self.openrouter_headers,
                json=payload,
                timeout=300  # 5 minutos timeout para textos longos
            )
            
            response.raise_for_status()
            result = response.json()
            
            generated_copy = result['choices'][0]['message']['content']
            
            # Análise e sugestões adicionais
            analysis = await self.analyze_copy(generated_copy, copy_type)
            
            return {
                "copy": generated_copy,
                "analysis": analysis,
                "research_used": len(research_data) > 0,
                "tokens_used": result.get('usage', {}).get('total_tokens', 0),
                "model_used": self.model_name,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar copy com OpenRouter: {e}")
            return {
                "error": str(e),
                "copy": "",
                "analysis": {}
            }
    
    def build_copy_prompt(self, user_prompt: str, copy_type: str, target_audience: str, 
                         tone: str, research_data: List[Dict]) -> str:
        """Constrói prompt detalhado para geração de copy"""
        
        research_context = ""
        if research_data:
            research_context = "\n📊 PESQUISA RECENTE:\n"
            for i, result in enumerate(research_data[:3], 1):
                research_context += f"{i}. {result.get('title', '')}: {result.get('content', '')[:200]}...\n"
        
        audience_context = f"\n🎯 PÚBLICO-ALVO: {target_audience}" if target_audience else ""
        
        copy_guidelines = self.get_copy_guidelines(copy_type)
        
        return f"""{user_prompt}

{audience_context}

{research_context}

📝 TIPO DE COPY: {copy_type}

{copy_guidelines}

⚡ REQUISITOS:
- Seguir rigorosamente o tom NTEX
- Ser persuasivo e orientado a ação
- Incluir call-to-action claro
- Otimizar para conversão
- Gerar copy completo e pronto para uso

🎯 OBJETIVO: Criar copy que converta e venda."""
    
    def get_copy_guidelines(self, copy_type: str) -> str:
        """Obtém diretrizes específicas por tipo de copy"""
        guidelines = {
            "social_post": """📱 DIRETRIZES PARA POST SOCIAL:
- Hook poderoso nos primeiros 3 segundos
- Quebra de linha a cada 1-2 frases
- Emojis estratégicos (máx 3)
- CTA no final
- Hashtags relevantes (5-10)""",
            
            "email": """📧 DIRETRIZES PARA EMAIL:
- Assunto: máx 50 caracteres, urgência/curiosidade
- Preview text: complementa o assunto
- Primeira linha: hook imediato
- Corpo: problema → agitação → solução
- CTA único e específico
- Assinatura com próximos passos""",
            
            "landing_page": """🎯 DIRETRIZES PARA LANDING PAGE:
- Headline: benefício principal + urgência
- Sub-headline: expande o benefício
- Problema: agite a dor do cliente
- Solução: apresente sua oferta
- Prova social: depoimentos/dados
- CTA: claro e repetido
- Garantia: remova o risco""",
            
            "ad_copy": """🚀 DIRETRIZES PARA ANÚNCIO:
- Headline: máx 30 caracteres, benefício direto
- Descrição: expande beneficios
- CTA: ação específica
- Palavras de poder: gratuito, novo, garantido
- Foco em 1 benefício por anúncio"""
        }
        
        return guidelines.get(copy_type, "📋 Use as diretrizes gerais NTEX")
    
    async def analyze_copy(self, copy: str, copy_type: str) -> Dict[str, Any]:
        """Analisa a copy gerada e fornece sugestões"""
        
        analysis_prompt = f"""Analise esta copy NTEX e forneça sugestões de melhoria:

COPY: {copy}

TIPO: {copy_type}

Forneça:
1. Pontos fortes (3)
2. Oportunidades de melhoria (3)
3. Score de conversão (1-10)
4. Sugestões específicas
5. Versão alternativa (se aplicável)

Formato JSON."""
        
        try:
            # Usa OpenRouter para análise também
            analysis_payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Você é um especialista em análise de copywriting. Seja objetivo e prático."},
                    {"role": "user", "content": analysis_prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.3,
                "stream": False
            }
            
            response = requests.post(
                f"{self.openrouter_url}/chat/completions",
                headers=self.openrouter_headers,
                json=analysis_payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            return json.loads(result['choices'][0]['message']['content'])
            
        except Exception as e:
            logger.error(f"Erro na análise com OpenRouter: {e}")
            return {"error": "Análise falhou"}
    
    def save_copy(self, copy_data: Dict, filename: str = None) -> str:
        """Salva copy gerada em arquivo"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"copy_{timestamp}.json"
        
        output_path = Path(f"/Users/lucasttn/Documents/Documents/Cérebro NTEX/output/copywriter/{filename}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(copy_data, f, ensure_ascii=False, indent=2)
        
        return str(output_path)

# Funções de utilidade para interface
async def create_copywriter_agent():
    """Cria e retorna uma instância do agente"""
    return NTEXCopywriterAgent()

async def quick_copy(prompt: str, copy_type: str = "social_post", **kwargs):
    """Função rápida para gerar copy"""
    agent = await create_copywriter_agent()
    result = await agent.generate_copy(prompt, copy_type, **kwargs)
    return result

# Exemplo de uso
if __name__ == "__main__":
    async def test():
        agent = await create_copywriter_agent()
        
        # Teste de geração de copy
        result = await agent.generate_copy(
            prompt="Crie um post sobre automação de marketing com IA para empresas B2B",
            copy_type="social_post",
            target_audience="Empresários B2B de tecnologia",
            max_tokens=1000
        )
        
        print("✅ Copy gerado:")
        print(result['copy'])
        print(f"\n📊 Análise: {result['analysis']}")
        
        # Salvar resultado
        saved_path = agent.save_copy(result)
        print(f"\n💾 Salvo em: {saved_path}")
    
    asyncio.run(test())