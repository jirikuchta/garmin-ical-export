#!/usr/bin/env python3

from __future__ import annotations

import requests
import urllib.parse
from functools import lru_cache
from typing import List, Dict, Any  # noqa

from . import types


GARMIN_WEB_BASE_URI = "https://connect.garmin.com/modern"

LOGIN_URI = (
    f"https://sso.garmin.com/sso/signin?"
    f"{urllib.parse.urlencode({'service': GARMIN_WEB_BASE_URI})}")


class GarminAPI:

    def __init__(self, username: str, password: str):
        self.session = self.login(username, password)

    def __enter__(self) -> GarminAPI:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()

    @staticmethod
    def login(username: str, password: str) -> requests.Session:
        session = requests.Session()
        session.headers.update({"referer": LOGIN_URI})
        session.post(LOGIN_URI, {"username": username, "password": password})
        session.get(GARMIN_WEB_BASE_URI)
        return session

    def activites(self, limit: int,
                  activity_type: str = None) -> List[types.ActivityData]:
        return get_activites(self.session, limit, activity_type)

    def activity_types(self) -> List[types.ActivityTypeData]:
        return get_activity_types(self.session)

    def timezones(self) -> List[types.TimezoneData]:
        return get_timezones(self.session)

    def user_settings(self) -> types.UserSettings:
        return get_user_settings(self.session)


@lru_cache()
def get_activites(session: requests.Session, limit: int,
                  activity_type: str = None) -> List[types.ActivityData]:
    path = "/proxy/activitylist-service/activities/search/activities"
    qs = {"limit": limit}  # type: Dict[str, Any]
    if activity_type is not None:
        qs["activityType"] = activity_type
    uri = f"{GARMIN_WEB_BASE_URI}{path}?{urllib.parse.urlencode(qs)}"
    res = session.get(uri)
    res.raise_for_status()
    return res.json()


@lru_cache()
def get_activity_types(session: requests.Session) -> \
        List[types.ActivityTypeData]:
    path = "/proxy/activity-service/activity/activityTypes"
    res = session.get(f"{GARMIN_WEB_BASE_URI}{path}")
    res.raise_for_status()
    return res.json()


@lru_cache()
def get_timezones(session: requests.Session) -> List[types.TimezoneData]:
    path = "/proxy/system-service/timezoneUnits"
    res = session.get(f"{GARMIN_WEB_BASE_URI}{path}")
    res.raise_for_status()
    return res.json()


@lru_cache()
def get_user_settings(session: requests.Session) -> types.UserSettings:
    path = "/proxy/userprofile-service/userprofile/user-settings"
    res = session.get(f"{GARMIN_WEB_BASE_URI}{path}")
    res.raise_for_status()
    return res.json()["userData"]
