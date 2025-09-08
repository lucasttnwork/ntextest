#!/bin/bash

# Script de setup do NTEX Copywriter Agent
# ========================================

echo "🚀 Iniciando setup do NTEX Copywriter Agent..."

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

# Verifica Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js 18+"
    exit 1
fi

# Define o diretório raiz do projeto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Cria diretório de saída
echo "📁 Criando diretórios de saída..."
mkdir -p "$PROJECT_ROOT/output/copywriter"

# Instala dependências Python
echo "📦 Instalando dependências Python..."
cd "$PROJECT_ROOT"

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "🐍 Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativa ambiente virtual
source venv/bin/activate

# Instala pacotes necessários
echo "📦 Instalando pacotes Python..."
pip install requests tavily-python python-dotenv aiohttp

# Verifica se .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando template..."
    cat > .env << EOF
# NTEX Copywriter Agent - Configurações

# OpenRouter API Configuration (obrigatório)
OPENROUTER_API_KEY=sua_openrouter_api_key_aqui
OPENROUTER_MODEL=x-ai/grok-code-fast-1
OPENROUTER_REFERER=https://ntex.com.br
OPENROUTER_TITLE=NTEX Copywriter Agent

# Tavily API (opcional - para busca na web)
TAVILY_API_KEY=sua_chave_tavily_aqui

# Configurações de Output
OUTPUT_DIR=$PROJECT_ROOT/output/copywriter
EOF
    echo "📝 Por favor, edite o arquivo .env e adicione suas chaves de API"
fi

# Instala dependências do frontend
echo "📦 Instalando dependências do frontend..."
cd "$PROJECT_ROOT/frontend"

if [ -f "package.json" ]; then
    npm install
    echo "✅ Frontend configurado com sucesso!"
else
    echo "⚠️  package.json não encontrado no frontend"
fi

# Torna scripts executáveis
echo "🔧 Tornando scripts executáveis..."
chmod +x "$PROJECT_ROOT/scripts/copywriter_cli.py"
chmod +x "$PROJECT_ROOT/agent_core/agents/copywriter_agent.py"

# Testa instalação
echo "🧪 Testando instalação..."
cd "$PROJECT_ROOT"

# Testa Python
python3 -c "import requests; print('✅ Requests OK')" 2>/dev/null || echo "⚠️  Requests não instalado"
python3 -c "import tavily; print('✅ Tavily OK')" 2>/dev/null || echo "⚠️  Tavily não instalado"

echo ""
echo "🎉 Setup concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo .env e adicione suas chaves de API"
echo "2. Teste o agente: python3 scripts/copywriter_cli.py --interactive"
echo "3. Inicie o frontend: cd frontend && npm run dev"
echo ""
echo "📖 Comandos úteis:"
echo "  • Modo interativo: python3 scripts/copywriter_cli.py --interactive"
echo "  • Gerar copy: python3 scripts/copywriter_cli.py --prompt 'Crie um post sobre...' --type social_post"
echo "  • Processar arquivo: python3 scripts/copywriter_cli.py --file prompts.txt"
echo ""
echo "🚀 Seu NTEX Copywriter Agent está pronto!"