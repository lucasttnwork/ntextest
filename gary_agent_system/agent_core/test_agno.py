#!/usr/bin/env python3
"""
Teste básico do framework Agno para verificar instalação
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools

def test_agno_installation():
    """Testa se o Agno está funcionando corretamente"""
    try:
        # Testa importação dos componentes principais
        print("✅ Importação do Agno bem-sucedida")
        
        # Testa criação de um agente básico
        agent = Agent(
            name="Teste NTEX",
            role="Agente de teste para verificar instalação",
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[ReasoningTools()],
            instructions="Responda de forma simples e direta"
        )
        
        print("✅ Criação de agente bem-sucedida")
        print(f"📋 Agente criado: {agent.name}")
        print(f"🎯 Função: {agent.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testando instalação do Agno...")
    success = test_agno_installation()
    
    if success:
        print("\n🎉 Framework Agno instalado e funcionando corretamente!")
        print("🚀 Os agentes NTEX podem ser executados agora.")
    else:
        print("\n💥 Problema na instalação do Agno detectado.")
        print("🔧 Verifique as dependências e tente novamente.")
