# The lab report checking agent – a skeleton for Lab 12

`checker.py` is a deterministic prototype without a model call: the place where your agent (Agent SDK)
will replace the rules. It receives ONLY the report text (no write permissions, no personal data).
`cases/` + `expected.json` is an eval set of five cases; `run_eval.py` compares the verdicts.
Run: `python -m pytest agents` or `python agents/checker/run_eval.py`.
