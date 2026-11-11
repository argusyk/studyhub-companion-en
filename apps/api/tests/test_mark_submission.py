"""Tests of the is_late flag. Note that the first test is GREEN – and that is exactly what is suspicious (Lab 9)."""
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from app.services.submissions import mark_submission

# Deadline 06.04.2026 23:59 Kyiv (daylight saving time, UTC+3) = 20:59 UTC
LAB = SimpleNamespace(deadline=datetime(2026, 4, 6, 20, 59, tzinfo=timezone.utc))


def _mark(at_utc: datetime) -> bool:
    sub = SimpleNamespace(is_late=None)
    mark_submission(sub, LAB, at_utc)
    return sub.is_late


def test_mark_submission_before_deadline(monkeypatch):
    monkeypatch.delenv("SERVER_TZ", raising=False)  # as on CI: the server is in UTC
    assert _mark(datetime(2026, 4, 6, 20, 58, tzinfo=timezone.utc)) is False


def test_mark_submission_after_deadline(monkeypatch):
    monkeypatch.delenv("SERVER_TZ", raising=False)
    assert _mark(datetime(2026, 4, 6, 21, 0, tzinfo=timezone.utc)) is True


@pytest.mark.xfail(reason="Lab 9: known bug – the server is in Europe/Kyiv, naive comparison", strict=False)
def test_not_late_one_minute_before_deadline_on_kyiv_server(monkeypatch):
    monkeypatch.setenv("SERVER_TZ", "Europe/Kyiv")
    # 23:58 Kyiv = 20:58 UTC, i.e. one minute before the deadline
    assert _mark(datetime(2026, 4, 6, 20, 58, tzinfo=timezone.utc)) is False
