from datetime import datetime, timedelta

from gdl_pernocta.models import Flight
from gdl_pernocta.normalization import normalize_registration
from gdl_pernocta.scheduler import build_schedule


def flight(reg, number, origin, departure, arrival, destination, row):
    return Flight(
        operation_date=departure,
        registration=normalize_registration(reg),
        flight_number=str(number),
        origin=origin,
        scheduled_departure=departure,
        scheduled_arrival=arrival,
        destination=destination,
        source_row=row,
    )


def test_cross_midnight_pernocta():
    flights = [
        flight("N533VL", 5245, "OAX", datetime(2026, 8, 15, 21, 45), datetime(2026, 8, 15, 23, 19), "GDL", 2),
        flight("N533VL", 149, "GDL", datetime(2026, 8, 16, 6, 2), datetime(2026, 8, 16, 7, 25), "MEX", 3),
    ]
    result = build_schedule(flights)
    assert len(result) == 1
    assert result[0].status == "PERNOCTA"
    assert result[0].ground_time == timedelta(hours=6, minutes=43)
    assert result[0].departure_flight == "149"


def test_less_than_three_hours_is_transit():
    flights = [
        flight("XAVLX", 1753, "SAT", datetime(2026, 8, 15, 21, 32), datetime(2026, 8, 15, 22, 27), "GDL", 2),
        flight("XAVLX", 5706, "GDL", datetime(2026, 8, 15, 23, 35), datetime(2026, 8, 16, 4, 41), "ORD", 3),
    ]
    result = build_schedule(flights)
    assert result[0].status == "TRANSIT CHECK"
    assert result[0].ground_time == timedelta(hours=1, minutes=8)


def test_exactly_three_hours_is_pernocta():
    flights = [
        flight("XAVAA", 1, "MEX", datetime(2026, 8, 15, 19), datetime(2026, 8, 15, 21), "GDL", 2),
        flight("XAVAA", 2, "GDL", datetime(2026, 8, 16, 0), datetime(2026, 8, 16, 1), "TIJ", 3),
    ]
    assert build_schedule(flights)[0].status == "PERNOCTA"


def test_searches_first_later_departure_not_only_next_row():
    flights = [
        flight("XAVAA", 1, "MEX", datetime(2026, 8, 15, 19), datetime(2026, 8, 15, 20), "GDL", 2),
        flight("XAVAA", 99, "MTY", datetime(2026, 8, 15, 21), datetime(2026, 8, 15, 22), "CUN", 3),
        flight("XAVAA", 2, "GDL", datetime(2026, 8, 16, 5), datetime(2026, 8, 16, 6), "TIJ", 4),
    ]
    assert build_schedule(flights)[0].departure_flight == "2"


def test_original_group_order():
    flights = [
        flight("XAVT1", 1, "MEX", datetime(2026, 8, 15, 18), datetime(2026, 8, 15, 19), "GDL", 1),
        flight("XAVT1", 2, "GDL", datetime(2026, 8, 15, 20), datetime(2026, 8, 15, 21), "MEX", 2),
        flight("XAVP1", 3, "MEX", datetime(2026, 8, 15, 18), datetime(2026, 8, 15, 21), "GDL", 3),
        flight("XAVP1", 4, "GDL", datetime(2026, 8, 16, 5), datetime(2026, 8, 16, 6), "MEX", 4),
        flight("XAVT2", 5, "MEX", datetime(2026, 8, 15, 23), datetime(2026, 8, 16, 1), "GDL", 5),
        flight("XAVT2", 6, "GDL", datetime(2026, 8, 16, 2), datetime(2026, 8, 16, 3), "MEX", 6),
    ]
    assert [item.registration for item in build_schedule(flights)] == ["XA-VT1", "XA-VP1", "XA-VT2"]
