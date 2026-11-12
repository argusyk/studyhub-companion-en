# StudyHub – the companion repository for the textbook

The companion repository for the textbook "Developing with Cursor".
Repository: https://github.com/argusyk/studyhub-companion-en. All data is invented; there are no real students or secrets here.

StudyHub is a service for tracking a department's lab assignments: a student submits work, the instructor
checks it and assigns a score, and sees group statistics. The repository is built so that each of the
12 lab assignments of Appendix D has a **starting point** (the git tag `lab-N-start`).
Reference solutions are kept in a separate private instructors' repository (https://github.com/argusyk/studyhub-solutions).
Each `lab-N-start` contains the state reached at the end of Lab N−1.

## Structure

```text
apps/api/            FastAPI (Python 3.12+), SQLAlchemy 2, Alembic, pytest
apps/web/            Next.js 15 + TypeScript, Vitest
packages/shared/     shared TypeScript types and pure functions
legacy/              the old Flask prototype "with smells" (Lab 10)
tools/schedule_mcp/  our own "department schedule" MCP server (Lab 11)
tools/hooks_testkit/ a test kit for hooks without executing dangerous commands (exercise 17.6, Lab 11)
agents/checker/      a skeleton of a report checking agent + an eval set (Lab 12)
.cursor/             rules/*.mdc, skills, agents, hooks, mcp.json, BUGBOT.md, worktrees.json
data/seed/           seed data (students, labs); data/schedule.json is the schedule
docs/                taxonomy, business-rules, specs, templates, design (mockup), threat-model, tasks
db/init/             PostgreSQL initialization (the studyhub_ro role is read-only)
```

## Quick start

Required: Git, Python 3.12+, Node.js 22+, Docker (for PostgreSQL; not needed for tests).

```bash
cp .env.example .env                       # Windows PowerShell: Copy-Item .env.example .env
cd apps/api
python -m venv .venv                       # activate: .venv/bin/activate or .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -X utf8 -m pytest                   # tests (SQLite in-memory, PostgreSQL is not needed)
python -m app.seed                         # seed into a local SQLite (or into the DB from DATABASE_URL)
uvicorn app.main:app --reload              # http://localhost:8000/docs
```

The PostgreSQL database: `docker compose up db` (change `POSTGRES_PASSWORD` in `.env`), then
`DATABASE_URL=postgresql+psycopg://...` and `alembic upgrade head` in `apps/api`.
Web: `npm install` in the root, then `npm run dev` (http://localhost:3000), `npm run test`, `npm run typecheck`.

Other checks (from the repository root): `python -m pytest legacy/tests tools agents`
(`pip install flask "mcp[cli]"` is required).

## How to switch between lab stages

```bash
git tag                                     # all stages
git switch -c my-lab-3 lab-3-start          # your own branch from the starting point of Lab 3
```

| Lab | Start tag | What is there at the start | What is handed in |
|---|---|---|---|
| 1 | `lab-1-start` | an empty monorepo, `.gitignore`, `.env.example`, `docker-compose.yml` | the structure, `.cursorignore`, a report |
| 2 | `lab-2-start` | the FastAPI skeleton: `/api/v1/health`, `/api/v1/labs`, the Student/Lab models, seed, tests | filters of the lab list, `docs/model-policy.md` |
| 3 | `lab-3-start` | + `labs` filters | the `Submission` model, Pydantic schemas, a validation test |
| 4 | `lab-4-start` | + `Submission`, `docs/architecture.md` | `docs/taxonomy.md`, a context report |
| 5 | `lab-5-start` | + Alembic 0001, the Next.js skeleton, `packages/shared` | `POST /api/v1/labs/{id}/submissions`, migration 0002, the submission page |
| 6 | `lab-6-start` | a working submission flow | `.cursor/rules`, `AGENTS.md`, the "new migration" skill |
| 7 | `lab-7-start` | + the PRD/spec/plan/todo templates | the grading module per the specification, rule R-07 |
| 8 | `lab-8-start` | + the mockup `docs/design/dashboard-mockup.svg`, sample data | the instructor dashboard, `design-system.mdc` |
| 9 | `lab-9-start` | **a deliberate bug** in `is_late` (naive datetime, Kyiv time zone), an xfail test, `scripts/repro_deadline_bug.py` | a root cause fix, a regression test, hooks |
| 10 | `lab-10-start` | `legacy/` (Flask), fixtures and the snapshot `cs21_golden.json` | characterization tests, ported endpoints, `docs/business-rules.md`, a TS module |
| 11 | `lab-11-start` | `guard_shell.py`, `tools/hooks_testkit`, `data/schedule.json`, the `studyhub_ro` role | the schedule MCP server, `mcp.json`, a threat model, an injection protocol |
| 12 | `lab-12-start` | tasks A/B/C for worktrees, eval cases, `tools/test_gitignore.py` | three features, CI/Bugbot, an agent with an eval, an experiment protocol |

The `main` branch = `lab-12-start` + this README. The `lab-N-start` tags are "what the instructor hands out".

## Canonical decisions

- A single **Submission** entity: `id, student_id, lab_id, submitted_at (UTC), file_url, filename,
  size_bytes, status (submitted|reviewed|returned), score (0..100|null), is_late`. The score calculation is in `Grade`.
- All API paths have the **`/api/v1`** prefix, set by `app/main.py`.
- The late penalty rule has a single identifier **R-07** (`docs/business-rules.md`):
  10% of the score per calendar day (Kyiv time), at most 30%.
- Backend layers: `routers -> services -> Session` (without `repositories`).
- Time: only aware UTC in the database (`UtcDateTime`); conversion to `Europe/Kyiv` at the API boundary.
- The Postgres-MCP provider: the PyPI package `postgres-mcp` (crystaldba, MIT), see `docs/postgres-mcp.md`.

## Hooks and security

`.cursor/hooks/guard_shell.py` reads JSON from stdin (the `command` field), answers with
`{"permission": "allow|deny|ask"}` and exit code 2 on denial; it depends only on `hook_io.py`.
It blocks `rm --recursive`, `rm -fr`, `Remove-Item -Recurse`, `rd /s`, `find -delete`, `rmtree`,
`git push --force`, `curl | sh`, reading `.env` and so on; recursive deletion is allowed only for caches
(`node_modules`, `.next`, `dist`, …). A check without executing commands:
`python -m pytest tools/hooks_testkit`. This is an auxiliary layer, not a security boundary (Chapter 17).

## The schedule MCP server

`pip install "mcp[cli]"`, then `python tools/schedule_mcp/server.py` (stdio) or through `.cursor/mcp.json`.
Cursor must launch `python` from the venv where `mcp` is installed (or give an absolute path in `command`).
The server is compatible with `mcp` 1.x (`FastMCP`) and 2.x (`MCPServer`). The DB user for `postgres-mcp`
is created by `db/init/10-readonly-role.sh` (the variable `STUDYHUB_RO_PASSWORD`).

## Known limitations

- Migration files have short names (`0002_subm.py`, `0003_grade.py`, `0004_late.py`), and some
  test directories are shortened (`tests/moodle`, `tests/notif`) so as not to exceed the Windows path length limit.
- The Vitest tests and `npm run typecheck` were verified on Node 24; Playwright scenarios are not added.
- Check the formats of `permissions.json` and `hooks.json` against the documentation of your Cursor version.
- Prices, tokens and dates in `docs/model-policy.md` and the protocols are [placeholders] to be filled in.
