from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from typing import Any


DATE_FORMATS = ("%d-%m-%y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y")
TIME_FORMATS = ("%H:%M:%S", "%H:%M")


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip().upper()


def normalize_registration(value: Any) -> str:
    """Unifica XAVSC/XA-VSC como XA-VSC y conserva matrículas N."""
    raw = re.sub(r"[^A-Z0-9]", "", normalize_text(value))
    if raw.startswith("XA") and len(raw) > 2:
        return f"XA-{raw[2:]}"
    return raw


def parse_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Fecha no reconocida: {value!r}")


def parse_time(value: Any) -> time:
    if isinstance(value, datetime):
        return value.time().replace(microsecond=0)
    if isinstance(value, time):
        return value.replace(microsecond=0)
    if isinstance(value, (int, float)):
        seconds = round((float(value) % 1) * 86400) % 86400
        return (datetime.min + timedelta(seconds=seconds)).time()
    text = str(value).strip()
    for fmt in TIME_FORMATS:
        try:
            return datetime.strptime(text, fmt).time()
        except ValueError:
            pass
    raise ValueError(f"Hora no reconocida: {value!r}")


def combine(date_value: Any, time_value: Any) -> datetime:
    return datetime.combine(parse_date(date_value), parse_time(time_value))
