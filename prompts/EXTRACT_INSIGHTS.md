### Como Usar Este Prompt (Explicação Simples para Humanos)

- **Para que serve?**: Destilar insights acionáveis de transcrições e briefings.
- **Quem deve usar?**: Estratégia, conteúdo e analytics.
- **O que ele faz?**: Identifica tópicos, oportunidades e riscos com timestamps.
- **Como usar na prática?**
  1) Copie o prompt abaixo.
  2) Cole na IA e preencha `{{transcricao}}` e `{{objetivo}}`.
  3) Peça a saída em JSON + lista para fácil importação.
- **O que esperar como resultado?**: Tabela JSON com tópicos e uma lista de oportunidades e riscos.
- **Como se encaixa no processo NTEX?**: Alimenta `sops/02_destilacao_ideacao.md` e `frameworks/content_calendar.md`.

# EXTRACT_INSIGHTS

**Objetivo:** extrair tópicos únicos, profundidade e timestamps de transcrições/briefings.

**Entrada obrigatória**
- `{{transcricao}}` (texto bruto ou link)
- `{{objetivo}}` (ex.: funil topo/médio/fundo)

**Saída (JSON + lista)** 
- tópicos[ {titulo, porquê_importa, timestamp_inicial, timestamp_final, profundidade(1–5)} ]
- oportunidades de conteúdo (3–7 bullets)
- riscos/armadilhas (até 5)

**Instruções**
- Não resuma; **destile** ideias acionáveis.
- Use notas curtas e claras.
