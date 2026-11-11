# Specification: grading module

## Data Model
- Submission is canonical (docs/taxonomy.md); `score` is the published integer score.
- Grade: `submission_id`, `raw_score`, `late_days`, `penalty_percent`, `penalty`,
  `final_score`, `status` (draft | final).

## Rules
R-06, R-07, R-08, R-09, R-10 – see docs/business-rules.md (R-11 is outside the scope of this iteration).

## Edge Cases
E1. The deadline is stored in UTC; it is displayed in the department's time zone.
E2. A submission exactly at the moment of the deadline is not considered late.
E3. The switch to daylight saving time does not change the number of calendar days.

## Acceptance Criteria
AC1. Given a rubric 50/50 and scores 8/10 and 6/10, When the instructor saves the grade, Then raw_score = 70.0.
AC2. Given a deadline of Mar 1 23:59 (Kyiv) and a submission on Mar 3 00:30 (Kyiv), When the penalty is calculated,
     Then penalty = 20% of raw_score (R-07).
AC3. Given a submission exactly at 23:59:00 on the deadline day, When the penalty is calculated, Then penalty = 0.
AC4. Given 5 days late, When the penalty is calculated, Then penalty = 30% (cap, R-07).

## Out of Scope
Audit of changes (R-11), export, notifications.

## Open questions
Whether to round the published score to an integer (accepted: yes, R-08).
