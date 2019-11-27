#!/usr/bin/env python3

import argparse
import garmin_api
import vobject
from activity import get_activity


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Exports Garmin Connect activities to ICAL format.")
    parser.add_argument(
        "--email",
        required=True,
        help="your Garmin Connect login e-mail")
    parser.add_argument(
        "--password",
        required=True,
        help="your Garmin Connect password")
    parser.add_argument(
        "--limit",
        default=10000,
        help="max. number of activities to export")
    parser.add_argument(
        "--target_file",
        help="target .ics file (prints to stdout if not passed)")

    return parser.parse_args()


def main(args):
    garmin_api.login = garmin_api.Login(args.email, args.password)
    activities_data = garmin_api.activites(args.limit)

    cal = vobject.iCalendar()
    for activity_data in activities_data:
        cal.add(get_activity(activity_data).to_vevent())

    if args.target_file:
        with open(args.target_file, "w+") as file:
            file.write(cal.serialize())
    else:
        print(cal.serialize())


if __name__ == "__main__":
    main(parse_arguments())
