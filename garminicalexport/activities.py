import vobject
from datetime import datetime, timedelta, tzinfo
from typing import Optional

from .garmin_api import get_activity_types, get_timezones, GARMIN_WEB_BASE_URI
from . import format_utils
from .data_types import ActivityType, ActivityData, ActivityTypeData, \
    MeasurementSystem


class Activity:

    def __init__(self, data: ActivityData,
                 measurement_system: Optional[MeasurementSystem]):
        self._data = data
        self._measurement_system = measurement_system
        if not self._measurement_system:
            self._measurement_system = MeasurementSystem.METRIC
        self._tzinfo = get_tzinfo_from_garmin_id(self._data["timeZoneId"])

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

        if self._measurement_system is MeasurementSystem.METRIC:
            return format_utils.distance_kilometers(distance)
        else:
            return format_utils.distance_miles(distance)

    @property
    def average_speed(self) -> str:
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        if self._measurement_system is MeasurementSystem.METRIC:
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
        start_time = datetime.strptime(
            self._data["startTimeLocal"], "%Y-%m-%d %H:%M:%S")
        if self._tzinfo:
            start_time = start_time.replace(tzinfo=self._tzinfo)
        return start_time

    @property
    def ical_dtend(self) -> datetime:
        duration = self._data.get(
            "elapsedDuration", self._data.get("duration"))
        return self.ical_dtstart + timedelta(seconds=round(duration or 0))


class RunningActivity(Activity):

    @property
    def average_speed(self):
        speed = self._data.get("averageSpeed")

        if speed is None:
            return "---"

        if self._measurement_system is MeasurementSystem.METRIC:
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


def get_activity(data: ActivityData,
                 measurement_system: Optional[MeasurementSystem]) -> Activity:
    activity_type = get_activity_type(data)

    if activity_type is ActivityType.RUNNING:
        return RunningActivity(data, measurement_system)

    if activity_type is ActivityType.CYCLING:
        return CyclingActivity(data, measurement_system)

    if activity_type is ActivityType.SWIMMING:
        return SwimmingActivity(data, measurement_system)

    if activity_type is ActivityType.MULTISPORT:
        return MultisportActivity(data, measurement_system)

    if activity_type is ActivityType.FITNESS:
        return FitnessActivity(data, measurement_system)

    return Activity(data, measurement_system)


def get_activity_type(data: ActivityData) -> ActivityType:
    all_types = get_activity_types()
    type_data = data["activityType"]

    def is_known(type_data: ActivityTypeData):
        try:
            ActivityType(type_data["typeKey"])
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
        return ActivityType(type_data["typeKey"])

    return ActivityType.OTHER


def get_tzinfo_from_garmin_id(id: int) -> Optional[tzinfo]:
    timezones = get_timezones()
    match = next(filter(lambda tz: tz["unitId"] == id, timezones), None)
    return vobject.icalendar.getTzid(match["timeZone"]) if match else None
