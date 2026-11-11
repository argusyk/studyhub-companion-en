# Bug report: "Late" for submissions before the deadline (Lab 9)

**Symptom.** Students submit work at 21:00–23:59 Kyiv time, minutes before the deadline,
and StudyHub records `is_late = true` and shows "Late". The value is stored in the database (not a cache).

**Conditions.** The production server runs in `Europe/Kyiv`; in CI the time zone is UTC and the test is green.
The week after the switch to daylight saving time (29.03.2026) seems worse because the difference from UTC grew from 2 to 3 h.

**Reproduction.** `python scripts/repro_deadline_bug.py` (imitates a server in Kyiv with the variable
SERVER_TZ) or the test `test_not_late_one_minute_before_deadline_on_kyiv_server` (xfail).

**Task.** Find the root cause (not the symptom), fix it, add a regression test
that fails without the fix. Weakening existing tests is forbidden.
