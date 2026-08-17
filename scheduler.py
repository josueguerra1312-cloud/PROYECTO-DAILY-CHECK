from __future__ import annotations

from collections import defaultdict
from datetime import datetime, time, timedelta
from typing import Iterable

from .models import Flight, GroundWindow


def is_in_night_arrival_window(moment: datetime, start: time, end: time) -> bool:
    current = moment.time()
    return current >= start or current <= end


def operational_night_date(moment: datetime, night_end: time) -> datetime:
    """01:00 pertenece a la noche operacional iniciada el día anterior."""
    day = moment.date()
    if moment.time() <= night_end:
        day -= timedelta(days=1)
    return datetime.combine(day, time.min)


def _sort_group(status: str, arrival_at: datetime, night_start: time, night_end: time) -> int:
    current = arrival_at.time()
    if status == "TRANSIT CHECK" and current >= night_start:
        return 1
    if status == "PERNOCTA":
        return 2
    if status == "TRANSIT CHECK" and current <= night_end:
        return 3
    return 4


def _night_clock_minutes(moment: datetime, night_end: time) -> int:
    minutes = moment.hour * 60 + moment.minute
    if moment.time() <= night_end:
        minutes += 24 * 60
    return minutes


def build_schedule(
    flights: Iterable[Flight],
    station: str = "GDL",
    night_start: time = time(18, 0),
    night_end: time = time(6, 0),
    transit_limit: timedelta = timedelta(hours=3),
    include_spares: bool = False,
) -> list[GroundWindow]:
    """Replica la intención del macro y corrige cruces de fecha y búsquedas frágiles.

    - Agrupa por matrícula.
    - Por cada llegada a GDL busca la primera salida posterior desde GDL.
    - Conserva llegadas en 18:00-06:00, como la lógica original.
    - Menos de 3 horas es TRANSIT CHECK; 3 horas o más es PERNOCTA.
    - Orden: transit 18-24, pernoctas, transit 00-06, casos especiales.
    """
    station = station.strip().upper()
    grouped: dict[str, list[Flight]] = defaultdict(list)
    for flight in flights:
        if flight.origin == station or flight.destination == station:
            grouped[flight.registration].append(flight)

    result: list[GroundWindow] = []
    for registration, movements in grouped.items():
        movements.sort(key=lambda item: (item.scheduled_departure, item.source_row))
        for index, arrival_flight in enumerate(movements):
            if arrival_flight.destination != station:
                continue
            arrival_at = arrival_flight.scheduled_arrival
            if not is_in_night_arrival_window(arrival_at, night_start, night_end):
                continue

            next_departure = next(
                (
                    candidate
                    for candidate in movements[index + 1 :]
                    if candidate.origin == station
                    and candidate.scheduled_departure >= arrival_at
                ),
                None,
            )

            if next_departure is None:
                if not include_spares:
                    continue
                status = "SPARE"
                departure_at = None
                ground_time = None
                note = "No se encontró una salida posterior desde GDL."
            else:
                departure_at = next_departure.scheduled_departure
                ground_time = departure_at - arrival_at
                if ground_time < timedelta(0):
                    status = "REVISAR"
                    note = "La salida calculada es anterior a la llegada."
                elif ground_time < transit_limit:
                    status = "TRANSIT CHECK"
                    note = ""
                else:
                    status = "PERNOCTA"
                    note = ""

            group = _sort_group(status, arrival_at, night_start, night_end)
            result.append(
                GroundWindow(
                    registration=registration,
                    arrival_flight=arrival_flight.flight_number,
                    arrival_at=arrival_at,
                    departure_flight=next_departure.flight_number if next_departure else None,
                    departure_at=departure_at,
                    ground_time=ground_time,
                    status=status,
                    sort_group=group,
                    operational_date=operational_night_date(arrival_at, night_end),
                    note=note,
                )
            )

    return sorted(
        result,
        key=lambda item: (
            item.operational_date,
            item.sort_group,
            _night_clock_minutes(item.arrival_at, night_end),
            item.registration,
        ),
    )
