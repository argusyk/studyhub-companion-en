"""Regenerates the snapshot of the old code's behavior: python legacy/tools/make_golden.py"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ["STUDYHUB_DB_URL"] = "sqlite:///:memory:"

from legacy.flask_app.app import app, seed_from_fixtures  # noqa: E402

FIX = ROOT / "legacy" / "tests" / "fixtures"
seed_from_fixtures(FIX / "group_cs21.json")
resp = app.test_client().get("/api/groups/cs-21/grades")
with open(FIX / "cs21_golden.json", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(resp.get_json(), ensure_ascii=False, indent=2) + "\n")
print("golden written, status", resp.status_code)
