# SOP 06: Governança e Prompt QA — O que fazemos aqui?

## O que fazemos aqui?
Implementar automações (atendimento, vendas, processos) com governança e qualidade.

## Até onde este processo vai (e o que ele não faz)?
**Inclui**: Chatbots, automação de vendas, processos internos, governança de IA
**Exclui**: Criação de campanhas, análise de resultados

## Quem faz o quê?
- **Responsável (R)**: Especialista em automação
- **Aprovador (A)**: Diretor de operações
- **Consultados (C)**: Equipe de atendimento, vendas, cliente
- **Informados (I)**: Gestão, equipe técnica

## O que precisamos para começar?
- **Triggers**: Necessidade de automação identificada
- **Dados necessários**: Processos mapeados, FAQs, scripts
- **Referências**: Políticas de atendimento, procedimentos internos

## Quais ferramentas usamos (e para que servem)?
- **Apps principais**: Chatbots, CRM, n8n, Zapier, ferramentas de IA
- **Chaves/API**: APIs de chatbots, CRM, automação
- **Integrações**: WhatsApp, Instagram, Facebook, sistemas internos
- **IA**: LLMs, processamento de linguagem natural

## Procedimento (checklist)

### 1. Preparação
- [ ] Mapear processos existentes
- [ ] Identificar oportunidades de automação
- [ ] Definir políticas de governança
  - [ ] Políticas de ética e transparência: mitigar vieses, evitar conteúdo inadequado/tendencioso, explicar limitações dos modelos
- [ ] Preparar scripts e FAQs

### 2. Execução
- [ ] **Automação de Atendimento**:
  - [ ] Implementar chatbot principal
  - [ ] Configurar integrações com canais
  - [ ] Treinar com FAQs e políticas
  - [ ] Configurar escalonamento automático
  - [ ] Implementar monitoramento de satisfação

- [ ] **Automação de Vendas**:
  - [ ] Configurar lead scoring
  - [ ] Implementar geração de propostas
  - [ ] Configurar previsões de vendas
  - [ ] Automatizar follow-ups
  - [ ] Treinar equipe de vendas

- [ ] **Automação de Processos Internos**:
  - [ ] Identificar processos repetitivos
  - [ ] Mapear fluxos detalhados
  - [ ] Implementar automação piloto
  - [ ] Validar e escalar
  - [ ] Estabelecer governança

### 3. Validação
- [ ] Testar funcionalidade dos sistemas
- [ ] Validar com usuários finais
- [ ] Aprovar com stakeholders
- [ ] Implementar feedback

### 4. Entrega
- [ ] Treinar equipe no uso
- [ ] Documentar funcionalidades
- [ ] Configurar monitoramento
- [ ] Estabelecer manutenção

## O que entregamos ao final?
- **Artefatos gerados**: Sistemas automatizados, documentação, treinamentos
- **Formatos**: Chatbots, workflows, manuais, vídeos
- **Status**: Automações ativas, equipe treinada

## Quando está pronto e aprovado?
- [ ] Chatbots funcionando corretamente
- [ ] Automações de vendas implementadas
- [ ] Processos internos automatizados
- [ ] Equipe treinada
- [ ] Cliente aprovou sistemas

## Prazos e escalonamento (SLA)
- **Prazos típicos**: 20-30 dias úteis
- **Urgência**: Média
- **Escalonamento**: Diretor após 25 dias

## Como medimos sucesso?
- **KPIs**: Taxa de resolução automática, satisfação do usuário
- **Metas**: 80% de resolução automática, 90% de satisfação
- **Fonte de dados**: Sistemas de automação, feedback

## O que é automático (e o que precisa de humano)?
- **Triggers**: Interações de usuário, eventos do sistema
- **Ações**: Respostas automáticas, encaminhamentos
- **Erros comuns**: Falhas de integração, respostas inadequadas
- **Retentativas**: 3 tentativas de processamento
 - **Human-in-the-loop**: Escalonamento, validação de respostas (qualidade da linguagem, ausência de vieses, aderência ao tom de voz)

## Integrações
- **Chatbots**: Atendimento automático
- **CRM**: Gestão de leads e clientes
- **n8n**: Workflows de automação
- **Zapier**: Integrações simples
- **WhatsApp/Instagram**: Canais de atendimento

## Recursos e ajuda adicional
- **Links úteis**: [Guia de chatbots], [Templates de automação]
- **Exemplos**: [Sistemas de sucesso], [Workflows de automação]
- **Contatos**: [Especialista em automação], [Suporte técnico]
- **Referências**: [knowledge/NTEX_PAPER.md], [prompts/QA_GUARDRAILS.md], [tools/supabase_setup.md], [tools/search_tavily.ts]
