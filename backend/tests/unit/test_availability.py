from datetime import datetime, timedelta, timezone

import pytest

from app.engines.scheduler.availability import (
    calculate_available_intervals,
)


UTC = timezone.utc


def dt(hour: int, day: int = 3) -> datetime:
    return datetime(2026, 11, day, hour, 0, tzinfo=UTC)


def test_calculate_free_intervals_for_normal_day():
    result = calculate_available_intervals(
        dt(7),
        dt(23),
        [
            (dt(9), dt(13)),
            (dt(13), dt(14)),
            (dt(16), dt(17)),
        ],
    )

    assert result == [
        (dt(7), dt(9)),
        (dt(14), dt(16)),
        (dt(17), dt(23)),
    ]


def test_overlapping_commitments_are_merged():
    result = calculate_available_intervals(
        dt(8),
        dt(18),
        [
            (dt(9), dt(13)),
            (dt(12), dt(14)),
        ],
    )

    assert result == [
        (dt(8), dt(9)),
        (dt(14), dt(18)),
    ]


def test_adjacent_commitments_are_merged():
    result = calculate_available_intervals(
        dt(8),
        dt(18),
        [
            (dt(9), dt(11)),
            (dt(11), dt(13)),
        ],
    )

    assert result == [
        (dt(8), dt(9)),
        (dt(13), dt(18)),
    ]


def test_no_commitments_returns_entire_window():
    result = calculate_available_intervals(
        dt(8),
        dt(18),
        [],
    )

    assert result == [(dt(8), dt(18))]


def test_commitments_outside_window_are_ignored():
    result = calculate_available_intervals(
        dt(8),
        dt(18),
        [
            (dt(5), dt(7)),
            (dt(19), dt(21)),
        ],
    )

    assert result == [(dt(8), dt(18))]


def test_commitments_are_clipped_to_window():
    result = calculate_available_intervals(
        dt(8),
        dt(18),
        [
            (dt(7), dt(10)),
            (dt(16), dt(20)),
        ],
    )

    assert result == [
        (dt(10), dt(16)),
    ]


def test_overnight_commitment():
    next_day = dt(2, day=4)

    result = calculate_available_intervals(
        dt(20),
        next_day,
        [
            (dt(22), dt(2, day=4)),
        ],
    )

    assert result == [
        (dt(20), dt(22)),
    ]


def test_invalid_window_is_rejected():
    with pytest.raises(ValueError):
        calculate_available_intervals(
            dt(18),
            dt(8),
            [],
        )


def test_naive_datetime_is_rejected():
    naive_start = datetime(2026, 11, 3, 8, 0)

    with pytest.raises(ValueError):
        calculate_available_intervals(
            naive_start,
            dt(18),
            [],
        )


def test_invalid_blocked_interval_is_rejected():
    with pytest.raises(ValueError):
        calculate_available_intervals(
            dt(8),
            dt(18),
            [(dt(12), dt(10))],
        )
