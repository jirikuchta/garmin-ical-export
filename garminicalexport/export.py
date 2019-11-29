#!/usr/bin/env python3

import vobject

from . import activities
from .garmin_api import GarminAPI


def export(email: str, password: str, limit: int,
           activity_type: str = None) -> str:
    with GarminAPI(email, password) as api:
        activities_data = api.activites(limit, activity_type=activity_type)

        cal = vobject.iCalendar()
        for activity_data in activities_data:
            activity = activities.get_activity(activity_data, api)
            event = vobject.newFromBehavior("vevent")

            event.add("uid").value = activity.ical_uid
            event.add("summary").value = activity.ical_summary
            event.add("dtstart").value = activity.ical_dtstart
            event.add("dtend").value = activity.ical_dtend
            event.add("description").value = activity.detail_link

            cal.add(event)

    return cal.serialize()
