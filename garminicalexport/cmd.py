#!/usr/bin/env python3

import argparse
import getpass
import os
import sys

from .garmin_api import login as login_garmin
from . import to_ical
from .data_types import ActivityType, MeasurementSystem


EMAIL_ENV_VAR = "GARMIN_ICAL_EXPORT_EMAIL"
PASSWORD_ENV_VAR = "GARMIN_ICAL_EXPORT_PASSWORD"


def build_parser():
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


def resolve_credentials(args, parser):
    """Resolve login e-mail/password from args, env vars, or an
    interactive prompt (in that order). Env vars and the prompt exist so
    credentials don't have to be passed as plain CLI arguments, where
    they'd be visible in shell history and the process list."""

    username = args.garmin_username or os.environ.get(EMAIL_ENV_VAR)
    if not username:
        if not sys.stdin.isatty():
            parser.error(
                "login_email is required: pass it as an argument, set "
                f"{EMAIL_ENV_VAR}, or run interactively")
        username = input("Garmin Connect email: ")

    password = args.garmin_password or os.environ.get(PASSWORD_ENV_VAR)
    if not password:
        if not sys.stdin.isatty():
            parser.error(
                "password is required: pass it as an argument, set "
                f"{PASSWORD_ENV_VAR}, or run interactively")
        password = getpass.getpass("Garmin Connect password: ")

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
