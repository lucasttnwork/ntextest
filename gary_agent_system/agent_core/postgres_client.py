#!/usr/bin/env python3
"""
Cliente PostgreSQL para o sistema NTEX
Substitui o Supabase por banco local via Docker
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresClient:
    """Cliente para interagir com PostgreSQL local"""
    
    def __init__(self):
        """Inicializa conexão com PostgreSQL"""
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.database = os.getenv("POSTGRES_DB", "ntex_db")
        self.user = os.getenv("POSTGRES_USER", "ntex_user")
        self.password = os.getenv("POSTGRES_PASSWORD", "ntex_password")
        self.connection = None
        
        self.connect()
    
    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            logger.info("Conexão com PostgreSQL estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar com PostgreSQL: {e}")
            self.connection = None
    
    def disconnect(self):
        """Fecha conexão com o banco"""
        if self.connection:
            self.connection.close()
            logger.info("Conexão com PostgreSQL fechada")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Executa query SELECT e retorna resultados"""
        if not self.connection:
            self.connect()
            if not self.connection:
                return []
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                # SELECT -> fetch all
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
                # INSERT/UPDATE with RETURNING -> fetchone
                elif "RETURNING" in query.upper():
                    result = cursor.fetchone()
                    self.connection.commit()
                    return [dict(result)] if result else []
                else:
                    self.connection.commit()
                    return []
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            return []
    
    def create_chat_session(self, session_name: str) -> Dict[str, Any]:
        """Cria nova sessão de chat"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        query = """
        INSERT INTO chat_sessions (session_id, session_name)
        VALUES (%s, %s)
        RETURNING id, session_id, session_name, created_at
        """
        
        try:
            results = self.execute_query(query, (session_id, session_name))
            if results:
                return {
                    "success": True,
                    "session_id": session_id,
                    "session": results[0]
                }
            else:
                return {"success": False, "error": "Falha ao criar sessão"}
        except Exception as e:
            logger.error(f"Erro ao criar sessão: {e}")
            return {"success": False, "error": str(e)}
    
    def add_message(self, session_id: str, role: str, content: str, 
                   agent_name: str = None, metadata: Dict = None):
        """Adiciona mensagem à sessão"""
        query = """
        INSERT INTO chat_messages (session_id, role, content, agent_name, metadata)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            metadata_json = json.dumps(metadata) if metadata else None
            self.execute_query(query, (session_id, role, content, agent_name, metadata_json))
            logger.info(f"Mensagem adicionada à sessão {session_id}")
        except Exception as e:
            logger.error(f"Erro ao adicionar mensagem: {e}")
    
    def add_agent_log(self, session_id: str, log_data: Dict):
        """Adiciona log do agente"""
        query = """
        INSERT INTO agent_logs (session_id, agent_name, message, log_level, 
                               log_type, step_number, execution_time_ms, metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            metadata_json = json.dumps(log_data.get('metadata', {}))
            params = (
                session_id,
                log_data['agent_name'],
                log_data['message'],
                log_data['log_level'],
                log_data['log_type'],
                log_data.get('step_number'),
                log_data.get('execution_time_ms'),
                metadata_json
            )
            self.execute_query(query, params)
        except Exception as e:
            logger.error(f"Erro ao adicionar log do agente: {e}")
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Obtém contexto da sessão"""
        query = """
        SELECT cm.role, cm.content, cm.agent_name, cm.created_at
        FROM chat_messages cm
        WHERE cm.session_id = %s
        ORDER BY cm.created_at DESC
        LIMIT 20
        """
        
        try:
            messages = self.execute_query(query, (session_id,))
            
            # Formatar contexto
            context_lines = []
            for msg in reversed(messages):
                if msg['role'] == 'user':
                    context_lines.append(f"Usuário: {msg['content']}")
                elif msg['role'] == 'assistant':
                    agent = msg['agent_name'] or 'Sistema'
                    context_lines.append(f"{agent}: {msg['content']}")
            
            return {
                "success": True,
                "context": "\n".join(context_lines)
            }
        except Exception as e:
            logger.error(f"Erro ao obter contexto: {e}")
            return {"success": False, "error": str(e)}
    
    def list_chat_sessions(self, limit: int = 50) -> Dict[str, Any]:
        """Lista sessões de chat"""
        query = """
        SELECT session_id, session_name, created_at, updated_at
        FROM chat_sessions
        ORDER BY updated_at DESC
        LIMIT %s
        """
        
        try:
            sessions = self.execute_query(query, (limit,))
            return {
                "success": True,
                "sessions": sessions
            }
        except Exception as e:
            logger.error(f"Erro ao listar sessões: {e}")
            return {"success": False, "error": str(e)}

def get_postgres_client() -> PostgresClient:
    """Factory para obter cliente PostgreSQL"""
    return PostgresClient()

# Teste da conexão
if __name__ == "__main__":
    client = get_postgres_client()
    if client.connection:
        print("✅ Conexão com PostgreSQL estabelecida!")
        result = client.list_chat_sessions(5)
        print(f"Sessões encontradas: {len(result.get('sessions', []))}")
        client.disconnect()
    else:
        print("❌ Falha na conexão com PostgreSQL")
