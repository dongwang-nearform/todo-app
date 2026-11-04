import re
from datetime import date, datetime, time

_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_TIME = re.compile(r"\d{2}:\d{2}:\d{2}")


def parse_optional_date(value: object) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime) or not isinstance(value, (date, str)):
        raise ValueError("must be YYYY-MM-DD")
    if isinstance(value, date):
        return value
    if _DATE.fullmatch(value) is None:
        raise ValueError("must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("must be YYYY-MM-DD") from exc


def parse_required_date(value: object) -> date:
    if value is None:
        raise ValueError("must be YYYY-MM-DD")
    parsed = parse_optional_date(value)
    if parsed is None:
        raise ValueError("must be YYYY-MM-DD")
    return parsed


def parse_optional_time(value: object) -> time | None:
    if value is None:
        return None
    if isinstance(value, datetime) or not isinstance(value, (time, str)):
        raise ValueError("must be HH:MM:SS")
    if isinstance(value, time):
        if value.microsecond:
            raise ValueError("must be HH:MM:SS")
        return value
    if _TIME.fullmatch(value) is None:
        raise ValueError("must be HH:MM:SS")
    hour, minute, second = (int(part) for part in value.split(":"))
    if hour > 23 or minute > 59 or second > 59:
        raise ValueError("must be HH:MM:SS")
    return time(hour, minute, second)


def require_date(value: object, field: str) -> date:
    try:
        return parse_required_date(value)
    except ValueError as exc:
        raise ValueError(f"{field} {exc}") from exc
