#!/usr/bin/env python3

import enum
import functools
import requests
from collections import namedtuple
from mypy_extensions import TypedDict
from typing import List, Optional
from urllib.parse import quote as q


WEB_BASE_URI = "https://connect.garmin.com/modern"
LOGIN_URI = f"https://sso.garmin.com/sso/signin?service={q(WEB_BASE_URI)}"

Login = namedtuple("Login", ["username", "password"])
login = None

ROOT_ACTIVITY_TYPE_ID = 17


class BaseActivities(enum.Enum):
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


def with_login(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        with requests.Session() as session:
            session.headers.update({"referer": LOGIN_URI})
            session.post(LOGIN_URI, login._asdict())
            session.get(WEB_BASE_URI)
            return func(*args, **kwargs, login_session=session)
    return wrap


@with_login
def activites(activity_type: str,
              limit: int = 10000,
              login_session=None) -> List[ActivityData]:
    path = "/proxy/activitylist-service/activities/search/activities"
    res = login_session.get((
        f"{WEB_BASE_URI}{path}"
        f"?limit={limit}&activityType={activity_type}"))
    res.raise_for_status()
    return res.json()


@functools.lru_cache()
def activity_types() -> List[ActivityTypeData]:
    uri = f"{WEB_BASE_URI}/proxy/activity-service/activity/activityTypes"
    res = requests.get(uri)
    res.raise_for_status()
    return res.json()


@functools.lru_cache()
@with_login
def timezones(login_session=None) -> List[TimezoneData]:
    uri = f"{WEB_BASE_URI}/proxy/system-service/timezoneUnits"
    res = login_session.get(uri)
    res.raise_for_status()
    return res.json()


@functools.lru_cache()
@with_login
def user_settings(login_session=None) -> UserSettings:
    uri = f"{WEB_BASE_URI}/proxy/userprofile-service/userprofile/user-settings"
    res = login_session.get(uri)
    res.raise_for_status()
    return res.json()["userData"]
