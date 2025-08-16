"""
Exemplo de uso do Sistema de Agentes IA NTEX
Demonstra como usar os agentes para criar conteúdo e campanhas
"""

from datetime import datetime, timedelta
from master_agent import get_master_agent
from agno_config import get_agno_config

def exemplo_criacao_conteudo():
    """Exemplo de criação de conteúdo usando o agente mestre"""
    
    print("=== EXEMPLO: Criação de Conteúdo Instagram ===\n")
    
    # Obter instância do agente mestre
    master = get_master_agent()
    
    # Verificar status do sistema
    status = master.get_system_status()
    print(f"Status do sistema: {status['master_agent']['status']}")
    
    # Criar briefing para post do Instagram
    task_id = master.create_content_brief(
        content_type="post",
        platform="instagram",
        objective="Gerar engajamento e leads",
        target_audience="Empreendedores B2B buscando crescimento",
        key_messages=[
            "A NTEX transforma negócios em máquinas de crescimento",
            "Resultados em 60 dias com estratégias comprovadas",
            "Foco em ROI e automação inteligente"
        ],
        call_to_action="Agende sua consultoria gratuita",
        priority=2
    )
    
    print(f"Tarefa criada com ID: {task_id}")
    
    # Verificar tarefas pendentes
    pending_tasks = len([t for t in master.task_manager.tasks.values() if t.status == "pending"])
    print(f"Tarefas pendentes: {pending_tasks}")
    
    return task_id

def exemplo_criacao_campanha():
    """Exemplo de criação de campanha usando o agente mestre"""
    
    print("\n=== EXEMPLO: Criação de Campanha Google Ads ===\n")
    
    # Obter instância do agente mestre
    master = get_master_agent()
    
    # Definir público-alvo
    target_audience = {
        "location": ["Brasil"],
        "age_range": [25, 55],
        "interests": ["marketing digital", "empreendedorismo", "negócios"],
        "job_titles": ["Diretor de Marketing", "CEO", "Empreendedor"],
        "company_size": ["pequena", "média"]
    }
    
    # Criar briefing para campanha
    campaign_task_id = master.create_campaign_brief(
        campaign_name="NTEX - Marketing Digital Estratégico",
        platform="google_search",
        objective="conversion",
        budget=150.0,  # R$ por dia
        target_audience=target_audience,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        priority=1
    )
    
    print(f"Tarefa de campanha criada com ID: {campaign_task_id}")
    
    return campaign_task_id

def exemplo_aprovacao_conteudo():
    """Exemplo de aprovação de conteúdo"""
    
    print("\n=== EXEMPLO: Aprovação de Conteúdo ===\n")
    
    # Obter instância do agente mestre
    master = get_master_agent()
    
    # Simular criação de conteúdo (em um sistema real, isso viria dos agentes especializados)
    from utils import content_manager
    
    # Criar conteúdo de exemplo
    content_id = content_manager.create_content(
        content_type="instagram_post",
        platform="instagram",
        title="Como a NTEX Transforma Negócios",
        content="Descubra como transformamos empresas em máquinas de crescimento em 60 dias.",
        metadata={"hashtags": ["#marketing", "#crescimento", "#ntex"]},
        created_by="copy_agent"
    )
    
    print(f"Conteúdo criado com ID: {content_id}")
    
    # Verificar se precisa de aprovação
    if content_id in content_manager.approval_queue:
        print("Conteúdo enviado para aprovação")
        
        # Aprovar conteúdo
        success = master.approve_content(content_id, "master_agent")
        if success:
            print("Conteúdo aprovado com sucesso!")
        else:
            print("Falha ao aprovar conteúdo")
    
    return content_id

def exemplo_otimizacao_sistema():
    """Exemplo de otimização do sistema"""
    
    print("\n=== EXEMPLO: Otimização do Sistema ===\n")
    
    # Obter instância do agente mestre
    master = get_master_agent()
    
    # Executar otimização
    optimization_result = master.optimize_system()
    
    if optimization_result["success"]:
        print(f"Otimizações encontradas: {optimization_result['total_optimizations']}")
        
        for opt in optimization_result["optimizations"]:
            if "agent" in opt:
                print(f"- Agente {opt['agent']}: {opt['issue']}")
                print(f"  Recomendação: {opt['recommendation']}")
            else:
                print(f"- Sistema: {opt['issue']}")
                print(f"  Recomendação: {opt['recommendation']}")
    else:
        print(f"Erro na otimização: {optimization_result['error']}")
    
    return optimization_result

def exemplo_configuracao_agno():
    """Exemplo de uso da configuração Agno"""
    
    print("\n=== EXEMPLO: Configuração Agno ===\n")
    
    # Obter configuração Agno
    agno_config = get_agno_config()
    
    # Verificar configuração do agente de copy
    copy_config = agno_config.get_agno_agent_config("copy")
    print(f"Configuração do Agente Copy:")
    print(f"- Modelo: {copy_config['model']}")
    print(f"- Temperature: {copy_config['temperature']}")
    print(f"- Max Tokens: {copy_config['max_tokens']}")
    
    # Verificar modelo para tarefa específica
    model_for_post = agno_config.get_model_for_content("instagram_post")
    print(f"\nModelo para post do Instagram: {model_for_post}")
    
    # Verificar regras de otimização
    optimization_rules = agno_config.get_optimization_rules()
    print(f"\nRegras de otimização:")
    print(f"- Tarefas complexas: {optimization_rules['model_selection']['complex_tasks']}")
    print(f"- Tarefas simples: {optimization_rules['model_selection']['simple_tasks']}")

def main():
    """Função principal para executar todos os exemplos"""
    
    print("🚀 SISTEMA DE AGENTES IA NTEX - EXEMPLOS DE USO\n")
    print("=" * 60)
    
    try:
        # Exemplo 1: Criação de conteúdo
        content_task = exemplo_criacao_conteudo()
        
        # Exemplo 2: Criação de campanha
        campaign_task = exemplo_criacao_campanha()
        
        # Exemplo 3: Aprovação de conteúdo
        content_id = exemplo_aprovacao_conteudo()
        
        # Exemplo 4: Otimização do sistema
        optimization = exemplo_otimizacao_sistema()
        
        # Exemplo 5: Configuração Agno
        exemplo_configuracao_agno()
        
        print("\n" + "=" * 60)
        print("✅ Todos os exemplos executados com sucesso!")
        print(f"📝 Tarefa de conteúdo: {content_task}")
        print(f"📊 Tarefa de campanha: {campaign_task}")
        print(f"📄 Conteúdo criado: {content_id}")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")
        print("Verifique se todas as dependências estão configuradas corretamente.")

if __name__ == "__main__":
    main()
