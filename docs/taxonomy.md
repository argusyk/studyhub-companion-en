# StudyHub taxonomy (the Lab 4 reference)

## Glossary of components
| Term | Where in the code | Meaning |
|---|---|---|
| Student | `apps/api/app/models/student.py` | a student; `group_code` is the group slug (`cs-21`) |
| Lab | `apps/api/app/models/lab.py` | a lab assignment with a deadline (UTC) and a maximum score |
| Submission | `apps/api/app/models/submission.py` | a submission: file, time, status, the final `score` |
| Grade | `apps/api/app/models/grade.py` (Chapter 8) | the calculation: `raw_score`, `penalty`, `final_score` |
| Router | `apps/api/app/routers/` | the HTTP layer; the `/api/v1` prefix is set by `main.py` |
| Service | `apps/api/app/services/` | business logic (grading, deadlines, submissions) |
| UtcDateTime | `apps/api/app/db/types.py` | a column type "aware UTC only" |

## Flow map "submit a lab"
Form (`apps/web`) -> `lib/api.ts` -> `POST /api/v1/labs/{id}/submissions` ->
`routers/submissions.py` -> `services/submissions.py` -> the `submissions` table.

## Rules for the agent
- Do not invent new layers (there is no `repositories`).
- Time is aware UTC only; conversion to the department time zone is at the API boundary.
- The late penalty is rule R-07 (`docs/business-rules.md`).
