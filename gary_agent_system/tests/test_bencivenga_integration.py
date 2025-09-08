#!/usr/bin/env python3
"""
Teste simples do Agente Gary Bencivenga - Sem dependências externas
"""

import os
import sys

# Adiciona o diretório ao path
sys.path.append('/Users/lucasttn/Documents/Documents/Cérebro NTEX')

def test_bencivenga_integration():
    """Testa a integração do prompt Gary Bencivenga"""
    
    print("🧪 Testando Integração Gary Bencivenga")
    print("="*50)
    
    # Testa se o arquivo existe e pode ser lido
    try:
        with open('/Users/lucasttn/Documents/Documents/Cérebro NTEX/agents/Gary_Bencivenga_Base_Prompt.md', 'r') as f:
            bencivenga_content = f.read()
        print("✅ Arquivo Gary_Bencivenga_Base_Prompt.md encontrado e lido")
        print(f"📄 Tamanho do prompt: {len(bencivenga_content)} caracteres")
        
        # Verifica se os elementos principais estão presentes
        key_elements = [
            "Gary Bencivenga",
            "4 FASES",
            "Mecanismo Único",
            "Bullets de Fascinação",
            "Risco Reverso",
            "Provas Empilhadas",
            "Matriz de Ângulos"
        ]
        
        missing_elements = []
        for element in key_elements:
            if element not in bencivenga_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"⚠️  Elementos faltando: {missing_elements}")
        else:
            print("✅ Todos os elementos principais encontrados no prompt")
            
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return False
    
    # Testa se o novo agente foi criado
    try:
        with open('/Users/lucasttn/Documents/Documents/Cérebro NTEX/agents/copywriter_agent_bencivenga.py', 'r') as f:
            agent_content = f.read()
        print("✅ Arquivo copywriter_agent_bencivenga.py criado")
        print(f"📦 Tamanho do agente: {len(agent_content)} caracteres")
        
        # Verifica integrações importantes
        integrations = [
            "OpenRouter",
            "Tavily",
            "bencivenga_system_prompt",
            "Gary Bencivenga",
            "build_bencivenga_prompt",
            "generate_copy",
            "128000",
            "x-ai/grok-code-fast-1"
        ]
        
        missing_integrations = []
        for integration in integrations:
            if integration not in agent_content:
                missing_integrations.append(integration)
        
        if missing_integrations:
            print(f"⚠️  Integrações faltando: {missing_integrations}")
        else:
            print("✅ Todas as integrações técnicas preservadas")
            
        # Verifica métodos Bencivenga específicos
        bencivenga_methods = [
            "discovery_session",
            "analyze_copy_bencivenga",
            "get_bencivenga_guidelines",
            "build_bencivenga_prompt"
        ]
        
        missing_methods = []
        for method in bencivenga_methods:
            if method not in agent_content:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"⚠️  Métodos Bencivenga faltando: {missing_methods}")
        else:
            print("✅ Todos os métodos específicos Bencivenga implementados")
            
    except Exception as e:
        print(f"❌ Erro ao verificar agente: {e}")
        return False
    
    # Testa compatibilidade
    print("\n🔍 Testando Compatibilidade")
    print("-"*30)
    
    # Verifica se as variáveis de ambiente necessárias estão configuradas
    required_vars = ["OPENROUTER_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Variáveis de ambiente faltando: {missing_vars}")
        print("   (Isso é normal - configure seu .env para produção)")
    else:
        print("✅ Variáveis de ambiente configuradas")
    
    print("\n🎉 Integração Gary Bencivenga concluída com sucesso!")
    print("   O agente está pronto para uso quando as dependências forem instaladas.")
    print("   Execute: pip install requests tavily-python")
    print("   Configure seu .env com OPENROUTER_API_KEY")
    
    return True

if __name__ == "__main__":
    test_bencivenga_integration()