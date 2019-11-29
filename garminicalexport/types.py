#!/usr/bin/env python3

import enum
from mypy_extensions import TypedDict
from typing import Optional


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
    STATUTE_US = "statute_us"
    STATUTE_UK = "statute_uk"


class UserSettings(TypedDict):
    measurementSystem: str
