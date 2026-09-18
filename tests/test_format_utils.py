from garminicalexport import format_utils


def test_time():
    assert format_utils.time(0) == "00:00:00"
    assert format_utils.time(59) == "00:00:59"
    assert format_utils.time(3661) == "01:01:01"


def test_distance_metres():
    assert format_utils.distance_metres(1500.4) == "1500 m"


def test_distance_kilometers():
    assert format_utils.distance_kilometers(1500) == "1.5 km"


def test_distance_miles():
    assert format_utils.distance_miles(1609.34) == "1.0 mi"


def test_speed_kmph():
    assert format_utils.speed_kmph(10) == "36.0 km/h"


def test_speed_mph():
    assert format_utils.speed_mph(10) == "22.4 mi/h"


def test_speed_minutes_per_100_metres():
    assert format_utils.speed_minutes_per_100_metres(1) == "1:40 min/100m"
    assert format_utils.speed_minutes_per_100_metres(0) == "0:00 min/100m"


def test_speed_minutes_per_kilometer():
    assert format_utils.speed_minutes_per_kilometer(1) == "16:40 min/km"
    assert format_utils.speed_minutes_per_kilometer(0) == "0:00 min/km"


def test_speed_minutes_per_mile():
    assert format_utils.speed_minutes_per_mile(1) == "26:49 min/mi"
    assert format_utils.speed_minutes_per_mile(0) == "0:00 min/mi"
