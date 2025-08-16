### Como usar este framework (explicação simples)

- **Propósito**: padronizar KPIs e dashboards para leitura rápida.
- **Para quem**: analytics, gestores e clientes.
- **Como usar**: escolha nível de acesso, defina KPIs, configure fontes e alertas. Siga as convenções.

# Framework: Especificação de Dashboard de KPIs NTEX

## Visão Geral
Sistema centralizado de métricas e indicadores para monitoramento em tempo real da performance de marketing digital.

## Estrutura do Dashboard

### Níveis de Acesso
- **Executivo**: Visão estratégica e resumo
- **Gerencial**: Visão tática e operacional
- **Operacional**: Visão detalhada e executiva
- **Cliente**: Visão limitada e personalizada

### Frequência de Atualização
- **Tempo real**: Métricas críticas (conversões, gastos)
- **Diário**: Performance de campanhas
- **Semanal**: Relatórios consolidados
- **Mensal**: Análise estratégica

## Campos Mínimos

### Metadados do Dashboard
```
- ID: [AUTO]
- Nome: [TEXT]
- Nível de Acesso: [SELECT: Executivo, Gerencial, Operacional, Cliente]
- Frequência de Atualização: [SELECT: Tempo Real, Diário, Semanal, Mensal]
- Status: [SELECT: Ativo, Em Desenvolvimento, Arquivado]
- Responsável: [USER]
- Última Atualização: [TIMESTAMP]
```

### Configuração
```
- Fonte de Dados: [SELECT: GA4, BigQuery, CRM, Ads, Social]
- Filtros Disponíveis: [TEXT]
- Gráficos Incluídos: [TEXT]
- Alertas Configurados: [TEXT]
```

### KPIs Principais
```
- Visitas: [NUMBER]
- Conversões: [NUMBER]
- Taxa de Conversão: [PERCENTAGE]
- Custo por Conversão: [CURRENCY]
- ROI: [PERCENTAGE]
- Receita: [CURRENCY]
```

## Fonte de Dados
- **GA4**: Analytics e comportamento
- **BigQuery**: Dados consolidados
- **CRM**: Conversões e vendas
- **Plataformas de Ads**: Performance de campanhas
- **Social Media**: Engajamento e alcance

## Convenções

### Nomenclatura
- **Dashboards**: [NÍVEL]_[FUNÇÃO]_[FREQUÊNCIA]
- **Métricas**: [CATEGORIA]_[INDICADOR]_[PERÍODO]
- **Relatórios**: [TIPO]_[DATA]_[VERSÃO]
 - Observação: usar linguagem direta e sem jargões desnecessários para facilitar a interpretação pelo cliente

### Cores por Performance
- **Excelente**: Verde (#10B981)
- **Bom**: Azul (#3B82F6)
- **Atenção**: Amarelo (#F59E0B)
- **Crítico**: Vermelho (#EF4444)

### Unidades
- **Percentuais**: 2 casas decimais
- **Moeda**: R$ com 2 casas decimais
- **Números**: Separador de milhares
- **Datas**: DD/MM/AAAA
 - Observação: rotular unidades de forma explícita e simples (ex.: "Conversões (unid)", "Receita (R$)")

## Automação

### Triggers
- **Novos dados**: Atualização automática
- **Métricas críticas**: Alertas em tempo real
- **Relatórios**: Geração automática
- **Anomalias**: Detecção automática

### Ações Automáticas
- **Atualização**: Coleta de dados em tempo real
- **Alertas**: Notificações por email/Slack
- **Relatórios**: Geração e envio automático
- **Otimização**: Sugestões automáticas

## KPIs e Métricas

### Indicadores de Tráfego
- **Visitas**: Total de sessões únicas
- **Usuários**: Total de usuários únicos
- **Páginas/Sessão**: Média de páginas por sessão
- **Tempo na Página**: Tempo médio de permanência

### Indicadores de Conversão
- **Conversões**: Total de conversões
- **Taxa de Conversão**: Conversões/Visitas
- **Custo por Conversão**: Gastos/Conversões
- **Valor por Conversão**: Receita/Conversões

### Indicadores de Performance
- **CTR**: Taxa de clique
- **CPC**: Custo por clique
- **CPM**: Custo por mil impressões
- **ROAS**: Retorno sobre gastos em anúncios

### Indicadores de Engajamento
- **Likes**: Total de curtidas
- **Comentários**: Total de comentários
- **Compartilhamentos**: Total de compartilhamentos
- **Alcance**: Total de pessoas alcançadas

## Integrações

### Ferramentas Principais
- **GA4**: Analytics e métricas
- **BigQuery**: Processamento de dados
- **Looker Studio**: Visualizações
- **Metabase**: Dashboards interativos

### APIs e Webhooks
- **GA4 API**: Métricas de analytics
- **BigQuery API**: Dados consolidados
- **CRM API**: Dados de conversão
- **Ads API**: Performance de campanhas

## Templates de Dashboard

### Dashboard Executivo
```
Nome: Executivo_Resumo_Diario
Nível: Executivo
Frequência: Diário
KPIs Incluídos:
- Visitas totais
- Conversões totais
- Receita total
- ROI geral
- Performance por canal
```

### Dashboard Gerencial
```
Nome: Gerencial_Campanhas_Semanal
Nível: Gerencial
Frequência: Semanal
KPIs Incluídos:
- Performance por campanha
- Segmentação de público
- Otimizações realizadas
- Próximas ações
```

### Dashboard Operacional
```
Nome: Operacional_Detalhado_TempoReal
Nível: Operacional
Frequência: Tempo Real
KPIs Incluídos:
- Métricas detalhadas por anúncio
- Performance por hora
- Alertas de performance
- Ações corretivas
```

## Processo de Implementação

### 1. Planejamento
- [ ] Definir objetivos do dashboard
- [ ] Identificar KPIs necessários
- [ ] Mapear fontes de dados
- [ ] Estabelecer frequência de atualização

### 2. Desenvolvimento
- [ ] Configurar fontes de dados
- [ ] Criar estrutura do dashboard
- [ ] Implementar visualizações
- [ ] Configurar alertas

### 3. Teste
- [ ] Validar dados
- [ ] Testar funcionalidades
- [ ] Validar com usuários
- [ ] Ajustar configurações

### 4. Implementação
- [ ] Ativar dashboard
- [ ] Treinar usuários
- [ ] Monitorar performance
- [ ] Coletar feedback

### 5. Manutenção
- [ ] Atualizar dados
- [ ] Otimizar performance
- [ ] Adicionar novos KPIs
- [ ] Manter documentação

## Manutenção

### Revisões Diárias
- [ ] Verificar atualizações de dados
- [ ] Validar alertas
- [ ] Ajustar configurações
- [ ] Documentar observações

### Revisões Semanais
- [ ] Analisar performance geral
- [ ] Identificar tendências
- [ ] Ajustar KPIs
- [ ] Otimizar visualizações

### Revisões Mensais
- [ ] Relatório de performance
- [ ] Análise de uso
- [ ] Planejamento de melhorias
- [ ] Atualização de objetivos

## Referências
- [knowledge/NTEX_PAPER.md]
- [prompts/EXTRACT_INSIGHTS.md]
- [sops/05_analise_e_aprendizado.md]
