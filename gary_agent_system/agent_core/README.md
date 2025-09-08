# Sistema de Agentes IA NTEX - Framework Agno

## 🚀 Status: **INSTALADO E FUNCIONANDO**

O framework Agno foi instalado com sucesso e o sistema de agentes NTEX está operacional.

## 📋 Pré-requisitos

- Python 3.10+
- Framework Agno 1.7.11+
- APIs de IA (OpenAI, Anthropic)
- APIs de marketing (Meta, Google)

## 🛠️ Instalação

### 1. Framework Agno
```bash
# Instalar o framework principal
python3 -m pip install agno

# Verificar instalação
python3 -c "import agno; print('Agno instalado com sucesso!')"
```

### 2. Dependências
```bash
# Instalar dependências principais
python3 -m pip install openai anthropic python-dotenv pydantic requests aiohttp

# Verificar dependências
python3 -c "from agno.agent import Agent; print('Dependências OK!')"
```

### 3. Configuração
```bash
# Copiar arquivo de exemplo
cp env_config_example.txt .env

# Editar .env com suas chaves de API
nano .env
```

## 🧪 Testes

### Teste Básico
```bash
# Teste simples
python3 test_agno.py
```

### Demonstração Completa
```bash
# Carregar variáveis de ambiente
source env_test.txt

# Executar demonstração
python3 demo_sistema.py
```

## 🎯 Componentes do Sistema

### Agente Mestre
- **Arquivo**: `master_agent.py`
- **Função**: Coordenação central de todos os agentes
- **Status**: ✅ Funcionando

### Agentes Especializados
- **Copy Agent**: Criação de conteúdo
- **Design Agent**: Criação visual
- **Campaign Agent**: Gestão de campanhas
- **Analytics Agent**: Análise de dados
- **Support Agent**: Atendimento

### Ferramentas
- **TaskManager**: Gerenciamento de tarefas
- **ContentManager**: Gestão de conteúdo
- **PerformanceTracker**: Rastreamento de performance

## 🔧 Configurações

### Modelos de IA
- **GPT-5**: Tarefas complexas e criativas
- **GPT-4.1**: Tarefas simples e suporte

### Marca NTEX
- **Tom**: Direto, punchy, focado em resultados
- **Canais**: Instagram @ntex.a, Google
- **Objetivo**: Máquina de crescimento em 60 dias

## 📊 Monitoramento

### Métricas
- Response time
- Output quality
- Approval rate
- Error rate
- User satisfaction

### Alertas
- High error rate (>10%)
- Low approval rate (<70%)
- Slow response time (>30s)

## 🚀 Próximos Passos

1. **Implementar agentes especializados**
2. **Configurar APIs externas**
3. **Implementar automações**
4. **Criar interface de usuário**
5. **Deploy em produção**

## 📚 Documentação

- [Framework Agno](https://github.com/agno-agi/agno)
- [Documentação Agno](https://docs.agno.com)
- [Exemplos Agno](https://github.com/agno-agi/agno/tree/main/cookbook)

## 🆘 Suporte

Para problemas técnicos:
1. Verificar logs em `master_agent.py`
2. Executar `demo_sistema.py` para diagnóstico
3. Verificar configurações em `config.py`
4. Validar variáveis de ambiente

---

**Sistema NTEX Operacional** ✅  
**Framework Agno Funcionando** ✅  
**Pronto para Campanhas** 🚀
