
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models import Commitment, Task


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_create_one_time_commitment(db_session):
    commitment = Commitment(
        title="Doctor Appointment",
        start_at=datetime(2026, 11, 18, 14, 0, tzinfo=timezone.utc),
        end_at=datetime(2026, 11, 18, 15, 0, tzinfo=timezone.utc),
        recurrence_type="one_time",
        timezone="Asia/Kolkata",
    )

    db_session.add(commitment)
    db_session.commit()
    db_session.refresh(commitment)

    assert commitment.id is not None
    assert commitment.title == "Doctor Appointment"
    assert commitment.recurrence_type == "one_time"
    assert commitment.is_active is True


def test_create_weekly_commitment(db_session):
    commitment = Commitment(
        title="College",
        start_at=datetime(2026, 11, 16, 9, 0, tzinfo=timezone.utc),
        end_at=datetime(2026, 11, 16, 16, 0, tzinfo=timezone.utc),
        recurrence_type="weekly",
        days_of_week=[0, 1, 2, 3, 4],
        timezone="Asia/Kolkata",
    )

    db_session.add(commitment)
    db_session.commit()
    db_session.refresh(commitment)

    assert commitment.recurrence_type == "weekly"
    assert commitment.days_of_week == [0, 1, 2, 3, 4]


def test_commitment_default_values(db_session):
    commitment = Commitment(
        title="Study Session",
        start_at=datetime(2026, 11, 16, 10, 0, tzinfo=timezone.utc),
        end_at=datetime(2026, 11, 16, 11, 0, tzinfo=timezone.utc),
    )

    db_session.add(commitment)
    db_session.commit()
    db_session.refresh(commitment)

    assert commitment.recurrence_type == "one_time"
    assert commitment.timezone == "Asia/Kolkata"
    assert commitment.is_active is True
    assert commitment.days_of_week is None


def test_database_rejects_invalid_time_range(db_session):
    commitment = Commitment(
        title="Invalid Commitment",
        start_at=datetime(2026, 11, 16, 16, 0, tzinfo=timezone.utc),
        end_at=datetime(2026, 11, 16, 9, 0, tzinfo=timezone.utc),
    )

    db_session.add(commitment)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()
