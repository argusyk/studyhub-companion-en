"""The server clock. WARNING: teaching code with a deliberate defect for Lab 9.

`server_now_naive` imitates `datetime.now()` on a server where the TZ environment variable is set:
it returns a "naive" (without tzinfo) local time. On CI SERVER_TZ is not set – that is UTC.
(On Windows there is no `time.tzset`, so the server TZ is imitated by the SERVER_TZ variable.)
"""
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def server_now_naive(at_utc: datetime | None = None) -> datetime:
    moment = at_utc or datetime.now(timezone.utc)
    tz_name = os.environ.get("SERVER_TZ")
    local = moment.astimezone(ZoneInfo(tz_name)) if tz_name else moment.astimezone(timezone.utc)
    return local.replace(tzinfo=None)
