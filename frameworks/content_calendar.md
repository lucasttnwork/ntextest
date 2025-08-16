### Como usar este framework (explicação simples)

- **Propósito**: organizar produção, automação e medição de conteúdo por canal.
- **Para quem**: social media, conteúdo e growth.
- **Como usar**: defina frequências, preencha campos mínimos, ative automações e revise KPIs.

# Framework: Calendário de Conteúdo NTEX

## Visão Geral
Sistema de planejamento e execução de conteúdo automatizado com IA para múltiplos canais.

## Estrutura do Calendário

### Frequências por Canal
- **Instagram**: 1-2 posts/dia + 3-5 stories/dia
- **LinkedIn**: 3-4 posts/semana
- **Facebook**: 2-3 posts/dia
- **Blog**: 2-3 artigos/semana
- **Email**: 1-2 newsletters/semana
- **YouTube**: 1 vídeo/semana

### Tipos de Conteúdo
- **Educativo**: 40% (dicas, tutoriais, insights)
- **Inspiracional**: 25% (casos de sucesso, motivação)
- **Promocional**: 20% (produtos, serviços, ofertas)
- **Engajamento**: 15% (perguntas, enquetes, interação)

## Campos Mínimos

### Metadados do Post
```
- ID: [AUTO]
- Título: [TEXT]
- Descrição: [TEXT]
- Canal: [SELECT: Instagram, LinkedIn, Facebook, Blog, Email, YouTube]
- Tipo: [SELECT: Educativo, Inspiracional, Promocional, Engajamento]
- Status: [SELECT: Rascunho, Aprovado, Agendado, Publicado, Arquivado]
- Data de Criação: [DATE]
- Data de Publicação: [DATE]
- Responsável: [USER]
- Aprovador: [USER]
```

### Conteúdo
```
- Texto Principal: [TEXT]
- Hashtags: [TEXT]
- Call-to-Action: [TEXT]
- Imagem/Vídeo: [FILE]
- Link: [URL]
- UTM: [TEXT]
```

### Performance
```
- Alcance: [NUMBER]
- Engajamento: [NUMBER]
- Cliques: [NUMBER]
- Conversões: [NUMBER]
- ROI: [CURRENCY]
```

## Fonte de Dados
- **Airtable**: Base principal do calendário
- **Buffer**: Agendamento e publicação
- **GA4**: Métricas de performance
- **CRM**: Dados de conversão

## Convenções

### Nomenclatura
- **Posts**: [CANAL]_[TIPO]_[DATA]_[TÍTULO]
- **Imagens**: [CANAL]_[TIPO]_[TÍTULO]_[DIMENSÕES]
- **Vídeos**: [CANAL]_[TIPO]_[TÍTULO]_[DURAÇÃO]

### Cores por Tipo
- **Educativo**: Azul (#3B82F6)
- **Inspiracional**: Verde (#10B981)
- **Promocional**: Laranja (#F59E0B)
- **Engajamento**: Roxo (#8B5CF6)

### Status
- **Rascunho**: Cinza
- **Aprovado**: Verde
- **Agendado**: Azul
- **Publicado**: Verde escuro
- **Arquivado**: Cinza escuro

## Automação

### Triggers
- **Novo post criado**: Gera imagem com IA
- **Post aprovado**: Agenda automaticamente
- **Post publicado**: Inicia monitoramento
- **Performance baixa**: Sugere otimizações

### Ações Automáticas
- **Geração de imagens**: Midjourney/DALL-E
 - **Otimização de texto**: ChatGPT (sempre aplicar diretrizes de tom e copy da NTEX: direto, sem jargão, sem metáforas)
- **Agendamento**: Buffer
- **Relatórios**: GA4 + BigQuery

## KPIs e Métricas

### Indicadores de Volume
- Posts criados por semana
- Posts publicados por canal
- Taxa de aprovação

### Indicadores de Performance
- Alcance médio por post
- Taxa de engajamento
- CTR por canal
- Conversões por post

### Metas Mensais
- **Volume**: 120 posts criados
- **Performance**: 5% de engajamento médio
- **Conversão**: 2% de CTR médio

## Integrações

### Ferramentas Principais
- **Airtable**: Base de dados
- **Buffer**: Agendamento
- **OpenAI**: Geração de conteúdo
- **Midjourney**: Criação de imagens

### APIs e Webhooks
- **Buffer API**: Agendamento automático
- **OpenAI API**: Geração de texto
- **GA4 API**: Métricas de performance
- **CRM API**: Dados de conversão

## Templates

### Post Educativo
```
📚 [TÍTULO]

[DESCRIÇÃO PRINCIPAL]

💡 Dica: [INSIGHT PRÁTICO]

🔗 Saiba mais: [LINK]

#hashtag1 #hashtag2 #hashtag3
```

### Post Inspiracional
```
✨ [TÍTULO]

[HISTÓRIA/CASO DE SUCESSO]

🎯 [LIÇÃO PRINCIPAL]

💪 [CALL-TO-ACTION]

#hashtag1 #hashtag2 #hashtag3
```

### Post Promocional
```
🚀 [TÍTULO]

[OFERTA/PRODUTO]

💰 [BENEFÍCIO PRINCIPAL]

⏰ [URGÊNCIA/DEADLINE]

🔗 [LINK DE AÇÃO]

#hashtag1 #hashtag2 #hashtag3
```

## Manutenção

### Revisões Semanais
- [ ] Analisar performance dos posts
- [ ] Ajustar estratégia de conteúdo
- [ ] Otimizar hashtags
- [ ] Revisar calendário da próxima semana

### Revisões Mensais
- [ ] Relatório de performance geral
- [ ] Análise de tendências
- [ ] Ajuste de metas
- [ ] Otimização de processos

## Referências
- [knowledge/NTEX_PAPER.md]
- [prompts/BUILD_SOCIAL_POST.md]
- [sops/04_distribuicao_campanhas.md]
