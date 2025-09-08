#!/usr/bin/env python3
"""
Script de Inicialização do Sistema NTEX
Inicia todos os agentes e a interface de chat
"""

import os
import sys
import time
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("🔍 Verificando configurações do ambiente...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    required_vars = [
        "OPENAI_API_KEY",
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis de ambiente ausentes: {', '.join(missing_vars)}")
        print("💡 Verifique o arquivo .env ou credentials.txt")
        return False
    
    print("✅ Todas as variáveis de ambiente configuradas")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    try:
        import openai
        import flask
        import supabase
        print("✅ Dependências principais instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência ausente: {e}")
        print("💡 Execute: pip install -r requirements.txt")
        return False

def initialize_agents():
    """Inicializa todos os agentes"""
    print("🤖 Inicializando agentes...")
    
    try:
        from master_agent import get_master_agent
        from copy_agent import get_copy_agent
        from design_agent import get_design_agent
        
        # Inicializar agentes
        master = get_master_agent()
        copy_agent = get_copy_agent()
        design_agent = get_design_agent()
        
        # Verificar status
        master_status = master.get_system_status()
        copy_status = copy_agent.get_agent_status()
        design_status = design_agent.get_agent_status()
        
        print("✅ Agentes inicializados com sucesso:")
        print(f"   • Master Agent: {master_status['master_agent']['status']}")
        print(f"   • Copy Agent: {copy_status['status']}")
        print(f"   • Design Agent: {design_status['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar agentes: {e}")
        return False

def start_chat_interface():
    """Inicia a interface de chat"""
    print("🚀 Iniciando interface de chat...")
    
    try:
        from chat_interface import app
        
        print("✅ Interface de chat carregada")
        print("🌐 Acesse: http://localhost:5000")
        print("💡 Use /help para ver comandos disponíveis")
        print("🔄 Pressione Ctrl+C para parar")
        
        # Iniciar servidor
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 SISTEMA NTEX - INICIALIZAÇÃO")
    print("=" * 50)
    
    # Verificar ambiente
    if not check_environment():
        sys.exit(1)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Inicializar agentes
    if not initialize_agents():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Sistema NTEX inicializado com sucesso!")
    print("🤖 Agentes ativos e funcionando")
    print("💻 Interface web pronta para uso")
    print("=" * 50)
    
    # Aguardar um pouco antes de iniciar a interface
    time.sleep(2)
    
    # Iniciar interface de chat
    start_chat_interface()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema NTEX interrompido pelo usuário")
        print("👋 Até logo!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        logger.error(f"Erro fatal na inicialização: {e}")
        sys.exit(1)
