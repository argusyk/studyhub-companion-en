# Task C: deadline notifications (worktree 3)

A pure function that builds a reminder text for a student about a lab deadline
(in department time, Europe/Kyiv) and decides whom to send to (those who have not yet submitted).
**File zone:** `apps/api/app/notifications/**`, `apps/api/tests/notif/**`.
Do NOT implement sending email/messenger: only building messages (`list[Message]`).
Acceptance: a test for summer/winter time, for a student who has already submitted, and for an empty list.
