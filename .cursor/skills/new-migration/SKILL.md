---
name: new-migration
description: Creating an Alembic migration for StudyHub. Use when the database schema needs to change.
---

# New migration

1. Change the ORM model in apps/api/app/models/.
2. Create a revision: `alembic revision --autogenerate -m "<description>"`.
3. Open the generated file and check it manually: autogeneration misses
   renames and type changes.
4. Add a downgrade that exactly reverses the upgrade.
5. Apply it on the local database: `alembic upgrade head`, then `alembic downgrade -1`
   and `upgrade head` again.
6. Add or update a test (apps/api/tests/test_migrations.py).
7. In the PR description, state whether the migration is reversible and whether it requires data backfilling.

Do not run migrations on the shared database. Do not edit revisions that have already been merged.
