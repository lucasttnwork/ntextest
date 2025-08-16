#!/usr/bin/env python3
"""
Design Agent NTEX - Especialista em Design Visual
Cria elementos visuais para campanhas de marketing digital
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

class DesignAgent:
    """Agente especializado em design visual da NTEX"""
    
    def __init__(self):
        """Inicializa o Design Agent"""
        self.name = "NTEX Design Agent"
        self.status = "active"
        self.capabilities = [
            "design visual", "templates", "branding", "criatividade",
            "posts", "stories", "banners", "landing pages", "logos"
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
            "temperature": 0.9,
            "max_designs_per_request": 3,
            "brand_guidelines": "moderno, limpo, profissional"
        }
        
        # Estado interno
        self.design_history: List[Dict] = []
        self.active_projects: List[Dict] = []
        self.performance_metrics: Dict[str, Any] = {
            "designs_created": 0,
            "success_rate": 100,
            "average_quality_score": 9.0
        }
        
        logger.info(f"Design Agent {self.name} inicializado com sucesso")
    
    def process_message(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Processa mensagem e retorna resposta especializada em design"""
        try:
            message_lower = message.lower()
            
            # Análise de intenção
            if any(word in message_lower for word in ['post', 'instagram', 'facebook', 'social']):
                return self._handle_social_media_design(message, context)
            elif any(word in message_lower for word in ['banner', 'anúncio', 'ad', 'publicidade']):
                return self._handle_advertising_design(message, context)
            elif any(word in message_lower for word in ['logo', 'branding', 'identidade']):
                return self._handle_branding_design(message, context)
            elif any(word in message_lower for word in ['landing', 'página', 'website']):
                return self._handle_web_design(message, context)
            elif any(word in message_lower for word in ['template', 'modelo', 'layout']):
                return self._handle_template_design(message, context)
            else:
                return self._handle_general_design_request(message, context)
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            return self._create_error_response(str(e))
    
    def _handle_social_media_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de design para redes sociais"""
        try:
            # Identificar plataforma
            platform = self._identify_platform(message)
            
            # Criar design para a plataforma
            design = self._create_social_media_design(message, platform, context)
            
            # Salvar no histórico
            self._save_design(design, "social_media", platform)
            
            return {
                "content": f"🎨 **Design para {platform.title()} Criado!**\n\n"
                          f"**Especificações:**\n{design['specifications']}\n\n"
                          f"**Paleta de Cores:**\n{design['color_palette']}\n\n"
                          f"**Elementos Visuais:**\n{design['visual_elements']}\n\n"
                          f"**Instruções de Criação:**\n{design['creation_instructions']}\n\n"
                          f"✅ Design pronto para desenvolvimento!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "platform": platform,
                "design": design
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar design para redes sociais: {e}")
            return self._create_error_response(f"Erro no design social: {str(e)}")
    
    def _handle_advertising_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de design publicitário"""
        try:
            # Criar design publicitário
            design = self._create_advertising_design(message, context)
            
            # Salvar no histórico
            self._save_design(design, "advertising", "multi_platform")
            
            return {
                "content": f"📢 **Design Publicitário Criado!**\n\n"
                          f"**Formato:**\n{design['format']}\n\n"
                          f"**Layout:**\n{design['layout']}\n\n"
                          f"**Elementos Visuais:**\n{design['visual_elements']}\n\n"
                          f"**Call-to-Action Visual:**\n{design['visual_cta']}\n\n"
                          f"✅ Design pronto para campanhas!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "design": design
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar design publicitário: {e}")
            return self._create_error_response(f"Erro no design publicitário: {str(e)}")
    
    def _handle_branding_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de design de branding"""
        try:
            # Criar design de branding
            design = self._create_branding_design(message, context)
            
            # Salvar no histórico
            self._save_design(design, "branding", "brand_identity")
            
            return {
                "content": f"🏷️ **Design de Branding Criado!**\n\n"
                          f"**Identidade Visual:**\n{design['visual_identity']}\n\n"
                          f"**Paleta de Cores:**\n{design['color_palette']}\n\n"
                          f"**Tipografia:**\n{design['typography']}\n\n"
                          f"**Elementos Gráficos:**\n{design['graphic_elements']}\n\n"
                          f"✅ Branding pronto para implementação!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "design": design
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar design de branding: {e}")
            return self._create_error_response(f"Erro no branding: {str(e)}")
    
    def _handle_web_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de design web"""
        try:
            # Criar design web
            design = self._create_web_design(message, context)
            
            # Salvar no histórico
            self._save_design(design, "web_design", "website")
            
            return {
                "content": f"🌐 **Design Web Criado!**\n\n"
                          f"**Layout da Página:**\n{design['page_layout']}\n\n"
                          f"**Seções Principais:**\n{design['main_sections']}\n\n"
                          f"**Elementos Visuais:**\n{design['visual_elements']}\n\n"
                          f"**Call-to-Action:**\n{design['cta_design']}\n\n"
                          f"✅ Design web pronto para desenvolvimento!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "design": design
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar design web: {e}")
            return self._create_error_response(f"Erro no design web: {str(e)}")
    
    def _handle_template_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações de templates"""
        try:
            # Criar template
            design = self._create_template_design(message, context)
            
            # Salvar no histórico
            self._save_design(design, "template", "multi_platform")
            
            return {
                "content": f"📋 **Template Criado!**\n\n"
                          f"**Tipo de Template:**\n{design['template_type']}\n\n"
                          f"**Estrutura:**\n{design['structure']}\n\n"
                          f"**Elementos Reutilizáveis:**\n{design['reusable_elements']}\n\n"
                          f"**Instruções de Uso:**\n{design['usage_instructions']}\n\n"
                          f"✅ Template pronto para uso!",
                "agent": self.name,
                "capabilities": self.capabilities,
                "timestamp": datetime.now().isoformat(),
                "design": design
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar template: {e}")
            return self._create_error_response(f"Erro no template: {str(e)}")
    
    def _handle_general_design_request(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Gerencia solicitações gerais de design"""
        return {
            "content": f"🎨 **Design Agent - Especialista Visual!**\n\n"
                      f"**Como posso ajudar você hoje?**\n\n"
                      f"📱 **Para redes sociais:** Peça posts, stories, reels\n"
                      f"📢 **Para anúncios:** Solicite banners, ads\n"
                      f"🏷️ **Para branding:** Peça logos, identidade visual\n"
                      f"🌐 **Para web:** Solicite landing pages, sites\n"
                      f"📋 **Para templates:** Peça modelos reutilizáveis\n\n"
                      f"**Exemplos:**\n"
                      f"• 'Criar post visual para Instagram sobre automação'\n"
                      f"• 'Fazer banner para Facebook sobre vendas'\n"
                      f"• 'Criar logo para empresa de tecnologia'\n\n"
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
    
    def _create_social_media_design(self, message: str, platform: str, context: Dict = None) -> Dict[str, Any]:
        """Cria design para redes sociais usando IA"""
        try:
            prompt = f"""
            Crie design para {platform} baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            PLATAFORMA: {platform}
            
            Crie especificações de design incluindo:
            1. Dimensões e formato
            2. Paleta de cores
            3. Elementos visuais principais
            4. Instruções de criação
            5. Dicas de otimização para a plataforma
            
            Formato JSON:
            {{
                "specifications": "dimensões e formato",
                "color_palette": "paleta de cores",
                "visual_elements": "elementos visuais",
                "creation_instructions": "instruções de criação",
                "platform_optimization": "otimizações para {platform}"
            }}
            
            Use estilo {self.config['brand_guidelines']} e foco em engajamento.
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
            logger.error(f"Erro ao criar design social: {e}")
            # Fallback para design básico
            return {
                "specifications": f"1080x1080px para {platform}",
                "color_palette": "Azul corporativo (#0066CC), Branco (#FFFFFF), Cinza (#666666)",
                "visual_elements": "Ícone de automação, gradiente azul, texto em branco",
                "creation_instructions": "Criar layout limpo com foco na mensagem principal",
                "platform_optimization": f"Otimizar para feed do {platform}, usar cores contrastantes"
            }
    
    def _create_advertising_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria design publicitário usando IA"""
        try:
            prompt = f"""
            Crie design publicitário baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie especificações de design incluindo:
            1. Formato e dimensões
            2. Layout da composição
            3. Elementos visuais principais
            4. Call-to-action visual
            5. Dicas de conversão
            
            Formato JSON:
            {{
                "format": "formato e dimensões",
                "layout": "layout da composição",
                "visual_elements": "elementos visuais",
                "visual_cta": "call-to-action visual",
                "conversion_tips": "dicas de conversão"
            }}
            
            Use estilo {self.config['brand_guidelines']} e foco em conversões.
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
            logger.error(f"Erro ao criar design publicitário: {e}")
            # Fallback para design básico
            return {
                "format": "1200x628px para Facebook, 1080x1080px para Instagram",
                "layout": "Layout em grid com imagem principal e texto sobreposto",
                "visual_elements": "Imagem de fundo, overlay com texto, botão CTA",
                "visual_cta": "Botão azul com texto branco 'Saiba Mais'",
                "conversion_tips": "Usar cores contrastantes, texto legível, CTA destacado"
            }
    
    def _create_branding_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria design de branding usando IA"""
        try:
            prompt = f"""
            Crie design de branding baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie especificações de design incluindo:
            1. Identidade visual geral
            2. Paleta de cores corporativa
            3. Tipografia recomendada
            4. Elementos gráficos principais
            5. Diretrizes de aplicação
            
            Formato JSON:
            {{
                "visual_identity": "identidade visual geral",
                "color_palette": "paleta de cores corporativa",
                "typography": "tipografia recomendada",
                "graphic_elements": "elementos gráficos principais",
                "application_guidelines": "diretrizes de aplicação"
            }}
            
            Use estilo {self.config['brand_guidelines']} e foco em consistência.
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
            logger.error(f"Erro ao criar design de branding: {e}")
            # Fallback para design básico
            return {
                "visual_identity": "Identidade moderna e profissional com foco em tecnologia",
                "color_palette": "Azul corporativo (#0066CC), Verde (#00CC66), Branco (#FFFFFF)",
                "typography": "Fonte sans-serif moderna (Inter ou Roboto) para títulos, Arial para corpo",
                "graphic_elements": "Ícone minimalista, formas geométricas simples, gradientes sutis",
                "application_guidelines": "Manter consistência de cores, usar tipografia hierárquica, aplicar elementos com moderação"
            }
    
    def _create_web_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria design web usando IA"""
        try:
            prompt = f"""
            Crie design web baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie especificações de design incluindo:
            1. Layout da página
            2. Seções principais
            3. Elementos visuais
            4. Call-to-action visual
            5. Responsividade
            
            Formato JSON:
            {{
                "page_layout": "layout da página",
                "main_sections": "seções principais",
                "visual_elements": "elementos visuais",
                "cta_design": "call-to-action visual",
                "responsiveness": "dicas de responsividade"
            }}
            
            Use estilo {self.config['brand_guidelines']} e foco em conversão.
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
            logger.error(f"Erro ao criar design web: {e}")
            # Fallback para design básico
            return {
                "page_layout": "Layout em coluna única com header, hero section, benefícios, CTA e footer",
                "main_sections": "Header com logo, Hero com título e CTA, Seção de benefícios, Formulário de contato",
                "visual_elements": "Imagens de alta qualidade, ícones ilustrativos, botões destacados",
                "cta_design": "Botão principal azul com texto branco, posicionado estrategicamente",
                "responsiveness": "Design mobile-first, breakpoints em 768px e 1024px, elementos flexíveis"
            }
    
    def _create_template_design(self, message: str, context: Dict = None) -> Dict[str, Any]:
        """Cria template usando IA"""
        try:
            prompt = f"""
            Crie template baseado na seguinte solicitação:
            
            SOLICITAÇÃO: {message}
            
            Crie especificações de template incluindo:
            1. Tipo de template
            2. Estrutura base
            3. Elementos reutilizáveis
            4. Instruções de uso
            5. Variações possíveis
            
            Formato JSON:
            {{
                "template_type": "tipo de template",
                "structure": "estrutura base",
                "reusable_elements": "elementos reutilizáveis",
                "usage_instructions": "instruções de uso",
                "variations": "variações possíveis"
            }}
            
            Use estilo {self.config['brand_guidelines']} e foco em reutilização.
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
            logger.error(f"Erro ao criar template: {e}")
            # Fallback para template básico
            return {
                "template_type": "Template de post para redes sociais",
                "structure": "Header com logo, área de conteúdo principal, footer com CTA",
                "reusable_elements": "Logo, paleta de cores, tipografia, botões CTA, ícones",
                "usage_instructions": "Substituir conteúdo, manter proporções, usar cores da marca",
                "variations": "Post quadrado, story vertical, banner horizontal"
            }
    
    def _save_design(self, design: Dict, design_type: str, platform: str):
        """Salva design no histórico"""
        design_item = {
            "id": f"design_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": design_type,
            "platform": platform,
            "design": design,
            "created_at": datetime.now().isoformat(),
            "quality_score": self._calculate_quality_score(design)
        }
        
        self.design_history.append(design_item)
        self.performance_metrics["designs_created"] += 1
        
        logger.info(f"Design {design_type} salvo para {platform}")
    
    def _calculate_quality_score(self, design: Dict) -> float:
        """Calcula score de qualidade do design"""
        score = 8.0  # Base
        
        # Bônus por elementos
        if "color_palette" in design:
            score += 0.5
        
        if "visual_elements" in design:
            score += 0.5
        
        if "creation_instructions" in design:
            score += 0.3
        
        if "platform_optimization" in design:
            score += 0.2
        
        return min(score, 10.0)  # Máximo 10
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Cria resposta de erro padronizada"""
        return {
            "content": f"❌ **Erro no Design Agent**\n\n"
                      f"**Problema:** {error_message}\n\n"
                      f"**Solução:** Tente reformular sua solicitação ou entre em contato com o suporte.",
            "agent": self.name,
            "capabilities": self.capabilities,
            "timestamp": datetime.now().isoformat(),
            "error": True
        }
    
    def create_visual_design(self, design_type: str, platform: str, 
                           objective: str, target_audience: str,
                           key_elements: List[str]) -> Dict[str, Any]:
        """Cria design visual usando IA"""
        try:
            prompt = f"""
            Crie design visual com:
            
            TIPO: {design_type}
            PLATAFORMA: {platform}
            OBJETIVO: {objective}
            PÚBLICO-ALVO: {target_audience}
            ELEMENTOS-CHAVE: {', '.join(key_elements)}
            
            Crie especificações completas de design incluindo:
            1. Dimensões e formato
            2. Paleta de cores
            3. Layout e composição
            4. Elementos visuais
            5. Instruções de criação
            
            Formato JSON:
            {{
                "specifications": "dimensões e formato",
                "color_palette": "paleta de cores",
                "layout": "layout e composição",
                "visual_elements": "elementos visuais",
                "creation_instructions": "instruções de criação"
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
            self._save_design(result, design_type, platform)
            
            return {
                "success": True,
                "design": result,
                "type": design_type,
                "platform": platform,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar design visual: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_design_history(self, design_type: str = None, platform: str = None) -> List[Dict]:
        """Obtém histórico de designs"""
        if design_type and platform:
            return [d for d in self.design_history if d["type"] == design_type and d["platform"] == platform]
        elif design_type:
            return [d for d in self.design_history if d["type"] == design_type]
        elif platform:
            return [d for d in self.design_history if d["platform"] == platform]
        else:
            return self.design_history
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Obtém métricas de performance"""
        return {
            "agent_info": {
                "name": self.name,
                "status": self.status,
                "capabilities": self.capabilities
            },
            "performance": self.performance_metrics,
            "recent_designs": len(self.design_history[-10:]) if self.design_history else 0,
            "last_updated": datetime.now().isoformat()
        }
    
    def optimize_design(self, design_id: str, feedback: str) -> Dict[str, Any]:
        """Otimiza design baseado em feedback"""
        try:
            # Encontrar design
            design_item = next((d for d in self.design_history if d["id"] == design_id), None)
            
            if not design_item:
                return {"success": False, "error": "Design não encontrado"}
            
            # Otimizar usando IA
            prompt = f"""
            Otimize o seguinte design baseado no feedback:
            
            DESIGN ORIGINAL: {json.dumps(design_item['design'], indent=2)}
            FEEDBACK: {feedback}
            
            Crie uma versão otimizada mantendo a essência mas melhorando:
            1. Clareza visual
            2. Harmonia de cores
            3. Composição
            4. Aplicabilidade
            
            Retorne apenas o design otimizado em JSON.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            optimized_design = json.loads(response.choices[0].message.content)
            
            # Salvar versão otimizada
            self._save_design(optimized_design, f"{design_item['type']}_optimized", design_item['platform'])
            
            return {
                "success": True,
                "original_design": design_item['design'],
                "optimized_design": optimized_design,
                "feedback_applied": feedback
            }
            
        except Exception as e:
            logger.error(f"Erro ao otimizar design: {e}")
            return {"success": False, "error": str(e)}
