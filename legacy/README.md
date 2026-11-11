# legacy/ – the old StudyHub prototype (Flask) for Lab 10

This is a deliberately "bad" prototype that students will port to FastAPI. It must NOT be
used as an example of style: the code retains typical smells (see below).
The data is invented. Run the tests from the repository ROOT:

    pip install -r legacy/requirements.txt
    python -m pytest legacy/tests

## Endpoints (current, actual behavior)
- `GET /api/groups/<group>/grades` – group scores
- `GET /api/groups/<group>/stats` – group statistics
- `GET /api/submissions/<id>/score` – the final score of a submission

## Smells you have to find (do not fix them in legacy/)
a global database connection; SQL built by concatenation (SQL injection); `print` debugging;
a "bare" `except`; magic numbers; everything in `utils.py`; copy-paste between endpoints; naive dates
without a time zone; a hidden penalty and rounding policy.

## Fixtures
`legacy/tests/fixtures/group_cs21.json` – the input data; `cs21_golden.json` – the actual
response of the old code (a snapshot). To regenerate the snapshot: `python legacy/tools/make_golden.py`.
