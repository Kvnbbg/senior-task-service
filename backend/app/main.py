"""
Couche API FastAPI – fine, délègue au service.
Typage strict des réponses.
"""
from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.repository import InMemoryTaskRepository, TaskRepository
from app.schemas import TaskCreate, TaskResponse, TaskUpdateStatus
from app.service import TaskService

app = FastAPI(
    title="Senior Task Service",
    description="Brique fonctionnelle avec architecture senior : typage strict, séparation des couches, tests 100%.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton simple pour la démo (en prod : DI container ou Depends avec scope)
_repository = InMemoryTaskRepository()


def get_service() -> TaskService:
    return TaskService(repository=_repository)


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate, service: TaskService = Depends(get_service)) -> TaskResponse:
    task = service.create_task(payload)
    return TaskResponse.model_validate(task)


@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(service: TaskService = Depends(get_service)) -> List[TaskResponse]:
    return [TaskResponse.model_validate(t) for t in service.list_tasks()]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID, service: TaskService = Depends(get_service)) -> TaskResponse:
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return TaskResponse.model_validate(task)


@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
def update_status(
    task_id: UUID,
    payload: TaskUpdateStatus,
    service: TaskService = Depends(get_service),
) -> TaskResponse:
    try:
        task = service.change_status(task_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return TaskResponse.model_validate(task)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "architecture": "senior-layered"}
