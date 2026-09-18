#!/usr/bin/env python3

import argparse
import getpass
import os
import sys
from typing import Callable, Optional, Tuple

from .garmin_api import login as login_garmin
from . import to_ical
from .data_types import ActivityType, MeasurementSystem


EMAIL_ENV_VAR = "GARMIN_ICAL_EXPORT_EMAIL"
PASSWORD_ENV_VAR = "GARMIN_ICAL_EXPORT_PASSWORD"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Exports Garmin Connect activities to iCalendar file.")
    parser.add_argument(
        "garmin_username",
        nargs="?",
        type=str,
        metavar="login_email",
        help=(
            "your Garmin Connect login e-mail "
            f"(falls back to the {EMAIL_ENV_VAR} env var, "
            "then an interactive prompt)"))
    parser.add_argument(
        "garmin_password",
        nargs="?",
        type=str,
        metavar="password",
        help=(
            "your Garmin Connect login password "
            f"(falls back to the {PASSWORD_ENV_VAR} env var, "
            "then an interactive, hidden prompt)"))
    parser.add_argument(
        "--activity_type",
        default="all",
        type=ActivityType,
        choices=list(ActivityType),
        help="export only specific type of activity")
    parser.add_argument(
        "--limit",
        type=int,
        default=10000,
        help="max. number of activities to export")
    parser.add_argument(
        "--measurement_system",
        default=MeasurementSystem.METRIC,
        type=MeasurementSystem,
        choices=list(MeasurementSystem),
        help="which system to use to calculate activity properties")
    parser.add_argument(
        "--target_file",
        type=str,
        help="target .ics file (prints to stdout if not passed)")

    return parser


def _resolve_credential(value: Optional[str], env_var: str,
                        prompt: Callable[[], str],
                        parser: argparse.ArgumentParser, label: str) -> str:
    resolved = value or os.environ.get(env_var)
    if not resolved:
        if not sys.stdin.isatty():
            parser.error(
                f"{label} is required: pass it as an argument, set "
                f"{env_var}, or run interactively")
        resolved = prompt()
        if not resolved:
            parser.error(f"{label} is required")
    return resolved


def resolve_credentials(args: argparse.Namespace,
                        parser: argparse.ArgumentParser) -> Tuple[str, str]:
    """Resolve login e-mail/password from args, env vars, or an
    interactive prompt (in that order). Env vars and the prompt exist so
    credentials don't have to be passed as plain CLI arguments, where
    they'd be visible in shell history and the process list."""

    username = _resolve_credential(
        args.garmin_username, EMAIL_ENV_VAR,
        lambda: input("Garmin Connect email: "), parser, "login_email")
    password = _resolve_credential(
        args.garmin_password, PASSWORD_ENV_VAR,
        lambda: getpass.getpass("Garmin Connect password: "), parser,
        "password")

    return username, password


def main():
    parser = build_parser()
    args = parser.parse_args()
    username, password = resolve_credentials(args, parser)

    login_garmin(username, password)

    ical = to_ical(args.limit,
                   activity_type=args.activity_type,
                   measurement_system=args.measurement_system)

    if args.target_file:
        with open(args.target_file, "w+") as file:
            file.write(ical)
    else:
        print(ical)


if __name__ == "__main__":
    main()
