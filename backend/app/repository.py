"""
Repository abstrait + implémentation in-memory.
En production : remplacer par SQLAlchemy / PostgreSQL.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.schemas import Task, TaskCreate, TaskStatus, TaskPriority


class TaskRepository(ABC):
    @abstractmethod
    def create(self, data: TaskCreate) -> Task: ...

    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[Task]: ...

    @abstractmethod
    def list_all(self) -> List[Task]: ...

    @abstractmethod
    def update_status(self, task_id: UUID, status: TaskStatus) -> Optional[Task]: ...


class InMemoryTaskRepository(TaskRepository):
    """Implémentation pure pour tests et démo. Thread-safe basique via dict."""

    def __init__(self) -> None:
        self._store: Dict[UUID, Task] = {}

    def create(self, data: TaskCreate) -> Task:
        now = datetime.utcnow()
        task = Task(
            id=uuid4(),
            title=data.title,
            description=data.description,
            status=TaskStatus.TODO,
            priority=data.priority,
            due_date=data.due_date,
            created_at=now,
            updated_at=now,
        )
        self._store[task.id] = task
        return task

    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        return self._store.get(task_id)

    def list_all(self) -> List[Task]:
        return list(self._store.values())

    def update_status(self, task_id: UUID, status: TaskStatus) -> Optional[Task]:
        task = self._store.get(task_id)
        if not task:
            return None
        updated = task.model_copy(update={"status": status, "updated_at": datetime.utcnow()})
        self._store[task_id] = updated
        return updated
