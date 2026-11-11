"""Generates data/schedule.json (invented data): python tools/schedule_mcp/make_schedule.py"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "data" / "schedule.json"
GROUPS = ["CS-22a", "CS-22b", "CS-21"]
TEACHERS = ["Kovalenko O. M.", "Petrenko I. V.", "Melnychuk S. A."]
SUBJECTS = ["Databases", "Programming", "Software Testing", "Computer Networks"]
ROOMS = ["3.214", "3.216", "2.101", "4.005"]


def build() -> dict:
    slots = []
    for week in range(1, 19):
        for day in range(1, 6):
            for period in range(1, 5):
                gi = (week + day + period) % len(GROUPS)
                ti = (day + period) % len(TEACHERS)
                # some periods are free: the instructor is not busy
                if (week * 7 + day * 3 + period) % 4 == 0:
                    continue
                slots.append({"week": week, "day": day, "period": period, "group": GROUPS[gi],
                              "teacher": TEACHERS[ti], "subject": SUBJECTS[(gi + ti) % len(SUBJECTS)],
                              "room": ROOMS[(gi + period) % len(ROOMS)]})
    # the Chapter 12 example: Thursday, periods 2-3 in week 7 for Kovalenko O. M.
    slots = [s for s in slots if not (s["week"] == 7 and s["day"] == 4 and s["period"] in (2, 3))]
    slots += [
        {"week": 7, "day": 4, "period": 2, "group": "CS-22a", "teacher": "Kovalenko O. M.",
         "subject": "Databases", "room": "3.214"},
        {"week": 7, "day": 4, "period": 3, "group": "CS-22b", "teacher": "Kovalenko O. M.",
         "subject": "Databases", "room": "3.214"},
    ]
    slots.sort(key=lambda s: (s["week"], s["day"], s["period"], s["group"]))
    return {"periods_per_day": 6, "slots": slots}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, indent=0) + "\n")
    print("schedule: slots =", len(data["slots"]))
