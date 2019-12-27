#!/usr/bin/env python3

import argparse

from . import to_ical
from .data_types import LoginData, ActivityType, MeasurementSystem


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Exports Garmin Connect activities to iCalendar file.")
    parser.add_argument(
        "garmin_username",
        type=str,
        metavar="login_email",
        help="your Garmin Connect login e-mail")
    parser.add_argument(
        "garmin_password",
        type=str,
        metavar="password",
        help="your Garmin Connect login password")
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

    return parser.parse_args()


def main():
    args = parse_arguments()

    login_data = LoginData(args.garmin_username, args.garmin_password)

    ical = to_ical(login_data, args.limit,
                   activity_type=args.activity_type,
                   measurement_system=args.measurement_system)

    if args.target_file:
        with open(args.target_file, "w+") as file:
            file.write(ical)
    else:
        print(ical)


if __name__ == "__main__":
    main()
