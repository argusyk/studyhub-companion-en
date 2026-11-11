# Task B: export of a group's scores to CSV (worktree 2)

`GET /api/v1/groups/{group}/grades.csv` returns `text/csv; charset=utf-8` with a BOM (Excel),
the delimiter `;`, columns: student, lab, score, penalty %, days late.
**File zone:** `apps/api/app/exports/**`, `apps/api/app/routers/exports.py`,
`apps/api/tests/exports/**`; the only change outside the zone is the `include_router` line in `main.py`.
WARNING: the directory `apps/api/app/exports/` must get into git (check `.gitignore`).
Protection against CSV injection: values starting with `=`, `+`, `-`, `@` are escaped.
