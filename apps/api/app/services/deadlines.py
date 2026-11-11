"""Deadlines: the single place where points in time are compared (Chapter 10, Lab 9)."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

DEPARTMENT_TZ = ZoneInfo("Europe/Kyiv")


def require_aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def local_deadline_to_utc(local_iso: str) -> datetime:
    """Converts a deadline entered by the instructor in department time to UTC."""
    naive = datetime.fromisoformat(local_iso)
    return naive.replace(tzinfo=DEPARTMENT_TZ).astimezone(timezone.utc)


def is_late(submitted_at: datetime, deadline: datetime) -> bool:
    """Late: strictly after the deadline. Exactly at the deadline is not late (E2)."""
    submitted = require_aware(submitted_at, "submitted_at").astimezone(timezone.utc)
    due = require_aware(deadline, "deadline").astimezone(timezone.utc)
    return submitted > due
