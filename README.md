## Bem-vindo ao Repositório NTEX

- **O que é**: Base operacional da NTEX para marketing com IA, automações e documentação clara.
- **Para quem é**: Fundadores, marketing, operações e parceiros.
- **Como usar**: Siga os Passos Rápidos; navegue pelos arquivos via links abaixo.

### Passos Rápidos
1) Adicione seu paper em `knowledge/NTEX_PAPER.md`.
2) Crie o `.env` na raiz:
```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```
3) No Cursor (Agent mode), use `prompts/NTEX_BUILDER_PROMPT.md` para revisão/edição automática.
4) Ou use `PROMPT_AGENT_NTEX.md` para gerar o seed inicial.
5) Deixe o agente atualizar backlog, SOPs, frameworks e roadmap.

Observação: O seed inclui prompts, templates e regras. Os conteúdos serão preenchidos a partir do seu paper.

### Navegação
- SOPs: `sops/01_captura_de_contexto.md` … `sops/06_governanca_prompt_QA.md`
- Prompts de agentes: `prompts/AGENT_*.md`
- Blueprints/Frameworks: `prompts/LP_BLUEPRINT.md`, `frameworks/content_calendar.md`, `frameworks/ad_testing_matrix.md`, `frameworks/kpis_dashboard_spec.md`
- QA: `prompts/QA_GUARDRAILS.md`
- Backlog/Roadmap: `workflows/backlog.md`, `workflows/roadmap_8_semanas.md`
