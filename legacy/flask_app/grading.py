from legacy.flask_app.utils import parse_dt, DEBUG


def late_days(deadline, submitted):
    d = parse_dt(deadline)
    s = parse_dt(submitted)
    days = (s - d).days  # full days
    if days < 0:
        days = 0
    return days


def calc_final(score, deadline, submitted):
    days = late_days(deadline, submitted)
    if DEBUG:
        print("calc_final", score, days)
    # penalty: 10% for each full day, not accepted after 5 days
    if days > 5:
        return None
    if days > 0:
        score = score - score * 0.1 * days
    return round(score)  # Python's round(): halves go to even
