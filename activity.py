#!/usr/bin/env python3

import vobject
import garmin_api
from datetime import datetime, timedelta, tzinfo
from typing import Optional

try:
    from functools import cached_property  # noqa
except ImportError:
    class cached_property:  # noqa
        def __init__(self, func):
            self.func = func

        def __get__(self, instance, type=None):
            if instance is None:
                return self
            res = instance.__dict__[self.func.__name__] = self.func(instance)
            return res


class Activity:

    def __init__(self, data: garmin_api.ActivityData):
        self._data = data

    @property
    def uid(self) -> str:
        return (
            f"garmin-activity-"
            f"{self._data['ownerId']}-{self._data['activityId']}")

    @cached_property
    def summary(self):
        return str(self._data.get("activityName", "Other"))

    @cached_property
    def start_time(self) -> datetime:
        start_time = datetime.fromisoformat(self._data["startTimeLocal"])
        timezone = get_tzinfo_from_garmin_id(self._data["timeZoneId"])
        if timezone:
            start_time = start_time.replace(tzinfo=timezone)
        return start_time

    @property
    def end_time(self) -> datetime:
        duration = 0
        if self._data["duration"] is not None:
            duration = round(self._data["duration"])
        return self.start_time + timedelta(seconds=duration)

    @property
    def detail_link(self) -> str:
        return f"{garmin_api.WEB_BASE_URI}/activity/{self._data['activityId']}"

    def to_vevent(self):
        event = vobject.newFromBehavior("vevent")

        event.add("uid").value = self.uid
        event.add("summary").value = self.summary
        event.add("dtstart").value = self.start_time
        event.add("dtend").value = self.end_time
        event.add("attach").value = self.detail_link

        return event


def get_activity(data: garmin_api.ActivityData) -> Activity:
    return Activity(data)


def get_tzinfo_from_garmin_id(id: int) -> Optional[tzinfo]:
    timezones = garmin_api.timezones()
    match = next(filter(lambda tz: tz["unitId"] == id, timezones), None)
    return vobject.icalendar.getTzid(match["timeZone"]) if match else None
