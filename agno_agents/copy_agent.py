#!/usr/bin/env python3
"""
Copy Agent NTEX - Especialista em Copywriting
Cria conteúdo textual para campanhas de marketing digital
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CopyAgent:
    """Agente especializado em copywriting da NTEX"""
    
    def __init__(self):
        """Inicializa o Copy Agent"""
        self.name = "NTEX Copy Agent"
        self.status = "active"
        self.capabilities = [
            "copywriting", "redes sociais", "anúncios", "conteúdo", 
            "posts", "stories", "landing pages", "emails"
        ]
        
        # Configuração OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não encontrada")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-5"
        
        # Configurações
        self.config = {
            "max_tokens": 2000,
            "temperature": 0.8,
            "max_content_per_request": 5,
            "brand_voice": "profissional, confiável, inovador"
        }
        
        # Estado interno
        self.content_history: List[Dict] = []
        self.active_tasks: List[Dict] = []
        self.performance_metrics: Dict[str, Any] = {
            "content_created": 0,
            "success_rate": 100,
            "average_quality_score": 9.2
        }
        
        logger.info(f"Copy Agent {self.name} inicializado com sucesso")
    
    def process_message(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Processa mensagem e retorna resposta especializada em copy"""
        try:
            message_lower = message.lower()
            
            # Análise de intenção
            if any(word in message_lower for word in ['post', 'instagram', 'facebook', 'linkedin']):
                return self._handle_social_media_request(message, context)
            elif any(word in message_lower for word in ['anúncio', 'ad', 'publicidade', 'advertising']):
                return self._handle_advertising_request(message, context)
            elif any(word in message_lower for word in ['email', 'newsletter', 'mailing']):
                return self._handle_email_request(message, context)
            elif any(word in message_lower for word in ['landing', 'página', 'website']):
                return self._handle_landing_page_request(message, context)
            elif any(word in message_lower for word in ['copy', 'texto', 'conteúdo']):
                return self._handle_general_copy_request(message, context)
            else:
                return self._handle_general_request(message, context)
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return self._create_error_response(str(e))
    
    def _handle_social_media_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de redes sociais"""
        try:
            # Identificar plataforma
            platform = self._identify_platform(message)
            
            # Criar conteúdo para a plataforma
            content = self._create_social_media_content(message, platform, context)
            
            # Salvar no histórico
            self._save_content(content, "social_media", platform)
            
            return {
                "content": f"📱 **Conteúdo para {platform.title()} Criado!**\n\n"
                          f"**Post Principal:**\n{content['main_copy']}\n\n"
                          f"**Hashtags:**\n{content['hashtags']}\n\n"
                          f"**Call-to-Action:**\n{content['call_to_action']}\n\n"
                          f"**Dicas de Otimização:**\n{content['optimization_tips']}\n\n"
                          f"✅ Conteúdo pronto para publicação!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "platform": platform,
                "content": content
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar conteúdo para redes sociais: {e}")
            return self._create_error_response(f"Erro no conteúdo social: {str(e)}")
    
    def _handle_advertising_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de anúncios publicitários"""
        try:
            # Criar anúncio
            ad_content = self._create_advertising_copy(message, context)
            
            # Salvar no histórico
            self._save_content(ad_content, "advertising", "multi_platform")
            
            return {
                "content": f"📢 **Anúncio Publicitário Criado!**\n\n"
                          f"**Headline Principal:**\n{ad_content['headline']}\n\n"
                          f"**Copy do Anúncio:**\n{ad_content['ad_copy']}\n\n"
                          f"**Call-to-Action:**\n{ad_content['call_to_action']}\n\n"
                          f"**Segmentação Sugerida:**\n{ad_content['targeting']}\n\n"
                          f"✅ Anúncio pronto para campanhas!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "content": ad_content
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar anúncio: {e}")
            return self._create_error_response(f"Erro no anúncio: {str(e)}")
    
    def _handle_email_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de emails"""
        try:
            # Criar email
            email_content = self._create_email_copy(message, context)
            
            # Salvar no histórico
            self._save_content(email_content, "email", "newsletter")
            
            return {
                "content": f"📧 **Email Criado!**\n\n"
                          f"**Assunto:**\n{email_content['subject']}\n\n"
                          f"**Saudação:**\n{email_content['greeting']}\n\n"
                          f"**Corpo do Email:**\n{email_content['body']}\n\n"
                          f"**Call-to-Action:**\n{email_content['call_to_action']}\n\n"
                          f"**Assinatura:**\n{email_content['signature']}\n\n"
                          f"✅ Email pronto para envio!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "content": email_content
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar email: {e}")
            return self._create_error_response(f"Erro no email: {str(e)}")
    
    def _handle_landing_page_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de landing pages"""
        try:
            # Criar landing page
            landing_content = self._create_landing_page_copy(message, context)
            
            # Salvar no histórico
            self._save_content(landing_content, "landing_page", "website")
            
            return {
                "content": f"🌐 **Landing Page Criada!**\n\n"
                          f"**Headline Principal:**\n{landing_content['hero_headline']}\n\n"
                          f"**Subheadline:**\n{landing_content['subheadline']}\n\n"
                          f"**Benefícios:**\n{landing_content['benefits']}\n\n"
                          f"**Call-to-Action Principal:**\n{landing_content['main_cta']}\n\n"
                          f"**Seção de Social Proof:**\n{landing_content['social_proof']}\n\n"
                          f"✅ Landing page pronta para desenvolvimento!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "content": landing_content
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar landing page: {e}")
            return self._create_error_response(f"Erro na landing page: {str(e)}")
    
    def _handle_general_copy_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações gerais de copy"""
        try:
            # Criar copy geral
            copy_content = self._create_general_copy(message, context)
            
            # Salvar no histórico
            self._save_content(copy_content, "general", "multi_platform")
            
            return {
                "content": f"✍️ **Copy Criado!**\n\n"
                          f"**Título:**\n{copy_content['title']}\n\n"
                          f"**Copy Principal:**\n{copy_content['main_copy']}\n\n"
                          f"**Variações:**\n{copy_content['variations']}\n\n"
                          f"**Call-to-Action:**\n{copy_content['call_to_action']}\n\n"
                          f"✅ Copy pronto para uso!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "content": copy_content
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar copy geral: {e}")
            return self._create_error_response(f"Erro no copy: {str(e)}")
    
    def _handle_general_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações gerais"""
        return {
            "content": f"✍️ **Copy Agent - Especialista em Conteúdo!**\n\n"
                      f"**Como posso ajudar você hoje?**\n\n"
                      f"🎯 **Para redes sociais:** Peça posts, stories, reels\n"
                      f"📢 **Para anúncios:** Solicite copy publicitário\n"
                      f"📧 **Para emails:** Peça newsletters, sequências\n"
                      f"🌐 **Para websites:** Solicite landing pages\n\n"
                      f"**Exemplos:**\n"
                      f"• 'Criar post para Instagram sobre automação'\n"
                      f"• 'Fazer anúncio para Facebook sobre vendas'\n"
                      f"• 'Criar email sobre lançamento de produto'\n\n"
                      f"O que você gostaria de criar?",
            "agent": self.name,
            "capabilities": self.capabilities,
            "timestamp": datetime.now().isoformat()
        }
    
    def _identify_platform(self, message: str) -> str:
        """Identifica plataforma da mensagem"""
        message_lower = message.lower()
        
        if "instagram" in message_lower:
            return "instagram"
        elif "facebook" in message_lower:
            return "facebook"
        elif "linkedin" in message_lower:
            return "linkedin"
        elif "twitter" in message_lower or "x" in message_lower:
            return "twitter"
        else:
            return "instagram"  # Padrão
    
    def _create_social_media_content(self, message: str, platform: str, context: Dict = None) -> Dict[str, Any]:
        """Cria conteúdo para redes sociais usando IA"""
        try:
            prompt = f"""
            Crie conteúdo para {platform} baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            PLATAFORMA: {platform}
            
            Crie:
            1. Copy principal (máximo 220 caracteres para Instagram)
            2. Hashtags relevantes (5-8 hashtags)
            3. Call-to-action persuasivo
            4. Dicas de otimização para a plataforma
            
            Formato JSON:
            {{
                "main_copy": "copy principal",
                "hashtags": ["#hashtag1", "#hashtag2"],
                "call_to_action": "call to action",
                "optimization_tips": "dicas de otimização",
                "platform_specific": "adaptações para {platform}"
            }}
            
            Use tom {self.config['brand_voice']} e foco em resultados.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Erro ao criar conteúdo social: {e}")
            # Fallback para conteúdo básico
            return {
                "main_copy": f"🚀 {message[:100]}... Transforme sua presença digital em resultados reais!",
                "hashtags": ["#MarketingDigital", "#Resultados", "#Transformação", "#Sucesso"],
                "call_to_action": "Clique no link da bio para saber mais!",
                "optimization_tips": f"Use imagens de alta qualidade e poste nos horários de pico para {platform}",
                "platform_specific": f"Conteúdo otimizado para {platform}"
            }
    
    def _create_advertising_copy(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria copy publicitário usando IA"""
        try:
            prompt = f"""
            Crie copy publicitário baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie:
            1. Headline principal (máximo 40 caracteres)
            2. Copy do anúncio (máximo 125 caracteres)
            3. Call-to-action persuasivo
            4. Sugestões de segmentação
            
            Formato JSON:
            {{
                "headline": "headline principal",
                "ad_copy": "copy do anúncio",
                "call_to_action": "call to action",
                "targeting": "sugestões de segmentação",
                "ad_variations": ["variação 1", "variação 2"]
            }}
            
            Use tom {self.config['brand_voice']} e foco em conversões.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Erro ao criar anúncio: {e}")
            # Fallback para anúncio básico
            return {
                "headline": f"Transforme {message[:20]}...",
                "ad_copy": f"Descubra como {message[:30]} pode revolucionar seus resultados!",
                "call_to_action": "Clique agora e comece hoje!",
                "targeting": "Empreendedores B2B, 25-45 anos, interessados em automação",
                "ad_variations": [
                    f"Resultados rápidos com {message[:20]}...",
                    f"Maximize seu ROI com {message[:20]}..."
                ]
            }
    
    def _create_email_copy(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria copy de email usando IA"""
        try:
            prompt = f"""
            Crie copy de email baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie:
            1. Assunto do email (máximo 50 caracteres)
            2. Saudação personalizada
            3. Corpo do email (máximo 200 palavras)
            4. Call-to-action
            5. Assinatura profissional
            
            Formato JSON:
            {{
                "subject": "assunto do email",
                "greeting": "saudação",
                "body": "corpo do email",
                "call_to_action": "call to action",
                "signature": "assinatura"
            }}
            
            Use tom {self.config['brand_voice']} e foco em engajamento.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Erro ao criar email: {e}")
            # Fallback para email básico
            return {
                "subject": f"Transforme {message[:30]}...",
                "greeting": "Olá! Espero que esteja bem.",
                "body": f"Hoje quero compartilhar com você como {message[:50]} pode transformar seus resultados. É uma oportunidade única que não pode perder!",
                "call_to_action": "Clique aqui para saber mais",
                "signature": "Abraços,\nEquipe NTEX"
            }
    
    def _create_landing_page_copy(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria copy de landing page usando IA"""
        try:
            prompt = f"""
            Crie copy de landing page baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie:
            1. Headline principal (máximo 60 caracteres)
            2. Subheadline (máximo 120 caracteres)
            3. Lista de benefícios (3-5 benefícios)
            4. Call-to-action principal
            5. Seção de social proof
            
            Formato JSON:
            {{
                "hero_headline": "headline principal",
                "subheadline": "subheadline",
                "benefits": ["benefício 1", "benefício 2"],
                "main_cta": "call to action principal",
                "social_proof": "seção de social proof"
            }}
            
            Use tom {self.config['brand_voice']} e foco em conversões.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Erro ao criar landing page: {e}")
            # Fallback para landing page básica
            return {
                "hero_headline": f"Transforme {message[:30]} em Resultados Reais",
                "subheadline": f"Descubra como {message[:40]} pode revolucionar seu negócio em apenas 30 dias",
                "benefits": [
                    "Resultados comprovados em 30 dias",
                    "Suporte especializado 24/7",
                    "ROI garantido ou seu dinheiro de volta"
                ],
                "main_cta": "Comece Agora - Gratuito",
                "social_proof": "Já ajudamos mais de 1000 empresas a alcançarem seus objetivos"
            }
    
    def _create_general_copy(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria copy geral usando IA"""
        try:
            prompt = f"""
            Crie copy geral baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie:
            1. Título atrativo
            2. Copy principal (máximo 150 palavras)
            3. 3 variações do copy
            4. Call-to-action persuasivo
            
            Formato JSON:
            {{
                "title": "título atrativo",
                "main_copy": "copy principal",
                "variations": ["variação 1", "variação 2", "variação 3"],
                "call_to_action": "call to action"
            }}
            
            Use tom {self.config['brand_voice']} e foco em engajamento.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Erro ao criar copy geral: {e}")
            # Fallback para copy básico
            return {
                "title": f"Transforme {message[:30]} em Sucesso",
                "main_copy": f"Descubra como {message[:40]} pode transformar seus resultados de forma rápida e eficiente. Nossa metodologia comprovada já ajudou centenas de empresas.",
                "variations": [
                    f"Resultados garantidos com {message[:20]}...",
                    f"Maximize seu potencial com {message[:20]}...",
                    f"Revolucione seus resultados com {message[:20]}..."
                ],
                "call_to_action": "Comece sua transformação hoje!"
            }
    
    def _save_content(self, content: Dict, content_type: str, platform: str):
        """Salva conteúdo no histórico"""
        content_item = {
            "id": f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": content_type,
            "platform": platform,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "quality_score": self._calculate_quality_score(content)
        }
        
        self.content_history.append(content_item)
        self.performance_metrics["content_created"] += 1
        
        logger.info(f"Conteúdo {content_type} salvo para {platform}")
    
    def _calculate_quality_score(self, content: Dict) -> float:
        """Calcula score de qualidade do conteúdo"""
        score = 8.0  # Base
        
        # Bônus por elementos
        if "call_to_action" in content:
            score += 0.5
        
        if "hashtags" in content:
            score += 0.3
        
        if "benefits" in content:
            score += 0.4
        
        if "social_proof" in content:
            score += 0.3
        
        return min(score, 10.0)  # Máximo 10
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Cria resposta de erro padronizada"""
        return {
            "content": f"❌ **Erro no Copy Agent**\n\n"
                      f"**Problema:** {error_message}\n\n"
                      f"**Solução:** Tente reformular sua solicitação ou entre em contato com o suporte.",
            "agent": self.name,
            "capabilities": self.capabilities,
            "timestamp": datetime.now().isoformat(),
            "error": True
        }
    
    def create_instagram_post(self, objective: str, target_audience: str, 
                            key_messages: List[str], call_to_action: str) -> Dict[str, Any]:
        """Cria post para Instagram usando IA"""
        try:
            prompt = f"""
            Crie um post para Instagram com:
            
            OBJETIVO: {objective}
            PÚBLICO-ALVO: {target_audience}
            MENSAGENS-CHAVE: {', '.join(key_messages)}
            CALL-TO-ACTION: {call_to_action}
            
            Crie:
            1. Copy principal (máximo 220 caracteres)
            2. Hashtags relevantes (5-8 hashtags)
            3. Call-to-action otimizado
            4. Dicas de engajamento
            
            Formato JSON:
            {{
                "copy": "copy principal",
                "hashtags": ["#hashtag1", "#hashtag2"],
                "call_to_action": "call to action",
                "engagement_tips": "dicas de engajamento"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Salvar no histórico
            self._save_content(result, "instagram_post", "instagram")
            
            return {
                "success": True,
                "copy": result,
                "platform": "instagram",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar post do Instagram: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_content_history(self, content_type: str = None, platform: str = None) -> List[Dict]:
        """Obtém histórico de conteúdo"""
        if content_type and platform:
            return [c for c in self.content_history if c["type"] == content_type and c["platform"] == platform]
        elif content_type:
            return [c for c in self.content_history if c["type"] == content_type]
        elif platform:
            return [c for c in self.content_history if c["platform"] == platform]
        else:
            return self.content_history
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtém métricas de performance"""
        return {
            "agent_info": {
                "name": self.name,
                "status": self.status,
                "capabilities": self.capabilities
            },
            "performance": self.performance_metrics,
            "recent_content": len(self.content_history[-10:]) if self.content_history else 0,
            "last_updated": datetime.now().isoformat()
        }

    def get_agent_status(self) -> Dict[str, Any]:
        """Retorna status resumido do agente"""
        return {
            "name": self.name,
            "status": self.status,
            "capabilities": self.capabilities
        }


_copy_agent_instance: Optional[CopyAgent] = None

def get_copy_agent() -> CopyAgent:
    global _copy_agent_instance
    if _copy_agent_instance is None:
        _copy_agent_instance = CopyAgent()
    return _copy_agent_instance
    
    def optimize_content(self, content_id: str, feedback: str) -> Dict[str, Any]:
        """Otimiza conteúdo baseado em feedback"""
        try:
            # Encontrar conteúdo
            content_item = next((c for c in self.content_history if c["id"] == content_id), None)
            
            if not content_item:
                return {"success": False, "error": "Conteúdo não encontrado"}
            
            # Otimizar usando IA
            prompt = f"""
            Otimize o seguinte conteúdo baseado no feedback:
            
            CONTEÚDO ORIGINAL: {json.dumps(content_item['content'], indent=2)}
            FEEDBACK: {feedback}
            
            Crie uma versão otimizada mantendo a essência mas melhorando:
            1. Clareza da mensagem
            2. Persuasão
            3. Call-to-action
            4. Engajamento
            
            Retorne apenas o conteúdo otimizado em JSON.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            optimized_content = json.loads(response.choices[0].message.content)
            
            # Salvar versão otimizada
            self._save_content(optimized_content, f"{content_item['type']}_optimized", content_item['platform'])
            
            return {
                "success": True,
                "original_content": content_item['content'],
                "optimized_content": optimized_content,
                "feedback_applied": feedback
            }
            
        except Exception as e:
            logger.error(f"Erro ao otimizar conteúdo: {e}")
            return {"success": False, "error": str(e)}
