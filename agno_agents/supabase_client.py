"""
Cliente Supabase para Sistema de Memória dos Agentes NTEX
Gerencia persistência de conversas, logs e contexto dos agentes
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

logger = logging.getLogger(__name__)

class NTEXSupabaseClient:
    """Cliente para gerenciar dados dos agentes no Supabase"""
    
    def __init__(self):
        """Inicializa cliente Supabase"""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL e SUPABASE_ANON_KEY devem estar configurados")
        
        try:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)
            logger.info("Cliente Supabase inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente Supabase: {e}")
            raise
    
    def create_chat_session(self, session_name: str, user_id: str = None, context_summary: str = None) -> Dict[str, Any]:
        """Cria nova sessão de chat"""
        try:
            data = {
                "session_name": session_name,
                "user_id": user_id,
                "context_summary": context_summary,
                "status": "active"
            }
            
            result = self.client.table("chat_sessions").insert(data).execute()
            
            if result.data:
                session_id = result.data[0]["id"]
                logger.info(f"Nova sessão criada: {session_id}")
                return {"success": True, "session_id": session_id, "data": result.data[0]}
            else:
                return {"success": False, "error": "Falha ao criar sessão"}
                
        except Exception as e:
            logger.error(f"Erro ao criar sessão: {e}")
            return {"success": False, "error": str(e)}
    
    def add_message(self, session_id: str, role: str, content: str, agent_name: str = None, 
                   message_type: str = "text", metadata: Dict = None) -> Dict[str, Any]:
        """Adiciona mensagem à sessão"""
        try:
            # Obter próxima sequência
            sequence_result = self.client.table("chat_messages")\
                .select("sequence_order")\
                .eq("session_id", session_id)\
                .order("sequence_order", desc=True)\
                .limit(1)\
                .execute()
            
            next_sequence = 1
            if sequence_result.data:
                next_sequence = sequence_result.data[0]["sequence_order"] + 1
            
            data = {
                "session_id": session_id,
                "role": role,
                "content": content,
                "agent_name": agent_name,
                "message_type": message_type,
                "sequence_order": next_sequence,
                "metadata": metadata or {}
            }
            
            result = self.client.table("chat_messages").insert(data).execute()
            
            if result.data:
                logger.info(f"Mensagem adicionada à sessão {session_id}")
                return {"success": True, "message_id": result.data[0]["id"]}
            else:
                return {"success": False, "error": "Falha ao adicionar mensagem"}
                
        except Exception as e:
            logger.error(f"Erro ao adicionar mensagem: {e}")
            return {"success": False, "error": str(e)}
    
    def add_agent_log(self, session_id: str, agent_name: str, message: str, 
                      log_level: str = "info", log_type: str = "execution", 
                      step_number: int = None, execution_time_ms: int = None,
                      metadata: Dict = None) -> Dict[str, Any]:
        """Adiciona log de execução do agente"""
        try:
            data = {
                "session_id": session_id,
                "agent_name": agent_name,
                "log_level": log_level,
                "message": message,
                "log_type": log_type,
                "step_number": step_number,
                "execution_time_ms": execution_time_ms,
                "metadata": metadata or {}
            }
            
            result = self.client.table("agent_logs").insert(data).execute()
            
            if result.data:
                logger.info(f"Log adicionado para agente {agent_name}")
                return {"success": True, "log_id": result.data[0]["id"]}
            else:
                return {"success": False, "error": "Falha ao adicionar log"}
                
        except Exception as e:
            logger.error(f"Erro ao adicionar log: {e}")
            return {"success": False, "error": str(e)}
    
    def add_agent_file(self, session_id: str, agent_name: str, file_name: str,
                      file_type: str, file_path: str, file_size: int = None,
                      mime_type: str = None, metadata: Dict = None) -> Dict[str, Any]:
        """Adiciona arquivo gerado pelo agente"""
        try:
            data = {
                "session_id": session_id,
                "agent_name": agent_name,
                "file_name": file_name,
                "file_type": file_type,
                "file_path": file_path,
                "file_size": file_size,
                "mime_type": mime_type,
                "metadata": metadata or {}
            }
            
            result = self.client.table("agent_files").insert(data).execute()
            
            if result.data:
                logger.info(f"Arquivo {file_name} registrado para agente {agent_name}")
                return {"success": True, "file_id": result.data[0]["id"]}
            else:
                return {"success": False, "error": "Falha ao registrar arquivo"}
                
        except Exception as e:
            logger.error(f"Erro ao registrar arquivo: {e}")
            return {"success": False, "error": str(e)}
    
    def update_agent_context(self, session_id: str, agent_name: str, context_key: str,
                            context_value: str, context_type: str = "text",
                            importance_score: int = 1, expires_at: datetime = None) -> Dict[str, Any]:
        """Atualiza contexto do agente"""
        try:
            # Verificar se já existe
            existing = self.client.table("agent_context")\
                .select("id")\
                .eq("session_id", session_id)\
                .eq("agent_name", agent_name)\
                .eq("context_key", context_key)\
                .execute()
            
            data = {
                "context_value": context_value,
                "context_type": context_type,
                "importance_score": importance_score,
                "updated_at": datetime.now().isoformat()
            }
            
            if expires_at:
                data["expires_at"] = expires_at.isoformat()
            
            if existing.data:
                # Atualizar existente
                result = self.client.table("agent_context")\
                    .update(data)\
                    .eq("id", existing.data[0]["id"])\
                    .execute()
            else:
                # Criar novo
                data.update({
                    "session_id": session_id,
                    "agent_name": agent_name,
                    "context_key": context_key
                })
                result = self.client.table("agent_context").insert(data).execute()
            
            if result.data:
                logger.info(f"Contexto atualizado para agente {agent_name}")
                return {"success": True, "context_id": result.data[0]["id"]}
            else:
                return {"success": False, "error": "Falha ao atualizar contexto"}
                
        except Exception as e:
            logger.error(f"Erro ao atualizar contexto: {e}")
            return {"success": False, "error": str(e)}
    
    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Obtém contexto completo da sessão"""
        try:
            # Usar função RPC do banco
            result = self.client.rpc("get_session_context", {"session_uuid": session_id}).execute()
            
            if result.data:
                return {"success": True, "context": result.data}
            else:
                return {"success": False, "error": "Falha ao obter contexto"}
                
        except Exception as e:
            logger.error(f"Erro ao obter contexto: {e}")
            return {"success": False, "error": str(e)}
    
    def get_session_messages(self, session_id: str, limit: int = 50) -> Dict[str, Any]:
        """Obtém mensagens da sessão"""
        try:
            result = self.client.table("chat_messages")\
                .select("*")\
                .eq("session_id", session_id)\
                .order("sequence_order")\
                .limit(limit)\
                .execute()
            
            if result.data is not None:
                return {"success": True, "messages": result.data}
            else:
                return {"success": False, "error": "Falha ao obter mensagens"}
                
        except Exception as e:
            logger.error(f"Erro ao obter mensagens: {e}")
            return {"success": False, "error": str(e)}
    
    def get_agent_logs(self, session_id: str, agent_name: str = None, 
                       log_type: str = None, limit: int = 100) -> Dict[str, Any]:
        """Obtém logs dos agentes"""
        try:
            query = self.client.table("agent_logs")\
                .select("*")\
                .eq("session_id", session_id)
            
            if agent_name:
                query = query.eq("agent_name", agent_name)
            
            if log_type:
                query = query.eq("log_type", log_type)
            
            result = query.order("created_at")\
                .limit(limit)\
                .execute()
            
            if result.data is not None:
                return {"success": True, "logs": result.data}
            else:
                return {"success": False, "error": "Falha ao obter logs"}
                
        except Exception as e:
            logger.error(f"Erro ao obter logs: {e}")
            return {"success": False, "error": str(e)}
    
    def get_agent_files(self, session_id: str, agent_name: str = None, 
                       file_type: str = None) -> Dict[str, Any]:
        """Obtém arquivos dos agentes"""
        try:
            query = self.client.table("agent_files")\
                .select("*")\
                .eq("session_id", session_id)
            
            if agent_name:
                query = query.eq("agent_name", agent_name)
            
            if file_type:
                query = query.eq("file_type", file_type)
            
            result = query.order("created_at").execute()
            
            if result.data is not None:
                return {"success": True, "files": result.data}
            else:
                return {"success": False, "error": "Falha ao obter arquivos"}
                
        except Exception as e:
            logger.error(f"Erro ao obter arquivos: {e}")
            return {"success": False, "error": str(e)}
    
    def list_chat_sessions(self, user_id: str = None, status: str = "active", 
                          limit: int = 20) -> Dict[str, Any]:
        """Lista sessões de chat"""
        try:
            query = self.client.table("chat_sessions")\
                .select("*")\
                .eq("status", status)
            
            if user_id:
                query = query.eq("user_id", user_id)
            
            result = query.order("last_activity", desc=True)\
                .limit(limit)\
                .execute()
            
            if result.data is not None:
                return {"success": True, "sessions": result.data}
            else:
                return {"success": False, "error": "Falha ao listar sessões"}
                
        except Exception as e:
            logger.error(f"Erro ao listar sessões: {e}")
            return {"success": False, "error": str(e)}
    
    def close_session(self, session_id: str) -> Dict[str, Any]:
        """Fecha uma sessão de chat"""
        try:
            result = self.client.table("chat_sessions")\
                .update({"status": "inactive", "updated_at": datetime.now().isoformat()})\
                .eq("id", session_id)\
                .execute()
            
            if result.data:
                logger.info(f"Sessão {session_id} fechada")
                return {"success": True}
            else:
                return {"success": False, "error": "Falha ao fechar sessão"}
                
        except Exception as e:
            logger.error(f"Erro ao fechar sessão: {e}")
            return {"success": False, "error": str(e)}
    
    def cleanup_old_sessions(self, days_old: int = 30) -> Dict[str, Any]:
        """Limpa sessões antigas"""
        try:
            result = self.client.rpc("cleanup_old_sessions", {"days_old": days_old}).execute()
            
            if result.data is not None:
                deleted_count = result.data
                logger.info(f"{deleted_count} sessões antigas removidas")
                return {"success": True, "deleted_count": deleted_count}
            else:
                return {"success": False, "error": "Falha ao limpar sessões"}
                
        except Exception as e:
            logger.error(f"Erro ao limpar sessões: {e}")
            return {"success": False, "error": str(e)}

# Instância global do cliente
supabase_client = None

def get_supabase_client() -> NTEXSupabaseClient:
    """Retorna instância global do cliente Supabase"""
    global supabase_client
    if supabase_client is None:
        supabase_client = NTEXSupabaseClient()
    return supabase_client
