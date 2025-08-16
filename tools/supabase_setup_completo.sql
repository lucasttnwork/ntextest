-- ========================================
-- SISTEMA DE MEMÓRIA COMPLETO PARA AGENTES NTEX
-- Execute este script do ZERO no Supabase
-- ========================================

-- ========================================
-- 1. LIMPEZA E PREPARAÇÃO
-- ========================================

-- Remover tabelas existentes se houver
DROP TABLE IF EXISTS agent_context CASCADE;
DROP TABLE IF EXISTS agent_files CASCADE;
DROP TABLE IF EXISTS agent_logs CASCADE;
DROP TABLE IF EXISTS chat_messages CASCADE;
DROP TABLE IF EXISTS chat_sessions CASCADE;

-- Remover funções existentes se houver
DROP FUNCTION IF EXISTS update_session_activity() CASCADE;
DROP FUNCTION IF EXISTS cleanup_old_sessions(INTEGER) CASCADE;
DROP FUNCTION IF EXISTS get_session_context(UUID) CASCADE;

-- Remover extensões se houver
DROP EXTENSION IF EXISTS "uuid-ossp";
DROP EXTENSION IF EXISTS "pg_net";
DROP EXTENSION IF EXISTS "pg_stat_statements";

-- ========================================
-- 2. EXTENSÕES NECESSÁRIAS
-- ========================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_net";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- ========================================
-- 3. TABELAS PRINCIPAIS
-- ========================================

-- Tabela de sessões de conversa
CREATE TABLE chat_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL,
    user_id VARCHAR(255), -- ID do usuário (pode ser anônimo)
    status VARCHAR(50) DEFAULT 'active',
    context_summary TEXT, -- Resumo do contexto da conversa
    metadata JSONB DEFAULT '{}', -- Metadados adicionais
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de mensagens da conversa
CREATE TABLE chat_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    agent_name VARCHAR(100), -- Nome do agente que respondeu
    message_type VARCHAR(50) DEFAULT 'text', -- 'text', 'image', 'file', 'log'
    metadata JSONB DEFAULT '{}', -- Metadados da mensagem
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sequence_order INTEGER -- Ordem na conversa
);

-- Tabela de logs de execução dos agentes
CREATE TABLE agent_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    log_level VARCHAR(20) DEFAULT 'info', -- 'debug', 'info', 'warning', 'error'
    message TEXT NOT NULL,
    log_type VARCHAR(50) DEFAULT 'execution', -- 'execution', 'thinking', 'result'
    step_number INTEGER, -- Número do passo na execução
    execution_time_ms INTEGER, -- Tempo de execução em milissegundos
    metadata JSONB DEFAULT '{}', -- Dados adicionais do log
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de arquivos gerados pelos agentes
CREATE TABLE agent_files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL, -- 'image', 'document', 'video'
    file_path VARCHAR(500) NOT NULL, -- Caminho para o arquivo
    file_size BIGINT, -- Tamanho em bytes
    mime_type VARCHAR(100),
    metadata JSONB DEFAULT '{}', -- Metadados do arquivo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de contexto e memória dos agentes
CREATE TABLE agent_context (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    context_key VARCHAR(255) NOT NULL, -- Chave do contexto
    context_value TEXT, -- Valor do contexto
    context_type VARCHAR(50) DEFAULT 'text', -- 'text', 'json', 'url'
    importance_score INTEGER DEFAULT 1, -- Score de importância (1-10)
    expires_at TIMESTAMP WITH TIME ZONE, -- Quando o contexto expira
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- 4. ÍNDICES PARA PERFORMANCE
-- ========================================

CREATE INDEX idx_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_status ON chat_sessions(status);
CREATE INDEX idx_chat_sessions_updated_at ON chat_sessions(updated_at);

CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_created_at ON chat_messages(created_at);
CREATE INDEX idx_chat_messages_sequence_order ON chat_messages(sequence_order);

CREATE INDEX idx_agent_logs_session_id ON agent_logs(session_id);
CREATE INDEX idx_agent_logs_agent_name ON agent_logs(agent_name);
CREATE INDEX idx_agent_logs_created_at ON agent_logs(created_at);
CREATE INDEX idx_agent_logs_log_type ON agent_logs(log_type);

CREATE INDEX idx_agent_files_session_id ON agent_files(session_id);
CREATE INDEX idx_agent_files_agent_name ON agent_files(agent_name);
CREATE INDEX idx_agent_files_file_type ON agent_files(file_type);

CREATE INDEX idx_agent_context_session_id ON agent_context(session_id);
CREATE INDEX idx_agent_context_agent_name ON agent_context(agent_name);
CREATE INDEX idx_agent_context_key ON agent_context(context_key);

-- ========================================
-- 5. FUNÇÕES ÚTEIS
-- ========================================

-- Função para atualizar timestamp de última atividade
CREATE OR REPLACE FUNCTION update_session_activity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE chat_sessions 
    SET last_activity = NOW(), updated_at = NOW()
    WHERE id = NEW.session_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para atualizar atividade da sessão
CREATE TRIGGER trigger_update_session_activity
    AFTER INSERT ON chat_messages
    FOR EACH ROW EXECUTE FUNCTION update_session_activity();

-- Função para limpar sessões antigas
CREATE OR REPLACE FUNCTION cleanup_old_sessions(days_old INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM chat_sessions 
    WHERE last_activity < NOW() - INTERVAL '1 day' * days_old
    AND status = 'inactive';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Função para obter contexto de uma sessão (CORRIGIDA - sem agregações aninhadas)
CREATE OR REPLACE FUNCTION get_session_context(session_uuid UUID)
RETURNS JSONB AS $$
DECLARE
    context_data JSONB;
    recent_messages JSONB;
    agent_contexts JSONB;
BEGIN
    -- Obter mensagens recentes (últimas 10)
    SELECT jsonb_agg(
        jsonb_build_object(
            'role', cm.role,
            'content', cm.content,
            'agent', cm.agent_name,
            'timestamp', cm.created_at
        ) ORDER BY cm.sequence_order DESC
    ) INTO recent_messages
    FROM (
        SELECT role, content, agent_name, created_at, sequence_order
        FROM chat_messages 
        WHERE session_id = session_uuid 
        ORDER BY sequence_order DESC 
        LIMIT 10
    ) cm;
    
    -- Obter contextos dos agentes (sem agregações aninhadas)
    SELECT jsonb_build_object(
        'contexts', jsonb_agg(
            jsonb_build_object(
                'key', ac.context_key,
                'value', ac.context_value,
                'importance', ac.importance_score
            )
        )
    ) INTO agent_contexts
    FROM agent_context ac
    WHERE ac.session_id = session_uuid;
    
    -- Construir resposta final
    SELECT jsonb_build_object(
        'session_info', row_to_json(cs),
        'recent_messages', COALESCE(recent_messages, '[]'::jsonb),
        'agent_contexts', COALESCE(agent_contexts, '{"contexts": []}'::jsonb)
    ) INTO context_data
    FROM chat_sessions cs
    WHERE cs.id = session_uuid;
    
    RETURN context_data;
END;
$$ LANGUAGE plpgsql;

-- ========================================
-- 6. POLÍTICAS DE SEGURANÇA (RLS)
-- ========================================

ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_context ENABLE ROW LEVEL SECURITY;

-- Políticas básicas (ajustar conforme necessidade de autenticação)
CREATE POLICY "Permitir acesso público às sessões" ON chat_sessions
    FOR ALL USING (true);

CREATE POLICY "Permitir acesso público às mensagens" ON chat_messages
    FOR ALL USING (true);

CREATE POLICY "Permitir acesso público aos logs" ON agent_logs
    FOR ALL USING (true);

CREATE POLICY "Permitir acesso público aos arquivos" ON agent_files
    FOR ALL USING (true);

CREATE POLICY "Permitir acesso público ao contexto" ON agent_context
    FOR ALL USING (true);

-- ========================================
-- 7. DADOS DE EXEMPLO
-- ========================================

-- Inserir sessão de exemplo
INSERT INTO chat_sessions (session_name, user_id, context_summary) 
VALUES ('Conversa sobre Marketing Digital', 'user_001', 'Discussão sobre estratégias de marketing digital para pequenas empresas');

-- Inserir mensagens de exemplo
INSERT INTO chat_messages (session_id, role, content, agent_name, message_type, sequence_order)
SELECT 
    cs.id,
    'user',
    'Quero criar uma campanha de marketing digital para minha empresa',
    NULL,
    'text',
    1
FROM chat_sessions cs WHERE cs.session_name = 'Conversa sobre Marketing Digital';

INSERT INTO chat_messages (session_id, role, content, agent_name, message_type, sequence_order)
SELECT 
    cs.id,
    'assistant',
    'Vou ajudá-lo a criar uma campanha completa. Primeiro, preciso entender melhor seu negócio.',
    'NTEX_Master_Agent',
    'text',
    2
FROM chat_sessions cs WHERE cs.session_name = 'Conversa sobre Marketing Digital';

-- Inserir log de exemplo
INSERT INTO agent_logs (session_id, agent_name, log_level, message, log_type, step_number)
SELECT 
    cs.id,
    'NTEX_Master_Agent',
    'info',
    'Iniciando análise de requisitos da campanha',
    'execution',
    1
FROM chat_sessions cs WHERE cs.session_name = 'Conversa sobre Marketing Digital';

-- ========================================
-- 8. VERIFICAÇÃO FINAL
-- ========================================

-- Verificar se todas as tabelas foram criadas
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('chat_sessions', 'chat_messages', 'agent_logs', 'agent_files', 'agent_context')
ORDER BY tablename;

-- Verificar se as funções foram criadas
SELECT 
    proname as function_name,
    prosrc as function_source
FROM pg_proc 
WHERE proname IN ('update_session_activity', 'cleanup_old_sessions', 'get_session_context');

-- Verificar se os triggers foram criados
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table
FROM information_schema.triggers 
WHERE trigger_name = 'trigger_update_session_activity';

-- Testar a função principal
SELECT 
    'Teste da função get_session_context' as teste,
    get_session_context(
        (SELECT id FROM chat_sessions LIMIT 1)
    ) IS NOT NULL as funcionou;

-- ========================================
-- 9. COMENTÁRIOS E DOCUMENTAÇÃO
-- ========================================

COMMENT ON TABLE chat_sessions IS 'Sessões de conversa entre usuários e agentes IA';
COMMENT ON TABLE chat_messages IS 'Mensagens individuais em cada conversa';
COMMENT ON TABLE agent_logs IS 'Logs de execução e pensamento dos agentes';
COMMENT ON TABLE agent_files IS 'Arquivos gerados pelos agentes (imagens, documentos)';
COMMENT ON TABLE agent_context IS 'Contexto e memória persistente dos agentes';

COMMENT ON FUNCTION get_session_context IS 'Retorna contexto completo de uma sessão para os agentes';
COMMENT ON FUNCTION cleanup_old_sessions IS 'Remove sessões antigas para limpeza do banco';

-- ========================================
-- SISTEMA CONFIGURADO COM SUCESSO! 🎉
-- ========================================

-- Agora você pode:
-- 1. Configurar as variáveis de ambiente no arquivo .env
-- 2. Executar o sistema de agentes NTEX
-- 3. Testar a interface web em http://localhost:5003
