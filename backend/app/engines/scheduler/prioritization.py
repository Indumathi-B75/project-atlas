
from collections.abc import Iterable

from app.models.task import Task


PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}

VALID_STATUSES = {
    "pending",
    "in_progress",
    "completed",
}


def prioritize_tasks(tasks: Iterable[Task]) -> list[Task]:
    """
    Rank eligible tasks deterministically.

    Rules:
    1. Exclude completed tasks.
    2. Rank high priority before medium and low.
    3. Within the same priority, earlier deadlines come first.
    4. Tasks without deadlines come last within their priority.
    5. Preserve input order when all ranking fields are equal.
    """

    eligible_tasks = []

    for task in tasks:
        if task.status not in VALID_STATUSES:
            raise ValueError(f"Invalid task status: {task.status}")

        if task.status == "completed":
            continue

        if task.priority not in PRIORITY_ORDER:
            raise ValueError(f"Invalid task priority: {task.priority}")

        if task.due_at is not None:
            if (
                task.due_at.tzinfo is None
                or task.due_at.utcoffset() is None
            ):
                raise ValueError(
                    f"Task {task.id} has a timezone-naive deadline"
                )

        eligible_tasks.append(task)

    return sorted(
        eligible_tasks,
        key=lambda task: (
            PRIORITY_ORDER[task.priority],
            task.due_at is None,
            task.due_at,
        ),
    )
