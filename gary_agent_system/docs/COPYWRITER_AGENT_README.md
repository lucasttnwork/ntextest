# 🤖 NTEX Copywriter Agent

> Um agente de IA especializado em criar copy de alta conversão seguindo as diretrizes NTEX de "vibe marketing"

## 🎯 O que é?

O NTEX Copywriter Agent é um sistema completo que combina:
- **Agente Python** com capacidade de gerar textos longos (até 32k tokens)
- **Interface Web Moderna** com AI SDK 5 e AI Elements
- **Busca na Internet** via Tavily para informações atualizadas
- **Tom NTEX** exclusivo: direto, punchy, zero buzzwords

## ✨ Características Principais

### 🧠 Inteligência Artificial Avançada
- **GPT-4 Turbo** para geração de copy de alta qualidade
- **Contexto de 32k tokens** para textos longos e detalhados
- **Análise de sentimento** e otimização automática
- **Aprendizado contínuo** com base nos resultados

### 🔍 Pesquisa em Tempo Real
- **Tavily API** para buscas na web
- **Informações atualizadas** sobre tendências e melhores práticas
- **Contexto relevante** para copy mais preciso
- **Fontes confiáveis** e verificadas

### 🎨 Interface Web Moderna
- **Next.js 14** com App Router
- **AI SDK 5** para streaming em tempo real
- **Tailwind CSS** para design responsivo
- **Componentes interativos** e intuitivos

### 📋 Tipos de Copy Suportados
- 📱 **Posts Sociais** - Instagram, LinkedIn, Twitter
- 📧 **Emails Marketing** - Newsletters, campanhas, nutrição
- 🎯 **Landing Pages** - Páginas de captura e vendas
- 🚀 **Anúncios** - Google Ads, Facebook Ads, LinkedIn Ads
- 📝 **Blog Posts** - Artigos longos e SEO-otimizados
- 💰 **Páginas de Vendas** - Copy persuasivo para conversão

## 🚀 Como Usar

### 1. Instalação Rápida
```bash
# Executa o script de setup completo
cd /Users/lucasttn/Documents/Documents/Cérebro NTEX
chmod +x scripts/setup_copywriter.sh
./scripts/setup_copywriter.sh
```

### 2. Configuração das APIs
```bash
# Edite o arquivo .env
nano .env

# Adicione suas chaves:
OPENAI_API_KEY=sua_chave_openai_aqui
TAVILY_API_KEY=sua_chave_tavily_aqui
```

### 3. Uso via Linha de Comando
```bash
# Modo interativo
python3 scripts/copywriter_cli.py --interactive

# Gerar copy específico
python3 scripts/copywriter_cli.py \
  --prompt "Crie um post sobre automação de marketing para empresários B2B" \
  --type social_post \
  --audience "Empresários de tecnologia" \
  --research

# Processar múltiplos prompts
python3 scripts/copywriter_cli.py --file prompts.txt
```

### 4. Interface Web
```bash
# Iniciar frontend
cd frontend/copywriter-app
npm run dev

# Acessar em http://localhost:3000
```

## 📖 Exemplos de Prompts

### Posts Sociais
```
Crie um post sobre como IA está transformando o marketing digital para pequenas empresas. 
Inclua 3 dicas práticas e um call-to-action para experimentar nossa ferramenta.
```

### Email Marketing
```
Crie um email para reengajar leads frios sobre nosso serviço de automação de marketing.
Use urgência escassa e inclua um caso de sucesso com números específicos.
```

### Landing Page
```
Crie copy para landing page de um curso sobre automação de marketing com IA.
Público: empresários de ecommerce. Preço: R$997. Garantia: 7 dias.
```

### Anúncio
```
Crie copy para Google Ads sobre agência de marketing automatizado.
Palavras-chave: marketing automation, IA, agência digital.
Orçamento: R$5k+/mês. Tom: profissional mas direto.
```

## 🎯 Tom NTEX - Diretrizes

### ✔️ O que FAZER:
- **Comece com o valor** - Benefício principal na primeira frase
- **Seja específico** - Use números, prazos e exemplos concretos
- **Use frases curtas** - Máximo 20 palavras por frase
- **Foque em resultados** - O que o cliente ganha, não o que você faz
- **CTA claro** - Uma única ação específica

### ❌ O que EVITAR:
- **Jargões corporativos** - "sinergia", "paradigma", "disrupção"
- **Metáforas vagas** - "navegar nas ondas do mercado"
- **Buzzwords** - "inovação", "transformação digital" (sem contexto)
- **Textos longos** - Parágrafos de mais de 3 linhas
- **CTAs múltiplos** - Foque em uma única ação

## 🔧 Arquitetura Técnica

### Backend (Python)
```
agents/
├── copywriter_agent.py          # Core do agente
├── __init__.py

scripts/
├── copywriter_cli.py            # Interface CLI
├── setup_copywriter.sh          # Script de setup
```

### Frontend (Next.js)
```
frontend/copywriter-app/
├── app/
│   ├── api/
│   │   ├── copywriter/          # API com AI SDK
│   │   └── python-copywriter/   # Integração com Python
│   ├── page.tsx                   # Interface principal
│   └── layout.tsx
├── package.json
└── tailwind.config.js
```

### Output
```
output/
└── copywriter/
    ├── copy_20241201_143022.json  # Arquivos salvos
    └── batch_results.json         # Resultados em lote
```

## 🎮 Comandos Avançados

### Batch Processing
```bash
# Crie um arquivo prompts.txt:
echo "social_post|Crie post sobre Black Friday para ecommerce" > prompts.txt
echo "email|Crie email de abandono de carrinho" >> prompts.txt
echo "ad_copy|Crie anúncio para serviço de consultoria" >> prompts.txt

# Processa todos
python3 scripts/copywriter_cli.py --file prompts.txt
```

### Integração com Workflow
```bash
# Combine com outros agentes NTEX
python3 agents/ntex_builder.py  # Usa o copy gerado
```

### Customização
```python
# No copywriter_agent.py, ajuste:
- SYSTEM_PROMPT  # Tom e diretrizes
- temperature    # Criatividade (0.1-1.0)
- max_tokens     # Tamanho do texto
- copy_types     # Novos tipos de copy
```

## 📊 Métricas e Análise

O agente fornece:
- **Análise de copy** - Pontos fortes, melhorias, score de conversão
- **Tokens utilizados** - Controle de custos OpenAI
- **Pesquisa aplicada** - Fontes usadas para contexto
- **Timestamp** - Histórico de gerações

## 🚨 Solução de Problemas

### Erro: "OPENAI_API_KEY não encontrada"
```bash
# Verifique o .env
cat .env
# Adicione sua chave
export OPENAI_API_KEY="sua_chave_aqui"
```

### Erro: "Module not found"
```bash
# Reinstale dependências
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "Tavily não funciona"
```bash
# Verifique sua chave ou desative pesquisa
# No código: include_research=False
```

## 🔄 Integrações

### Airtable
```python
# Adicione ao agente:
from pyairtable import Table
# Salva copy no Airtable automaticamente
```

### Zapier/Make
```python
# Webhook para automações:
import requests
requests.post('https://hooks.zapier.com/hooks/catch/...', json=data)
```

### Analytics
```python
# Tracking de performance:
# - Click rates
# - Conversion rates
# - A/B testing results
```

## 📈 Próximos Passos

1. **Fine-tuning** com copy de sucesso da NTEX
2. **Integração CRM** para personalização
3. **A/B testing automático** com resultados reais
4. **Multi-idioma** para mercado internacional
5. **Templates customizados** por indústria

## 🤝 Contribuindo

1. Teste o agente com diferentes prompts
2. Compartilhe resultados e melhorias
3. Adicione novos tipos de copy
4. Otimize o prompt do sistema
5. Documente casos de uso

---

**🚀 Pronto para criar copy que converte?**

Inicie o agente agora:
```bash
python3 scripts/copywriter_cli.py --interactive
```

**NTEX - Vibe Marketing com IA** 💜