# Guia de Uso da Base NTEX para Iniciar o Marketing da Própria NTEX

## O que fazemos aqui?
Mapear, passo a passo, como usar esta base para dar start no marketing institucional da NTEX (prospectar, gerar demanda e marcar reuniões).

## Até onde este processo vai (e o que ele não faz)?
- **Inclui**: preparação de contexto, setup de dados e integrações, planejamento editorial, produção de ativos com IA, configuração de campanhas, publicação, análise e otimização.
- **Exclui**: entrega de projetos de clientes, desenvolvimento de apps complexos, implementação de CRM avançado.

## Quem faz o quê?
- **Responsável (R)**: Lucas (Founder)
- **Aprovador (A)**: Lucas
- **Consultados (C)**: Parceiros pontuais (design/ads quando necessário)
- **Informados (I)**: Leads em nutrição (via e‑mail/LinkedIn)

## O que precisamos para começar?
- **Arquivos**: `knowledge/NTEX_PAPER.md`, `knowledge/glossary.md`
- **Prompts**: `prompts/AGENT_MARKETING_PROMPT.md`, `prompts/BUILD_SOCIAL_POST.md`, `prompts/LONGFORM_OUTLINE.md`, `prompts/QA_GUARDRAILS.md`
- **SOPs de apoio**: `sops/01_captura_de_contexto.md`, `sops/02_destilacao_ideacao.md`, `sops/03_producao_de_ativos.md`, `sops/04_distribuicao_campanhas.md`, `sops/05_analise_e_aprendizado.md`
- **Triggers**: formulário de lead, novo conteúdo aprovado, limite de gasto diário.
- **Dados necessários**: persona, proposta de valor, canais, orçamento, metas de curto prazo.

## Quais ferramentas usamos (e para que servem)?
- **Apps principais**: LinkedIn, Meta/Instagram, Google Ads, GA4
- **Chaves/API**: GA4, Google Ads, Meta Ads, LinkedIn, Supabase/BigQuery
- **Integrações**: Zapier/Make/n8n para orquestração; Supabase/BigQuery para dados
- **IA**: Agente de Marketing (`prompts/AGENT_MARKETING_PROMPT.md`) e prompts de conteúdo/QA

## Procedimento (checklist)
1) **Preparação**
- [ ] Ler `knowledge/NTEX_PAPER.md` (proposta, serviços, vibe marketing)
- [ ] Revisar `knowledge/glossary.md` (tom de voz)
- [ ] Definir objetivo de 30 dias: ex. 20 conexões/dia no LinkedIn, 10 leads, 5 reuniões

2) **Setup de dados e integrações**
- [ ] GA4 instalado no site/LP (evento de lead)
- [ ] Criar projeto de dados: Supabase (mínimo) ou BigQuery
- [ ] Conectar fontes (Ads, Social) via Zapier/Make → banco de dados
- [ ] Configurar nomenclaturas UTM e convenções

3) **Planejamento editorial e de campanhas**
- [ ] Abrir `frameworks/content_calendar.md` (referência) e montar 4 semanas
- [ ] Definir temas: casos de automação, bastidores, ofertas, estudos de caso
- [ ] Mapear mix: 3 posts/semana LinkedIn + 1 newsletter + 1 LP de oferta

4) **Produção de ativos com IA**
- [ ] Usar `prompts/BUILD_SOCIAL_POST.md` para rascunhos
- [ ] Validar com `prompts/QA_GUARDRAILS.md`
- [ ] Criar LP com `prompts/LP_BLUEPRINT.md` (se aplicável)

5) **Configuração de campanhas**
- [ ] Definir 1 oferta principal (ex.: diagnóstico gratuito de automação)
- [ ] Configurar campanhas Meta/Google com segmentação inicial
- [ ] Aplicar `prompts/AGENT_MARKETING_PROMPT.md` para variações A/B

6) **Publicação e distribuição**
- [ ] Agendar LinkedIn (3/semana) e newsletter
- [ ] Publicar LP e ativar UTMs
- [ ] Ligar automações de captação de lead → CRM/banco de dados

7) **Análise e otimização**
- [ ] Montar dashboard mínimo (ver KPIs)
- [ ] Rodar rotina semanal com o agente: otimizações e relatório
- [ ] Ajustar criativos, lances e orçamento conforme metas

## O que entregamos ao final?
- **Artefatos**: calendário editorial, LP, campanhas ativas, dashboard, relatórios semanais
- **Formatos**: Markdown (docs), URLs (LPs), CSV/DB (dados), PDFs (relatórios)
- **Status**: conteúdos publicados, campanhas ativas, tracking validado

## Quando está pronto e aprovado?
- **Pronto**: calendário das próximas 4 semanas, 1 LP ativo, campanhas com UTMs, dashboard com dados, automações funcionando
- **Qualidade mínima**: tom de voz aderente, criativos validados por QA, tracking sem quebra
- **Aprovação**: Lucas valida antes de ativar orçamento

## Prazos e escalonamento (SLA)
- **Kickoff**: 2 dias
- **Produção inicial**: 5 dias
- **Go‑live**: até D+7
- **Atraso**: se integração quebrar > 24h, pausar mídia, abrir tarefa de correção

## Como medimos sucesso?
- **KPIs (mensal)**: visitas, leads, taxa de conversão, custo por lead, reuniões, ROI/ROAS
- **Metas de 30 dias**: 10 leads, 5 reuniões, ROAS ≥ 2.0
- **Fonte de dados**: GA4, Ads, CRM/DB, LinkedIn

## O que é automático (e o que precisa de humano)?
- **Triggers**
  - Novo lead do form → inserir em `leads` (DB) e enviar e‑mail
  - Gasto diário > alvo/campanha com ROAS < meta → alerta Slack e reduzir lances 10%
  - Conteúdo aprovado → agendar e atualizar status
- **Ações automáticas**: coleta/ETL de dados, agendamento, ajustes de lance conforme limites
- **Erros comuns**: UTM faltando, metas mal definidas, orçamento desalinhado
- **Retentativas**: 3 tentativas de integração; após isso, abrir ticket manual
- **Human‑in‑the‑loop**: aprovação de criativos, mudança de orçamento total, pausar campanha

## Integrações
- **Buffer/Agendamento**: posts LinkedIn
- **Meta/Google Ads**: campanhas e gastos
- **GA4**: analytics e conversões
- **n8n/Zapier/Make**: orquestração
- **Supabase/BigQuery**: camada de dados

### Chaves e credenciais (mínimo)
- GA4 API, Google Ads API, Meta Marketing API, LinkedIn (dev/app), Supabase URL + KEY

### Esquema mínimo de dados (Supabase)
```
Tabela: leads
- id (uuid, pk)
- source (text)
- name (text)
- email (text)
- company (text)
- country (text)
- status (enum: new, qualified, meeting, won, lost)
- created_at (timestamp)

Tabela: content_queue
- id (uuid, pk)
- platform (text: linkedin, instagram)
- type (text: post, ad)
- status (enum: draft, approved, scheduled, posted)
- due_date (date)
- url (text)
- kpi_target (json)

Tabela: campaigns
- id (uuid, pk)
- channel (text: meta, google, linkedin)
- objective (text)
- budget_daily (numeric)
- start_date (date)
- end_date (date)
- utm_campaign (text)
- status (enum: active, paused)
```

## Recursos e ajuda adicional
- `frameworks/kpis_dashboard_spec.md` (métricas e dashboards)
- `frameworks/content_calendar.md` (planejamento)
- `tools/supabase_setup.md` (setup de dados)
- `scripts/checklist_release.md` (checklist de publicação)
- `prompts/AGENT_MARKETING_PROMPT.md` (otimização)


