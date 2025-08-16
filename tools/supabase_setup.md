### Como configurar (passo a passo simples)

1) Crie conta no Supabase e um novo projeto.
2) Copie URL e anon key nas variáveis de ambiente (`.env.local`).
3) No SQL do Supabase, cole e execute as tabelas (leads, campanhas, metricas, processos).
4) Execute as funções RPC (score de lead e ROI).
5) Habilite RLS e políticas conforme abaixo.
6) Crie a tabela `webhooks` e ative o trigger de notificação.
7) Ative extensões necessárias.
8) Teste com inserts simples e verifique permissões.

# Setup do Data Lake - Supabase NTEX

## Objetivo
Configurar infraestrutura de dados centralizada para agentes IA e automações.

## Pré-requisitos
- Conta Supabase (gratuita para começar)
- Projeto criado no Supabase
- Credenciais de API (URL + anon key)

## Estrutura do Banco

### 1. Tabelas Principais

#### leads
```sql
CREATE TABLE leads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  empresa VARCHAR(255),
  telefone VARCHAR(20),
  origem VARCHAR(100),
  status VARCHAR(50) DEFAULT 'novo',
  score INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### campanhas
```sql
CREATE TABLE campanhas (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  plataforma VARCHAR(100),
  orcamento DECIMAL(10,2),
  status VARCHAR(50) DEFAULT 'rascunho',
  data_inicio DATE,
  data_fim DATE,
  kpis JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### metricas
```sql
CREATE TABLE metricas (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  campanha_id UUID REFERENCES campanhas(id),
  data DATE NOT NULL,
  impressoes INTEGER DEFAULT 0,
  cliques INTEGER DEFAULT 0,
  conversoes INTEGER DEFAULT 0,
  custo DECIMAL(10,2) DEFAULT 0,
  ctr DECIMAL(5,4),
  cpc DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### processos
```sql
CREATE TABLE processos (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  tipo VARCHAR(100),
  status VARCHAR(50) DEFAULT 'ativo',
  etapas JSONB,
  responsaveis JSONB,
  kpis JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 2. Funções RPC

#### calcular_score_lead
```sql
CREATE OR REPLACE FUNCTION calcular_score_lead(lead_id UUID)
RETURNS INTEGER AS $$
DECLARE
  score INTEGER := 0;
  lead_data RECORD;
BEGIN
  SELECT * INTO lead_data FROM leads WHERE id = lead_id;
  
  -- Score baseado em origem
  CASE lead_data.origem
    WHEN 'google_ads' THEN score := score + 30;
    WHEN 'meta_ads' THEN score := score + 25;
    WHEN 'linkedin' THEN score := score + 20;
    WHEN 'organico' THEN score := score + 15;
    ELSE score := score + 10;
  END CASE;
  
  -- Score baseado em empresa
  IF lead_data.empresa IS NOT NULL THEN score := score + 20; END IF;
  IF lead_data.telefone IS NOT NULL THEN score := score + 15; END IF;
  
  -- Atualizar score na tabela
  UPDATE leads SET score = score, updated_at = NOW() WHERE id = lead_id;
  
  RETURN score;
END;
$$ LANGUAGE plpgsql;
```

#### calcular_roi_campanha
```sql
CREATE OR REPLACE FUNCTION calcular_roi_campanha(campanha_id UUID)
RETURNS DECIMAL AS $$
DECLARE
  receita_total DECIMAL := 0;
  custo_total DECIMAL := 0;
  roi DECIMAL;
BEGIN
  -- Calcular receita (exemplo simplificado)
  SELECT COALESCE(SUM(conversoes * 100), 0) INTO receita_total 
  FROM metricas WHERE campanha_id = $1;
  
  -- Calcular custo
  SELECT COALESCE(SUM(custo), 0) INTO custo_total 
  FROM metricas WHERE campanha_id = $1;
  
  -- Calcular ROI
  IF custo_total > 0 THEN
    roi := ((receita_total - custo_total) / custo_total) * 100;
  ELSE
    roi := 0;
  END IF;
  
  RETURN roi;
END;
$$ LANGUAGE plpgsql;
```

### 3. Políticas de Segurança (RLS)

```sql
-- Habilitar RLS em todas as tabelas
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE campanhas ENABLE ROW LEVEL SECURITY;
ALTER TABLE metricas ENABLE ROW LEVEL SECURITY;
ALTER TABLE processos ENABLE ROW LEVEL SECURITY;

-- Política para leads (apenas usuários autenticados)
CREATE POLICY "Usuários podem ver leads" ON leads
  FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Usuários podem inserir leads" ON leads
  FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Política para campanhas
CREATE POLICY "Usuários podem gerenciar campanhas" ON campanhas
  FOR ALL USING (auth.role() = 'authenticated');
```

## Configuração de Integrações

### 1. Webhooks para Automações
```sql
-- Tabela para webhooks
CREATE TABLE webhooks (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  url VARCHAR(500) NOT NULL,
  eventos JSONB,
  ativo BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Trigger para notificar mudanças
CREATE OR REPLACE FUNCTION notify_webhook()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM net.http_post(
    url := 'https://hooks.zapier.com/hooks/catch/...',
    headers := '{"Content-Type": "application/json"}'::jsonb,
    body := jsonb_build_object(
      'table', TG_TABLE_NAME,
      'action', TG_OP,
      'record', row_to_json(NEW)
    )
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger em leads
CREATE TRIGGER leads_webhook
  AFTER INSERT OR UPDATE ON leads
  FOR EACH ROW EXECUTE FUNCTION notify_webhook();
```

### 2. Configuração de APIs
```sql
-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_net";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
```

## Variáveis de Ambiente

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=sua_url_do_supabase
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua_chave_anonima
SUPABASE_SERVICE_ROLE_KEY=sua_chave_service_role
```

## Próximos Passos

1. **Configurar credenciais** no projeto Supabase
2. **Executar scripts SQL** para criar estrutura
3. **Testar funções RPC** com dados de exemplo
4. **Configurar webhooks** para Zapier/Make
5. **Implementar agente de marketing** com acesso ao banco

## Status
- [ ] Projeto Supabase criado
- [ ] Estrutura de tabelas implementada
- [ ] Funções RPC criadas
- [ ] Políticas de segurança configuradas
- [ ] Webhooks configurados
- [ ] Testes de integração realizados

