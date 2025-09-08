#!/usr/bin/env python3
"""
Script para iniciar apenas o frontend Next.js do sistema Gary Bencivenga
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    print("""
🎨 NTEX - Frontend Gary Bencivenga
==================================
Interface de chat com o agente Gary Bencivenga
    """)

def check_requirements():
    """Verifica se Node.js está instalado"""
    print("📋 Verificando requisitos...")

    try:
        result = subprocess.run(["node", "--version"], capture_output=True, check=True, text=True)
        print(f"✅ Node.js instalado: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js não encontrado. Instale o Node.js 18+ primeiro.")
        return False

    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, check=True, text=True)
        print(f"✅ NPM instalado: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ NPM não encontrado.")
        return False

    return True

def start_frontend():
    """Inicia o frontend Next.js"""
    print("\n🎨 Iniciando frontend Next.js...")

    frontend_dir = Path(__file__).parent.parent / "frontend"

    if not frontend_dir.exists():
        print(f"❌ Diretório frontend não encontrado: {frontend_dir}")
        return False

    try:
        # Verificar se node_modules existe, se não, instalar dependências
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Instalando dependências Node.js...")
            subprocess.run(["npm", "install"], check=True, cwd=frontend_dir)

        # Iniciar frontend
        print("🌟 Iniciando servidor Next.js...")
        print("   🎨 Frontend: http://localhost:3000")
        print("   🔄 Desenvolvimento ativo com hot reload")

        subprocess.run([
            "npm", "run", "dev"
        ], cwd=frontend_dir)

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar frontend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend interrompido pelo usuário")
        return True

def main():
    """Função principal"""
    print_header()

    if not check_requirements():
        sys.exit(1)

    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")

    print("\n📝 Para parar o frontend: Ctrl+C")
    print("🎯 Backend deve estar rodando em: http://localhost:8000")

if __name__ == "__main__":
    main()
