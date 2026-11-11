# StudyHub business rules

The single register of rules. The identifier `R-NN` unambiguously points to a rule in all documents,
specifications and tests (test names contain `r07_` and so on).

## Deadlines
- The deadline is stored in UTC (aware) and is entered and displayed in department time
  (`Europe/Kyiv`). A submission exactly at the moment of the deadline is not considered late.

## R-06. Score by rubric
`raw_score = Σ (criterion_score / criterion_max × weight)`, the sum of weights = 100, the result is
rounded to 0.1 (R-08).

## R-07. Late penalty
- Rule: 10% of `raw_score` for each calendar day of lateness (the difference of calendar dates
  in department time), at most 30%. The work is always accepted.
- Example: deadline Mar 1 23:59, submission Mar 3 00:30 (Kyiv) = 2 days = 20%.
- Origin: a deliberate policy change compared with legacy (there "full days, after 5 days
  not accepted"). See docs/legacy-diff.md (Lab 10).
- Code: `apps/api/app/services/grading.py::late_penalty_percent`.

## R-08. Rounding
Mathematical (halves round up) to 0.1 for `raw_score`/`penalty`; the published
`Submission.score` is rounded to an integer, also "halves round up".
Legacy rounded "halves to even" (Python `round`).

## R-09. Final score
`final_score = max(0, raw_score − penalty)`.

## R-10. Resubmission
The latest work is graded; the penalty is calculated from the date of resubmission
relative to the original deadline.

## R-11. Audit of a score change
Any change to `final_score` creates an audit record with a reason (implemented in Chapter 14).
