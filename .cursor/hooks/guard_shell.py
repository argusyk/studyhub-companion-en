"""beforeShellExecution: the shell command guard.

Reads JSON from stdin (the `command` field), answers with JSON on stdout (`permission`) and with exit code 2 on
denial. Depends only on hook_io.py next to it (there are no other modules). It NEVER executes commands.

Policy: recursive deletion is allowed only for an explicit list of cache directories inside
the project (SAFE_DIRS). Anything that looks like recursive deletion but is not on the list is blocked.

An honest limitation: a denylist is not a security boundary. The agent can write a command to a file and
run it, obfuscate the string, and so on. This hook catches typical mistakes (the 300 GB story),
while deliberate circumvention is stopped by the OS sandbox and the container (Chapter 17).
"""
import re
from pathlib import Path

from hook_io import allow, ask, deny, read_event, workspace_root

SAFE_DIRS = {".next", "node_modules", ".pytest_cache", "__pycache__", "build", "dist",
             ".turbo", ".mypy_cache", ".ruff_cache"}
DELETE_CMDS = {"rm", "rmdir", "rd", "del", "erase", "remove-item", "ri"}
INTERPRETERS = {"bash", "sh", "zsh", "dash", "pwsh", "powershell", "cmd", "python", "python3",
                "py", "node", "eval", "xargs", "sudo", "env", "time", "nohup", "exec", "start"}
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n&]")
TOKEN = re.compile(r"\"[^\"]*\"?|'[^']*'?|\S+")
PS_RECURSE = re.compile(r"^-r(e(c(u(r(s(e)?)?)?)?)?)?(:.*)?$", re.IGNORECASE)
WIN_FLAGS = re.compile(r"^(/[a-zA-Z])+$")
BAD_PATH_CHARS = set("$`~%*?{}()<>|")

DENY_PATTERNS = [
    (r"\bfind\b[^|;&\n]*\s-delete\b", "find -delete is forbidden"),
    (r"\b(shutil\.)?rmtree\b|\bos\.removedirs\b", "programmatic recursive deletion (rmtree) is forbidden"),
    (r"\bgit\s+push\b[^|;&\n]*(--force\b|--force-with-lease|\s-f\b|\s\+\S)", "force-push is forbidden"),
    (r"\bgit\s+clean\b[^|;&\n]*\s-[a-zA-Z]*f", "git clean -f deletes files with no way to restore them"),
    (r"\bchmod\b[^|;&\n]*(-R|--recursive)[^|;&\n]*\b777\b", "chmod -R 777 is forbidden"),
    (r"\bmkfs(\.\w+)?\b|\bdd\b[^|;&\n]*\bof=/dev/|:\(\)\s*\{|\bformat\s+[a-z]:", "disk formatting is forbidden"),
    (r"\b(curl|wget|iwr|invoke-webrequest)\b[^\n]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", "running a downloaded script (curl | sh) is forbidden"),
    (r"\b(curl|wget|iwr|invoke-webrequest)\b[^\n]*\|\s*(iex|invoke-expression|pwsh|powershell)\b", "running a downloaded script is forbidden"),
    (r"\b(cat|type|get-content|gc|less|more|head|tail|bat)\b[^|;&\n]*\.env(?!\.example)\b", "reading .env (secrets) is forbidden"),
]
ASK_PATTERNS = [
    (r"\bgit\s+reset\s+[^|;&\n]*--hard\b", "git reset --hard destroys uncommitted changes"),
    (r"\b(drop\s+(table|database|schema)|truncate\s+table)\b", "SQL that destroys data"),
]


def cmd_name(token: str) -> str:
    base = token.replace("\\", "/").rsplit("/", 1)[-1].lower()
    for ext in (".exe", ".cmd", ".bat", ".ps1"):
        if base.endswith(ext):
            base = base[: -len(ext)]
    return base


def unquote(token: str) -> str:
    if token[:1] in "\"'":
        token = token[1:]
        if token[-1:] in "\"'":
            token = token[:-1]
    return token


def is_recursive(name: str, args: list[str]) -> bool:
    for a in args:
        if name == "rm":
            if a.startswith("--") and len(a) > 2 and "recursive".startswith(a[2:].split("=")[0]):
                return True
            if re.fullmatch(r"-[A-Za-z]*[rR][A-Za-z]*", a):
                return True
        elif name in {"remove-item", "ri"}:
            if PS_RECURSE.match(a):
                return True
        else:  # rmdir, rd, del, erase (cmd.exe): /s
            if re.search(r"(?i)(^|/)s(?![a-z])", a) and a.startswith("/"):
                return True
    return False


def target_args(name: str, args: list[str]) -> list[str]:
    out, seen_dd = [], False
    for a in args:
        if a == "--" and not seen_dd:
            seen_dd = True
        elif not seen_dd and a.startswith("-") and a != "-":
            continue
        elif name in {"rmdir", "rd", "del", "erase"} and WIN_FLAGS.match(a):
            continue
        else:
            out.append(a)
    return out


def targets_are_safe(targets: list[str], root: Path, cwd: Path) -> bool:
    if not targets:
        return False
    for raw in targets:
        t = unquote(raw).replace("\\", "/")
        if not t or any(c in BAD_PATH_CHARS for c in t):
            return False
        p = Path(t)
        resolved = (p if p.is_absolute() else cwd / p).resolve()
        if resolved == root or root not in resolved.parents or resolved.name not in SAFE_DIRS:
            return False
    return True


def analyze(command: str, root: Path, cwd: Path, depth: int = 0) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    if depth > 3:
        return [("deny", "command nesting is too deep")]
    for segment in SEGMENT_SPLIT.split(command):
        tokens = [unquote(t) for t in TOKEN.findall(segment)]
        seen_interpreter = False
        for i, tok in enumerate(tokens):
            name = cmd_name(tok)
            if name in INTERPRETERS:
                seen_interpreter = True
            elif seen_interpreter and re.search(r"\s", tok):
                findings += analyze(tok, root, cwd, depth + 1)
            if name in DELETE_CMDS:
                args = tokens[i + 1:]
                if is_recursive(name, args) and not targets_are_safe(target_args(name, args), root, cwd):
                    findings.append(("deny", "Recursive deletion is allowed only for: "
                                     + ", ".join(sorted(SAFE_DIRS)) + " inside the project."))
    return findings


def evaluate(command: str, root: Path, cwd: Path) -> tuple[str, str]:
    findings = analyze(command, root, cwd)
    for pattern, message in DENY_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            findings.append(("deny", message))
    for pattern, message in ASK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            findings.append(("ask", message))
    for level in ("deny", "ask"):
        for lvl, msg in findings:
            if lvl == level:
                return level, msg
    return "allow", ""


def main() -> None:
    event = read_event()
    command = event.get("command")
    if not isinstance(command, str) or not command.strip():
        deny("The hook could not read command (fail closed).")
    root = workspace_root(event).resolve()
    cwd = Path(event.get("cwd") or root)
    level, message = evaluate(command, root, cwd.resolve() if cwd.exists() else root)
    if level == "deny":
        deny(message)
    elif level == "ask":
        ask(message)
    else:
        allow()


if __name__ == "__main__":
    main()
