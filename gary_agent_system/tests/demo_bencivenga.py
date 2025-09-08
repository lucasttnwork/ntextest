#!/usr/bin/env python3
"""
Demo do Agente Gary Bencivenga - Simulação de Funcionamento
"""

def demo_bencivenga_agent():
    """Demonstra o funcionamento do agente Gary Bencivenga"""
    
    print("🎯 AGENTE GARY BENCIVENGA - DEMONSTRAÇÃO")
    print("="*60)
    print()
    
    print("Gary Bencivenga: Antes de escrever qualquer linha, me diga:")
    print("1) O que vendemos? Para quem? Em qual canal/formato?")
    print("2) Qual a promessa mais valiosa que podemos sustentar com provas?")
    print("3) Que mecanismo torna essa promessa crível e diferente?")
    print("4) Quais provas (números/casos/depoimentos) posso citar?")
    print("5) Quais objeções derrubam a compra no último minuto?")
    print("6) Qual é a oferta completa (preço, termos, bônus, garantia, prazo)?")
    print("7) Há restrições legais/compliance?")
    print("8) Qual tom desejado (sério, consultivo, empolgado, calmo)?")
    print("9) Quais concorrentes/peças você admira (para não copiar, e sim diferenciar)?")
    print("10) Qual KPI de sucesso desta peça?")
    print()
    
    # Simula uma sessão de descoberta
    print("📊 EXEMPLO DE SESSÃO DE DESCOBERTA:")
    print("-"*40)
    
    exemplo_produto = {
        "produto": "Curso online 'Copy Mestre Bencivenga'",
        "publico": "Copywriters e marketers que ganham +5k/mês e querem dobrar conversões",
        "promessa": "Aumentar taxa de conversão em 300% em 90 dias ou dinheiro de volta",
        "mecanismo": "Método Bencivenga 4.0 com IA e testes A/B validados",
        "provas": "1,847 alunos, 94% de satisfação, cases de +500% ROI",
        "objecoes": "Preço alto, tempo limitado, experiência anterior",
        "oferta": "R$ 2.997 ou 12x de R$ 299, bônus de 1h comigo, garantia 90 dias",
        "canal": "Landing page long-form",
        "tom": "Consultivo, didático, com autoridade"
    }
    
    for chave, valor in exemplo_produto.items():
        print(f"{chave.upper()}: {valor}")
    
    print()
    print("🏗️  ESTRUTURA DA PEÇA (Metodologia Bencivenga):")
    print("-"*50)
    
    estrutura = [
        "1) ABERTURA: História sobre copywriter que dobrou conversões",
        "2) ALIANÇA: 'Nós' vs. charlatões de marketing digital", 
        "3) BENEFÍCIOS: 300% mais conversões → 2x receita → liberdade financeira",
        "4) MECANISMO: Explicar como o método 4.0 funciona com neurociência",
        "5) PROVAS: Depoimentos, números, cases, garantia",
        "6) OFERTA: Ancorar valor real R$ 15k vs. preço R$ 2.997",
        "7) RISCO REVERSO: Garantia 300% ou devolvemos + R$ 1k pelo tempo",
        "8) CTA: Botão único com escassez real (vagas limitadas)",
        "9) PS: Urgência + bônus extra por tempo limitado"
    ]
    
    for item in estrutura:
        print(f"  {item}")
    
    print()
    print("🎯 BULLETS DE FASCINAÇÃO (Exemplos):")
    print("-"*40)
    
    bullets = [
        "• Como 1 bullet simples aumentou conversões em 47% (página 3)",
        "• O erro silencioso que 9 em 10 copywriters cometem (e como evitar)",
        "• Por que 'benefícios' não vendem mais - e o que vende em 2025",
        "• A técnica de 5 minutos que transforma objeções em vendas",
        "• Como escrever copy que vende até dormendo (automatizado)",
        "• O segredo dos 3 números que multiplicam qualquer oferta",
        "• Por que garantias longas vendem mais que garantias curtas",
        "• A palavra proibida que aumenta urgência sem parecer spam"
    ]
    
    for bullet in bullets:
        print(f"  {bullet}")
    
    print()
    print("📈 SCORECARD DE QUALIDADE (0-10):")
    print("-"*35)
    
    scorecard = {
        "Clareza da promessa": 9,
        "Especificidade/números": 10,
        "Força do mecanismo": 8,
        "Provas e legitimidade": 9,
        "Ordem de benefícios": 9,
        "Fluidez (frase puxa frase)": 8,
        "Originalidade dos ângulos": 7,
        "Risco reverso crível": 10,
        "CTA claro e inevitável": 9,
        "Alinhamento com o canal": 9
    }
    
    total = sum(scorecard.values())
    media = total / len(scorecard)
    
    for item, nota in scorecard.items():
        print(f"  {item}: {nota}")
    
    print(f"\n  MÉDIA GERAL: {media:.1f}/10")
    
    print()
    print("🚀 PRÓXIMOS PASSOS:")
    print("-"*20)
    print("1. Instale as dependências: pip install requests")
    print("2. Configure OPENROUTER_API_KEY no .env")
    print("3. Execute: python3 agents/copywriter_agent_bencivenga.py")
    print("4. Use o agente para criar copy de altíssimo desempenho!")
    
    print()
    print("💡 DICA MESTRE: Sempre comece com pesquisa. Quanto mais souber")
    print("   sobre seu público, produto e provas, melhor será a copy.")
    
    return True

if __name__ == "__main__":
    demo_bencivenga_agent()