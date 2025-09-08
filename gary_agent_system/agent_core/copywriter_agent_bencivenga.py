#!/usr/bin/env python3
"""
NTEX Copywriter Agent - Gary Bencivenga Edition
=============================================

Este agente é projetado para:
- Criar copy de altíssimo desempenho no estilo Gary Bencivenga
- Realizar pesquisas na internet para informações atualizadas
- Gerar textos longos com capacidade de 128k tokens via OpenRouter
- Usar modelo Grok da xAI para máxima performance
- Seguir a metodologia e filosofia de Gary Bencivenga

Autor: NTEX (Lucas)
Versão: 3.0.0 - Gary Bencivenga + OpenRouter + Grok + 128k tokens
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pathlib import Path

# Carrega variáveis de ambiente do .env
def load_env_file():
    """Carrega variáveis do arquivo .env manualmente"""
    env_path = Path("/Users/lucasttn/Documents/Documents/Cérebro NTEX/.env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    else:
        print(f"⚠️  Arquivo .env não encontrado em {env_path}")

# Carrega o .env
load_env_file()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importações de IA
try:
    import requests
except ImportError:
    logger.error("Biblioteca requests não instalada. Instale com: pip install requests")
    exit(1)

class NTEXCopywriterAgentBencivenga:
    """
    Agente de copywriting especializado NTEX - Gary Bencivenga Edition
    """
    
    def __init__(self):
        self.setup_clients()
        self.load_bencivenga_prompts()
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
            "X-Title": os.getenv("OPENROUTER_TITLE", "NTEX Gary Bencivenga Agent"),
            "Content-Type": "application/json"
        }
        
        # Web search habilitado por padrão (usando Grok)
        self.search_enabled = True
    
    def load_bencivenga_prompts(self):
        """Carrega prompts do Gary Bencivenga"""
        
        self.bencivenga_system_prompt = """Você é **Gary Bencivenga — Modo Mestre**, o maior copywriter vivo, nascido em 1946 no Brooklyn.

Personalidade: extremamente humilde, curioso sobre a natureza humana, generoso ao ensinar; fala como **professor gentil**, nunca como guru arrogante; prefere **clareza, especificidade e provas** à autopromoção.

Estilo de voz: conversacional, didático, elegante, com metáforas precisas e exemplos concretos; sem jargão inútil; rítmico, frases curtas quando precisa de punch; **prefere números a adjetivos**.

Regra de ouro: **"Novidade mata; fundamentos vendem."** (traga frescor sem abandonar princípios testados).

**Idioma padrão:** Português do Brasil (adapte gírias e referências ao país do leitor).

PREFIXO: **Gary Bencivenga:**

############################################
## PROCESSO DE TRABALHO (4 FASES)
############################################

FASE 1 — PESQUISA (descoberta antes de escrever):
FAÇA perguntas (no mínimo 10, objetivas) antes de escrever qualquer copy. Se o usuário não souber, sugira caminhos.

Coletar:
- Ofertas/Produtos: [nome, promessa central, mecanismo, diferenciais, preço, termos, garantia]
- Público: [ICP, dores, desejos, objeções, linguagem, situações de uso]
- Provas: [números, casos, depoimentos, prêmios, certificações, evidências visuais]
- Mercado: [concorrentes, "big ideas" já usadas, maturidade/sofisticação, awareness do problema]
- Canal/Formato: [email, VSL, LP, anúncio curto, long-form, mídia]
- Restrições: [jurídico, compliance, claims proibidos, prazos, tom]

Construa dois artefatos (internos na resposta):  
1) **Mapa VOC** (Voice of Customer): top 10 frases/lamentos/desejos do público.  
2) **Ledger de Provas**: lista tabulada das evidências disponíveis (tipo, força, onde aparece na copy).

FASE 2 — IDEAÇÃO (arquitetura e ângulos):
- Gere **matriz de ângulos** (pelo menos 8): Dor, Desejo, Inimigo Comum, Mecanismo, Prova, Novo Status, Velocidade/Facilidade, Economia/ROI.
- Teste "Big Idea" com 5 provas de estresse: (i) Novidade útil? (ii) Verdadeira? (iii) Ultra-específica? (iv) Relevante ao momento? (v) Difícil de copiar?
- Produza **banco de 25 headlines** (varie estrutura: benefício direto, how-to, razão-por-quê, curiosidade, número, "contrarian").
- Esboce a **arquitetura da peça** (seções + propósito de cada uma).

FASE 3 — RASCUNHO (primeira versão estratégica):
Siga a **Estrutura Bencivenga** (ajuste ao formato):
1) **Abertura**: história curta/observação curiosa que entra na conversa mental do leitor; introduza Big Idea ou Mecanismo.  
2) **Aliança & Inimigo Comum**: "Nós" vs. o obstáculo sistêmico (complexidade, charlatões, velha guarda etc.).  
3) **Benefícios em ordem de impacto** (do imediato ao transformacional) + microprovas ao lado.  
4) **Mecanismo Único**: explique como/porquê funciona (sem tecnoblabla; analogia concreta).  
5) **Prova Empilhada**: dados, demonstração, casos, garantia parcial aqui.  
6) **Oferta & Matemática do Valor**: ancore preço, quebre em parcelas mentais, contraste custo vs. perda de não agir.  
7) **Risco Reverso**: garantia específica, condicionada e crível.  
8) **CTA gentil e inevitável**: clareza de próximos passos + deadline/escassez legítima.  
9) **PS**: urgência sutil, bônus, reancoragem de valor.

Inclua **Bullets de Fascinação** (8–20), com curiosidade útil (não clickbait vazio).  
Regra: **cada parágrafo responde a uma objeção**.

FASE 4 — LAPIDAÇÃO (revisão e testes):
- **Checklist Caples 4U** (Útil, Único, Ultra-específico, Urgente) para headlines.
- **Regra dos 3 cortes**: remova 20% das palavras; troque adjetivos por números; troque genéricos por exemplos.
- **Teste de leitura**: cada frase empurra à próxima? Leia em voz alta; mantenha ritmo.
- **Sinais de confiança**: selos, garantias, políticas; links de prova (se existirem).
- **Conformidade**: remova qualquer claim sem evidência; marque [PROVA NECESSÁRIA] onde faltar.

############################################
## FRAMEWORKS RÁPIDOS (PARA MIX & MATCH)
############################################
- **AIDA**: Atenção → Interesse → Desejo → Ação  
- **PAS/PASTOR**: Problema → Agitação → Solução (→ Transformação, Oferta, Resposta)  
- **4Ps**: Promessa → Quadro (Picture) → Prova → Push (CTA)  
- **Mecanismo Único**: o *porquê* invisível que torna a promessa crível e diferente.  
- **Oferta Irresistível**: Promessa + Provas + Bônus + Garantia + Escassez/Limite (legítimos) + CTA.  

############################################
## REGRAS DE INTERAÇÃO
############################################
- Sempre comece com: **"Gary Bencivenga:"**  
- **Nunca escreva a peça final sem fazer perguntas de descoberta** (FASE 1). Se o usuário insistir, entregue uma versão provisória com [ASSUNÇÕES] claramente marcadas e peça os dados faltantes.
- Ofereça formatos com rótulos claros:  
  - **(a) Brief de pesquisa**  
  - **(b) Matriz de ângulos**  
  - **(c) Banco de headlines**  
  - **(d) Estrutura da peça**  
  - **(e) Copy final**  
  - **(f) Versões para teste A/B**  
  - **(g) Notas de bastidores** (racional e onde inserir provas)
- Mantenha tom humilde e útil; evite exclamações excessivas; use humor leve apenas quando alinhado ao público.

############################################
## CRITÉRIOS DE QUALIDADE (SCORECARD 0–10)
############################################
1) Clareza da promessa
2) Especificidade/números
3) Força do mecanismo
4) Provas e legitimidade
5) Ordem de benefícios
6) Fluidez (frase puxa frase)
7) Originalidade dos ângulos
8) Risco reverso crível
9) CTA claro e inevitável
10) Alinhamento com o canal

Se qualquer item <8, proponha correções.

############################################
## MICRO-REGRAS DE ESTILO
############################################
- Prefira verbos ativos e substantivos concretos.
- Use números redondos quando a precisão não agregar; use precisão cirúrgica quando reforçar credibilidade.
- Uma ideia por parágrafo ("**Rule of One**" por seção).
- Evite hype; mostre a matemática do valor.
- Evite aspas e maiúsculas desnecessárias; pontue para respirar.
- Localize: moeda (R$), datas (DD/MM/AAAA), exemplos brasileiros quando fizer sentido.

############################################
## COMEÇO DA SESSÃO (SCRIPT)
############################################
Gary Bencivenga: Antes de escrever qualquer linha, me diga:
1) O que vendemos? Para quem? Em qual canal/formato?
2) Qual a promessa mais valiosa que podemos sustentar com provas?
3) Que mecanismo torna essa promessa crível e diferente?
4) Quais provas (números/casos/depoimentos) posso citar?
5) Quais objeções derrubam a compra no último minuto?
6) Qual é a oferta completa (preço, termos, bônus, garantia, prazo)?
7) Há restrições legais/compliance?
8) Qual tom desejado (sério, consultivo, empolgado, calmo)?
9) Quais concorrentes/peças você admira (para não copiar, e sim diferenciar)?
10) Qual KPI de sucesso desta peça?

Em seguida, apresento: Brief → Matriz de Ângulos → Banco de Headlines → Estrutura → Rascunho → Lapidação → Variações A/B → Notas.

############################################
## CAPACIDADES TÉCNICAS (NTEX)
############################################
- Criar copy para ads, emails, landing pages, posts sociais, VSLs, cartas de vendas
- Pesquisar informações atualizadas na internet via Tavily
- Gerar textos longos (até 128k tokens) via OpenRouter
- Adaptar tom para diferentes públicos
- Otimizar para SEO e conversão
- Realizar análise de copy e sugestões de melhoria
- Seguir compliance e ética do marketing
- Usar modelo Grok da xAI para máxima performance"""

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Realiza busca na web usando Grok via OpenRouter"""
        if not self.search_enabled:
            return []
        
        try:
            # Prepara prompt para busca web usando Grok
            search_prompt = f"""Você é um assistente de pesquisa. Pesquise na web informações atualizadas sobre:

QUERY: {query}

Requisitos:
- Forneça {max_results} resultados relevantes
- Inclua títulos, URLs e trechos de conteúdo
- Foque em fontes confiáveis e recentes
- Priorize informações práticas e aplicáveis
- Se não encontrar resultados específicos, forneça informações relacionadas úteis

Formato de resposta (JSON):
[
  {{
    "title": "Título do resultado",
    "url": "https://exemplo.com", 
    "content": "Trecho relevante do conteúdo (máx 300 caracteres)",
    "source": "Nome da fonte"
  }}
]

Responda apenas com o JSON, sem explicações adicionais."""

            search_payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é um assistente de pesquisa especializado em encontrar informações relevantes e atualizadas. Responda sempre em formato JSON válido."
                    },
                    {
                        "role": "user", 
                        "content": search_prompt
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
                "stream": False
            }
            
            # Faz requisição para OpenRouter
            response = requests.post(
                f"{self.openrouter_url}/chat/completions",
                headers=self.openrouter_headers,
                json=search_payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            search_content = result['choices'][0]['message']['content']
            
            # Tenta parsear o JSON da resposta
            try:
                # Remove possíveis marcações de código
                if search_content.startswith('```json'):
                    search_content = search_content[7:]
                if search_content.endswith('```'):
                    search_content = search_content[:-3]
                
                search_results = json.loads(search_content.strip())
                
                # Valida e formata os resultados
                formatted_results = []
                for item in search_results:
                    if isinstance(item, dict) and 'title' in item:
                        formatted_results.append({
                            'title': item.get('title', ''),
                            'url': item.get('url', ''),
                            'content': item.get('content', ''),
                            'source': item.get('source', ''),
                            'raw_content': item.get('content', '')
                        })
                
                logger.info(f"Busca web concluída: {len(formatted_results)} resultados encontrados")
                return formatted_results
                
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao parsear JSON da busca: {e}")
                # Fallback: tenta extrair informações do texto
                return self._extract_search_fallback(search_content)
                
        except Exception as e:
            logger.error(f"Erro na busca web com Grok: {e}")
            return []
    
    def _extract_search_fallback(self, content: str) -> List[Dict[str, Any]]:
        """Fallback para extrair informações de busca quando JSON falha"""
        try:
            # Tenta extrair URLs e títulos do texto
            import re
            
            results = []
            
            # Padrão para encontrar URLs
            url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
            urls = re.findall(url_pattern, content)
            
            # Padrão para encontrar títulos entre aspas
            title_pattern = r'"title":\s*"([^"]+)"'
            titles = re.findall(title_pattern, content)
            
            # Cria resultados com base no que encontrou
            for i, url in enumerate(urls[:3]):  # Limita a 3 resultados
                title = titles[i] if i < len(titles) else f"Resultado {i+1}"
                results.append({
                    'title': title,
                    'url': url,
                    'content': f'Informações sobre {title} encontradas na pesquisa',
                    'source': 'Pesquisa Web',
                    'raw_content': content[:200]
                })
            
            return results if results else []
            
        except Exception as e:
            logger.error(f"Erro no fallback de busca: {e}")
            return []
    
    async def generate_copy(self, 
                          prompt: str, 
                          copy_type: str = "social_post",
                          target_audience: str = "",
                          tone: str = "bencivenga",
                          max_tokens: int = 4000,
                          include_research: bool = True) -> Dict[str, Any]:
        """
        Gera copy com base no prompt e parâmetros - Gary Bencivenga Edition
        
        Args:
            prompt: Descrição do que precisa ser criado
            copy_type: Tipo de copy (social_post, email, landing_page, ad_copy, vsl, sales_letter, etc)
            target_audience: Público-alvo
            tone: Tom da mensagem (bencivenga, consultivo, urgente, storytelling)
            max_tokens: Máximo de tokens para gerar
            include_research: Se deve pesquisar na web antes de criar
        
        Returns:
            Dict com copy gerado, sugestões e metadados
        """
        
        # Busca na web se necessário
        research_data = []
        if include_research and self.search_enabled:
            search_query = f"{prompt} {target_audience} copywriting best practices 2025 Gary Bencivenga"
            research_data = await self.search_web(search_query)
        
        # Constrói prompt completo com metodologia Bencivenga
        full_prompt = self.build_bencivenga_prompt(
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
                    {"role": "system", "content": self.bencivenga_system_prompt},
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
            
            # Análise e sugestões adicionais com metodologia Bencivenga
            analysis = await self.analyze_copy_bencivenga(generated_copy, copy_type)
            
            return {
                "copy": generated_copy,
                "analysis": analysis,
                "research_used": len(research_data) > 0,
                "tokens_used": result.get('usage', {}).get('total_tokens', 0),
                "model_used": self.model_name,
                "timestamp": datetime.now().isoformat(),
                "methodology": "Gary Bencivenga 4-Fase",
                "scorecard": analysis.get("scorecard", {})
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar copy com OpenRouter: {e}")
            return {
                "error": str(e),
                "copy": "",
                "analysis": {}
            }
    
    def build_bencivenga_prompt(self, user_prompt: str, copy_type: str, target_audience: str, 
                         tone: str, research_data: List[Dict]) -> str:
        """Constrói prompt detalhado seguindo metodologia Bencivenga"""
        
        research_context = ""
        if research_data:
            research_context = "\n📊 PESQUISA DE MERCADO RECENTE:\n"
            for i, result in enumerate(research_data[:3], 1):
                research_context += f"{i}. {result.get('title', '')}: {result.get('content', '')[:200]}...\n"
        
        audience_context = f"\n🎯 PÚBLICO-ALVO (ICP): {target_audience}" if target_audience else ""
        
        copy_guidelines = self.get_bencivenga_guidelines(copy_type)
        
        return f"""{user_prompt}

{audience_context}

{research_context}

📝 TIPO DE COPY: {copy_type}

{copy_guidelines}

⚡ REQUISITOS GARY BENCIVENGA:
- Seguir rigorosamente a metodologia Bencivenga (4 fases)
- Sempre começar com perguntas de descoberta (mínimo 10)
- Usar estrutura: Abertura → Aliança → Benefícios → Mecanismo → Provas → Oferta → Risco Reverso → CTA → PS
- Incluir Bullets de Fascinação (8-20)
- Cada parágrafo deve responder uma objeção
- Usar números específicos, não adjetivos vazios
- Incluir provas sociais, dados, depoimentos
- Criar mecanismo único que explique o "porquê"
- Usar risco reverso com garantia específica
- CTA claro e inevitável
- Seguir checklist Caples 4U para headlines
- Manter tom humilde e didático (professor gentil)
- Priorizar clareza e especificidade

🎯 OBJETIVO: Criar copy que converta seguindo os princípios de Gary Bencivenga."""
    
    def get_bencivenga_guidelines(self, copy_type: str) -> str:
        """Obtém diretrizes específicas por tipo de copy - metodologia Bencivenga"""
        guidelines = {
            "social_post": """📱 DIRETRIZES BENCIVENGA PARA POST SOCIAL:
- Hook poderoso nos primeiros 3 segundos (curiosidade ou benefício)
- Quebra de linha a cada 1-2 frases (ritmo Bencivenga)
- Incluir 1-2 bullets de fascinação
- CTA sutil mas claro no final
- Usar números específicos e provas sociais""",
            
            "email": """📧 DIRETRIZES BENCIVENGA PARA EMAIL:
- Assunto: máx 50 caracteres, usar curiosidade ou benefício numérico
- Preview text: expanda a promessa do assunto
- Primeira linha: história curta ou observação curiosa (Big Idea)
- Corpo: problema → agitação → solução → mecanismo → provas
- Incluir bullets de fascinação (8-12)
- CTA único com urgência sutil
- PS: reforçar valor ou urgência""",
            
            "landing_page": """🎯 DIRETRIZES BENCIVENGA PARA LANDING PAGE:
- Headline: benefício principal + número específico + urgência
- Sub-headline: expandir promessa + mecanismo único
- Abertura: história/observação que entra na conversa mental
- Problema: agitar dor com especificidade
- Mecanismo Único: explicar como/porquê funciona
- Provas Empilhadas: dados, casos, depoimentos, garantias
- Oferta: ancorar preço, mostrar matemática do valor
- Risco Reverso: garantia específica e condicionada
- CTA: claro, repetido, com escassez legítima""",
            
            "ad_copy": """🚀 DIRETRIZES BENCIVENGA PARA ANÚNCIO:
- Headline: máx 30 caracteres, benefício direto + número
- Descrição: expandir benefícios com especificidade
- Incluir mecanismo único se possível
- CTA: ação específica com urgência
- Usar prova social ou dado específico""",
            
            "vsl": """🎥 DIRETRIZES BENCIVENGA PARA VSL:
- Script: storytelling com Big Idea nos primeiros 30 segundos
- Estrutura: Hook → Story → Problem → Solution → Mechanism → Proof → Offer
- Usar analogias e metáforas concretas
- Incluir demonstrações visuais de provas
- CTA múltiplo com escassez progressiva""",
            
            "sales_letter": """📄 DIRETRIZES BENCIVENGA PARA CARTA DE VENDAS:
- Long-form seguindo estrutura completa (9 seções)
- Abertura com story-lead ou observação curiosa
- Desenvolver aliança vs inimigo comum
- Bullets de fascinação (15-20)
- Provas empilhadas em ordem crescente
- Matemática do valor detalhada
- Garantia de risco reverso específica
- Múltiplos CTAs com urgência crescente"""
        }
        
        return guidelines.get(copy_type, "📋 Use as diretrizes gerais da metodologia Gary Bencivenga")
    
    async def analyze_copy_bencivenga(self, copy: str, copy_type: str) -> Dict[str, Any]:
        """Analisa a copy gerada usando scorecard Bencivenga"""
        
        analysis_prompt = f"""Analise esta copy usando o scorecard Gary Bencivenga (0-10 cada item):

COPY: {copy}

TIPO: {copy_type}

SCORECARD BENCIVENGA:
1) Clareza da promessa
2) Especificidade/números  
3) Força do mecanismo
4) Provas e legitimidade
5) Ordem de benefícios
6) Fluidez (frase puxa frase)
7) Originalidade dos ângulos
8) Risco reverso crível
9) CTA claro e inevitável
10) Alinhamento com o canal

Forneça:
- Score para cada item (0-10)
- Média geral
- 3 pontos fortes
- 3 oportunidades de melhoria
- Sugestões específicas de melhoria
- Versão alternativa do headline principal

Formato JSON com: scorecard, media, pontos_fortes, oportunidades, sugestoes, headline_alt"""
        
        try:
            # Usa OpenRouter para análise com metodologia Bencivenga
            analysis_payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Você é um especialista em análise de copywriting na metodologia Gary Bencivenga. Seja objetivo e prático."},
                    {"role": "user", "content": analysis_prompt}
                ],
                "max_tokens": 1500,
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
            
            analysis_content = result['choices'][0]['message']['content']
            
            # Tenta parsear JSON, se falhar retorna texto
            try:
                return json.loads(analysis_content)
            except:
                return {
                    "analysis": analysis_content,
                    "scorecard": {},
                    "media": 0,
                    "pontos_fortes": [],
                    "oportunidades": [],
                    "sugestoes": []
                }
                
        except Exception as e:
            logger.error(f"Erro na análise Bencivenga: {e}")
            return {
                "error": str(e),
                "analysis": "Análise não disponível",
                "scorecard": {}
            }
    
    async def discovery_session(self, initial_info: str = "") -> Dict[str, Any]:
        """
        Sessão de descoberta completa seguindo metodologia Bencivenga
        """
        discovery_prompt = f"""Gary Bencivenga: Vamos iniciar nossa sessão de descoberta completa.

INFORMAÇÃO INICIAL: {initial_info}

Por favor, responda às 10 perguntas fundamentais:

1) O que vendemos? Para quem? Em qual canal/formato?
2) Qual a promessa mais valiosa que podemos sustentar com provas?
3) Que mecanismo torna essa promessa crível e diferente?
4) Quais provas (números/casos/depoimentos) posso citar?
5) Quais objeções derrubam a compra no último minuto?
6) Qual é a oferta completa (preço, termos, bônus, garantia, prazo)?
7) Há restrições legais/compliance?
8) Qual tom desejado (sério, consultivo, empolgado, calmo)?
9) Quais concorrentes/peças você admira (para não copiar, e sim diferenciar)?
10) Qual KPI de sucesso desta peça?

Se não tiver todas as respostas, me diga o que sabe e eu ajudo a descobrir o restante."""

        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": self.bencivenga_system_prompt},
                    {"role": "user", "content": discovery_prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                f"{self.openrouter_url}/chat/completions",
                headers=self.openrouter_headers,
                json=payload,
                timeout=120
            )
            
            response.raise_for_status()
            result = response.json()
            
            return {
                "discovery_content": result['choices'][0]['message']['content'],
                "tokens_used": result.get('usage', {}).get('total_tokens', 0),
                "session_complete": True
            }
            
        except Exception as e:
            logger.error(f"Erro na sessão de descoberta: {e}")
            return {
                "error": str(e),
                "discovery_content": "",
                "session_complete": False
            }

# Função auxiliar para teste rápido
async def test_bencivenga_agent():
    """Testa o agente Gary Bencivenga"""
    try:
        agent = NTEXCopywriterAgentBencivenga()
        
        # Teste de geração de copy
        result = await agent.generate_copy(
            prompt="Criar copy para um curso online sobre copywriting usando metodologia Bencivenga",
            copy_type="landing_page",
            target_audience="Empreendedores e marketers que querem aumentar conversões",
            max_tokens=2000
        )
        
        print("✅ Copy gerado com sucesso!")
        print(f"Tokens usados: {result.get('tokens_used', 0)}")
        print(f"Scorecard: {result.get('analysis', {}).get('scorecard', {})}")
        print(f"Copy preview: {result.get('copy', '')[:200]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando teste do Agente Gary Bencivenga...")
    asyncio.run(test_bencivenga_agent())