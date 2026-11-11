# A test kit for hooks (exercise 17.6, Lab 11)

The kit feeds JSON events to a hook via stdin and checks the response. **No command from
`cases.json` is executed**: these are only strings in the `command` field. Run from the repository root:

    python tools/hooks_testkit/run_cases.py          # results table
    python -m pytest tools/hooks_testkit             # the same as tests

Add your own cases to `cases.json` (fields `id`, `command`, `expect`: allow | deny | ask).
If you find a bypass, first add a case (the test fails), then fix the hook.
An honest note: a denylist hook is not a security boundary, see the docstring in `.cursor/hooks/guard_shell.py`.
