#!/usr/bin/env python3
"""
Script para iniciar o sistema completo Gary Bencivenga
Inicia Docker (Postgres + PgAdmin) e depois o backend FastAPI
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def print_header():
    print("""
🚀 NTEX - Sistema Gary Bencivenga
==================================
Especialista em Copywriting usando metodologia Bencivenga
    """)

def check_requirements():
    """Verifica se os requisitos estão instalados"""
    print("📋 Verificando requisitos...")

    # Verificar Docker
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✅ Docker instalado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker não encontrado. Instale o Docker primeiro.")
        return False

    # Verificar Docker Compose
    try:
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        print("✅ Docker Compose instalado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["docker", "compose", "version"], capture_output=True, check=True)
            print("✅ Docker Compose V2 instalado")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Docker Compose não encontrado.")
            return False

    # Verificar Python
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, check=True, text=True)
        print(f"✅ Python instalado: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Python não encontrado.")
        return False

    return True

def start_docker_services():
    """Inicia os serviços Docker (Postgres + PgAdmin)"""
    print("\n🐳 Iniciando serviços Docker...")

    project_root = Path(__file__).parent.parent
    docker_compose_file = project_root / "docker-compose.yml"

    if not docker_compose_file.exists():
        print(f"❌ Arquivo docker-compose.yml não encontrado em {docker_compose_file}")
        print(f"   Procurado em: {docker_compose_file}")
        return False

    try:
        # Tentar docker-compose primeiro, depois docker compose
        try:
            subprocess.run([
                "docker-compose",
                "-f", str(docker_compose_file),
                "up", "-d"
            ], check=True, cwd=project_root)
        except FileNotFoundError:
            subprocess.run([
                "docker", "compose",
                "-f", str(docker_compose_file),
                "up", "-d"
            ], check=True, cwd=project_root)

        print("✅ Serviços Docker iniciados com sucesso!")
        print("   📊 Postgres: localhost:5432")
        print("   🗄️  PgAdmin: http://localhost:8080")
        print("   👤 PgAdmin user: admin@ntex.com")
        print("   🔑 PgAdmin pass: admin123")

        # Aguardar serviços ficarem prontos
        print("⏳ Aguardando serviços ficarem prontos...")
        time.sleep(10)

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar serviços Docker: {e}")
        return False

def start_backend():
    """Inicia o backend FastAPI"""
    print("\n🚀 Iniciando backend FastAPI...")

    backend_dir = Path(__file__).parent.parent / "backend"

    if not backend_dir.exists():
        print(f"❌ Diretório backend não encontrado: {backend_dir}")
        return False

    # Verificar se .env existe
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  Arquivo .env não encontrado. Procurando em config/...")
        # Primeiro tentar no diretório config
        config_env = Path(__file__).parent.parent / "config" / ".env"
        if config_env.exists():
            import shutil
            shutil.copy(config_env, backend_dir / ".env")
            print("✅ Arquivo .env copiado de config/. Configure suas chaves de API!")
        else:
            # Se não encontrar, tentar .env.example
            env_example = backend_dir / ".env.example"
            if env_example.exists():
                import shutil
                shutil.copy(env_example, env_file)
                print("✅ Arquivo .env criado. Configure suas chaves de API!")
            else:
                print("❌ Arquivo .env ou .env.example não encontrado")
                return False

    try:
        # Instalar dependências se necessário
        requirements_file = backend_dir / "requirements.txt"
        if requirements_file.exists():
            print("📦 Instalando dependências Python...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True, cwd=backend_dir)

        # Iniciar backend
        print("🌟 Iniciando servidor FastAPI...")
        print("   📡 Backend: http://localhost:8000")
        print("   📚 Documentação: http://localhost:8000/docs")
        print("   🔄 Health check: http://localhost:8000/health")

        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], cwd=backend_dir)

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend interrompido pelo usuário")
        return True

def start_frontend():
    """Inicia o frontend Next.js em background"""
    print("\n🎨 Iniciando frontend Next.js...")

    frontend_dir = Path(__file__).parent.parent / "frontend"

    if not frontend_dir.exists():
        print(f"❌ Diretório frontend não encontrado: {frontend_dir}")
        return False

    try:
        # Verificar se node_modules existe
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Instalando dependências Node.js...")
            subprocess.run(["npm", "install"], check=True, cwd=frontend_dir)

        print("🌟 Iniciando servidor Next.js em background...")
        print("   🎨 Frontend: http://localhost:3000")

        # Iniciar em background
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=frontend_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print("✅ Frontend iniciado em background")
        return process

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar frontend: {e}")
        return False

def main():
    """Função principal"""
    print_header()

    if not check_requirements():
        sys.exit(1)

    if not start_docker_services():
        sys.exit(1)

    # Perguntar se quer iniciar o frontend
    start_frontend_option = input("\n❓ Deseja iniciar o frontend Next.js também? (y/n): ").lower().strip()

    frontend_process = None
    if start_frontend_option in ['y', 'yes', 's', 'sim']:
        frontend_process = start_frontend()

    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")

    # Terminar processo do frontend se estiver rodando
    if frontend_process:
        print("\n🛑 Encerrando frontend...")
        frontend_process.terminate()
        frontend_process.wait()

    print("\n📝 Para parar os serviços Docker:")
    print("   docker-compose down")
    print("\n🎯 Sistema encerrado com sucesso!")

if __name__ == "__main__":
    main()
