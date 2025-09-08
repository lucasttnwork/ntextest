#!/usr/bin/env python3
"""
Teste dos Agentes IA NTEX
Verifica se os agentes reais podem ser inicializados e funcionam corretamente
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_config():
    """Testa se as configurações estão sendo carregadas"""
    print("🔧 Testando configurações...")
    
    required_vars = [
        'OPENAI_API_KEY',
        'SUPABASE_URL', 
        'SUPABASE_ANON_KEY'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:20]}...")
        else:
            print(f"❌ {var}: Não encontrada")
    
    print()

def test_master_agent():
    """Testa se o Master Agent pode ser inicializado"""
    print("🤖 Testando Master Agent...")
    
    try:
        from master_agent import NTEXMasterAgent
        agent = NTEXMasterAgent()
        print(f"✅ Master Agent inicializado: {agent.name}")
        print(f"   Status: {agent.status}")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar Master Agent: {e}")
        return False

def test_copy_agent():
    """Testa se o Copy Agent pode ser inicializado"""
    print("📝 Testando Copy Agent...")
    
    try:
        from copy_agent import CopyAgent
        agent = CopyAgent()
        print(f"✅ Copy Agent inicializado: {agent.name}")
        print(f"   Status: {agent.status}")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar Copy Agent: {e}")
        return False

def test_design_agent():
    """Testa se o Design Agent pode ser inicializado"""
    print("🎨 Testando Design Agent...")
    
    try:
        from design_agent import DesignAgent
        agent = DesignAgent()
        print(f"✅ Design Agent inicializado: {agent.name}")
        print(f"   Status: {agent.status}")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar Design Agent: {e}")
        return False

def test_openai_connection():
    """Testa se a conexão com OpenAI está funcionando"""
    print("🔌 Testando conexão OpenAI...")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': 'Teste simples'}],
            max_tokens=10
        )
        
        print(f"✅ OpenAI funcionando: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Erro OpenAI: {e}")
        return False

def test_supabase_connection():
    """Testa se a conexão com Supabase está funcionando"""
    print("🗄️ Testando conexão Supabase...")
    
    try:
        from supabase_client import get_supabase_client
        client = get_supabase_client()
        print("✅ Supabase conectado")
        return True
    except Exception as e:
        print(f"❌ Erro Supabase: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Testando Sistema de Agentes IA NTEX\n")
    
    # Testar configurações
    test_config()
    
    # Testar conexões
    openai_ok = test_openai_connection()
    supabase_ok = test_supabase_connection()
    
    print()
    
    # Testar agentes
    master_ok = test_master_agent()
    copy_ok = test_copy_agent()
    design_ok = test_design_agent()
    
    print()
    
    # Resumo
    print("📊 RESUMO DOS TESTES:")
    print(f"   OpenAI: {'✅' if openai_ok else '❌'}")
    print(f"   Supabase: {'✅' if supabase_ok else '❌'}")
    print(f"   Master Agent: {'✅' if master_ok else '❌'}")
    print(f"   Copy Agent: {'✅' if copy_ok else '❌'}")
    print(f"   Design Agent: {'✅' if design_ok else '❌'}")
    
    if all([openai_ok, supabase_ok, master_ok, copy_ok, design_ok]):
        print("\n🎉 Todos os testes passaram! Sistema funcionando perfeitamente.")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main()
