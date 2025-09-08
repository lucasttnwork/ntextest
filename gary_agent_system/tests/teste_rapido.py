#!/usr/bin/env python3
"""
Teste rápido do Agente Gary Bencivenga
"""

import asyncio
import sys
sys.path.append('/Users/lucasttn/Documents/Documents/Cérebro NTEX')

async def teste_agente():
    print('🚀 Inicializando agente Gary Bencivenga...')
    
    try:
        from agents.copywriter_agent_bencivenga import NTEXCopywriterAgentBencivenga
        agente = NTEXCopywriterAgentBencivenga()
        
        print('✅ Agente inicializado com sucesso!')
        print('📝 Testando geração de copy...')
        
        resultado = await agente.generate_copy(
            prompt='Criar copy persuasiva para vender curso de copywriting no LinkedIn',
            copy_type='social_post', 
            target_audience='Empreendedores e profissionais de marketing',
            max_tokens=800
        )
        
        print(f'✅ Copy gerada! Tokens usados: {resultado.get("tokens_used", 0)}')
        print('\n📝 COPY GERADA:')
        print(resultado['copy'])
        print('\n📊 SCORECARD:')
        analysis = resultado.get('analysis', {})
        print(f'Média: {analysis.get("media", "N/A")}')
        
        if analysis.get('pontos_fortes'):
            print('Pontos fortes:', analysis['pontos_fortes'])
        
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(teste_agente())