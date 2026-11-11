import json

import pytest

pytest.importorskip("mcp")
from tools.schedule_mcp import server  # noqa: E402


@pytest.fixture
def schedule(tmp_path, monkeypatch):
    data = {"periods_per_day": 6, "slots": [
        {"week": 7, "day": 4, "period": 2, "group": "CS-22a",
         "teacher": "Kovalenko O. M.", "subject": "DB", "room": "3.214"}]}
    path = tmp_path / "schedule.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(server, "DATA", path)


def test_busy_period_is_not_offered(schedule):
    free = server.find_free_slot("Kovalenko O. M.", duration=2, week=7)
    thursday = [f["start_period"] for f in free if f["day"] == "Thursday"]
    assert 1 not in thursday and 2 not in thursday


def test_unknown_group_explains_format(schedule):
    with pytest.raises(ValueError, match="CS-22a"):
        server.get_schedule("CS22", week=7)


def test_week_out_of_range(schedule):
    with pytest.raises(ValueError):
        server.get_schedule("CS-22a", week=19)


def test_result_is_capped_at_10(schedule):
    assert len(server.find_free_slot("Kovalenko O. M.", duration=1, week=1)) <= 10


def test_real_dataset_has_the_book_example():
    rows = server.get_schedule("CS-22a", week=7)
    assert any(r["day"] == 4 and r["period"] == 2 and r["teacher"] == "Kovalenko O. M." for r in rows)


def test_tools_are_registered():
    names = {t.name for t in __import__("asyncio").run(server.mcp.list_tools())}
    assert names == {"get_schedule", "find_free_slot"}
