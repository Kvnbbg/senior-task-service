"""
Service métier – logique isolée, testable sans FastAPI.
Dépendance injectée via constructeur (prêt pour DI).
"""
from typing import List, Optional
from uuid import UUID

from app.repository import TaskRepository
from app.schemas import Task, TaskCreate, TaskStatus


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repo = repository

    def create_task(self, data: TaskCreate) -> Task:
        # Règles métier additionnelles possibles ici (ex: max tasks par user)
        return self._repo.create(data)

    def get_task(self, task_id: UUID) -> Optional[Task]:
        return self._repo.get_by_id(task_id)

    def list_tasks(self) -> List[Task]:
        return self._repo.list_all()

    def change_status(self, task_id: UUID, new_status: TaskStatus) -> Optional[Task]:
        # Exemple de règle : impossible de passer de DONE à TODO
        existing = self._repo.get_by_id(task_id)
        if existing and existing.status == TaskStatus.DONE and new_status == TaskStatus.TODO:
            raise ValueError("Impossible de rouvrir une tâche terminée")
        return self._repo.update_status(task_id, new_status)
