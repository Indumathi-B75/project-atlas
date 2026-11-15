
import pytest
from pydantic import ValidationError

from app.schemas.commitment import CommitmentCreate


def valid_commitment(**overrides):
    data = {
        "title": "College",
        "start_at": "2026-11-16T09:00:00+05:30",
        "end_at": "2026-11-16T16:00:00+05:30",
        "recurrence_type": "weekly",
        "days_of_week": [0, 1, 2, 3, 4],
        "timezone": "Asia/Kolkata",
    }

    data.update(overrides)
    return data


def test_valid_weekly_commitment():
    commitment = CommitmentCreate(**valid_commitment())

    assert commitment.title == "College"
    assert commitment.recurrence_type == "weekly"
    assert commitment.days_of_week == [0, 1, 2, 3, 4]


def test_valid_one_time_commitment():
    commitment = CommitmentCreate(
        title="Doctor Appointment",
        start_at="2026-11-18T14:00:00+05:30",
        end_at="2026-11-18T15:00:00+05:30",
    )

    assert commitment.recurrence_type == "one_time"
    assert commitment.days_of_week is None


def test_title_cannot_be_empty():
    with pytest.raises(ValidationError):
        CommitmentCreate(**valid_commitment(title="   "))


def test_naive_datetime_is_rejected():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(
                start_at="2026-11-16T09:00:00"
            )
        )


def test_end_before_start_is_rejected():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(
                start_at="2026-11-16T16:00:00+05:30",
                end_at="2026-11-16T09:00:00+05:30",
            )
        )


def test_weekly_commitment_requires_days():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(days_of_week=None)
        )


def test_one_time_commitment_rejects_weekdays():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            title="Appointment",
            start_at="2026-11-18T14:00:00+05:30",
            end_at="2026-11-18T15:00:00+05:30",
            recurrence_type="one_time",
            days_of_week=[0],
        )


def test_invalid_weekday_is_rejected():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(days_of_week=[0, 7])
        )


def test_duplicate_weekdays_are_rejected():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(days_of_week=[0, 1, 1])
        )


def test_empty_weekdays_are_rejected():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(days_of_week=[])
        )


def test_invalid_timezone_is_rejected():
    with pytest.raises(ValidationError):
        CommitmentCreate(
            **valid_commitment(timezone="Invalid/Timezone")
        )


def test_weekdays_are_sorted():
    commitment = CommitmentCreate(
        **valid_commitment(days_of_week=[4, 2, 0, 3, 1])
    )

    assert commitment.days_of_week == [0, 1, 2, 3, 4]
