"""beforeMCPExecution: allows only read tools (an allowlist); rejects the rest.

The event fields (`tool_name`, `tool_input`) should be checked against the hooks documentation of your Cursor version.
For execute_sql it additionally checks that this is a single read statement. This is an auxiliary layer:
the main protection is the studyhub_ro role and the --access-mode=restricted mode.
"""
import re

from hook_io import allow, deny, read_event

ALLOWED_TOOLS = {"get_schedule", "find_free_slot",  # studyhub-schedule
                 "list_schemas", "list_objects", "get_object_details",  # postgres-mcp, read
                 "execute_sql", "explain_query"}
READ_SQL = re.compile(r"^\s*(select|with|explain|show)\b", re.IGNORECASE)
WRITE_WORDS = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy)\b",
                         re.IGNORECASE)


def main() -> None:
    event = read_event()
    tool = event.get("tool_name") or event.get("toolName") or ""
    if tool not in ALLOWED_TOOLS:
        deny(f"MCP tool {tool!r} is not on the allowlist (read-only).")
    if tool == "execute_sql":
        raw = event.get("tool_input") or {}
        if isinstance(raw, str):
            raw = {"sql": raw}
        sql = str(raw.get("sql", "")).strip().rstrip(";")
        if ";" in sql or not READ_SQL.match(sql) or WRITE_WORDS.search(sql):
            deny("execute_sql: only a single read statement is allowed (SELECT/WITH/EXPLAIN/SHOW).")
    allow()


if __name__ == "__main__":
    main()
