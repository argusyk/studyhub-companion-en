"""Parity of the new implementation with the legacy snapshot. Differences – only the documented ones (docs/legacy-diff.md)."""
import json
from pathlib import Path

import pytest

from app.testing import FIXTURE, seed_db

GOLDEN = json.loads((FIXTURE.parent / "cs21_golden.json").read_text("utf-8"))

# (student, lab) -> (final in legacy, final in the new implementation): intended differences only
INTENDED_DIFFS = {
    ("Ivanenko O. P.", 3): (76, 68),      # 1 full day -> 2 calendar days: 85 - 20% = 68
    ("Shevchenko A. I.", 2): (67, 59),   # 74 - 20 % = 59.2 -> 59
    ("Bondarenko D. S.", 3): (None, 49),  # legacy did not accept after 5 days; the new policy accepts
}


@pytest.fixture
def seeded(db):
    seed_db(db)


def test_new_endpoint_matches_legacy_except_documented_diffs(client, seeded):
    new = client.get("/api/v1/groups/cs-21/grades").json()
    assert new["group"] == GOLDEN["group"]
    assert len(new["grades"]) == len(GOLDEN["grades"])
    for old, cur in zip(GOLDEN["grades"], new["grades"]):
        key = (old["student"], old["lab"])
        assert (cur["student"], cur["lab"], cur["raw"]) == (old["student"], old["lab"], old["raw"])
        if key in INTENDED_DIFFS:
            assert (old["final"], cur["final"]) == INTENDED_DIFFS[key], key
        else:
            assert cur["final"] == old["final"] and cur["late_days"] == old["late_days"], key


def test_score_endpoint_for_1042(client, seeded):
    body = client.get("/api/v1/submissions/1042/score").json()
    assert body == {"id": 1042, "raw": 85, "final": 68, "late_days": 2}


def test_stats(client, seeded):
    body = client.get("/api/v1/groups/cs-21/stats").json()
    assert body["submissions"] == 9 and body["late_count"] == 3


def test_unknown_group_404(client, seeded):
    assert client.get("/api/v1/groups/xx-99/grades").status_code == 404
