# Task A: importing scores from Moodle (worktree 1)

Read a CSV export of the Moodle gradebook and return scores by student email.
**File zone (other tasks do not enter here):**
`apps/api/app/integrations/moodle/**`, `apps/api/tests/moodle/**`.
Do not change `main.py`, the models or other people's modules. Format: delimiter `;`, the first line is the header
(`Email;Lab1;Lab2;…`), an empty value = no score. The data is invented only.
Acceptance: a test for a correct file, an empty cell, an invalid number, extra columns.
