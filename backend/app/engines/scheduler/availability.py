from datetime import datetime
from typing import Iterable

TimeInterval = tuple[datetime, datetime]


def _validate_datetime(value: datetime, field_name: str) -> None:
    """Reject naive datetimes because scheduling requires timezone awareness."""

    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")


def calculate_available_intervals(
    window_start: datetime,
    window_end: datetime,
    blocked_intervals: Iterable[TimeInterval],
) -> list[TimeInterval]:
    """
    Calculate free intervals inside a scheduling window.

    Blocked intervals outside the window are ignored.
    Overlapping or adjacent blocked intervals are merged.
    """

    _validate_datetime(window_start, "window_start")
    _validate_datetime(window_end, "window_end")

    if window_start >= window_end:
        raise ValueError("window_start must be earlier than window_end")

    clipped_intervals: list[TimeInterval] = []

    for index, interval in enumerate(blocked_intervals):
        if len(interval) != 2:
            raise ValueError(
                f"Blocked interval {index} must contain exactly two datetimes"
            )

        block_start, block_end = interval

        _validate_datetime(block_start, f"blocked_intervals[{index}].start")
        _validate_datetime(block_end, f"blocked_intervals[{index}].end")

        if block_start >= block_end:
            raise ValueError(
                f"Blocked interval {index} must have start before end"
            )

        # Ignore commitments completely outside the scheduling window.
        if block_end <= window_start or block_start >= window_end:
            continue

        # Clip partially overlapping commitments to the window.
        clipped_start = max(block_start, window_start)
        clipped_end = min(block_end, window_end)

        clipped_intervals.append((clipped_start, clipped_end))

    # Sort commitments chronologically.
    clipped_intervals.sort(key=lambda interval: interval[0])

    # Merge overlapping and adjacent commitments.
    merged_intervals: list[TimeInterval] = []

    for block_start, block_end in clipped_intervals:
        if not merged_intervals:
            merged_intervals.append((block_start, block_end))
            continue

        previous_start, previous_end = merged_intervals[-1]

        if block_start <= previous_end:
            merged_intervals[-1] = (
                previous_start,
                max(previous_end, block_end),
            )
        else:
            merged_intervals.append((block_start, block_end))

    # Calculate the gaps between commitments.
    available_intervals: list[TimeInterval] = []
    cursor = window_start

    for block_start, block_end in merged_intervals:
        if cursor < block_start:
            available_intervals.append((cursor, block_start))

        cursor = max(cursor, block_end)

    # Include the remaining time after the last commitment.
    if cursor < window_end:
        available_intervals.append((cursor, window_end))

    return available_intervals
