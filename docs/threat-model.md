# A fragment of the StudyHub threat model (the STRIDE method, Lab 11)

Risk level = likelihood (1–5) × impact (1–5). The values below are an example calculation;
recalculate them for your deployment. Identifiers TM-NN (not to be confused with business rules R-NN).

| ID | STRIDE | Threat | L | I | Risk | Countermeasure | Owner |
|---|---|---|---|---|---|---|---|
| TM-01 | I | Leak of students' personal data through studyhub-db (MCP) | 3 | 5 | 15 | the `studyhub_ro` role, `--access-mode=restricted`, anonymized data | [name] |
| TM-02 | T | Prompt injection in a README/data returned by MCP | 4 | 4 | 16 | the `mcp_readonly.py` allowlist, confirmation of dangerous steps, a sandbox | [name] |
| TM-03 | E | The agent deletes files outside the caches (`rm -rf`) | 2 | 5 | 10 | `guard_shell.py` + an OS/container sandbox | [name] |
| TM-04 | I | A secret in `.env` is read by a terminal command | 3 | 4 | 12 | `guard_shell.py` (cat .env), `.cursorignore`, secrets outside the repository | [name] |
| TM-05 | R | No trace of the commands the agent executed | 3 | 3 | 9 | `audit_log.py` -> `.cursor/hooks/audit.log` | [name] |
| TM-06 | S | A student submits work on behalf of another (`student_id` in the form) | 4 | 3 | 12 | authentication, `student_id` from the token (not from the form) | [name] |
| TM-07 | D | A 10 MB file in every request | 3 | 2 | 6 | a size limit, rate limiting | [name] |

Limitation: a hooks denylist can be bypassed (writing a command to a file), so it is not a security boundary.
