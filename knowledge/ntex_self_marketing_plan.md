# **Plano operativo para lançar o marketing da própria NTEX**

## **Introdução**

A NTEX precisa testar, validar e refinar seus serviços atuando como o **primeiro cliente** da agência. Essa prática "comer sua própria comida para cachorro" (ou *dogfooding*) permitirá demonstrar expertise, construir um portfólio real e aprimorar processos antes de escalar para outros clientes. A seguir está um plano passo a passo para tirar a NTEX do zero e montar sua máquina de marketing integrada, focando no **Instagram** e **Google** como canais principais.

**Observação:** todos os passos devem seguir o estilo de copy "direto, punchy, zero buzzwords" definido nas diretrizes internas e manter o tom de voz da marca NTEX. Sempre que utilizar IA para criar textos ou mensagens, revise com o prompt **QA_GUARDRAILS.md** e garanta aderência.

## **1\. Preparação e captura de contexto**

1. **Kick‑off interno**: faça uma reunião gravada (via Zoom ou Riverside) para alinhar missão, visão, objetivos de curto e médio prazo (30‑90 dias) e definir o público‑alvo da NTEX. Essa gravação será transcrita via **Granola** ou similar, gerando o contexto inicial.

2. **Organização do Project**: crie um projeto "NTEX‑Self‑Marketing" em ChatGPT/Claude. Armazene no Project:

   * A transcrição da reunião.

   * Os documentos NTEX_PAPER.md e 00_guia_uso_base_marketing_ntex.md (resumo de serviços e procedimentos).

   * O glossário de voz (se existir) e quaisquer FAQs ou materiais de referência.

3. **Frameworks e prompts**: revisite e compreenda os prompts e SOPs fornecidos nos arquivos:

   * sops/01_captura_de_contexto.md a sops/06_governanca_prompt_QA.md (quando forem gerados pelo NTEX‑Builder).

   * prompts/AGENT_MARKETING_PROMPT.md, prompts/BUILD_SOCIAL_POST.md, prompts/LONGFORM_OUTLINE.md, prompts/QA_GUARDRAILS.md.

   * Os frameworks de calendário editorial, matriz de testes de anúncios e especificações de KPI/dashboards.

4. **Definição de metas**: a partir do 00_guia_uso_base_marketing_ntex.md, estabeleça metas mensais para o marketing institucional (ex.: 10 leads, 5 reuniões e ROAS ≥ 2,0 ). Estabeleça KPIs mínimos: visitas ao site, leads gerados, taxa de conversão, custo por lead, número de reuniões.

## **2\. Setup de dados e integrações**

1. **Plataformas e contas**:

   * Configure ou valide contas no **Instagram** (@ntex.a) e **Google Ads** com acesso administrativo.

   * Configure **GA4** (Google Analytics 4) no site da NTEX. Implemente eventos de conversão (ex. envio de formulário de lead).

   * Configure um banco de dados simplificado no **Supabase** ou **BigQuery** com as tabelas sugeridas no guia (leads, content_queue, campaigns ). Isso servirá como camada de dados para dashboards e automações.

2. **Integração de fontes**:

   * Use **Zapier**, **Make** ou **n8n** para sincronizar leads do formulário do site para a tabela leads e disparar notificações/seguimento.

   * Conecte APIs de Meta Ads (Instagram) e Google Ads ao BigQuery/Supabase para coletar dados de campanha diariamente .

   * Configure padrões de nomenclatura e UTMs para campanhas (ex.: utm_campaign=ntex_selfmarketing_instagram_aug25).

3. **Chaves e credenciais**: prepare .env com as APIs (GA4, Google Ads, Meta/Instagram) conforme lista do guia . Mantenha as credenciais seguras e variáveis prontas para uso pelos scripts.

## **3\. Planejamento editorial e de campanhas**

1. **Calendário editorial**:

   * Utilize frameworks/content_calendar.md (referência) para planejar 4 semanas de conteúdo . Misture temas de bastidores (como está sendo a automação da NTEX), estudos de caso fictícios e ofertas (diagnóstico gratuito de automação).

   * Frequência recomendada: 5 posts por semana no Instagram, 1 newsletter/semana e 1 landing page de oferta por mês .

2. **Definição de ofertas**: escolha uma oferta principal (por exemplo, **diagnóstico gratuito de automação de marketing**), que será promovida em campanhas pagas . Monte a landing page com base no prompt LP_BLUEPRINT.md e garanta que o copy respeite as regras NTEX.

3. **Pesquisa de persona e diferenciais**: extraia da transcrição inicial e do paper os principais problemas que a NTEX resolve. Defina personas e pontos de dor. Analise concorrentes para posicionamento e preço.

4. **Matriz de canais**: priorize Instagram (conteúdo institucional e prova social), Google Ads para captar leads específicos e SEO para posicionamento orgânico.

## **4\. Produção de ativos (Vibe Marketing)**

1. **Posts sociais**:

   * Use o prompt **BUILD_SOCIAL_POST.md** para gerar rascunhos de posts com IA. Ajuste o tom para ser direto e funcional, destacando valor e prova social.

   * Após gerar, passe pelo checklist de qualidade **QA_GUARDRAILS.md**. Ajuste manualmente se necessário.

2. **Newsletter/blog**:

   * Para conteúdos longos, siga a estrutura LONGFORM_OUTLINE.md e escreva seções separadas via IA para manter coerência e escaneabilidade.

3. **Criação de landing pages (LP)**:

   * Use LP_BLUEPRINT.md e ferramentas como Framer AI ou Webflow AI. Garanta que o site seja responsivo, rápido e tenha call-to-action claro.

4. **Imagens e vídeos**:

   * Utilize ferramentas de IA (Midjourney, DALL·E) para ilustrações, mantendo consistência de marca. Para vídeos curtos (reels), roteirize com IA e grave com smartphone; edite com CapCut ou similar.

5. **Automação de copy**: implemente A/B testing de títulos, descrições e criativos; use agentes de IA para gerar variações e avaliar quais têm melhor performance .

## **5\. Configuração e execução de campanhas**

1. **Configuração inicial**:

   * Crie campanhas no Meta Ads (Instagram) e Google Ads direcionadas para a landing page de diagnóstico. Defina segmentação básica (ex.: empresas de serviços B2B no Brasil e exterior, diretores de marketing/ops, faixas etárias 25-50).

   * Utilize agentes de IA para ajustar lances, segmentação e criativos em tempo real .

2. **Estrutura das campanhas**:

   * Separe por canal (Instagram, Google Search) e mensagem (atrativo vs. educativo). Use UTMs consistentes.

   * Defina orçamentos diários e limite de gasto. Crie scripts de alerta para desvio de budget (ex.: se campanha gastar > x, reduzir lances em 10%) .

3. **Automação de leads**:

   * Configure automações no CRM para categorizar leads, enviar e‑mails automáticos e marcar follow-up.

   * Use o **Agente de Atendimento NTEX** para responder dúvidas, qualificar leads e agendar reuniões .

4. **Testes contínuos**:

   * Aplique a matriz ad_testing_matrix.md: varie títulos, texto, oferta, público e formato. Deixe a IA priorizar as variações com maior CTR e conversão.

## **6\. Publicação e distribuição**

1. **Agendamento**: utilize Buffer ou a ferramenta de social media de preferência para agendar posts para as próximas semanas . Mantenha consistência nas datas e horários.

2. **Envio de newsletter**: programe a newsletter semanalmente via ferramenta de e‑mail (ex.: Mailchimp). Inclua links para a landing page e conteúdos do blog.

3. **Disparo de anúncios**: verifique que todas as campanhas estão ativas, com UTMs corretas, orçamentos dentro do limite e tracking funcional.

4. **Monitoramento de redes**: configure notificações para responder rapidamente comentários e mensagens. Use o Agente de Atendimento para triagens e escalonamento .

## **7\. Análise e otimização**

1. **Dashboards**:

   * Construa dashboards mínimos seguindo frameworks/kpis_dashboard_spec.md, reunindo métricas de GA4, Ads e CRM.

   * Use ferramentas com chat (Lightdash, Superset) ou agentes de IA para perguntas de negócios ("qual canal gerou mais leads esta semana?").

   * Aplique análises preditivas (ex.: previsão de leads futuros, ROI) e ajuste orçamento conforme previsões .

2. **Reuniões semanais**:

   * Execute o agente "Morning Intelligence Digest" (pode ser um prompt customizado) para obter resumo semanal de métricas e recomendações de melhoria.

   * Ajuste campanhas: pausando criativos com desempenho ruim, aumentando investimento nas melhores variações, testando novos públicos.

   * Documente aprendizados no backlog (workflows/backlog.md), sinalizando tasks com etiquetas [gap] quando houver bloqueios ou oportunidades de melhoria.

3. **Qualidade de conteúdo**:

   * Revise as copy e criativos que tiveram baixa performance e reforce aderência ao estilo NTEX. Utilize o prompt NTEX-Builder para sugerir melhorias nos textos e nos SOPs .

## **8\. Governança, segurança e melhoria contínua**

1. **Human‑in‑the‑loop**: embora a automação cubra a maior parte das tarefas, mantenha aprovação humana para:

   * Publicação de novos conteúdos e anúncios;

   * Alocação de grandes orçamentos;

   * Respostas complexas no atendimento (o agente deve escalonar) .

2. **Ética e transparência**: siga as políticas de ética definidas na SOP de governança. Revise modelos para mitigar vieses e garantir que IA não tome decisões discriminatórias .

3. **Segurança de dados**: proteja acessos a APIs e bases de dados com controles de permissões e criptografia. Ative MFA e revise periodicamente as integrações .

4. **Auditoria mensal**: ao final de cada mês, faça auditoria completa dos processos: avalie se as automações economizam tempo e geram resultados; ajuste prompts e workflows. Utilize o checklist scripts/checklist_release.md para releases de novos conteúdos ou campanhas.

## **9\. Roadmap de implantação (8 semanas)**

Baseado no guia‑mestre, adapte o roadmap para o marketing próprio:

| Semana | Objetivo principal | Ações chave |
| ----- | ----- | ----- |
| **1‑2** | **Auditoria interna e preparação** | Mapear todos os fluxos necessários, ler NTEX_PAPER.md e 00_guia_uso...; definir personas, objetivos e KPIs; configurar supabase/BigQuery e GA4; configurar contas de ads. |
| **3‑4** | **Captura de contexto e library de prompts** | Gravar reunião de kick‑off, transcrever com Granola; organizar Project; configurar e testar AGENT_MARKETING_PROMPT e AGENT_ATENDIMENTO_PROMPT; preparar conteúdo do glossário de voz. |
| **5‑6** | **Automação de conteúdo e campanhas piloto** | Construir calendário editorial; gerar primeiros posts e newsletter com IA; desenhar landing page; iniciar campanha piloto no Instagram e Google com orçamento pequeno; implementar integrações com CRM e ETL. |
| **7** | **Dashboards e análise inicial** | Montar dashboard mínimo com KPIs; validar tracking; rodar relatório semanal; ajustar campanhas conforme desempenho. |
| **8** | **Stress test e ajustes** | Simular ciclos completos (do brief ao relatório), medir tempo/humano, identificar bugs; revisar SOPs e prompts; planejar expansão para novos canais (ex.: YouTube Ads). |

## **10\. Considerações finais**

Seguindo este plano, a NTEX conseguirá **validar sua própria metodologia** de vibe marketing e automação de processos, construindo uma presença digital consistente e aprendendo com dados reais. Esse ciclo de auto‑experimentação fornecerá cases e depoimentos que servirão de prova social para conquistar clientes de maior porte. Lembre‑se de que a eficiência vem da combinação de automação com supervisão humana: automatize as rotinas, mas mantenha a estratégia, a curadoria e o relacionamento nas mãos de Lucas até que seja possível escalar a equipe.

