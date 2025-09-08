#!/usr/bin/env python3
"""
NTEX Copywriter CLI - Interface de linha de comando para o agente copywriter
=======================================================================

Uso:
    python copywriter_cli.py --prompt "Crie copy sobre..." --type social_post
    python copywriter_cli.py --interactive
    python copywriter_cli.py --file prompts.txt

Autor: NTEX (Lucas)
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

# Adiciona o diretório pai ao path para importar o agente
sys.path.append(str(Path(__file__).parent.parent))

from agents.copywriter_agent import create_copywriter_agent, quick_copy

class CopywriterCLI:
    def __init__(self):
        self.agent = None
    
    async def initialize(self):
        """Inicializa o agente"""
        print("🚀 Inicializando NTEX Copywriter Agent...")
        self.agent = await create_copywriter_agent()
        print("✅ Agente pronto!")
    
    async def generate_from_args(self, prompt: str, copy_type: str, **kwargs):
        """Gera copy a partir de argumentos de linha de comando"""
        if not self.agent:
            await self.initialize()
        
        print(f"📝 Gerando copy do tipo: {copy_type}")
        print(f"🎯 Prompt: {prompt[:100]}...")
        
        result = await self.agent.generate_copy(
            prompt=prompt,
            copy_type=copy_type,
            **kwargs
        )
        
        if 'error' in result:
            print(f"❌ Erro: {result['error']}")
            return
        
        # Mostra resultados
        print("\n" + "="*60)
        print("🎯 COPY GERADO:")
        print("="*60)
        print(result['copy'])
        print("\n" + "="*60)
        
        # Análise
        if result.get('analysis'):
            print("📊 ANÁLISE:")
            analysis = result['analysis']
            if isinstance(analysis, dict):
                for key, value in analysis.items():
                    print(f"  {key}: {value}")
        
        # Salva arquivo
        saved_path = self.agent.save_copy(result)
        print(f"\n💾 Arquivo salvo em: {saved_path}")
        
        return result
    
    async def interactive_mode(self):
        """Modo interativo"""
        await self.initialize()
        
        print("\n🎮 MODO INTERATIVO - NTEX Copywriter")
        print("Dig 'sair' para encerrar, 'ajuda' para comandos")
        
        while True:
            try:
                user_input = input("\n📝 O que você quer criar? > ").strip()
                
                if user_input.lower() == 'sair':
                    break
                
                if user_input.lower() == 'ajuda':
                    self.show_help()
                    continue
                
                if not user_input:
                    continue
                
                # Pergunta tipo de copy
                print("\n📋 Tipos de copy disponíveis:")
                copy_types = ["social_post", "email", "landing_page", "ad_copy", "blog_post", "sales_page"]
                for i, ct in enumerate(copy_types, 1):
                    print(f"  {i}. {ct}")
                
                type_choice = input("Escolha o tipo (número ou nome): ").strip()
                
                if type_choice.isdigit():
                    copy_type = copy_types[int(type_choice) - 1]
                else:
                    copy_type = type_choice if type_choice in copy_types else "social_post"
                
                # Pergunta público-alvo
                target_audience = input("🎯 Público-alvo (opcional): ").strip()
                
                # Pergunta se quer pesquisa
                research_choice = input("🔍 Incluir pesquisa na web? (s/n): ").strip().lower()
                include_research = research_choice == 's'
                
                # Gera copy
                result = await self.agent.generate_copy(
                    prompt=user_input,
                    copy_type=copy_type,
                    target_audience=target_audience,
                    include_research=include_research
                )
                
                if 'error' not in result:
                    print("\n✅ Copy gerado com sucesso!")
                    print(f"📁 Salvo em: {self.agent.save_copy(result)}")
                
            except KeyboardInterrupt:
                print("\n👋 Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    def show_help(self):
        """Mostra ajuda"""
        print("""
🎮 COMANDOS DO MODO INTERATIVO:

Comandos básicos:
  sair     - Encerra o programa
  ajuda    - Mostra esta ajuda

Dicas para prompts:
  - Seja específico sobre o que quer
  - Mencione o produto/serviço
  - Indique o objetivo (vender, informar, engajar)
  - Exemplo: "Crie copy para vender curso de automação para empresários"

Tipos de copy:
  social_post   - Posts para redes sociais
  email         - Emails marketing
  landing_page  - Páginas de captura
  ad_copy       - Anúncios pagos
  blog_post     - Artigos de blog
  sales_page    - Páginas de vendas
        """)
    
    async def process_file(self, filename: str):
        """Processa múltiplos prompts de um arquivo"""
        await self.initialize()
        
        file_path = Path(filename)
        if not file_path.exists():
            print(f"❌ Arquivo não encontrado: {filename}")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prompts = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            print(f"📁 Processando {len(prompts)} prompts de {filename}")
            
            results = []
            for i, prompt_line in enumerate(prompts, 1):
                print(f"\n📝 Processando prompt {i}/{len(prompts)}")
                
                # Parse formato: "tipo|prompt" ou só prompt
                if '|' in prompt_line:
                    copy_type, prompt = prompt_line.split('|', 1)
                else:
                    copy_type, prompt = "social_post", prompt_line
                
                result = await self.agent.generate_copy(
                    prompt=prompt.strip(),
                    copy_type=copy_type.strip()
                )
                
                results.append({
                    "prompt": prompt,
                    "copy_type": copy_type,
                    "result": result
                })
                
                # Salva individualmente
                if 'error' not in result:
                    self.agent.save_copy(result, f"batch_{i}_{copy_type}.json")
            
            # Salva resumo
            summary_file = file_path.parent / f"{file_path.stem}_results.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Lote processado! Resultados salvos em: {summary_file}")
            
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")

async def main():
    parser = argparse.ArgumentParser(description="NTEX Copywriter Agent CLI")
    parser.add_argument("--prompt", "-p", help="Prompt para gerar copy")
    parser.add_argument("--type", "-t", default="social_post", 
                       choices=["social_post", "email", "landing_page", "ad_copy", "blog_post", "sales_page"],
                       help="Tipo de copy (default: social_post)")
    parser.add_argument("--audience", "-a", help="Público-alvo")
    parser.add_argument("--research", "-r", action="store_true", help="Incluir pesquisa na web")
    parser.add_argument("--tokens", default=4000, type=int, help="Máximo de tokens (default: 4000)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Modo interativo")
    parser.add_argument("--file", "-f", help="Processar prompts de arquivo")
    
    args = parser.parse_args()
    
    cli = CopywriterCLI()
    
    try:
        if args.interactive:
            await cli.interactive_mode()
        elif args.file:
            await cli.process_file(args.file)
        elif args.prompt:
            await cli.generate_from_args(
                prompt=args.prompt,
                copy_type=args.type,
                target_audience=args.audience,
                include_research=args.research,
                max_tokens=args.tokens
            )
        else:
            print("❌ Use --prompt, --interactive ou --file")
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n👋 Até logo!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())