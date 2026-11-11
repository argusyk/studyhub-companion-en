# apps/api

- A new endpoint is added together with a schema, a service and a test.
- Errors are returned as HTTPException with a clear message in English.
- Time zones: everything in the database is in UTC (UtcDateTime), see docs/business-rules.md, the “Deadlines” section.
- Tests: `python -m pytest` (SQLite in-memory, without PostgreSQL).
- Migration files: short names `000N_xxx.py` (a path length limit on Windows).
