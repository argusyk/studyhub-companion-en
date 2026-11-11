"""Grading (specification docs/specs/grading/spec.md, rules R-06..R-10)."""
from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from zoneinfo import ZoneInfo

PENALTY_PER_DAY = 10  # % per calendar day (R-07)
PENALTY_CAP = 30  # % – the cap (R-07)


@dataclass(frozen=True)
class CriterionScore:
    name: str
    weight: Decimal
    score: Decimal
    max_score: Decimal


def _d(value) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))


def round1(value: Decimal) -> Decimal:
    """R-08: halves round up, to 0.1."""
    return value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def raw_score(criteria: list[CriterionScore]) -> Decimal:
    """R-06: the sum of (score / max × weight); the weights must add up to 100."""
    if not criteria:
        raise ValueError("the rubric is empty")
    if sum(c.weight for c in criteria) != 100:
        raise ValueError("the weights must add up to 100")
    total = Decimal(0)
    for c in criteria:
        if c.max_score <= 0 or not (0 <= c.score <= c.max_score):
            raise ValueError(f"invalid score for criterion {c.name!r}")
        total += c.score / c.max_score * c.weight
    return round1(total)


def late_days(submitted_at: datetime, deadline: datetime, tz: ZoneInfo) -> int:
    """The number of calendar days late in department time (E2: exactly at the deadline – 0)."""
    for name, value in (("submitted_at", submitted_at), ("deadline", deadline)):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(f"{name} must be timezone-aware")
    if submitted_at <= deadline:
        return 0
    return (submitted_at.astimezone(tz).date() - deadline.astimezone(tz).date()).days


def late_penalty_percent(days: int) -> int:
    """R-07: 10 % per day, at most 30 %."""
    return min(max(days, 0) * PENALTY_PER_DAY, PENALTY_CAP)


def penalty_points(raw: Decimal, percent: int) -> Decimal:
    return round1(raw * percent / 100)


def final_score(raw: Decimal, penalty: Decimal) -> Decimal:
    """R-09."""
    return max(Decimal(0), raw - penalty)


def published_score(final: Decimal) -> int:
    """R-08: an integer 0..100 for Submission.score (halves round up)."""
    return max(0, min(100, int(final.quantize(Decimal(1), rounding=ROUND_HALF_UP))))
