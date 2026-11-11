# The StudyHub team model policy (an example for Lab 2)

> The reference structure. Prices, tokens and the check date are [filled in by the student from the current
> Cursor documentation; the repository deliberately contains no invented figures].

Price check date: [date]. Source: [documentation URL].

## Comparison task
The `GET /api/v1/labs` endpoint with filters (`q`, `deadline_before`, `deadline_after`, `limit`,
`offset`). Quality criterion: the tests in `apps/api/tests/test_labs_filters.py` pass.

## Cost table (formula 3.1)
| Run | Model / mode | Input tokens | Output tokens | Cached tokens | Cost | Manual edits | Time |
|---|---|---|---|---|---|---|---|
| 1 | [Cursor model] | [n] | [n] | [n] | [calculation] | [n] | [min] |
| 2 | [stronger model] | [n] | [n] | [n] | [calculation] | [n] | [min] |
| 3 | Auto, Optimize For = [value] | [n] | [n] | [n] | [calculation] | [n] | [min] |

## Policy
| Task type | Model / mode | Why |
|---|---|---|
| Feature planning (Plan) | [strong model] | [rationale based on the table data] |
| Implementation from a plan | [fast model] | [...] |
| Small edits, docstrings | Tab / Inline | [...] |
| Review, security | [strong model] | [...] |

## Budget
The weekly limit for a team of 3 students: [value]; the alert threshold: [value].
