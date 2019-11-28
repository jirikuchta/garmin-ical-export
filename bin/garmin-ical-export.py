#!/usr/bin/env python3

import argparse
from garminicalexport.export import export


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Exports Garmin Connect activities to ICAL format.")
    parser.add_argument(
        "email",
        metavar="login_email",
        help="your Garmin Connect login e-mail")
    parser.add_argument(
        "password",
        metavar="login_password",
        help="your Garmin Connect password")
    parser.add_argument(
        "--activity_type",
        help="export only specific type of activity \
              Possible values are running, cycling, swimming, multi_sport, \
              fitness_equipment, hiking, walking, winter_sports and other.")
    parser.add_argument(
        "--limit",
        default=10000,
        help="max. number of activities to export")
    parser.add_argument(
        "--target_file",
        help="target .ics file (prints to stdout if not passed)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    ical = export(args.email, args.password, args.limit,
                  activity_type=args.activity_type)

    if args.target_file:
        with open(args.target_file, "w+") as file:
            file.write(ical)
    else:
        print(ical)
