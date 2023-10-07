import vobject
from typing import Optional

from . import activities
from . import data_types
from .garmin_api import get_activites


def to_ical(limit: int,
            activity_type: Optional[data_types.ActivityType],
            measurement_system: Optional[data_types.MeasurementSystem]) -> str:
    activities_data = get_activites(limit, activity_type)

    cal = vobject.iCalendar()
    for activity_data in activities_data:
        activity = activities.get_activity(
            activity_data, measurement_system=measurement_system)
        event = vobject.newFromBehavior("vevent")

        event.add("uid").value = activity.ical_uid
        event.add("summary").value = activity.ical_summary
        event.add("dtstart").value = activity.ical_dtstart
        event.add("dtend").value = activity.ical_dtend
        event.add("description").value = activity.detail_link

        cal.add(event)

    return cal.serialize()
