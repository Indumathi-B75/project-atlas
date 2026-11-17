from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.task import TaskCreate, TaskUpdate


def test_create_task_with_deadline_and_duration():
    task = TaskCreate(
        title="Complete ATLAS project",
        due_at="2026-11-20T18:00:00+05:30",
        estimated_duration_minutes=120,
    )

    assert task.due_at == datetime.fromisoformat(
        "2026-11-20T18:00:00+05:30"
    )
    assert task.estimated_duration_minutes == 120


def test_create_task_without_optional_scheduling_fields():
    task = TaskCreate(title="Read documentation")

    assert task.due_at is None
    assert task.estimated_duration_minutes is None


def test_reject_naive_deadline():
    with pytest.raises(ValidationError):
        TaskCreate(
            title="Complete assignment",
            due_at="2026-11-20T18:00:00",
        )


@pytest.mark.parametrize("duration", [0, -10])
def test_reject_non_positive_duration(duration):
    with pytest.raises(ValidationError):
        TaskCreate(
            title="Complete assignment",
            estimated_duration_minutes=duration,
        )


def test_update_task_with_deadline_and_duration():
    task = TaskUpdate(
        due_at="2026-11-21T10:00:00+05:30",
        estimated_duration_minutes=90,
    )

    assert task.due_at is not None
    assert task.estimated_duration_minutes == 90


def test_update_task_can_clear_optional_fields():
    task = TaskUpdate(
        due_at=None,
        estimated_duration_minutes=None,
    )

    assert task.due_at is None
    assert task.estimated_duration_minutes is None


def test_reject_naive_deadline_during_update():
    with pytest.raises(ValidationError):
        TaskUpdate(
            due_at="2026-11-20T18:00:00",
        )


def test_reject_zero_duration_during_update():
    with pytest.raises(ValidationError):
        TaskUpdate(estimated_duration_minutes=0)


def test_reject_blank_task_title():
    with pytest.raises(ValidationError):
        TaskCreate(title="   ")


def test_reject_null_required_update_fields():
    with pytest.raises(ValidationError):
        TaskUpdate(status=None)
