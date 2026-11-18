"""
Schémas Pydantic stricts pour le domaine Task.
Modèles étanches : validation à la frontière, pas de fuite de types faibles.
"""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, ConfigDict


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskCreate(BaseModel):
    """Payload de création – strict, pas d'id fourni par le client."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(..., min_length=3, max_length=200, examples=["Implémenter l'architecture senior"])
    description: Optional[str] = Field(None, max_length=2000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty_after_strip(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Le titre ne peut pas être vide ou uniquement des espaces")
        return v

    @field_validator("due_date")
    @classmethod
    def due_date_not_in_past(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v < datetime.now(v.tzinfo):
            raise ValueError("La date d'échéance ne peut pas être dans le passé")
        return v


class TaskUpdateStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: TaskStatus


class Task(BaseModel):
    """Modèle de domaine / réponse – immuable côté API."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class TaskResponse(Task):
    """Alias explicite pour les réponses HTTP."""
    pass
