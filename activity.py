#!/usr/bin/env python3

import vobject
from datetime import datetime, timedelta, tzinfo
from typing import Optional

import format_utils
import garmin_api


class Activity:

    def __init__(self, data: garmin_api.ActivityData):
        self._data = data
        self._tzinfo = get_tzinfo_from_garmin_id(self._data["timeZoneId"])
        self._user_settings = garmin_api.user_settings()

    @property
    def name(self) -> str:
        return str(self._data.get("activityName", "Other"))

    @property
    def duration(self) -> str:
        duration = self._data.get("duration")

        if duration is None:
            return "---"

        return format_utils.time(duration)

    @property
    def distance(self) -> str:
        distance = self._data.get("distance")

        if distance is None:
            return "---"

        if use_metric_system():
            return format_utils.distance_kilometers(distance)
        else:
            return format_utils.distance_miles(distance)

    @property
    def average_speed(self) -> str:
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        if use_metric_system():
            return format_utils.speed_kmph(speed)
        else:
            return format_utils.speed_mph(speed)

    @property
    def detail_link(self) -> str:
        return f"{garmin_api.WEB_BASE_URI}/activity/{self._data['activityId']}"

    @property
    def vevent_uid(self) -> str:
        return (
            f"garmin-activity-"
            f"{self._data['ownerId']}-{self._data['activityId']}")

    @property
    def vevent_summary(self) -> str:
        return f"{self.name} ({self.distance}, {self.duration})"

    @property
    def vevent_dtstart(self) -> datetime:
        start_time = datetime.fromisoformat(self._data["startTimeLocal"])
        if self._tzinfo:
            start_time = start_time.replace(tzinfo=self._tzinfo)
        return start_time

    @property
    def vevent_dtend(self) -> datetime:
        duration = 0
        if self._data["duration"] is not None:
            duration = round(self._data["duration"])
        return self.vevent_dtstart + timedelta(seconds=duration)


class RunningActivity(Activity):

    @property
    def average_speed(self):
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        if use_metric_system():
            return format_utils.speed_minutes_per_kilometer(speed)
        else:
            return format_utils.speed_minutes_per_mile(speed)

    @property
    def vevent_summary(self):
        return f"{self.name} ({self.distance}, {self.average_speed})"


class CyclingActivity(Activity):

    @property
    def vevent_summary(self):
        return f"{self.name} ({self.distance}, {self.average_speed})"


class SwimmingActivity(Activity):

    @property
    def distance(self) -> str:
        d = self._data.get("distance")
        return "---" if d is None else format_utils.distance_metres(d)

    @property
    def average_speed(self):
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        return format_utils.speed_minutes_per_100_metres(speed)

    @property
    def vevent_summary(self):
        return f"{self.name} ({self.distance}, {self.average_speed})"


class MultisportActivity(Activity):

    @property
    def vevent_summary(self):
        return f"{self.name} ({self.duration}, {self.distance})"


class FitnessActivity(Activity):

    @property
    def vevent_summary(self):
        return f"{self.name} ({self.duration})"


def get_activity(data: garmin_api.ActivityData) -> Activity:
    base_activity_type = get_base_activity_type(data["activityType"])
    activity_name = base_activity_type["typeKey"]

    if activity_name == garmin_api.BaseActivities.RUNNING.value:
        return RunningActivity(data)

    if activity_name == garmin_api.BaseActivities.CYCLING.value:
        return CyclingActivity(data)

    if activity_name == garmin_api.BaseActivities.SWIMMING.value:
        return SwimmingActivity(data)

    if activity_name == garmin_api.BaseActivities.MULTISPORT.value:
        return MultisportActivity(data)

    if activity_name == garmin_api.BaseActivities.FITNESS.value:
        return FitnessActivity(data)

    return Activity(data)


def get_base_activity_type(
        activity_type: garmin_api.ActivityTypeData
) -> garmin_api.ActivityTypeData:
    types = garmin_api.activity_types()
    while activity_type["parentTypeId"] != garmin_api.ROOT_ACTIVITY_TYPE_ID:
        activity_type = next(filter(
            lambda t: t["typeId"] == activity_type["parentTypeId"], types))
    return activity_type


def get_tzinfo_from_garmin_id(id: int) -> Optional[tzinfo]:
    timezones = garmin_api.timezones()
    match = next(filter(lambda tz: tz["unitId"] == id, timezones), None)
    return vobject.icalendar.getTzid(match["timeZone"]) if match else None


def use_metric_system() -> bool:
    return garmin_api.user_settings()["measurementSystem"] == \
        garmin_api.MeasurementSystem.METRIC.value
