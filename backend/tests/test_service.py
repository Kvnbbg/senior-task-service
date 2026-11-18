"""
Tests unitaires du service – 100% des chemins critiques couverts.
Exécuter avec : pytest -v
"""
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app.repository import InMemoryTaskRepository
from app.schemas import TaskCreate, TaskPriority, TaskStatus
from app.service import TaskService


@pytest.fixture
def service() -> TaskService:
    return TaskService(repository=InMemoryTaskRepository())


def test_create_task_success(service: TaskService) -> None:
    data = TaskCreate(
        title="Architecture senior",
        description="Implémenter couches strictes",
        priority=TaskPriority.HIGH,
    )
    task = service.create_task(data)

    assert task.title == "Architecture senior"
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.HIGH
    assert task.id is not None
    assert task.created_at is not None


def test_create_task_title_too_short_raises() -> None:
    with pytest.raises(Exception):  # Pydantic ValidationError
        TaskCreate(title="ab")


def test_create_task_due_date_in_past_raises() -> None:
    past = datetime.utcnow() - timedelta(days=1)
    with pytest.raises(Exception):
        TaskCreate(title="Tâche passée", due_date=past)


def test_list_and_get(service: TaskService) -> None:
    data = TaskCreate(title="Tâche listable")
    created = service.create_task(data)

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == created.id

    fetched = service.get_task(created.id)
    assert fetched is not None
    assert fetched.title == "Tâche listable"

    assert service.get_task(uuid4()) is None


def test_change_status_success(service: TaskService) -> None:
    data = TaskCreate(title="À faire avancer")
    created = service.create_task(data)

    updated = service.change_status(created.id, TaskStatus.IN_PROGRESS)
    assert updated is not None
    assert updated.status == TaskStatus.IN_PROGRESS


def test_cannot_reopen_done_task(service: TaskService) -> None:
    data = TaskCreate(title="Tâche terminée")
    created = service.create_task(data)
    service.change_status(created.id, TaskStatus.DONE)

    with pytest.raises(ValueError, match="Impossible de rouvrir"):
        service.change_status(created.id, TaskStatus.TODO)


def test_update_nonexistent_returns_none(service: TaskService) -> None:
    result = service.change_status(uuid4(), TaskStatus.DONE)
    assert result is None
