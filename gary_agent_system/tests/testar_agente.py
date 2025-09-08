#!/usr/bin/env python3
"""
Teste Interativo do Agente Gary Bencivenga
=======================================
Script simples para testar o agente com exemplos práticos
"""

import asyncio
import sys
import os

# Adiciona o diretório ao path
sys.path.append('/Users/lucasttn/Documents/Documents/Cérebro NTEX')

async def testar_agente_bencivenga():
    """Testa o agente Gary Bencivenga com exemplos práticos"""
    
    print("🎯 AGENTE GARY BENCIVENGA - TESTE INTERATIVO")
    print("="*60)
    print()
    
    try:
        # Importa o agente
        from agents.copywriter_agent_bencivenga import NTEXCopywriterAgentBencivenga
        
        print("✅ Agente importado com sucesso!")
        print("🚀 Inicializando...")
        
        # Cria instância do agente
        agente = NTEXCopywriterAgentBencivenga()
        print("✅ Agente inicializado!")
        print()
        
        # Teste 1: Sessão de Descoberta
        print("📋 TESTE 1: SESSÃO DE DESCOBERTA")
        print("-"*40)
        print("Gary Bencivenga vai fazer perguntas sobre seu produto...")
        print()
        
        resultado_descoberta = await agente.discovery_session(
            initial_info="Quero vender um curso online sobre copywriting para empreendedores"
        )
        
        print("📝 Resultado da Descoberta:")
        print(resultado_descoberta['discovery_content'])
        print()
        
        # Teste 2: Geração de Copy
        print("📝 TESTE 2: GERAÇÃO DE COPY")
        print("-"*40)
        
        resultado_copy = await agente.generate_copy(
            prompt="Criar copy para landing page vendendo curso de copywriting para empreendedores",
            copy_type="landing_page",
            target_audience="Empreendedores que querem aumentar vendas com copy melhor",
            tone="bencivenga",
            max_tokens=2000
        )
        
        print("✅ Copy gerado!")
        print(f"📊 Tokens usados: {resultado_copy.get('tokens_used', 0)}")
        print(f"📈 Scorecard: {resultado_copy.get('analysis', {}).get('scorecard', {})}")
        print()
        print("📝 Copy gerado (primeiros 500 caracteres):")
        print(resultado_copy['copy'][:500] + "...")
        print()
        
        # Teste 3: Análise de Copy Existente
        print("🔍 TESTE 3: ANÁLISE DE COPY")
        print("-"*40)
        
        copy_exemplo = """
        Descubra o segredo dos copywriters profissionais!
        Nosso curso vai transformar sua forma de escrever.
        Garantia de 30 dias ou seu dinheiro de volta.
        """
        
        resultado_analise = await agente.analyze_copy_bencivenga(copy_exemplo, "landing_page")
        print("📊 Análise Bencivenga:")
        print(f"Média: {resultado_analise.get('media', 'N/A')}")
        print(f"Pontos Fortes: {resultado_analise.get('pontos_fortes', [])}")
        print(f"Oportunidades: {resultado_analise.get('oportunidades', [])}")
        print()
        
        print("🎉 TODOS OS TESTES COMPLETADOS!")
        print("✅ O agente Gary Bencivenga está funcionando perfeitamente!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        print("🔧 Verificações:")
        print("1. Você executou: pip install requests")
        print("2. Sua API key está configurada no .env?")
        print("3. Tem conexão com internet?")
        return False

# Menu interativo simples
async def menu_testes():
    """Menu com opções de teste"""
    
    print("🎯 MENU DE TESTES - GARY BENCIVENGA")
    print("="*50)
    print("1. Testar Sessão de Descoberta")
    print("2. Testar Geração de Copy")
    print("3. Testar Análise de Copy")
    print("4. Rodar Todos os Testes")
    print("5. Sair")
    print()
    
    escolha = input("Escolha uma opção (1-5): ").strip()
    
    if escolha == "1":
        await testar_descoberta()
    elif escolha == "2":
        await testar_geracao()
    elif escolha == "3":
        await testar_analise()
    elif escolha == "4":
        await testar_agente_bencivenga()
    elif escolha == "5":
        print("👋 Até logo!")
    else:
        print("❌ Opção inválida!")

async def testar_descoberta():
    """Teste rápido da sessão de descoberta"""
    try:
        from agents.copywriter_agent_bencivenga import NTEXCopywriterAgentBencivenga
        agente = NTEXCopywriterAgentBencivenga()
        
        print("📝 Gary Bencivenga quer saber sobre seu produto...")
        info = input("Fale brevemente sobre seu produto/serviço: ")
        
        resultado = await agente.discovery_session(info)
        print("\n📋 Questões de Descoberta:")
        print(resultado['discovery_content'])
        
    except Exception as e:
        print(f"❌ Erro: {e}")

async def testar_geracao():
    """Teste rápido de geração de copy"""
    try:
        from agents.copywriter_agent_bencivenga import NTEXCopywriterAgentBencivenga
        agente = NTEXCopywriterAgentBencivenga()
        
        print("📝 Vamos criar uma copy...")
        prompt = input("O que você quer promover? ")
        publico = input("Quem é seu público-alvo? ")
        
        resultado = await agente.generate_copy(
            prompt=prompt,
            copy_type="social_post",
            target_audience=publico,
            max_tokens=1000
        )
        
        print(f"\n✅ Copy criada! ({resultado.get('tokens_used', 0)} tokens)")
        print("\n📝 RESULTADO:")
        print(resultado['copy'])
        
    except Exception as e:
        print(f"❌ Erro: {e}")

async def testar_analise():
    """Teste rápido de análise"""
    try:
        from agents.copywriter_agent_bencivenga import NTEXCopywriterAgentBencivenga
        agente = NTEXCopywriterAgentBencivenga()
        
        print("🔍 Vamos analisar um texto...")
        texto = input("Cole aqui o texto para análise (ou Enter para exemplo): ")
        
        if not texto.strip():
            texto = "Ganhe dinheiro rápido com nosso método revolucionário!"
        
        resultado = await agente.analyze_copy_bencivenga(texto, "social_post")
        
        print(f"\n📊 SCORECARD BENCIVENGA:")
        if 'scorecard' in resultado:
            for item, score in resultado['scorecard'].items():
                print(f"  {item}: {score}/10")
        print(f"\n📈 Média: {resultado.get('media', 'N/A')}/10")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando testes do Agente Gary Bencivenga...")
    asyncio.run(menu_testes())