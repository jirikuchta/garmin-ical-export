import enum
from collections import namedtuple
from mypy_extensions import TypedDict
from typing import Optional


LoginData = namedtuple("LoginData", "username password")


class ActivityType(enum.Enum):
    RUNNING = "running"
    CYCLING = "cycling"
    SWIMMING = "swimming"
    MULTISPORT = "multi_sport"
    FITNESS = "fitness_equipment"
    HIKING = "hiking"
    WALKING = "walking"
    WINTERSPORTS = "winter_sports"
    OTHER = "other"
    ALL = "all"

    def __str__(self):
        return self.value


class ActivityTypeData(TypedDict):
    typeId: int
    typeKey: str
    parentTypeId: int


class ActivityData(TypedDict):
    activityId: int
    activityName: Optional[str]
    activityType: ActivityTypeData
    averageSpeed: Optional[float]  # m/s
    description: Optional[str]
    distance: Optional[float]  # metres
    duration: Optional[float]  # seconds
    ownerId: int
    startTimeLocal: str
    timeZoneId: int


class TimezoneData(TypedDict):
    unitId: int
    timeZone: str


class MeasurementSystem(enum.Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

    def __str__(self):
        return self.value
