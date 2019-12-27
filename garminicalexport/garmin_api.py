import requests
import urllib.parse
from functools import lru_cache
from typing import Optional, List, Dict, Any  # noqa

from .data_types import LoginData, ActivityType, ActivityData, \
    ActivityTypeData, TimezoneData


GARMIN_WEB_BASE_URI = "https://connect.garmin.com/modern"

LOGIN_URI = (
    f"https://sso.garmin.com/sso/signin?"
    f"{urllib.parse.urlencode({'service': GARMIN_WEB_BASE_URI})}")


class GarminAPI:

    def __init__(self, login_data: LoginData):
        self.session = self.login(login_data)

    def __enter__(self) -> "GarminAPI":
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()

    @staticmethod
    def login(login_data: LoginData) -> requests.Session:
        session = requests.Session()
        session.headers.update({"referer": LOGIN_URI})
        session.post(LOGIN_URI, login_data._asdict())
        session.get(GARMIN_WEB_BASE_URI)
        return session

    def activites(self, limit: int,
                  activity_type: Optional[ActivityType]) -> List[ActivityData]:
        return get_activites(self.session, limit, activity_type)

    def activity_types(self) -> List[ActivityTypeData]:
        return get_activity_types(self.session)

    def timezones(self) -> List[TimezoneData]:
        return get_timezones(self.session)


@lru_cache()
def get_activites(session: requests.Session, limit: int,
                  activity_type: Optional[ActivityType]) -> List[ActivityData]:
    path = "/proxy/activitylist-service/activities/search/activities"
    qs = {"limit": limit}  # type: Dict[str, Any]
    if activity_type and activity_type is not ActivityType.ALL:
        qs["activityType"] = activity_type.value
    uri = f"{GARMIN_WEB_BASE_URI}{path}?{urllib.parse.urlencode(qs)}"
    res = session.get(uri)
    res.raise_for_status()
    return res.json()


@lru_cache()
def get_activity_types(session: requests.Session) -> List[ActivityTypeData]:
    path = "/proxy/activity-service/activity/activityTypes"
    res = session.get(f"{GARMIN_WEB_BASE_URI}{path}")
    res.raise_for_status()
    return res.json()


@lru_cache()
def get_timezones(session: requests.Session) -> List[TimezoneData]:
    path = "/proxy/system-service/timezoneUnits"
    res = session.get(f"{GARMIN_WEB_BASE_URI}{path}")
    res.raise_for_status()
    return res.json()
