import argparse
import vobject
from typing import Optional

from . import activities
from .garmin_api import GarminAPI
from .types import LoginData, ActivityType, MeasurementSystem


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


def get_ical(login_data: LoginData, limit: int,
             activity_type: Optional[ActivityType],
             measurement_system: Optional[MeasurementSystem]) -> str:
    with GarminAPI(login_data) as api:
        activities_data = api.activites(limit, activity_type)

        cal = vobject.iCalendar()
        for activity_data in activities_data:
            activity = activities.get_activity(
                activity_data, api, measurement_system=measurement_system)
            event = vobject.newFromBehavior("vevent")

            event.add("uid").value = activity.ical_uid
            event.add("summary").value = activity.ical_summary
            event.add("dtstart").value = activity.ical_dtstart
            event.add("dtend").value = activity.ical_dtend
            event.add("description").value = activity.detail_link

            cal.add(event)

    return cal.serialize()


def main():
    args = parse_arguments()
    login_data = LoginData(args.garmin_username, args.garmin_password)

    ical = get_ical(login_data, args.limit,
                    activity_type=args.activity_type,
                    measurement_system=args.measurement_system)

    if args.target_file:
        with open(args.target_file, "w+") as file:
            file.write(ical)
    else:
        print(ical)


if __name__ == "__main__":
    main()
