import os
import garth
import tempfile
import urllib.parse
from functools import lru_cache
from typing import Optional, List, Dict, Any  # noqa

from .data_types import ActivityType, ActivityData, \
    ActivityTypeData, TimezoneData


GARMIN_WEB_BASE_URI = "https://connect.garmin.com/modern"
STORED_SESSION_FILE = os.path.join(tempfile.gettempdir(), "garmin-ical-export-session")


def login(username: str, password: str):
    try:
        garth.resume(STORED_SESSION_FILE)
        if garth.client.username == username:
            return
    except:
        pass

    garth.login(username, password)
    garth.save(STORED_SESSION_FILE)


@lru_cache()
def get_activites(limit: int,
                  activity_type: Optional[ActivityType]) -> List[ActivityData]:
    path = "/activitylist-service/activities/search/activities"
    qs = {"limit": limit}  # type: Dict[str, Any]
    if activity_type and activity_type is not ActivityType.ALL:
        qs["activityType"] = activity_type.value
    url = f"{path}?{urllib.parse.urlencode(qs)}"
    return garth.connectapi(url)


@lru_cache()
def get_activity_types() -> List[ActivityTypeData]:
    path = "/activity-service/activity/activityTypes"
    return garth.connectapi(path)


@lru_cache()
def get_timezones() -> List[TimezoneData]:
    path = "/system-service/timezoneUnits"
    return garth.connectapi(path)
