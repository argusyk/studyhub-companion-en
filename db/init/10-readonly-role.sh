#!/bin/sh
# Runs ONCE when the PostgreSQL volume is created (docker-entrypoint-initdb.d).
# Creates the read-only user studyhub_ro (for Postgres-MCP, Lab 11).
set -e
if [ -z "$STUDYHUB_RO_PASSWORD" ]; then
  echo "STUDYHUB_RO_PASSWORD is not set: the role studyhub_ro is not created"
  exit 0
fi
psql -v ON_ERROR_STOP=1 -v ropass="$STUDYHUB_RO_PASSWORD" -v dbname="$POSTGRES_DB" \
     --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
CREATE ROLE studyhub_ro LOGIN PASSWORD :'ropass';
GRANT CONNECT ON DATABASE :"dbname" TO studyhub_ro;
GRANT USAGE ON SCHEMA public TO studyhub_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO studyhub_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO studyhub_ro;
ALTER ROLE studyhub_ro SET default_transaction_read_only = on;
SQL
