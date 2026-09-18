# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this is

A small CLI tool (`garmin-ical-export`) that logs into Garmin Connect,
fetches activity history, and writes it out as an iCalendar (`.ics`) file.
Single package, no web server, no database.

## Layout

- `garminicalexport/cmd.py` — CLI entry point (`argparse`), calls `login`
  then `to_ical`. Registered as the `garmin-ical-export` console script.
- `garminicalexport/__init__.py` — `to_ical()`: turns fetched activities into
  a `vobject.iCalendar`.
- `garminicalexport/garmin_api.py` — all network I/O. Wraps the `garth`
  library for Garmin Connect auth/session storage and the raw
  `connectapi()` calls. Results are `@lru_cache`d per process.
- `garminicalexport/activities.py` — `Activity` and per-sport subclasses
  (`RunningActivity`, `CyclingActivity`, `SwimmingActivity`,
  `MultisportActivity`, `FitnessActivity`). Each subclass overrides how its
  iCal summary/pace is formatted. `get_activity_type()` walks Garmin's
  activity-type hierarchy up to a parent type this tool recognizes.
- `garminicalexport/data_types.py` — `ActivityType` / `MeasurementSystem`
  enums and `TypedDict`s describing the raw Garmin API JSON shapes.
- `garminicalexport/format_utils.py` — pure string-formatting helpers
  (duration, distance, speed/pace) for metric and imperial units. No
  dependencies on the rest of the package — the easiest place to add
  coverage.

Only `garmin_api.py` talks to the network. Everything else is pure/testable
without mocking HTTP, though `activities.py` does call into `garmin_api`'s
cached lookups (`get_activity_types`, `get_timezones`) and needs those
monkeypatched in tests.

## Dev setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

Tests live in `tests/`, mirroring the package layout
(`tests/test_format_utils.py` etc.). There's no CI enforcing this yet — run
it yourself before handing back a change.

## Conventions

- Python 3.8+ syntax (see `python_requires` in `setup.py`) — no `match`
  statements, no `X | Y` union syntax in runtime code.
- Type hints are used throughout; keep new code annotated.
- No linter/formatter is configured. Follow the existing style (PEP 8,
  4-space indent, double quotes are not enforced either way).
