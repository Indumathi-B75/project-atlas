
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from app.engines.scheduler.prioritization import prioritize_tasks
from app.models.task import Task


IST = ZoneInfo("Asia/Kolkata")


def make_task(
    title,
    priority="medium",
    status="pending",
    due_at=None,
    duration=None,
):
    return Task(
        title=title,
        priority=priority,
        status=status,
        due_at=due_at,
        estimated_duration_minutes=duration,
    )


def test_high_priority_ranks_before_medium_and_low():
    tasks = [
        make_task("Low task", priority="low"),
        make_task("Medium task", priority="medium"),
        make_task("High task", priority="high"),
    ]

    result = prioritize_tasks(tasks)

    assert [task.title for task in result] == [
        "High task",
        "Medium task",
        "Low task",
    ]


def test_earlier_deadline_ranks_first_within_same_priority():
    tasks = [
        make_task(
            "Next week",
            due_at=datetime(2026, 11, 24, 10, tzinfo=IST),
        ),
        make_task(
            "Tomorrow",
            due_at=datetime(2026, 11, 18, 10, tzinfo=IST),
        ),
    ]

    result = prioritize_tasks(tasks)

    assert [task.title for task in result] == [
        "Tomorrow",
        "Next week",
    ]


def test_tasks_without_deadline_rank_after_tasks_with_deadline():
    tasks = [
        make_task("No deadline"),
        make_task(
            "Has deadline",
            due_at=datetime(2026, 11, 20, 10, tzinfo=IST),
        ),
    ]

    result = prioritize_tasks(tasks)

    assert [task.title for task in result] == [
        "Has deadline",
        "No deadline",
    ]


def test_completed_tasks_are_excluded():
    tasks = [
        make_task("Pending task"),
        make_task("Completed task", status="completed"),
    ]

    result = prioritize_tasks(tasks)

    assert [task.title for task in result] == ["Pending task"]


def test_in_progress_tasks_are_included():
    tasks = [
        make_task("In progress", status="in_progress"),
        make_task("Pending"),
    ]

    result = prioritize_tasks(tasks)

    assert len(result) == 2


def test_same_priority_and_deadline_preserve_input_order():
    deadline = datetime(2026, 11, 20, 10, tzinfo=IST)

    tasks = [
        make_task("First", due_at=deadline),
        make_task("Second", due_at=deadline),
    ]

    result = prioritize_tasks(tasks)

    assert [task.title for task in result] == [
        "First",
        "Second",
    ]


def test_invalid_status_is_rejected():
    tasks = [
        make_task("Invalid task", status="cancelled"),
    ]

    with pytest.raises(ValueError, match="Invalid task status"):
        prioritize_tasks(tasks)


def test_invalid_priority_is_rejected():
    tasks = [
        make_task("Invalid task", priority="urgent"),
    ]

    with pytest.raises(ValueError, match="Invalid task priority"):
        prioritize_tasks(tasks)


def test_naive_deadline_is_rejected():
    tasks = [
        make_task(
            "Invalid deadline",
            due_at=datetime(2026, 11, 20, 10),
        ),
    ]

    with pytest.raises(ValueError, match="timezone-naive deadline"):
        prioritize_tasks(tasks)


def test_duration_does_not_change_priority_order():
    tasks = [
        make_task("Short task", priority="high", duration=30),
        make_task("Long task", priority="high", duration=240),
    ]

    result = prioritize_tasks(tasks)

    assert [task.title for task in result] == [
        "Short task",
        "Long task",
    ]
