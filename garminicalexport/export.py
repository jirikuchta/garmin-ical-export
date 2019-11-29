#!/usr/bin/env python3

import vobject
from typing import Optional

from . import activities
from .garmin_api import GarminAPI
from .types import LoginData, ActivityType, MeasurementSystem


def export(login_data: LoginData, limit: int,
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
