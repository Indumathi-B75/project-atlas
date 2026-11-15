
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Commitment(Base):
    """Database model for fixed commitments managed by Project ATLAS."""

    __tablename__ = "commitments"

    __table_args__ = (
        CheckConstraint(
            "start_at < end_at",
            name="ck_commitments_valid_time_range",
        ),
        CheckConstraint(
            "recurrence_type IN ('one_time', 'weekly')",
            name="ck_commitments_valid_recurrence_type",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    recurrence_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="one_time",
        server_default="one_time",
    )

    days_of_week: Mapped[list[int] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="Asia/Kolkata",
        server_default="Asia/Kolkata",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
