#!/usr/bin/env python3

import argparse
import garmin_api
import vobject

from activity import get_activity


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
        default="all",
        help="type of activity to export. Possible values are running, \
              cycling, swimming, multi_sport, fitness_equipment, hiking, \
              walking, winter_sports, other or all")
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
    activities_data = garmin_api.activites(args.activity_type, args.limit)

    cal = vobject.iCalendar()
    for activity_data in activities_data:
        activity = get_activity(activity_data)
        event = vobject.newFromBehavior("vevent")

        event.add("uid").value = activity.vevent_uid
        event.add("summary").value = activity.vevent_summary
        event.add("dtstart").value = activity.vevent_dtstart
        event.add("dtend").value = activity.vevent_dtend
        event.add("description").value = activity.detail_link

        cal.add(event)

    if args.target_file:
        with open(args.target_file, "w+") as file:
            file.write(cal.serialize())
    else:
        print(cal.serialize())


if __name__ == "__main__":
    main(parse_arguments())
