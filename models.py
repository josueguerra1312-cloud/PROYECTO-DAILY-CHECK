from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class Flight:
    operation_date: datetime
    registration: str
    flight_number: str
    origin: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    destination: str
    source_row: int


@dataclass(frozen=True)
class GroundWindow:
    registration: str
    arrival_flight: str
    arrival_at: datetime
    departure_flight: Optional[str]
    departure_at: Optional[datetime]
    ground_time: Optional[timedelta]
    status: str
    sort_group: int
    operational_date: datetime
    note: str = ""
