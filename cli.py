from __future__ import annotations

import argparse
from datetime import time, timedelta
from pathlib import Path

from .io_excel import read_flights, write_csv, write_xlsx
from .scheduler import build_schedule


def parse_hhmm(value: str) -> time:
    try:
        hour, minute = (int(part) for part in value.split(":"))
        return time(hour, minute)
    except (ValueError, TypeError) as exc:
        raise argparse.ArgumentTypeError("Use HH:MM, por ejemplo 18:00") from exc


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Genera la secuencia ordenada de pernoctas y tránsitos en GDL."
    )
    result.add_argument("input", type=Path, help="Archivo .xlsx o .xlsm con la hoja VUELOS")
    result.add_argument("-o", "--output", type=Path, default=Path("SecuenciaGDL.xlsx"))
    result.add_argument("--sheet", default="VUELOS", help="Hoja de vuelos; default: VUELOS")
    result.add_argument("--station", default="GDL", help="Estación; default: GDL")
    result.add_argument("--night-start", type=parse_hhmm, default=time(18, 0))
    result.add_argument("--night-end", type=parse_hhmm, default=time(6, 0))
    result.add_argument("--transit-hours", type=float, default=3.0)
    result.add_argument("--include-spares", action="store_true")
    return result


def main() -> None:
    args = parser().parse_args()
    flights = read_flights(args.input, args.sheet)
    windows = build_schedule(
        flights,
        station=args.station,
        night_start=args.night_start,
        night_end=args.night_end,
        transit_limit=timedelta(hours=args.transit_hours),
        include_spares=args.include_spares,
    )
    if args.output.suffix.lower() == ".csv":
        write_csv(windows, args.output)
    else:
        write_xlsx(windows, args.output)
    print(f"Se generaron {len(windows)} ventanas en {args.output}")


if __name__ == "__main__":
    main()
