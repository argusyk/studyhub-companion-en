"""stop: runs the fast tests; on failure returns followup_message to the agent (not an exit code).

Cursor passes feedback from a hook to the agent only through the JSON `followup_message`;
`loop_limit` in hooks.json and `loop_count` in the input limit the number of repeats.
"""
import json
import subprocess
import sys

from hook_io import read_event, workspace_root

MAX_LOOPS = 3


def main() -> None:
    event = read_event()
    if event.get("status", "completed") != "completed" or event.get("loop_count", 0) >= MAX_LOOPS:
        sys.exit(0)
    api = workspace_root(event) / "apps" / "api"
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"],
                              cwd=api, capture_output=True, encoding="utf-8", errors="replace", timeout=100)
    except subprocess.TimeoutExpired:
        print(json.dumps({"followup_message": "The fast tests did not finish within 100 s: shorten the set."},
                         ))
        sys.exit(0)
    if proc.returncode not in (0, 5):  # 5 – no tests found
        tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-15:])
        print(json.dumps({"followup_message":
                          f"python -m pytest failed. Fix the cause without weakening the tests:\n{tail}"},
                         ))
    sys.exit(0)


if __name__ == "__main__":
    main()
