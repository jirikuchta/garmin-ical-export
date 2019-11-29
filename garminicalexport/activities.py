#!/usr/bin/env python3

import vobject
from datetime import datetime, timedelta, tzinfo
from typing import Optional

from . import format_utils
from . import types
from .garmin_api import GarminAPI, GARMIN_WEB_BASE_URI


class Activity:

    def __init__(self, data: types.ActivityData, garmin_api: GarminAPI):
        self._data = data
        self._garmin_api = garmin_api
        self._tzinfo = get_tzinfo_from_garmin_id(
            self._data["timeZoneId"], garmin_api)
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

        if use_metric_system(self._garmin_api):
            return format_utils.distance_kilometers(distance)
        else:
            return format_utils.distance_miles(distance)

    @property
    def average_speed(self) -> str:
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        if use_metric_system(self._garmin_api):
            return format_utils.speed_kmph(speed)
        else:
            return format_utils.speed_mph(speed)

    @property
    def detail_link(self) -> str:
        return f"{GARMIN_WEB_BASE_URI}/activity/{self._data['activityId']}"

    @property
    def ical_uid(self) -> str:
        return (
            f"garmin-activity-"
            f"{self._data['ownerId']}-{self._data['activityId']}")

    @property
    def ical_summary(self) -> str:
        return f"{self.name} ({self.distance}, {self.duration})"

    @property
    def ical_dtstart(self) -> datetime:
        start_time = datetime.fromisoformat(self._data["startTimeLocal"])
        if self._tzinfo:
            start_time = start_time.replace(tzinfo=self._tzinfo)
        return start_time

    @property
    def ical_dtend(self) -> datetime:
        duration = 0
        if self._data["duration"] is not None:
            duration = round(self._data["duration"])
        return self.ical_dtstart + timedelta(seconds=duration)


class RunningActivity(Activity):

    @property
    def average_speed(self):
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        if use_metric_system(self._garmin_api):
            return format_utils.speed_minutes_per_kilometer(speed)
        else:
            return format_utils.speed_minutes_per_mile(speed)

    @property
    def ical_summary(self):
        return f"{self.name} ({self.distance}, {self.average_speed})"


class CyclingActivity(Activity):

    @property
    def ical_summary(self):
        return f"{self.name} ({self.distance}, {self.average_speed})"


class SwimmingActivity(Activity):

    @property
    def distance(self) -> str:
        dist = self._data.get("distance")
        return "---" if dist is None else format_utils.distance_metres(dist)

    @property
    def average_speed(self):
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        return format_utils.speed_minutes_per_100_metres(speed)

    @property
    def ical_summary(self):
        return f"{self.name} ({self.distance}, {self.average_speed})"


class MultisportActivity(Activity):

    @property
    def ical_summary(self):
        return f"{self.name} ({self.duration}, {self.distance})"


class FitnessActivity(Activity):

    @property
    def ical_summary(self):
        return f"{self.name} ({self.duration})"


def get_activity(data: types.ActivityData, garmin_api: GarminAPI) -> Activity:
    activity_type = get_activity_type(data, garmin_api)

    if activity_type is types.ActivityType.RUNNING:  # noqa
        return RunningActivity(data, garmin_api)

    if activity_type is types.ActivityType.CYCLING:  # noqa
        return CyclingActivity(data, garmin_api)

    if activity_type is types.ActivityType.SWIMMING:  # noqa
        return SwimmingActivity(data, garmin_api)

    if activity_type is types.ActivityType.MULTISPORT:  # noqa
        return MultisportActivity(data, garmin_api)

    if activity_type is types.ActivityType.FITNESS:  # noqa
        return FitnessActivity(data, garmin_api)

    return Activity(data, garmin_api)


def get_activity_type(data: types.ActivityData,
                      garmin_api: GarminAPI) -> types.ActivityType:
    all_types = garmin_api.activity_types()
    type_data = data["activityType"]

    def is_known(type_data: types.ActivityTypeData):
        try:
            types.ActivityType(type_data["typeKey"])
            return True
        except ValueError:
            return False

    while not is_known(type_data):
        try:
            type_data = next(filter(
                lambda t: t["typeId"] == type_data["parentTypeId"], all_types))
        except StopIteration:
            break

    if is_known(type_data):
        return types.ActivityType(type_data["typeKey"])

    return types.ActivityType.OTHER


def get_tzinfo_from_garmin_id(
        id: int,
        garmin_api: GarminAPI) -> Optional[tzinfo]:
    timezones = garmin_api.timezones()
    match = next(filter(lambda tz: tz["unitId"] == id, timezones), None)
    return vobject.icalendar.getTzid(match["timeZone"]) if match else None


def use_metric_system(garmin_api: GarminAPI) -> bool:
    return garmin_api.user_settings()["measurementSystem"] == \
        types.MeasurementSystem.METRIC.value
