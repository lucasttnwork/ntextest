"""
Utilitários compartilhados para os Agentes IA NTEX
Funções e classes comuns usadas por todos os agentes
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Task:
    """Estrutura de dados para tarefas dos agentes"""
    id: str
    type: str
    priority: int  # 1-5, onde 1 é mais alta
    status: str  # pending, in_progress, completed, failed
    created_at: datetime
    assigned_to: str
    description: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None

@dataclass
class ContentItem:
    """Estrutura de dados para itens de conteúdo"""
    id: str
    type: str  # post, story, reel, ad_copy, landing_page
    platform: str  # instagram, google, website
    title: str
    content: str
    metadata: Dict[str, Any]
    status: str  # draft, pending_approval, approved, published
    created_by: str
    created_at: datetime
    published_at: Optional[datetime] = None
    performance_metrics: Optional[Dict[str, Any]] = None

@dataclass
class Campaign:
    """Estrutura de dados para campanhas"""
    id: str
    name: str
    platform: str  # instagram, google_search, google_display
    objective: str  # awareness, consideration, conversion
    budget: float
    status: str  # draft, active, paused, completed
    start_date: datetime
    targeting: Dict[str, Any]
    creatives: List[str]  # IDs dos criativos
    end_date: Optional[datetime] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class TaskManager:
    """Gerenciador de tarefas para coordenação entre agentes"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[str] = []
    
    def create_task(self, task_type: str, description: str, priority: int, 
                   assigned_to: str, input_data: Dict[str, Any]) -> str:
        """Cria uma nova tarefa"""
        task_id = self._generate_task_id()
        task = Task(
            id=task_id,
            type=task_type,
            priority=priority,
            status="pending",
            created_at=datetime.now(),
            assigned_to=assigned_to,
            description=description,
            input_data=input_data
        )
        
        self.tasks[task_id] = task
        self._add_to_queue(task_id)
        logger.info(f"Nova tarefa criada: {task_id} - {description}")
        
        return task_id
    
    def get_next_task(self, agent_name: str) -> Optional[Task]:
        """Obtém a próxima tarefa para um agente específico"""
        for task_id in self.task_queue:
            task = self.tasks[task_id]
            if (task.assigned_to == agent_name and 
                task.status == "pending"):
                return task
        return None
    
    def update_task_status(self, task_id: str, status: str, 
                          output_data: Optional[Dict[str, Any]] = None,
                          error_message: Optional[str] = None) -> bool:
        """Atualiza o status de uma tarefa"""
        if task_id not in self.tasks:
            logger.error(f"Tarefa {task_id} não encontrada")
            return False
        
        task = self.tasks[task_id]
        task.status = status
        
        if output_data:
            task.output_data = output_data
        
        if error_message:
            task.error_message = error_message
        
        if status == "completed":
            task.completed_at = datetime.now()
        
        logger.info(f"Tarefa {task_id} atualizada para status: {status}")
        return True
    
    def _generate_task_id(self) -> str:
        """Gera ID único para tarefa"""
        timestamp = str(int(time.time() * 1000))
        random_suffix = hashlib.md5(timestamp.encode()).hexdigest()[:8]
        return f"task_{timestamp}_{random_suffix}"
    
    def _add_to_queue(self, task_id: str):
        """Adiciona tarefa à fila de prioridade"""
        task = self.tasks[task_id]
        
        # Inserir na posição correta baseada na prioridade
        for i, queued_id in enumerate(self.task_queue):
            queued_task = self.tasks[queued_id]
            if task.priority < queued_task.priority:
                self.task_queue.insert(i, task_id)
                return
        
        # Se não encontrou posição, adiciona ao final
        self.task_queue.append(task_id)

class ContentManager:
    """Gerenciador de conteúdo para controle de qualidade e aprovação"""
    
    def __init__(self):
        self.content_items: Dict[str, ContentItem] = {}
        self.approval_queue: List[str] = []
    
    def create_content(self, content_type: str, platform: str, title: str,
                      content: str, metadata: Dict[str, Any], created_by: str) -> str:
        """Cria novo item de conteúdo"""
        content_id = self._generate_content_id()
        content_item = ContentItem(
            id=content_id,
            type=content_type,
            platform=platform,
            title=title,
            content=content,
            metadata=metadata,
            status="draft",
            created_by=created_by,
            created_at=datetime.now()
        )
        
        self.content_items[content_id] = content_item
        
        # Verificar se precisa de aprovação
        if self._requires_approval(content_type, platform):
            content_item.status = "pending_approval"
            self.approval_queue.append(content_id)
            logger.info(f"Conteúdo {content_id} enviado para aprovação")
        else:
            content_item.status = "approved"
            logger.info(f"Conteúdo {content_id} aprovado automaticamente")
        
        return content_id
    
    def approve_content(self, content_id: str, approved_by: str) -> bool:
        """Aprova um item de conteúdo"""
        if content_id not in self.content_items:
            logger.error(f"Conteúdo {content_id} não encontrado")
            return False
        
        content_item = self.content_items[content_id]
        if content_item.status != "pending_approval":
            logger.warning(f"Conteúdo {content_id} não está pendente de aprovação")
            return False
        
        content_item.status = "approved"
        content_item.metadata["approved_by"] = approved_by
        content_item.metadata["approved_at"] = datetime.now().isoformat()
        
        # Remover da fila de aprovação
        if content_id in self.approval_queue:
            self.approval_queue.remove(content_id)
        
        logger.info(f"Conteúdo {content_id} aprovado por {approved_by}")
        return True
    
    def reject_content(self, content_id: str, rejected_by: str, reason: str) -> bool:
        """Rejeita um item de conteúdo"""
        if content_id not in self.content_items:
            logger.error(f"Conteúdo {content_id} não encontrado")
            return False
        
        content_item = self.content_items[content_id]
        if content_item.status != "pending_approval":
            logger.warning(f"Conteúdo {content_id} não está pendente de aprovação")
            return False
        
        content_item.status = "draft"
        content_item.metadata["rejected_by"] = rejected_by
        content_item.metadata["rejected_at"] = datetime.now().isoformat()
        content_item.metadata["rejection_reason"] = reason
        
        # Remover da fila de aprovação
        if content_id in self.approval_queue:
            self.approval_queue.remove(content_id)
        
        logger.info(f"Conteúdo {content_id} rejeitado por {rejected_by}: {reason}")
        return True
    
    def publish_content(self, content_id: str, published_by: str) -> bool:
        """Marca conteúdo como publicado"""
        if content_id not in self.content_items:
            logger.error(f"Conteúdo {content_id} não encontrado")
            return False
        
        content_item = self.content_items[content_id]
        if content_item.status != "approved":
            logger.warning(f"Conteúdo {content_id} não está aprovado")
            return False
        
        content_item.status = "published"
        content_item.published_at = datetime.now()
        content_item.metadata["published_by"] = published_by
        
        logger.info(f"Conteúdo {content_id} publicado por {published_by}")
        return True
    
    def _generate_content_id(self) -> str:
        """Gera ID único para conteúdo"""
        timestamp = str(int(time.time() * 1000))
        random_suffix = hashlib.md5(timestamp.encode()).hexdigest()[:8]
        return f"content_{timestamp}_{random_suffix}"
    
    def _requires_approval(self, content_type: str, platform: str) -> bool:
        """Verifica se o conteúdo precisa de aprovação manual"""
        from config import get_config
        
        approval_required = get_config("quality", "approval_required")
        auto_approval = get_config("quality", "auto_approval")
        
        # Verificar se é conteúdo que precisa de aprovação
        for approval_type in approval_required:
            if approval_type.lower() in content_type.lower():
                return True
        
        # Verificar se é conteúdo de aprovação automática
        for auto_type in auto_approval:
            if auto_type.lower() in content_type.lower():
                return False
        
        # Por padrão, requer aprovação
        return True

class PerformanceTracker:
    """Rastreador de performance dos agentes"""
    
    def __init__(self):
        self.metrics: Dict[str, List[Dict[str, Any]]] = {}
        self.agent_stats: Dict[str, Dict[str, Any]] = {}
    
    def record_metric(self, agent_name: str, metric_name: str, value: Any, 
                     metadata: Optional[Dict[str, Any]] = None):
        """Registra uma métrica de performance"""
        if agent_name not in self.metrics:
            self.metrics[agent_name] = []
        
        metric_record = {
            "timestamp": datetime.now().isoformat(),
            "metric": metric_name,
            "value": value,
            "metadata": metadata or {}
        }
        
        self.metrics[agent_name].append(metric_record)
        
        # Atualizar estatísticas do agente
        self._update_agent_stats(agent_name, metric_name, value)
    
    def get_agent_performance(self, agent_name: str, 
                             time_window: Optional[timedelta] = None) -> Dict[str, Any]:
        """Obtém métricas de performance de um agente"""
        if agent_name not in self.metrics:
            return {}
        
        metrics = self.metrics[agent_name]
        
        # Filtrar por janela de tempo se especificada
        if time_window:
            cutoff_time = datetime.now() - time_window
            metrics = [
                m for m in metrics 
                if datetime.fromisoformat(m["timestamp"]) > cutoff_time
            ]
        
        # Calcular estatísticas
        performance = {
            "total_operations": len(metrics),
            "metrics_by_type": {},
            "recent_activity": metrics[-10:] if metrics else []
        }
        
        for metric in metrics:
            metric_type = metric["metric"]
            if metric_type not in performance["metrics_by_type"]:
                performance["metrics_by_type"][metric_type] = []
            performance["metrics_by_type"][metric_type].append(metric["value"])
        
        return performance
    
    def _update_agent_stats(self, agent_name: str, metric_name: str, value: Any):
        """Atualiza estatísticas agregadas do agente"""
        if agent_name not in self.agent_stats:
            self.agent_stats[agent_name] = {}
        
        if metric_name not in self.agent_stats[agent_name]:
            self.agent_stats[agent_name][metric_name] = {
                "count": 0,
                "total": 0,
                "min": float('inf'),
                "max": float('-inf'),
                "last_value": None
            }
        
        stats = self.agent_stats[agent_name][metric_name]
        stats["count"] += 1
        stats["last_value"] = value
        
        if isinstance(value, (int, float)):
            stats["total"] += value
            stats["min"] = min(stats["min"], value)
            stats["max"] = max(stats["max"], value)

# Instâncias globais
task_manager = TaskManager()
content_manager = ContentManager()
performance_tracker = PerformanceTracker()

def log_agent_operation(agent_name: str, operation: str, duration: float, 
                        success: bool, metadata: Optional[Dict[str, Any]] = None):
    """Função utilitária para logar operações dos agentes"""
    performance_tracker.record_metric(
        agent_name=agent_name,
        metric_name="operation_duration",
        value=duration,
        metadata={
            "operation": operation,
            "success": success,
            **(metadata or {})
        }
    )
    
    performance_tracker.record_metric(
        agent_name=agent_name,
        metric_name="operation_success_rate",
        value=1.0 if success else 0.0,
        metadata={"operation": operation}
    )
    
    logger.info(f"Agente {agent_name} executou {operation} em {duration:.2f}s - Sucesso: {success}")
