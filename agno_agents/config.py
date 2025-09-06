"""
Configuração dos Agentes IA NTEX - Framework Agno
Configurações centralizadas para todos os agentes do sistema
"""

import os
from typing import Dict, List, Any

# Configurações de API Keys (serão carregadas de variáveis de ambiente)
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "meta": os.getenv("META_ACCESS_TOKEN"),
    "google_ads": os.getenv("GOOGLE_ADS_API_KEY"),
    "google_analytics": os.getenv("GOOGLE_ANALYTICS_KEY"),
    "supabase": {
        "url": os.getenv("SUPABASE_URL"),
        "key": os.getenv("SUPABASE_ANON_KEY")
    }
}

# Configurações dos modelos de IA
AI_MODELS = {
    "master": "gpt-5-mini",  # Agente mestre usa GPT-5-mini para coordenação complexa
    "copy": "gpt-5-mini",    # Copy usa GPT-5-mini para criatividade e qualidade
    "design": "gpt-5-mini",  # Design usa GPT-5-mini para criatividade visual
    "campaign": "gpt-5-mini",     # Campanhas usam GPT-5-mini para estratégia
    "analytics": "gpt-5-mini",    # Analytics usa GPT-5-mini para análise complexa
    "support": "gpt-5-mini"       # Suporte usa GPT-5-mini para respostas
}

# Configurações específicas para diferentes tipos de tarefas
TASK_MODEL_MAPPING = {
    # Tarefas complexas - sempre GPT-5-mini
    "complex_tasks": {
        "models": ["gpt-5-mini"],
        "use_cases": [
            "estratégia de campanha",
            "análise de dados complexa",
            "criação de copy criativa",
            "planejamento de conteúdo",
            "otimização de campanhas",
            "análise de performance",
            "tomada de decisão estratégica"
        ]
    },

    # Tarefas moderadas - GPT-5-mini
    "moderate_tasks": {
        "models": ["gpt-5-mini"],
        "use_cases": [
            "criação de posts",
            "gestão de campanhas",
            "análise de métricas",
            "criação de landing pages",
            "otimização de anúncios"
        ]
    },

    # Tarefas simples - GPT-5-mini
    "simple_tasks": {
        "models": ["gpt-5-mini"],
        "use_cases": [
            "respostas de suporte simples",
            "comentários de engajamento",
            "validações básicas",
            "logs e relatórios simples",
            "notificações automáticas"
        ]
    }
}

# Configurações de modelo por tipo de conteúdo
CONTENT_MODEL_MAPPING = {
    "instagram_post": "gpt-5-mini",
    "instagram_story": "gpt-5-mini",
    "instagram_reel": "gpt-5-mini",
    "ad_copy": "gpt-5-mini",
    "landing_page": "gpt-5-mini",
    "newsletter": "gpt-5-mini",
    "blog_post": "gpt-5-mini",
    "email_response": "gpt-5-mini",
    "comment_reply": "gpt-5-mini",
    "support_ticket": "gpt-5-mini"
}

# Configurações de modelo por tipo de campanha
CAMPAIGN_MODEL_MAPPING = {
    "strategy_planning": "gpt-5-mini",
    "audience_targeting": "gpt-5-mini",
    "creative_brief": "gpt-5-mini",
    "budget_optimization": "gpt-5-mini",
    "performance_analysis": "gpt-5-mini",
    "a_b_testing": "gpt-5-mini",
    "campaign_setup": "gpt-5-mini",
    "basic_reporting": "gpt-5-mini"
}

# Configurações de modelo por tipo de tarefa
TASK_MODEL_MAPPING = {
    # Tarefas complexas - sempre GPT-5-mini
    "complex_tasks": {
        "models": ["gpt-5-mini"],
        "use_cases": [
            "estratégia de campanha",
            "análise de dados complexa",
            "criação de copy criativa",
            "planejamento de conteúdo",
            "otimização de campanhas",
            "análise de performance",
            "tomada de decisão estratégica"
        ]
    },

    # Tarefas moderadas - GPT-5-mini
    "moderate_tasks": {
        "models": ["gpt-5-mini"],
        "use_cases": [
            "criação de posts",
            "gestão de campanhas",
            "análise de métricas",
            "criação de landing pages",
            "otimização de anúncios"
        ]
    },

    # Tarefas simples - GPT-5-mini
    "simple_tasks": {
        "models": ["gpt-5-mini"],
        "use_cases": [
            "respostas de suporte simples",
            "comentários de engajamento",
            "validações básicas",
            "logs e relatórios simples",
            "notificações automáticas"
        ]
    }
}

# Configurações da marca NTEX
BRAND_CONFIG = {
    "name": "NTEX",
    "tagline": "Construa uma Máquina de Crescimento que Impulsiona suas Vendas em 60 Dias",
    "tone_of_voice": "Direto, punchy, zero buzzwords, focado em resultados",
    "target_audience": "Empresas B2B de pequeno e médio porte buscando crescimento acelerado",
    "services": [
        "Marketing Digital Estratégico",
        "Desenvolvimento de Marca", 
        "Tráfego Pago",
        "Integração de Marketing",
        "Consultoria e Gestão de Projetos",
        "Inovação e Inteligência Artificial"
    ],
    "social_media": {
        "instagram": "@ntex.a",
        "website": "https://ntexassessoria.com.br/"
    }
}

# Configurações de conteúdo
CONTENT_CONFIG = {
    "instagram": {
        "frequency": "5 posts por semana",
        "content_types": ["posts", "stories", "reels"],
        "topics": [
            "Bastidores da NTEX",
            "Dicas de marketing",
            "Cases de sucesso",
            "Tendências do mercado",
            "Ofertas e promoções"
        ]
    },
    "google": {
        "seo_focus": ["marketing digital", "automação", "crescimento empresarial"],
        "ads_keywords": ["marketing digital", "consultoria marketing", "automação marketing"]
    }
}

# Configurações de campanhas
CAMPAIGN_CONFIG = {
    "default_budget": {
        "instagram": 100,  # R$ por dia
        "google_search": 150,  # R$ por dia
        "google_display": 80   # R$ por dia
    },
    "targeting": {
        "location": ["Brasil"],
        "age_range": [25, 55],
        "interests": ["marketing digital", "empreendedorismo", "negócios"],
        "job_titles": ["Diretor de Marketing", "CEO", "Empreendedor"]
    },
    "conversion_goals": {
        "primary": "lead_qualificado",
        "secondary": "visita_site",
        "tertiary": "engajamento"
    }
}

# Configurações de qualidade e validação
QUALITY_CONFIG = {
    "qa_checklist": [
        "Tom de voz da marca",
        "Clareza da mensagem",
        "Call-to-action claro",
        "Sem buzzwords desnecessários",
        "Foco em resultados",
        "Gramática e ortografia"
    ],
    "approval_required": [
        "Posts com ofertas",
        "Copy de anúncios",
        "Landing pages",
        "Comunicações oficiais"
    ],
    "auto_approval": [
        "Respostas de suporte simples",
        "Posts de bastidores",
        "Comentários de engajamento"
    ]
}

# Configurações de integração
INTEGRATION_CONFIG = {
    "zapier": {
        "webhook_url": os.getenv("ZAPIER_WEBHOOK_URL"),
        "triggers": ["new_lead", "campaign_update", "content_published"]
    },
    "supabase_tables": {
        "leads": "leads",
        "content": "content_queue", 
        "campaigns": "campaigns",
        "analytics": "analytics_data"
    }
}

# Configurações de monitoramento
MONITORING_CONFIG = {
    "metrics": [
        "response_time",
        "output_quality", 
        "approval_rate",
        "error_rate",
        "user_satisfaction"
    ],
    "alerts": {
        "high_error_rate": 0.1,  # 10%
        "low_approval_rate": 0.7,  # 70%
        "slow_response_time": 30   # 30 segundos
    }
}

# Função para validar configurações
def validate_config() -> Dict[str, Any]:
    """Valida se todas as configurações necessárias estão presentes"""
    missing_keys = []
    
    for key, value in API_KEYS.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if not sub_value:
                    missing_keys.append(f"{key}.{sub_key}")
        elif not value:
            missing_keys.append(key)
    
    if missing_keys:
        return {
            "valid": False,
            "missing_keys": missing_keys,
            "message": "Configurações de API ausentes"
        }
    
    return {
        "valid": True,
        "message": "Configuração válida"
    }

# Função para obter configuração específica
def get_config(section: str, key: str = None) -> Any:
    """Obtém configuração específica por seção e chave"""
    config_sections = {
        "api": API_KEYS,
        "models": AI_MODELS,
        "brand": BRAND_CONFIG,
        "content": CONTENT_CONFIG,
        "campaign": CAMPAIGN_CONFIG,
        "quality": QUALITY_CONFIG,
        "integration": INTEGRATION_CONFIG,
        "monitoring": MONITORING_CONFIG,
        "TASK_MODEL_MAPPING": TASK_MODEL_MAPPING,
        "CONTENT_MODEL_MAPPING": CONTENT_MODEL_MAPPING,
        "CAMPAIGN_MODEL_MAPPING": CAMPAIGN_MODEL_MAPPING
    }
    
    if section not in config_sections:
        raise ValueError(f"Seção '{section}' não encontrada")
    
    if key is None:
        return config_sections[section]
    
    if key not in config_sections[section]:
        raise ValueError(f"Chave '{key}' não encontrada na seção '{section}'")
    
    return config_sections[section][key]
