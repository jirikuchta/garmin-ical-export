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
                        parser: argparse.ArgumentParser, label: str,
                        non_interactive_hint: str) -> str:
    resolved = value or os.environ.get(env_var)
    if not resolved:
        if not sys.stdin.isatty():
            parser.error(f"{label} is required: {non_interactive_hint}")
        resolved = prompt()
        if not resolved:
            parser.error(f"{label} is required")
    return resolved


def resolve_credentials(args: argparse.Namespace,
                        parser: argparse.ArgumentParser) -> Tuple[str, str]:
    """Resolve the login e-mail from args/env var/prompt, and the password
    from an env var or interactive prompt (never a CLI argument, since
    that would put it in shell history and the process list)."""

    username = _resolve_credential(
        args.garmin_username, EMAIL_ENV_VAR,
        lambda: input("Garmin Connect email: "), parser, "login_email",
        f"pass it as an argument, set {EMAIL_ENV_VAR}, or run interactively")
    password = _resolve_credential(
        None, PASSWORD_ENV_VAR,
        lambda: getpass.getpass("Garmin Connect password: "), parser,
        "password", f"set {PASSWORD_ENV_VAR}, or run interactively")

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
