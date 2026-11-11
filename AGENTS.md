# StudyHub

A service for tracking a department's lab assignments: students submit work, the
instructor checks it and assigns scores, and sees group statistics.

## Stack
- apps/web – Next.js 15, TypeScript, Vitest, Playwright
- apps/api – FastAPI, Python 3.12, SQLAlchemy, Alembic, pytest
- Database – PostgreSQL (docker compose up db); CI – GitHub Actions

## Commands
- API installation: `cd apps/api && python -m venv .venv && pip install -e ".[dev]"`
- API: `cd apps/api && uvicorn app.main:app --reload`
- API tests: `cd apps/api && python -m pytest`
- Web: `npm install` in the root, then `npm run dev`; tests: `npm run test`
- Migrations: `cd apps/api && alembic revision --autogenerate -m "<description>"`, `alembic upgrade head`

## Conventions
- Changes without tests are not accepted; one commit – one meaningful change.
- Branches: feature/<short-name>; a PR describes what was changed and how it was verified.
- Types are mandatory: mypy for Python, strict for TypeScript.
- API: prefix `/api/v1`, a single Submission entity (docs/taxonomy.md).

## Prohibitions
- Do not read or modify .env and secret files.
- Do not run migrations on the shared database; only on the local one.
- Do not modify migrations that have already been merged.

## Where to look
- Architecture: docs/architecture.md, terms: docs/taxonomy.md
- Business rules: docs/business-rules.md
- Model policy: docs/model-policy.md
