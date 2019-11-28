#!/usr/bin/env python3

import vobject

from . import activities
from . import garmin_api


def export(email: str, password: str, limit: int,
           activity_type: str = None) -> str:
    garmin_api.login = garmin_api.Login(email, password)
    activities_data = garmin_api.activites(limit, activity_type=activity_type)

    cal = vobject.iCalendar()
    for activity_data in activities_data:
        activity = activities.get_activity(activity_data)
        event = vobject.newFromBehavior("vevent")

        event.add("uid").value = activity.vevent_uid
        event.add("summary").value = activity.vevent_summary
        event.add("dtstart").value = activity.vevent_dtstart
        event.add("dtend").value = activity.vevent_dtend
        event.add("description").value = activity.detail_link

        cal.add(event)

    return cal.serialize()
