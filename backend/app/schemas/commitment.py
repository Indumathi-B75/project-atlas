
from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    field_validator,
    model_validator,
)


RecurrenceType = Literal["one_time", "weekly"]


class CommitmentCreate(BaseModel):
    """Validate data submitted when creating a fixed commitment."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None

    start_at: datetime
    end_at: datetime

    recurrence_type: RecurrenceType = "one_time"

    days_of_week: list[StrictInt] | None = None

    timezone: str = "Asia/Kolkata"

    is_active: bool = True

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("title cannot contain only whitespace")

        return value

    @field_validator("start_at", "end_at")
    @classmethod
    def validate_timezone_aware_datetime(
        cls,
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("datetime must be timezone-aware")

        return value

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError):
            raise ValueError("timezone must be a valid IANA timezone")

        return value

    @field_validator("days_of_week")
    @classmethod
    def validate_days_of_week(
        cls,
        value: list[int] | None,
    ) -> list[int] | None:
        if value is None:
            return value

        if not value:
            raise ValueError("days_of_week cannot be empty")

        if any(day < 0 or day > 6 for day in value):
            raise ValueError(
                "days_of_week values must be between 0 and 6"
            )

        if len(value) != len(set(value)):
            raise ValueError("days_of_week cannot contain duplicates")

        return sorted(value)

    @model_validator(mode="after")
    def validate_commitment(self):
        if self.start_at >= self.end_at:
            raise ValueError("start_at must be earlier than end_at")

        if self.recurrence_type == "weekly":
            if self.days_of_week is None:
                raise ValueError(
                    "weekly commitments require days_of_week"
                )

        elif self.days_of_week is not None:
            raise ValueError(
                "one_time commitments cannot have days_of_week"
            )

        return self


class CommitmentRead(BaseModel):
    """Define commitment data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    start_at: datetime
    end_at: datetime
    recurrence_type: RecurrenceType
    days_of_week: list[int] | None
    timezone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
