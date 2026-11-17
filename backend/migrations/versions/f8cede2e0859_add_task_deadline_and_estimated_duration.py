"""add task deadline and estimated duration

Revision ID: f8cede2e0859
Revises: 0f0222939fc2
Create Date: 2026-11-16 13:14:16.637694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8cede2e0859'
down_revision: Union[str, Sequence[str], None] = '0f0222939fc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "tasks",
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.add_column(
        "tasks",
        sa.Column("estimated_duration_minutes", sa.Integer(), nullable=True),
    )

    op.create_check_constraint(
        "ck_tasks_positive_estimated_duration",
        "tasks",
        "estimated_duration_minutes IS NULL "
        "OR estimated_duration_minutes > 0",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "ck_tasks_positive_estimated_duration",
        "tasks",
        type_="check",
    )

    op.drop_column("tasks", "estimated_duration_minutes")
    op.drop_column("tasks", "due_at")
