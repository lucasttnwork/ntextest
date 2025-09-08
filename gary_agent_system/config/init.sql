-- Criar tabelas para o sistema NTEX
CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    session_name VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    agent_name VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    agent_name VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    log_level VARCHAR(50) DEFAULT 'info',
    log_type VARCHAR(50) DEFAULT 'execution',
    step_number INTEGER,
    execution_time_ms INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_files (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    agent_name VARCHAR(255) NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    file_type VARCHAR(100),
    file_path VARCHAR(1000),
    file_size INTEGER,
    mime_type VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_context (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    agent_name VARCHAR(255) NOT NULL,
    context_key VARCHAR(255) NOT NULL,
    context_value TEXT,
    context_type VARCHAR(50) DEFAULT 'text',
    importance_score INTEGER DEFAULT 1,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, agent_name, context_key)
);

-- Índices para performance otimizados
CREATE INDEX IF NOT EXISTS idx_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at ON chat_sessions(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at ASC);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_created ON chat_messages(session_id, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_chat_messages_role ON chat_messages(role);
CREATE INDEX IF NOT EXISTS idx_agent_logs_session_id ON agent_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_logs_created_at ON agent_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_agent_files_session_id ON agent_files(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_context_session_id ON agent_context(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_context_key ON agent_context(context_key);
CREATE INDEX IF NOT EXISTS idx_agent_context_expires ON agent_context(expires_at) WHERE expires_at IS NOT NULL;

-- Trigger para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agent_context_updated_at BEFORE UPDATE ON agent_context FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
