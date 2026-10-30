from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TaskStatus = Literal["pending", "in_progress", "completed"]
TaskPriority = Literal["low", "medium", "high"]


class TaskCreate(BaseModel):
    """Validate data submitted when creating a task."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = "pending"
    priority: TaskPriority = "medium"


class TaskUpdate(BaseModel):
    """Validate fields supplied when updating a task."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    @model_validator(mode="after")
    def reject_null_for_required_fields(self):
        for field_name in ("title", "status", "priority"):
            if (
                field_name in self.model_fields_set
                and getattr(self, field_name) is None
            ):
                raise ValueError(f"{field_name} cannot be null")

        return self

class TaskRead(BaseModel):
    """Define the task data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
