#!/usr/bin/env python3
"""
NTEX Backend - API para Agente Gary Bencivenga
Backend FastAPI para interface de chat com IA SDK 5
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager
from enum import Enum
import hashlib
import json
import gc
import tracemalloc

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar agente Gary Bencivenga
try:
    import sys
    from pathlib import Path

    # Adicionar o diretório pai ao sys.path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    from agents.copywriter_agent_bencivenga import NTEXCopywriterAgentBencivenga
    gary_agent = NTEXCopywriterAgentBencivenga()
    logger.info("✅ Agente Gary Bencivenga carregado com sucesso")
except Exception as e:
    logger.error(f"❌ Erro ao carregar agente Gary: {e}")
    gary_agent = None

# Configurações do banco de dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "ntex_db"),
    "user": os.getenv("DB_USER", "ntex_user"),
    "password": os.getenv("DB_PASSWORD", "ntex_password")
}

# Classes de erro personalizadas
class ErrorCode(str, Enum):
    DATABASE_ERROR = "DATABASE_ERROR"
    AGENT_ERROR = "AGENT_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    STREAMING_ERROR = "STREAMING_ERROR"
    SESSION_ERROR = "SESSION_ERROR"
    RATE_LIMIT_ERROR = "RATE_LIMIT_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"

class GaryAgentError(Exception):
    """Exceção base para erros do sistema Gary Bencivenga"""

    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
                 status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class DatabaseError(GaryAgentError):
    """Erro relacionado ao banco de dados"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.DATABASE_ERROR, 500, details)

class AgentUnavailableError(GaryAgentError):
    """Erro quando o agente não está disponível"""

    def __init__(self, message: str = "Agente Gary não está disponível"):
        super().__init__(message, ErrorCode.AGENT_ERROR, 503)

class ValidationError(GaryAgentError):
    """Erro de validação de entrada"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.VALIDATION_ERROR, 400, details)

class StreamingError(GaryAgentError):
    """Erro relacionado ao streaming"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.STREAMING_ERROR, 500, details)

# Modelos de resposta de erro
class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    web_search: Optional[bool] = False
    stream: Optional[bool] = False

class SessionRequest(BaseModel):
    session_name: Optional[str] = None

# Gerenciamento de conexões do banco com pooling
class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.pool_config = {
            "minconn": int(os.getenv("DB_POOL_MIN", "2")),
            "maxconn": int(os.getenv("DB_POOL_MAX", "10")),
            **DB_CONFIG
        }

    def initialize_pool(self):
        """Inicializa o pool de conexões"""
        if not self.pool:
            try:
                self.pool = SimpleConnectionPool(
                    minconn=self.pool_config["minconn"],
                    maxconn=self.pool_config["maxconn"],
                    **DB_CONFIG
                )
                logger.info(f"✅ Pool de conexões PostgreSQL inicializado (min: {self.pool_config['minconn']}, max: {self.pool_config['maxconn']})")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar pool de conexões: {e}")
                raise

    def get_connection(self):
        """Obtém uma conexão do pool"""
        if not self.pool:
            self.initialize_pool()

        try:
            conn = self.pool.getconn()
            # Configurar cursor factory para a conexão
            with conn.cursor() as cursor:
                cursor.execute("SET TIME ZONE 'UTC'")
            logger.debug("🔗 Conexão obtida do pool")
            return conn
        except Exception as e:
            logger.error(f"❌ Erro ao obter conexão do pool: {e}")
            raise DatabaseError(f"Erro ao obter conexão do banco: {str(e)}", {"pool_stats": self.get_pool_stats()})

    def return_connection(self, conn):
        """Retorna uma conexão ao pool"""
        if self.pool and conn:
            try:
                self.pool.putconn(conn)
                logger.debug("🔄 Conexão retornada ao pool")
            except Exception as e:
                logger.error(f"❌ Erro ao retornar conexão ao pool: {e}")

    def close_all(self):
        """Fecha todas as conexões do pool"""
        if self.pool:
            try:
                self.pool.closeall()
                logger.info("🔌 Todas as conexões do pool fechadas")
            except Exception as e:
                logger.error(f"❌ Erro ao fechar pool: {e}")

    def get_pool_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do pool de conexões"""
        if not self.pool:
            return {"status": "not_initialized"}

        return {
            "min_connections": self.pool_config["minconn"],
            "max_connections": self.pool_config["maxconn"],
            "available_connections": len(self.pool._pool) if hasattr(self.pool, '_pool') else 0,
            "used_connections": self.pool._rused if hasattr(self.pool, '_rused') else 0,
            "waiting_requests": len(self.pool._wait_queue) if hasattr(self.pool, '_wait_queue') else 0
        }

# Classe de métricas básicas
class PerformanceMetrics:
    """Métricas básicas de performance do sistema"""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0
        self.response_times = []
        self.start_time = datetime.now()

    def record_request(self, response_time_ms: float, success: bool = True):
        """Registra uma requisição"""
        self.request_count += 1
        if not success:
            self.error_count += 1

        self.total_response_time += response_time_ms
        self.response_times.append(response_time_ms)

        # Manter apenas as últimas 1000 medições
        if len(self.response_times) > 1000:
            self.response_times.pop(0)

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas atuais"""
        if not self.response_times:
            return {
                "requests_total": self.request_count,
                "errors_total": self.error_count,
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
                "p50_response_time": 0,
                "p95_response_time": 0,
                "p99_response_time": 0,
                "avg_response_time": 0,
                "error_rate": 0
            }

        sorted_times = sorted(self.response_times)
        p50 = sorted_times[int(len(sorted_times) * 0.5)]
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]
        avg = self.total_response_time / len(self.response_times)
        error_rate = (self.error_count / self.request_count) * 100 if self.request_count > 0 else 0

        return {
            "requests_total": self.request_count,
            "errors_total": self.error_count,
            "uptime_seconds": round((datetime.now() - self.start_time).total_seconds(), 2),
            "p50_response_time_ms": round(p50, 2),
            "p95_response_time_ms": round(p95, 2),
            "p99_response_time_ms": round(p99, 2),
            "avg_response_time_ms": round(avg, 2),
            "error_rate_percent": round(error_rate, 2)
        }

# Classe de cache inteligente
class SmartCache:
    """Cache inteligente em memória com TTL e LRU eviction"""

    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.cache = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.access_order = []

    def _generate_key(self, *args, **kwargs) -> str:
        """Gera chave única para cache baseada nos argumentos"""
        key_data = {
            "args": args,
            "kwargs": kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _is_expired(self, entry: Dict) -> bool:
        """Verifica se entrada do cache expirou"""
        return datetime.now() > entry["expires_at"]

    def _evict_if_needed(self):
        """Remove entradas expiradas e aplica LRU se necessário"""
        # Remover entradas expiradas
        expired_keys = [k for k, v in self.cache.items() if self._is_expired(v)]
        for key in expired_keys:
            del self.cache[key]
            if key in self.access_order:
                self.access_order.remove(key)

        # Aplicar LRU se ainda estiver acima do limite
        while len(self.cache) >= self.max_size and self.access_order:
            lru_key = self.access_order.pop(0)
            if lru_key in self.cache:
                del self.cache[lru_key]

    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        if key in self.cache:
            entry = self.cache[key]
            if not self._is_expired(entry):
                # Atualizar ordem de acesso para LRU
                if key in self.access_order:
                    self.access_order.remove(key)
                self.access_order.append(key)
                return entry["value"]
            else:
                # Remover entrada expirada
                del self.cache[key]
                if key in self.access_order:
                    self.access_order.remove(key)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Define valor no cache"""
        self._evict_if_needed()

        expires_at = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
        self.cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": datetime.now()
        }

        # Adicionar à ordem de acesso
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

    def delete(self, key: str):
        """Remove entrada do cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.access_order:
            self.access_order.remove(key)

    def clear(self):
        """Limpa todo o cache"""
        self.cache.clear()
        self.access_order.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        total_entries = len(self.cache)
        expired_entries = sum(1 for v in self.cache.values() if self._is_expired(v))

        return {
            "total_entries": total_entries,
            "active_entries": total_entries - expired_entries,
            "expired_entries": expired_entries,
            "max_size": self.max_size,
            "hit_rate_estimate": 0,  # Seria calculado com métricas adicionais
            "memory_usage_estimate_mb": round(len(json.dumps(self.cache).encode()) / 1024 / 1024, 2)
        }

# Instâncias globais
db_manager = DatabaseManager()
performance_metrics = PerformanceMetrics()
response_cache = SmartCache(max_size=500, default_ttl=300)  # 5 minutos TTL

# Classe de profiling de memória
class MemoryProfiler:
    """Profiler de memória para detectar leaks e otimizar uso de recursos"""

    def __init__(self):
        self.tracemalloc_started = False
        self.baseline_snapshot = None
        self.memory_history = []
        self.gc_thresholds = (700, 10, 10)  # Thresholds originais do GC

    def start_profiling(self):
        """Inicia profiling de memória"""
        if not self.tracemalloc_started:
            tracemalloc.start()
            self.tracemalloc_started = True
            # Criar snapshot baseline
            self.baseline_snapshot = tracemalloc.take_snapshot()
            logger.info("🔍 Memory profiling iniciado")

    def stop_profiling(self):
        """Para profiling de memória"""
        if self.tracemalloc_started:
            tracemalloc.stop()
            self.tracemalloc_started = False
            logger.info("🔍 Memory profiling parado")

    def get_memory_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas de memória"""
        try:
            import psutil
            process = psutil.Process()

            stats = {
                "process_memory": {
                    "rss_mb": round(process.memory_info().rss / 1024 / 1024, 2),
                    "vms_mb": round(process.memory_info().vms / 1024 / 1024, 2),
                    "percent": round(process.memory_percent(), 2)
                },
                "system_memory": {
                    "total_mb": round(psutil.virtual_memory().total / 1024 / 1024, 2),
                    "available_mb": round(psutil.virtual_memory().available / 1024 / 1024, 2),
                    "used_mb": round(psutil.virtual_memory().used / 1024 / 1024, 2),
                    "percent": psutil.virtual_memory().percent
                },
                "garbage_collector": {
                    "collections": dict(zip(['gen0', 'gen1', 'gen2'], gc.get_count())),
                    "objects": gc.get_count()[0],
                    "thresholds": dict(zip(['gen0', 'gen1', 'gen2'], gc.get_threshold()))
                }
            }

            # Adicionar stats do tracemalloc se estiver ativo
            if self.tracemalloc_started:
                current_snapshot = tracemalloc.take_snapshot()

                # Comparar com baseline
                if self.baseline_snapshot:
                    stats_diff = current_snapshot.compare_to(self.baseline_snapshot, 'lineno')
                    stats["tracemalloc"] = {
                        "current_mb": round(tracemalloc.get_traced_memory()[0] / 1024 / 1024, 2),
                        "peak_mb": round(tracemalloc.get_traced_memory()[1] / 1024 / 1024, 2),
                        "baseline_diff_mb": round(sum(stat.size_diff for stat in stats_diff[:10]) / 1024 / 1024, 2),
                        "top_allocators": [
                            {
                                "file": stat.traceback[0].filename,
                                "line": stat.traceback[0].lineno,
                                "size_mb": round(stat.size / 1024 / 1024, 2),
                                "count": stat.count
                            }
                            for stat in stats_diff[:5]
                        ]
                    }

            # Registrar no histórico
            self.memory_history.append({
                "timestamp": datetime.now(),
                "stats": stats
            })

            # Manter apenas as últimas 50 medições
            if len(self.memory_history) > 50:
                self.memory_history.pop(0)

            return stats

        except Exception as e:
            logger.warning(f"Erro ao coletar estatísticas de memória: {e}")
            return {"error": str(e)}

    def detect_memory_leaks(self) -> Dict[str, Any]:
        """Detecta possíveis memory leaks"""
        if not self.memory_history or len(self.memory_history) < 5:
            return {"status": "insufficient_data"}

        # Analisar tendência de crescimento de memória
        recent_stats = self.memory_history[-5:]
        memory_values = [stat["stats"]["process_memory"]["rss_mb"] for stat in recent_stats]

        # Calcular tendência linear
        if len(memory_values) >= 2:
            trend = (memory_values[-1] - memory_values[0]) / len(memory_values)

            # Verificar se há crescimento consistente
            growing_trend = all(memory_values[i] <= memory_values[i+1] for i in range(len(memory_values)-1))

            return {
                "memory_trend_mb_per_measurement": round(trend, 2),
                "consistent_growth": growing_trend,
                "current_memory_mb": memory_values[-1],
                "min_memory_mb": min(memory_values),
                "max_memory_mb": max(memory_values),
                "leak_detected": growing_trend and trend > 1.0,  # Crescimento > 1MB por medição
                "recommendations": [
                    "Verificar se objetos estão sendo liberados corretamente",
                    "Considerar usar weakref para referências circulares",
                    "Monitorar crescimento do cache",
                    "Verificar se GC está sendo executado regularmente"
                ] if growing_trend and trend > 1.0 else []
            }

        return {"status": "analysis_pending"}

    def force_garbage_collection(self):
        """Força coleta de lixo"""
        collected = gc.collect()
        logger.info(f"🗑️ Garbage collection forçado: {collected} objetos coletados")
        return {"objects_collected": collected, "collections_per_gen": gc.get_count()}

    def optimize_memory(self) -> Dict[str, Any]:
        """Executa otimizações de memória"""
        results = {
            "garbage_collection": self.force_garbage_collection(),
            "cache_cleanup": {
                "cache_cleared": True,
                "cache_stats_before": response_cache.get_stats()
            },
            "memory_stats_after": self.get_memory_stats()
        }

        # Limpar cache se estiver muito grande
        cache_stats = response_cache.get_stats()
        if cache_stats["active_entries"] > cache_stats["max_size"] * 0.8:
            response_cache.clear()
            results["cache_cleanup"]["cache_cleared"] = True
            logger.info("🧹 Cache de resposta limpo devido ao alto uso")

        return results

# Instância global do profiler de memória
memory_profiler = MemoryProfiler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        db_manager.initialize_pool()
        # Iniciar profiling de memória
        memory_profiler.start_profiling()
        logger.info("🚀 Backend NTEX iniciado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro no startup: {e}")

    yield

    # Shutdown
    memory_profiler.stop_profiling()
    db_manager.close_all()

# Criar aplicação FastAPI
app = FastAPI(
    title="NTEX Backend - Gary Bencivenga Agent",
    description="API para interface de chat com o agente Gary Bencivenga",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de métricas
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware para coletar métricas de performance"""
    import time

    start_time = time.time()

    try:
        response = await call_next(request)
        response_time = (time.time() - start_time) * 1000  # em ms

        # Registrar métrica de sucesso
        performance_metrics.record_request(response_time, success=True)

        return response

    except Exception as e:
        response_time = (time.time() - start_time) * 1000  # em ms

        # Registrar métrica de erro
        performance_metrics.record_request(response_time, success=False)

        # Re-raise a exception
        raise

# Handler global de exceções
@app.exception_handler(GaryAgentError)
async def gary_agent_exception_handler(request, exc: GaryAgentError):
    """Handler para exceções personalizadas do Gary Agent"""
    import uuid
    request_id = str(uuid.uuid4())[:8]

    logger.error(f"[{request_id}] {exc.error_code}: {exc.message}", extra={
        "request_id": request_id,
        "error_code": exc.error_code,
        "status_code": exc.status_code,
        "details": exc.details,
        "url": str(request.url),
        "method": request.method
    })

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.message,
            code=exc.error_code,
            details=exc.details,
            timestamp=datetime.now(),
            request_id=request_id
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handler para exceções gerais não tratadas"""
    import uuid
    request_id = str(uuid.uuid4())[:8]

    logger.error(f"[{request_id}] Erro não tratado: {str(exc)}", extra={
        "request_id": request_id,
        "error_type": type(exc).__name__,
        "url": str(request.url),
        "method": request.method
    }, exc_info=True)

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Erro interno do servidor",
            code=ErrorCode.INTERNAL_ERROR,
            details={"original_error": str(exc)},
            timestamp=datetime.now(),
            request_id=request_id
        ).dict()
    )

class ChatSessionManager:
    """Gerenciador de sessões de chat"""

    def __init__(self):
        self.active_sessions = {}

    def create_session(self, session_name: str = None) -> str:
        """Cria nova sessão de chat"""
        import uuid
        session_id = str(uuid.uuid4())

        if not session_name:
            session_name = f"Conversa {session_id[-8:]}"

        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO chat_sessions (session_id, session_name)
                    VALUES (%s, %s)
                    RETURNING id
                """, (session_id, session_name))

                conn.commit()

            logger.info(f"📝 Nova sessão criada: {session_id}")
            return session_id
        finally:
            db_manager.return_connection(conn)

    def get_session_messages(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Obtém mensagens de uma sessão com cache inteligente"""
        cache_key = f"session_messages:{session_id}:{limit}"

        # Tentar obter do cache primeiro
        cached_result = response_cache.get(cache_key)
        if cached_result:
            logger.debug(f"✅ Cache hit: get_session_messages for {session_id}")
            return cached_result

        # Cache miss - executar query
        logger.debug(f"❌ Cache miss: get_session_messages for {session_id}")
        conn = db_manager.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Query otimizada com JOIN e informações da sessão
                cursor.execute("""
                    SELECT
                        cm.id,
                        cm.role,
                        cm.content,
                        cm.agent_name,
                        cm.metadata,
                        cm.created_at,
                        cs.session_name,
                        cs.created_at as session_created_at
                    FROM chat_messages cm
                    JOIN chat_sessions cs ON cm.session_id = cs.session_id
                    WHERE cm.session_id = %s
                    ORDER BY cm.created_at ASC
                    LIMIT %s
                """, (session_id, limit))

                messages = cursor.fetchall()

            # Converter para formato esperado pelo frontend
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "id": msg["id"],
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["created_at"].isoformat(),
                    "agent": msg["agent_name"],
                    "metadata": msg["metadata"] or {},
                    "session_name": msg["session_name"]
                })

            # Cachear resultado por 1 minuto
            response_cache.set(cache_key, formatted_messages, ttl=60)

            return formatted_messages
        finally:
            db_manager.return_connection(conn)

    def save_message(self, session_id: str, role: str, content: str,
                    agent_name: str = None, metadata: Dict = None):
        """Salva mensagem no banco e invalida cache"""
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO chat_messages (session_id, role, content, agent_name, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                """, (session_id, role, content, agent_name, json.dumps(metadata or {})))

                # Atualizar timestamp da sessão
                cursor.execute("""
                    UPDATE chat_sessions
                    SET updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = %s
                """, (session_id,))

                conn.commit()

            # Invalidar cache relacionado a esta sessão
            response_cache.delete(f"session_messages:{session_id}:50")  # Limite padrão
            response_cache.delete(f"session_messages:{session_id}:20")  # Limite menor
            response_cache.delete(f"session_messages:{session_id}:100")  # Limite maior
            response_cache.delete("all_sessions")  # Lista de todas as sessões

            logger.info(f"💾 Mensagem salva na sessão {session_id} (cache invalidado)")
        finally:
            db_manager.return_connection(conn)

    def get_all_sessions(self) -> List[Dict]:
        """Obtém todas as sessões ativas com cache inteligente"""
        cache_key = "all_sessions"

        # Tentar obter do cache primeiro
        cached_result = response_cache.get(cache_key)
        if cached_result:
            logger.debug("✅ Cache hit: get_all_sessions")
            return cached_result

        # Cache miss - executar query
        logger.debug("❌ Cache miss: get_all_sessions")
        conn = db_manager.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Query otimizada com estatísticas agregadas
                cursor.execute("""
                    SELECT
                        cs.session_id,
                        cs.session_name,
                        cs.created_at,
                        cs.updated_at,
                        COUNT(cm.id) as message_count,
                        MAX(cm.created_at) as last_message_at,
                        MIN(cm.created_at) as first_message_at
                    FROM chat_sessions cs
                    LEFT JOIN chat_messages cm ON cs.session_id = cm.session_id
                    GROUP BY cs.session_id, cs.session_name, cs.created_at, cs.updated_at
                    ORDER BY cs.updated_at DESC
                """)

                sessions = cursor.fetchall()

            result = [{
                "id": session["session_id"],
                "session_name": session["session_name"],
                "status": "active",
                "last_activity": session["updated_at"].isoformat(),
                "message_count": session["message_count"] or 0,
                "last_message_at": session["last_message_at"].isoformat() if session["last_message_at"] else None,
                "first_message_at": session["first_message_at"].isoformat() if session["first_message_at"] else None,
                "duration_days": round((session["updated_at"] - session["created_at"]).total_seconds() / 86400, 1) if session["updated_at"] and session["created_at"] else 0
            } for session in sessions]

            # Cachear resultado por 2 minutos
            response_cache.set(cache_key, result, ttl=120)

            return result
        finally:
            db_manager.return_connection(conn)

# Instância global do gerenciador de sessões
session_manager = ChatSessionManager()

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "🚀 NTEX Backend - Gary Bencivenga Agent",
        "version": "1.0.0",
        "status": "online",
        "agent_status": "active" if gary_agent else "inactive"
    }

@app.get("/health")
async def health_check():
    """Verificação básica de saúde do sistema"""
    try:
        # Verificar conexão com banco
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "healthy"

            agent_status = "active" if gary_agent else "inactive"

            return {
                "status": "healthy",
                "database": db_status,
                "agent": agent_status,
                "timestamp": datetime.now().isoformat()
            }
        finally:
            db_manager.return_connection(conn)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/health/detailed")
async def detailed_health_check():
    """Verificação detalhada de saúde do sistema"""
    import psutil
    import time

    start_time = time.time()
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "performance": {},
        "version": "1.0.0"
    }

    try:
        # Verificar banco de dados
        db_start = time.time()
        conn = db_manager.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as session_count FROM chat_sessions")
                session_count = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) as message_count FROM chat_messages")
                message_count = cursor.fetchone()[0]

                cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database())) as db_size")
                db_size = cursor.fetchone()[0]

            health_data["checks"]["database"] = {
                "status": "healthy",
                "response_time_ms": round((time.time() - db_start) * 1000, 2),
                "sessions_count": session_count,
                "messages_count": message_count,
                "database_size": db_size,
                "pool_stats": db_manager.get_pool_stats()
            }
        finally:
            db_manager.return_connection(conn)

    except Exception as e:
        health_data["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e),
            "response_time_ms": round((time.time() - db_start) * 1000, 2)
        }
        health_data["status"] = "degraded"

    try:
        # Verificar agente
        agent_start = time.time()
        if gary_agent:
            health_data["checks"]["agent"] = {
                "status": "healthy",
                "response_time_ms": round((time.time() - agent_start) * 1000, 2),
                "agent_name": "Gary Bencivenga"
            }
        else:
            health_data["checks"]["agent"] = {
                "status": "unhealthy",
                "error": "Agente não carregado",
                "response_time_ms": round((time.time() - agent_start) * 1000, 2)
            }
            health_data["status"] = "degraded"
    except Exception as e:
        health_data["checks"]["agent"] = {
            "status": "unhealthy",
            "error": str(e),
            "response_time_ms": round((time.time() - agent_start) * 1000, 2)
        }
        health_data["status"] = "degraded"

    # Métricas de sistema
    try:
        health_data["performance"] = {
            "memory_usage_mb": round(psutil.virtual_memory().used / 1024 / 1024, 2),
            "memory_percent": psutil.virtual_memory().percent,
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "total_response_time_ms": round((time.time() - start_time) * 1000, 2)
        }
    except Exception as e:
        logger.warning(f"Erro ao coletar métricas de sistema: {e}")

    # Verificar se sistema está degradado
    if health_data["status"] == "degraded":
        health_data["recommendations"] = [
            "Verificar conexão com banco de dados",
            "Verificar se agente Gary está carregado corretamente",
            "Verificar recursos do sistema"
        ]

    return health_data

@app.post("/cache/clear")
async def clear_cache():
    """Limpa todo o cache de resposta"""
    try:
        response_cache.clear()
        return {
            "success": True,
            "message": "Cache de resposta limpo com sucesso",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao limpar cache: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao limpar cache: {str(e)}")

@app.get("/metrics")
async def get_metrics():
    """Retorna métricas de performance do sistema"""
    try:
        metrics = performance_metrics.get_metrics()
        metrics["database_pool"] = db_manager.get_pool_stats()
        metrics["response_cache"] = response_cache.get_stats()
        metrics["memory_profiler"] = memory_profiler.get_memory_stats()
        metrics["memory_leak_detection"] = memory_profiler.detect_memory_leaks()

        # Adicionar informações do sistema
        import psutil
        metrics["system"] = {
            "memory_usage_mb": round(psutil.virtual_memory().used / 1024 / 1024, 2),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "disk_usage_percent": psutil.disk_usage('/').percent
        }

        return metrics
    except Exception as e:
        logger.error(f"Erro ao obter métricas: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

@app.get("/memory/stats")
async def get_memory_stats():
    """Retorna estatísticas detalhadas de memória"""
    try:
        stats = memory_profiler.get_memory_stats()
        leak_detection = memory_profiler.detect_memory_leaks()
        return {
            "memory_stats": stats,
            "leak_detection": leak_detection,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas de memória: {e}")
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

@app.post("/memory/optimize")
async def optimize_memory():
    """Executa otimizações de memória"""
    try:
        results = memory_profiler.optimize_memory()
        return {
            "success": True,
            "optimization_results": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro ao otimizar memória: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na otimização de memória: {str(e)}")

@app.post("/memory/gc")
async def force_garbage_collection():
    """Força coleta de lixo manual"""
    try:
        result = memory_profiler.force_garbage_collection()
        return {
            "success": True,
            "garbage_collection": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erro na coleta de lixo: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na coleta de lixo: {str(e)}")

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    """Endpoint principal para chat com Gary Bencivenga"""
    try:
        # Criar ou obter sessão
        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session()
        else:
            # Verificar se a sessão existe, se não existir, criar
            conn = db_manager.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT session_id FROM chat_sessions WHERE session_id = %s", (session_id,))
                    if not cursor.fetchone():
                        session_id = session_manager.create_session(f"Chat {session_id[:8]}")
            finally:
                db_manager.return_connection(conn)

        # Salvar mensagem do usuário
        session_manager.save_message(
            session_id=session_id,
            role="user",
            content=request.message,
            metadata={"web_search": request.web_search}
        )

        # Processar com agente Gary
        if not gary_agent:
            raise AgentUnavailableError()

        if request.stream:
            # Streaming não implementado ainda
            background_tasks.add_task(process_streaming_response, session_id, request.message, request.web_search)
            return {"success": True, "session_id": session_id, "streaming": True}
        else:
            # Resposta síncrona
            response = await process_gary_response(request.message, request.web_search)

            # Salvar resposta do agente
            session_manager.save_message(
                session_id=session_id,
                role="assistant",
                content=response["content"],
                agent_name="Gary Bencivenga",
                metadata={
                    "agent": "Gary Bencivenga",
                    "model_used": response.get("model_used"),
                    "tokens_used": response.get("tokens_used")
                }
            )

            return {
                "success": True,
                "session_id": session_id,
                "response": response["content"],
                "agent": "Gary Bencivenga",
                "tokens_used": response.get("tokens_used", 0),
                "model_used": response.get("model_used", "unknown")
            }

    except Exception as e:
        logger.error(f"Erro no chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/sessions")
async def get_sessions():
    """Obtém lista de sessões de chat"""
    try:
        sessions = session_manager.get_all_sessions()
        return sessions
    except Exception as e:
        logger.error(f"Erro ao obter sessões: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Obtém detalhes de uma sessão específica"""
    try:
        messages = session_manager.get_session_messages(session_id)

        # Mesmo que não haja mensagens, retornamos 200 com lista vazia.
        # Evita 404 no frontend quando a sessão existe mas ainda não tem mensagens.
        return {
            "session_info": {
                "id": session_id,
                "status": "active"
            },
            "recent_messages": messages or [],
            "total_messages": len(messages) if messages else 0
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter sessão: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/api/sessions")
async def create_session(request: SessionRequest):
    """Cria nova sessão de chat"""
    try:
        session_id = session_manager.create_session(request.session_name)
        return {
            "success": True,
            "session_id": session_id,
            "message": "Sessão criada com sucesso"
        }
    except Exception as e:
        logger.error(f"Erro ao criar sessão: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Endpoint SSE para chat em tempo real com Gary Bencivenga"""
    try:
        # Criar ou obter sessão
        session_id = request.session_id
        if not session_id:
            session_id = session_manager.create_session()
        else:
            # Verificar se a sessão existe, se não existir, criar
            conn = db_manager.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT session_id FROM chat_sessions WHERE session_id = %s", (session_id,))
                    if not cursor.fetchone():
                        session_id = session_manager.create_session(f"Chat {session_id[:8]}")
            finally:
                db_manager.return_connection(conn)

        # Salvar mensagem do usuário
        session_manager.save_message(
            session_id=session_id,
            role="user",
            content=request.message,
            metadata={"web_search": request.web_search}
        )

        # Verificar se agente está disponível
        if not gary_agent:
            raise AgentUnavailableError()

        # Retornar resposta de streaming
        return StreamingResponse(
            stream_chat_response(session_id, request.message, request.web_search),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Cache-Control",
            }
        )

    except Exception as e:
        logger.error(f"Erro no endpoint de streaming: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

async def process_gary_response(message: str, web_search: bool = False) -> Dict[str, Any]:
    """Processa mensagem com o agente Gary Bencivenga"""
    try:
        # Usar método de geração de copy do agente
        response = await gary_agent.generate_copy(
            prompt=message,
            copy_type="general",
            max_tokens=2000,
            include_research=web_search
        )

        return {
            "content": response.get("copy", "Erro: resposta vazia"),
            "model_used": response.get("model_used", "unknown"),
            "tokens_used": response.get("tokens_used", 0),
            "methodology": response.get("methodology", "Gary Bencivenga"),
            "scorecard": response.get("scorecard", {})
        }

    except Exception as e:
        logger.error(f"Erro ao processar com Gary: {e}")
        return {
            "content": f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}",
            "error": str(e),
            "model_used": "error",
            "tokens_used": 0
        }

async def stream_chat_response(session_id: str, message: str, web_search: bool):
    """Gera resposta em streaming com Server-Sent Events"""
    try:
        # Evento inicial
        yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"

        # Simular processamento em chunks para demonstração
        # Em produção, isso seria integrado com o agente Gary
        chunks = []
        full_response = ""

        # Processar com agente Gary (simulado por enquanto)
        response = await process_gary_response(message, web_search)
        content = response.get("content", "")

        # Dividir resposta em chunks para streaming
        words = content.split()
        for i, word in enumerate(words):
            chunk = word + " "
            full_response += chunk
            chunks.append(chunk)

            # Enviar chunk via SSE
            data = {
                "type": "chunk",
                "content": chunk,
                "chunk_index": i,
                "total_chunks": len(words),
                "session_id": session_id
            }
            yield f"data: {json.dumps(data)}\n\n"

            # Pequena pausa para simular processamento em tempo real
            await asyncio.sleep(0.05)

        # Salvar resposta completa do agente
        session_manager.save_message(
            session_id=session_id,
            role="assistant",
            content=full_response,
            agent_name="Gary Bencivenga",
            metadata={
                "agent": "Gary Bencivenga",
                "model_used": response.get("model_used"),
                "tokens_used": response.get("tokens_used"),
                "streaming": True
            }
        )

        # Evento de conclusão
        completion_data = {
            "type": "complete",
            "session_id": session_id,
            "total_chunks": len(chunks),
            "full_content": full_response,
            "metadata": {
                "agent": "Gary Bencivenga",
                "model_used": response.get("model_used", "unknown"),
                "tokens_used": response.get("tokens_used", 0),
                "methodology": response.get("methodology", "Gary Bencivenga")
            }
        }
        yield f"data: {json.dumps(completion_data)}\n\n"

    except Exception as e:
        logger.error(f"Erro no streaming: {e}")
        error_data = {
            "type": "error",
            "error": str(e),
            "session_id": session_id
        }
        yield f"data: {json.dumps(error_data)}\n\n"

async def process_streaming_response(session_id: str, message: str, web_search: bool):
    """Processa resposta em streaming (legacy - será removido)"""
    # Esta função será mantida para compatibilidade, mas o streaming agora usa SSE
    pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"🚀 Iniciando servidor FastAPI na porta {port}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
