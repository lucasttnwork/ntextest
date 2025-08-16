### Como usar este guia (explicação simples)

- **Propósito**: implementar o agente de marketing de ponta a ponta.
- **Para quem**: dev/ops com noções de TypeScript e Supabase.
- **Como usar**: siga a ordem das seções: dependências → conexão → módulos → ponto de entrada → próximos passos.
- **Resultado esperado**: agente funcionando, webhooks ativos e relatórios operando.

# Implementação do Agente de Marketing NTEX

## Objetivo
Sistema de IA autônomo para gestão de campanhas, otimização de performance e automação de marketing.

## Arquitetura

### 1. Estrutura de Arquivos
```
tools/
├── agente_marketing/
│   ├── index.ts              # Ponto de entrada
│   ├── types.ts              # Tipos TypeScript
│   ├── database.ts           # Conexão Supabase
│   ├── marketing_engine.ts   # Motor de marketing
│   ├── campaign_manager.ts   # Gestor de campanhas
│   ├── performance_analyzer.ts # Analisador de performance
│   └── automation_triggers.ts # Gatilhos de automação
```

### 2. Dependências
```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.39.0",
    "openai": "^4.20.0",
    "zod": "^3.22.0",
    "date-fns": "^2.30.0"
  }
}
```

## Implementação Core

### 1. Conexão com Supabase (database.ts)
```typescript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseKey);

export interface Lead {
  id: string;
  nome: string;
  email: string;
  empresa?: string;
  telefone?: string;
  origem: string;
  status: string;
  score: number;
  created_at: string;
  updated_at: string;
}

export interface Campanha {
  id: string;
  nome: string;
  plataforma: string;
  orcamento: number;
  status: string;
  data_inicio: string;
  data_fim: string;
  kpis: Record<string, any>;
  created_at: string;
}

export interface Metrica {
  id: string;
  campanha_id: string;
  data: string;
  impressoes: number;
  cliques: number;
  conversoes: number;
  custo: number;
  ctr: number;
  cpc: number;
  created_at: string;
}
```

### 2. Motor de Marketing (marketing_engine.ts)
```typescript
import { supabase, Lead, Campanha, Metrica } from './database';
import { OpenAI } from 'openai';

export class MarketingEngine {
  private openai: OpenAI;

  constructor() {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }

  // Analisar leads e calcular score
  async analisarLead(lead: Lead): Promise<number> {
    const { data, error } = await supabase.rpc('calcular_score_lead', {
      lead_id: lead.id
    });

    if (error) throw error;
    return data;
  }

  // Otimizar campanha baseado em performance
  async otimizarCampanha(campanhaId: string): Promise<void> {
    const { data: metricas } = await supabase
      .from('metricas')
      .select('*')
      .eq('campanha_id', campanhaId)
      .gte('data', new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString());

    if (!metricas || metricas.length === 0) return;

    const performance = this.calcularPerformance(metricas);
    const recomendacoes = await this.gerarRecomendacoes(performance);

    // Aplicar otimizações automaticamente
    await this.aplicarOtimizacoes(campanhaId, recomendacoes);
  }

  // Gerar recomendações com IA
  private async gerarRecomendacoes(performance: any): Promise<string[]> {
    const prompt = `
      Analise a performance desta campanha e sugira otimizações:
      
      CTR: ${performance.ctr}%
      CPC: R$ ${performance.cpc}
      Conversões: ${performance.conversoes}
      Custo: R$ ${performance.custo}
      
      Sugira 3-5 ações específicas para melhorar performance.
    `;

    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
      max_tokens: 300
    });

    return completion.choices[0].message.content?.split('\n').filter(Boolean) || [];
  }

  // Aplicar otimizações automaticamente
  private async aplicarOtimizacoes(campanhaId: string, recomendacoes: string[]): Promise<void> {
    // Implementar lógica de otimização automática
    // Ex: ajustar bids, pausar segmentos ruins, etc.
    console.log(`Aplicando otimizações para campanha ${campanhaId}:`, recomendacoes);
  }

  private calcularPerformance(metricas: Metrica[]) {
    const total = metricas.reduce((acc, m) => ({
      impressoes: acc.impressoes + m.impressoes,
      cliques: acc.cliques + m.cliques,
      conversoes: acc.conversoes + m.conversoes,
      custo: acc.custo + m.custo
    }), { impressoes: 0, cliques: 0, conversoes: 0, custo: 0 });

    return {
      ctr: total.impressoes > 0 ? (total.cliques / total.impressoes) * 100 : 0,
      cpc: total.cliques > 0 ? total.custo / total.cliques : 0,
      conversoes: total.conversoes,
      custo: total.custo
    };
  }
}
```

### 3. Gestor de Campanhas (campaign_manager.ts)
```typescript
import { supabase, Campanha, Metrica } from './database';

export class CampaignManager {
  // Criar nova campanha
  async criarCampanha(dados: Omit<Campanha, 'id' | 'created_at'>): Promise<Campanha> {
    const { data, error } = await supabase
      .from('campanhas')
      .insert([dados])
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  // Atualizar status da campanha
  async atualizarStatus(campanhaId: string, status: string): Promise<void> {
    const { error } = await supabase
      .from('campanhas')
      .update({ status })
      .eq('id', campanhaId);

    if (error) throw error;
  }

  // Inserir métricas diárias
  async inserirMetricas(metricas: Omit<Metrica, 'id' | 'created_at'>[]): Promise<void> {
    const { error } = await supabase
      .from('metricas')
      .insert(metricas);

    if (error) throw error;
  }

  // Buscar campanhas ativas
  async getCampanhasAtivas(): Promise<Campanha[]> {
    const { data, error } = await supabase
      .from('campanhas')
      .select('*')
      .eq('status', 'ativa')
      .lte('data_inicio', new Date().toISOString())
      .gte('data_fim', new Date().toISOString());

    if (error) throw error;
    return data || [];
  }

  // Calcular ROI de campanha
  async calcularROI(campanhaId: string): Promise<number> {
    const { data, error } = await supabase.rpc('calcular_roi_campanha', {
      campanha_id: campanhaId
    });

    if (error) throw error;
    return data || 0;
  }
}
```

### 4. Analisador de Performance (performance_analyzer.ts)
```typescript
import { supabase, Metrica, Campanha } from './database';

export class PerformanceAnalyzer {
  // Analisar tendências de performance
  async analisarTendencias(campanhaId: string, dias: number = 30): Promise<any> {
    const dataInicio = new Date(Date.now() - dias * 24 * 60 * 60 * 1000).toISOString();
    
    const { data: metricas } = await supabase
      .from('metricas')
      .select('*')
      .eq('campanha_id', campanhaId)
      .gte('data', dataInicio)
      .order('data', { ascending: true });

    if (!metricas) return null;

    return this.calcularTendencias(metricas);
  }

  // Identificar anomalias
  async identificarAnomalias(campanhaId: string): Promise<string[]> {
    const metricas = await this.analisarTendencias(campanhaId, 7);
    const anomalias: string[] = [];

    // Lógica para identificar anomalias
    if (metricas.ctr < 0.5) anomalias.push('CTR muito baixo');
    if (metricas.cpc > 10) anomalias.push('CPC muito alto');
    if (metricas.conversoes === 0) anomalias.push('Sem conversões');

    return anomalias;
  }

  // Gerar relatório de performance
  async gerarRelatorio(campanhaId: string): Promise<any> {
    const [metricas, campanha, roi] = await Promise.all([
      this.analisarTendencias(campanhaId),
      supabase.from('campanhas').select('*').eq('id', campanhaId).single(),
      supabase.rpc('calcular_roi_campanha', { campanha_id: campanhaId })
    ]);

    return {
      campanha: campanha.data,
      metricas,
      roi: roi.data,
      anomalias: await this.identificarAnomalias(campanhaId),
      recomendacoes: this.gerarRecomendacoes(metricas)
    };
  }

  private calcularTendencias(metricas: Metrica[]) {
    // Implementar cálculo de tendências
    return {
      ctr: metricas.reduce((acc, m) => acc + m.ctr, 0) / metricas.length,
      cpc: metricas.reduce((acc, m) => acc + m.cpc, 0) / metricas.length,
      conversoes: metricas.reduce((acc, m) => acc + m.conversoes, 0),
      custo: metricas.reduce((acc, m) => acc + m.custo, 0)
    };
  }

  private gerarRecomendacoes(metricas: any): string[] {
    const recomendacoes: string[] = [];
    
    if (metricas.ctr < 1.0) recomendacoes.push('Otimizar criativos para melhorar CTR');
    if (metricas.cpc > 5.0) recomendacoes.push('Revisar estratégia de bidding');
    if (metricas.conversoes === 0) recomendacoes.push('Verificar segmentação de público');

    return recomendacoes;
  }
}
```

### 5. Gatilhos de Automação (automation_triggers.ts)
```typescript
import { supabase } from './database';
import { MarketingEngine } from './marketing_engine';

export class AutomationTriggers {
  private marketingEngine: MarketingEngine;

  constructor() {
    this.marketingEngine = new MarketingEngine();
  }

  // Configurar webhooks para automações
  async configurarWebhooks(): Promise<void> {
    // Webhook para novos leads
    await this.configurarWebhookLead();
    
    // Webhook para mudanças de campanha
    await this.configurarWebhookCampanha();
    
    // Webhook para métricas
    await this.configurarWebhookMetricas();
  }

  // Automação: Novo lead qualificado
  async onNovoLead(lead: any): Promise<void> {
    const score = await this.marketingEngine.analisarLead(lead);
    
    if (score >= 70) {
      // Lead qualificado - iniciar sequência automática
      await this.iniciarSequenciaQualificacao(lead);
    }
  }

  // Automação: Campanha com performance baixa
  async onPerformanceBaixa(campanhaId: string): Promise<void> {
    await this.marketingEngine.otimizarCampanha(campanhaId);
  }

  // Automação: Orçamento esgotando
  async onOrcamentoBaixo(campanhaId: string): Promise<void> {
    // Pausar campanha ou ajustar bids
    await supabase
      .from('campanhas')
      .update({ status: 'pausada' })
      .eq('id', campanhaId);
  }

  private async configurarWebhookLead(): Promise<void> {
    // Implementar configuração de webhook
  }

  private async configurarWebhookCampanha(): Promise<void> {
    // Implementar configuração de webhook
  }

  private async configurarWebhookMetricas(): Promise<void> {
    // Implementar configuração de webhook
  }

  private async iniciarSequenciaQualificacao(lead: any): Promise<void> {
    // Implementar sequência automática de qualificação
    console.log(`Iniciando sequência para lead ${lead.email}`);
  }
}
```

## Ponto de Entrada (index.ts)
```typescript
import { MarketingEngine } from './marketing_engine';
import { CampaignManager } from './campaign_manager';
import { PerformanceAnalyzer } from './performance_analyzer';
import { AutomationTriggers } from './automation_triggers';

export class AgenteMarketing {
  private marketingEngine: MarketingEngine;
  private campaignManager: CampaignManager;
  private performanceAnalyzer: PerformanceAnalyzer;
  private automationTriggers: AutomationTriggers;

  constructor() {
    this.marketingEngine = new MarketingEngine();
    this.campaignManager = new CampaignManager();
    this.performanceAnalyzer = new PerformanceAnalyzer();
    this.automationTriggers = new AutomationTriggers();
  }

  // Inicializar agente
  async inicializar(): Promise<void> {
    await this.automationTriggers.configurarWebhooks();
    console.log('Agente de Marketing NTEX inicializado');
  }

  // Executar ciclo de otimização
  async executarCicloOtimizacao(): Promise<void> {
    const campanhasAtivas = await this.campaignManager.getCampanhasAtivas();
    
    for (const campanha of campanhasAtivas) {
      try {
        await this.marketingEngine.otimizarCampanha(campanha.id);
        console.log(`Campanha ${campanha.nome} otimizada`);
      } catch (error) {
        console.error(`Erro ao otimizar campanha ${campanha.nome}:`, error);
      }
    }
  }

  // Gerar relatório completo
  async gerarRelatorioCompleto(): Promise<any> {
    const campanhas = await this.campaignManager.getCampanhasAtivas();
    const relatorios = await Promise.all(
      campanhas.map(c => this.performanceAnalyzer.gerarRelatorio(c.id))
    );

    return {
      data: new Date().toISOString(),
      campanhas: relatorios,
      resumo: this.gerarResumo(relatorios)
    };
  }

  private gerarResumo(relatorios: any[]): any {
    // Implementar lógica de resumo
    return {
      totalCampanhas: relatorios.length,
      campanhasAtivas: relatorios.filter(r => r.campanha.status === 'ativa').length,
      roiMedio: relatorios.reduce((acc, r) => acc + r.roi, 0) / relatorios.length
    };
  }
}

// Exportar instância singleton
export const agenteMarketing = new AgenteMarketing();
```

## Uso do Agente

```typescript
import { agenteMarketing } from './tools/agente_marketing';

// Inicializar
await agenteMarketing.inicializar();

// Executar otimização automática
setInterval(async () => {
  await agenteMarketing.executarCicloOtimizacao();
}, 1000 * 60 * 60); // A cada hora

// Gerar relatório
const relatorio = await agenteMarketing.gerarRelatorioCompleto();
console.log(relatorio);
```

## Próximos Passos

1. **Configurar credenciais** Supabase e OpenAI
2. **Implementar testes** para cada módulo
3. **Configurar webhooks** reais para Zapier/Make
4. **Integrar com APIs** de Meta/Google Ads
5. **Implementar dashboard** de monitoramento

## Status
- [x] Estrutura de arquivos definida
- [x] Conexão Supabase implementada
- [x] Motor de marketing criado
- [x] Gestor de campanhas implementado
- [x] Analisador de performance criado
- [x] Gatilhos de automação configurados
- [ ] Testes implementados
- [ ] Webhooks configurados
- [ ] Integração com APIs externas

