"""The Cursor hooks protocol adapter.

Input: one JSON document on stdin. For beforeShellExecution these are, among others, the fields
`command`, `cwd`, `workspace_roots`. Output: JSON on stdout with the field `permission`
(`allow` | `deny` | `ask`) and optional `user_message` and `agent_message`.
Exit code 2 also means "deny". The format may change between versions of
Cursor: after an update, check it against the documentation and run
`python -m pytest tools/hooks_testkit`.
"""
import json
import os
import sys
from pathlib import Path


def read_event() -> dict:
    """Reads JSON from stdin; on empty or corrupted input returns {}."""
    raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def workspace_root(event: dict | None = None) -> Path:
    roots = (event or {}).get("workspace_roots") or []
    if roots:
        return Path(roots[0])
    env = os.environ.get("CURSOR_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2]  # .cursor/hooks/hook_io.py -> repository root


def _emit(payload: dict, code: int = 0) -> None:
    # ASCII escaping: safe for any stdout code page on Windows
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()
    sys.exit(code)


def allow() -> None:
    _emit({"permission": "allow"})


def ask(message: str) -> None:
    _emit({"permission": "ask", "user_message": message, "agent_message": message})


def deny(message: str) -> None:
    _emit({"permission": "deny", "user_message": message, "agent_message": message}, code=2)
