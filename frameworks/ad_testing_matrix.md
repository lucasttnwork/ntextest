### Como usar este framework (explicação simples)

- **Propósito**: planejar, executar e ler testes A/B de anúncios sem complicação.
- **Para quem**: performance, mídia paga e growth.
- **Como usar**: preencha os campos mínimos, siga as frequências e rode testes contínuos. Use as convenções de nome.

# Framework: Matriz de Testes de Anúncios NTEX

## Visão Geral
Sistema estruturado para testes A/B automáticos de anúncios com IA para otimização contínua de performance.

## Estrutura de Testes

### Variáveis Testáveis
- **Criativos**: Imagens, vídeos, textos
  - Nota: variações de texto devem seguir as diretrizes de copy da NTEX (direto, punchy, sem metáforas, valor primeiro)
- **Segmentação**: Público-alvo, demografia, comportamento
- **Lances**: Estratégias de bidding, orçamentos
- **Formato**: Tipo de anúncio, tamanho, posicionamento

### Frequência de Testes
- **Criativos**: Semanal (3-5 variações)
- **Segmentação**: Quinzenal (2-3 variações)
- **Lances**: Diário (ajustes automáticos)
- **Formato**: Mensal (validação de canais)

## Campos Mínimos

### Metadados do Teste
```
- ID: [AUTO]
- Nome do Teste: [TEXT]
- Tipo: [SELECT: Criativo, Segmentação, Lance, Formato]
- Status: [SELECT: Configurado, Em Execução, Concluído, Arquivado]
- Data de Início: [DATE]
- Data de Término: [DATE]
- Orçamento Total: [CURRENCY]
- Responsável: [USER]
```

### Configuração
```
- Plataforma: [SELECT: Google Ads, Meta Ads, LinkedIn, TikTok]
- Campanha Base: [TEXT]
- Variáveis Testadas: [TEXT]
- Hipótese: [TEXT]
- Critério de Sucesso: [TEXT]
```

### Resultados
```
- Variação A: [TEXT]
- Variação B: [TEXT]
- Variação C: [TEXT]
- Variação D: [TEXT]
- Variação E: [TEXT]
```

### Performance
```
- Impressões A: [NUMBER]
- Impressões B: [NUMBER]
- Impressões C: [NUMBER]
- Impressões D: [NUMBER]
- Impressões E: [NUMBER]
- CTR A: [PERCENTAGE]
- CTR B: [PERCENTAGE]
- CTR C: [PERCENTAGE]
- CTR D: [PERCENTAGE]
- CTR E: [PERCENTAGE]
- CPC A: [CURRENCY]
- CPC B: [CURRENCY]
- CPC C: [CURRENCY]
- CPC D: [CURRENCY]
- CPC E: [CURRENCY]
- Conversões A: [NUMBER]
- Conversões B: [NUMBER]
- Conversões C: [NUMBER]
- Conversões D: [NUMBER]
- Conversões E: [NUMBER]
- CPA A: [CURRENCY]
- CPA B: [CURRENCY]
- CPA C: [CURRENCY]
- CPA D: [CURRENCY]
- CPA E: [CURRENCY]
```

## Fonte de Dados
- **Google Ads API**: Métricas de campanhas
- **Meta Ads API**: Performance de anúncios
- **GA4**: Conversões e comportamento
- **CRM**: Dados de vendas

## Convenções

### Nomenclatura
- **Testes**: [TIPO]_[PLATAFORMA]_[DATA]_[DESCRIÇÃO]
- **Variações**: [TESTE]_[VARIANTE]_[VERSÃO]
- **Relatórios**: [TESTE]_[DATA]_[RESULTADO]

### Cores por Status
- **Configurado**: Azul (#3B82F6)
- **Em Execução**: Verde (#10B981)
- **Concluído**: Verde escuro (#059669)
- **Arquivado**: Cinza (#6B7280)

### Priorização
- **Alta**: Testes de criativos principais
- **Média**: Testes de segmentação
- **Baixa**: Testes de formato

## Automação

### Triggers
- **Novo teste criado**: Configura automaticamente
- **Teste iniciado**: Inicia monitoramento
- **Teste concluído**: Gera relatório
- **Performance baixa**: Sugere otimizações

### Ações Automáticas
- **Configuração**: Setup automático de campanhas
- **Monitoramento**: Coleta de métricas em tempo real
- **Otimização**: Ajustes automáticos de lances
- **Relatórios**: Geração automática de insights

## KPIs e Métricas

### Indicadores de Volume
- Testes ativos por mês
- Variações testadas por teste
- Orçamento investido em testes

### Indicadores de Performance
- Taxa de conversão por variação
- CPC médio por teste
- ROI por variação
- Lift de performance

### Metas Mensais
- **Volume**: 20 testes ativos
- **Performance**: 15% de lift médio
- **Eficiência**: 80% dos testes concluídos no prazo

## Integrações

### Ferramentas Principais
- **Google Ads**: Campanhas de busca
- **Meta Ads**: Campanhas sociais
- **n8n**: Automação de workflows
- **BigQuery**: Análise de dados

### APIs e Webhooks
- **Google Ads API**: Métricas e configuração
- **Meta Ads API**: Performance e otimização
- **GA4 API**: Conversões e comportamento
- **CRM API**: Dados de vendas

## Templates de Teste

### Teste de Criativo
```
Nome: Criativo_GoogleAds_20241201_CTA_Principal
Tipo: Criativo
Plataforma: Google Ads
Campanha Base: Campanha Principal
Variáveis Testadas: Call-to-Action, Imagem, Texto
Hipótese: CTA mais direto aumenta conversões
Critério de Sucesso: CTR > 2%, CPA < R$ 50
```

### Teste de Segmentação
```
Nome: Segmentacao_MetaAds_20241201_Idade_Genero
Tipo: Segmentação
Plataforma: Meta Ads
Campanha Base: Campanha Social
Variáveis Testadas: Faixa etária, Gênero, Interesses
Hipótese: Mulheres 25-34 convertem melhor
Critério de Sucesso: CPA < R$ 40, Taxa de conversão > 3%
```

## Processo de Execução

### 1. Planejamento
- [ ] Identificar oportunidade de teste
- [ ] Definir hipótese clara
- [ ] Estabelecer critérios de sucesso
- [ ] Calcular tamanho da amostra

### 2. Configuração
- [ ] Criar variações no sistema
- [ ] Configurar campanhas de teste
- [ ] Validar configurações
- [ ] Iniciar teste

### 3. Monitoramento
- [ ] Acompanhar métricas diariamente
- [ ] Identificar tendências
- [ ] Ajustar configurações se necessário
- [ ] Documentar observações

### 4. Análise
- [ ] Coletar dados finais
- [ ] Calcular significância estatística
- [ ] Identificar vencedor
- [ ] Gerar relatório

### 5. Implementação
- [ ] Aplicar vencedor na campanha principal
- [ ] Arquivar teste
- [ ] Documentar aprendizados
- [ ] Planejar próximo teste

## Manutenção

### Revisões Semanais
- [ ] Analisar testes ativos
- [ ] Ajustar configurações
- [ ] Planejar novos testes
- [ ] Otimizar processos

### Revisões Mensais
- [ ] Relatório de performance geral
- [ ] Análise de tendências
- [ ] Ajuste de estratégias
- [ ] Otimização de processos

## Referências
- [knowledge/NTEX_PAPER.md]
- [prompts/EXTRACT_INSIGHTS.md]
- [sops/04_distribuicao_campanhas.md]
