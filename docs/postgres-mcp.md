# Postgres-MCP for StudyHub (Lab 11)

We use an existing community server, **Postgres MCP Pro** (the PyPI package `postgres-mcp`,
repository github.com/crystaldba/postgres-mcp, MIT license). Launch: `uvx postgres-mcp`
(requires `uv`) or the Docker image `crystaldba/postgres-mcp`. The connection string is passed in
the environment variable `DATABASE_URI`.

For the teaching service, enable the `--access-mode=restricted` mode (read-only transactions
and a query time limit) AND additionally connect as the `studyhub_ro` role with SELECT-only rights.
The role is created by `db/init/10-readonly-role.sh` on the first start of `docker compose up db`
(the variable `STUDYHUB_RO_PASSWORD` is required in `.env`). For a volume that already exists, run the SQL
from this script manually or `docker compose down -v` (this will delete the data).

Pin the package version before use (`uvx postgres-mcp==<version>`) and check
the parameters against the package README [verified: date]. In a real service, student data
must be anonymized (Chapter 17); in the teaching repository the data is invented.
