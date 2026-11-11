"""Tests of the is_late flag (the Lab 9 bug fix + regression)."""
from datetime import datetime, timezone
from types import SimpleNamespace

from app.services.submissions import mark_submission

# Deadline 06.04.2026 23:59 Kyiv (daylight saving time, UTC+3) = 20:59 UTC
LAB = SimpleNamespace(deadline=datetime(2026, 4, 6, 20, 59, tzinfo=timezone.utc))


def _mark(submitted_utc: datetime) -> bool:
    sub = SimpleNamespace(submitted_at=submitted_utc, is_late=None)
    mark_submission(sub, LAB)
    return sub.is_late


def test_mark_submission_before_deadline():
    assert _mark(datetime(2026, 4, 6, 20, 58, tzinfo=timezone.utc)) is False


def test_mark_submission_after_deadline():
    assert _mark(datetime(2026, 4, 6, 21, 0, tzinfo=timezone.utc)) is True


def test_regression_server_timezone_does_not_matter(monkeypatch):
    # Earlier a server in Europe/Kyiv reported "Late" one minute before the deadline (naive comparison).
    monkeypatch.setenv("TZ", "Europe/Kyiv")
    monkeypatch.setenv("SERVER_TZ", "Europe/Kyiv")
    assert _mark(datetime(2026, 4, 6, 20, 58, tzinfo=timezone.utc)) is False
