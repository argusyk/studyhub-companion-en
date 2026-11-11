# Differences between legacy and the new implementation (Lab 10)

| Rule | Legacy (actual) | New implementation | Decision |
|---|---|---|---|
| R-07 penalty | 10% for each FULL day (`timedelta.days`); not accepted after 5 days (`final = null`) | 10% for each CALENDAR day in Kyiv time, cap 30%, always accepted | A deliberate policy change (approved by the head of department, [date]) |
| R-08 rounding | Python `round()`: halves to even (76.5 -> 76) | Halves round up (76.5 -> 77) | Doubtful in legacy; changed, see the test `test_r08_*` |
| Time zone | naive dates without a zone | aware, stored in UTC | A defect fix |
| Injections | SQL by concatenation | parameterized SQLAlchemy queries | A defect fix |
| API path | `/api/groups/<g>/grades` | `/api/v1/groups/{group}/grades` | The canonical prefix |

Examples of discrepancies are recorded in `apps/api/tests/test_legacy_parity.py::INTENDED_DIFFS`.
