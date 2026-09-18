from datetime import datetime

from garminicalexport import activities
from garminicalexport.data_types import ActivityType, MeasurementSystem

TIMEZONES = [{"unitId": 1, "timeZone": "Europe/Prague"}]

ACTIVITY_TYPES = [
    {"typeId": 1, "typeKey": "running", "parentTypeId": None},
    {"typeId": 2, "typeKey": "trail_running", "parentTypeId": 1},
    {"typeId": 3, "typeKey": "some_future_type", "parentTypeId": 999},
]


def make_activity_data(**overrides):
    data = {
        "activityId": 42,
        "ownerId": 7,
        "activityName": "Morning Run",
        "activityType": {"typeId": 1, "typeKey": "running", "parentTypeId": None},
        "averageSpeed": 3.0,
        "description": None,
        "distance": 5000.0,
        "duration": 1800.0,
        "elapsedDuration": 1800.0,
        "startTimeLocal": "2024-01-01 08:00:00",
        "timeZoneId": 1,
    }
    data.update(overrides)
    return data


def patch_lookups(monkeypatch, activity_types=ACTIVITY_TYPES, timezones=TIMEZONES):
    monkeypatch.setattr(activities, "get_activity_types", lambda: activity_types)
    monkeypatch.setattr(activities, "get_timezones", lambda: timezones)


def test_get_activity_type_known_type(monkeypatch):
    patch_lookups(monkeypatch)
    data = make_activity_data()
    assert activities.get_activity_type(data) == ActivityType.RUNNING


def test_get_activity_type_walks_up_to_known_parent(monkeypatch):
    patch_lookups(monkeypatch)
    data = make_activity_data(
        activityType={"typeId": 2, "typeKey": "trail_running", "parentTypeId": 1})
    assert activities.get_activity_type(data) == ActivityType.RUNNING


def test_get_activity_type_falls_back_to_other(monkeypatch):
    patch_lookups(monkeypatch)
    data = make_activity_data(
        activityType={"typeId": 3, "typeKey": "some_future_type", "parentTypeId": 999})
    assert activities.get_activity_type(data) == ActivityType.OTHER


def test_get_activity_dispatches_running_subclass(monkeypatch):
    patch_lookups(monkeypatch)
    data = make_activity_data()
    activity = activities.get_activity(data, MeasurementSystem.METRIC)
    assert isinstance(activity, activities.RunningActivity)


def test_activity_properties(monkeypatch):
    patch_lookups(monkeypatch)
    data = make_activity_data()
    activity = activities.Activity(data, MeasurementSystem.METRIC)

    assert activity.name == "Morning Run"
    assert activity.duration == "00:30:00"
    assert activity.distance == "5.0 km"
    assert activity.ical_uid == "garmin-activity-7-42"
    assert activity.ical_dtstart == datetime(2024, 1, 1, 8, 0, 0,
                                             tzinfo=activity._tzinfo)
    assert activity.ical_dtend == activity.ical_dtstart.replace(minute=30)


def test_activity_missing_fields_fall_back_to_placeholder(monkeypatch):
    patch_lookups(monkeypatch)
    data = make_activity_data(distance=None, duration=None, averageSpeed=None)
    activity = activities.Activity(data, MeasurementSystem.METRIC)

    assert activity.distance == "---"
    assert activity.duration == "---"
    assert activity.average_speed == "---"


def test_get_tzinfo_from_garmin_id_unknown_id_returns_none(monkeypatch):
    patch_lookups(monkeypatch)
    assert activities.get_tzinfo_from_garmin_id(999) is None
