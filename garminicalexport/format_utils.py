def time(seconds: float) -> str:
    hours, remainder = divmod(round(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def distance_metres(meters: float) -> str:
    return f"{round(meters)} m"


def distance_kilometers(meters: float) -> str:
    return f"{round(meters / 1000, 2)} km"


def distance_miles(meters: float) -> str:
    return f"{round((meters / 1000) * 0.62137, 2)} mi"


def speed_kmph(meters_per_second: float) -> str:
    return f"{round(meters_per_second * 3.6, 1)} km/h"


def speed_mph(meters_per_second: float) -> str:
    return f"{round((meters_per_second * 3.6) * 0.62137, 1)} mi/h"


def speed_minutes_per_100_metres(meters_per_second: float) -> str:
    minutes, seconds = divmod(100 / meters_per_second, 60)
    return f"{int(minutes)}:{round(seconds):02} min/100m"


def speed_minutes_per_kilometer(meters_per_second: float) -> str:
    minutes, seconds = divmod(1000 / meters_per_second, 60)
    return f"{int(minutes)}:{round(seconds):02} min/km"


def speed_minutes_per_mile(meters_per_second: float) -> str:
    minutes, seconds = divmod((1000 / 0.62137) / meters_per_second, 60)
    return f"{int(minutes)}:{round(seconds):02} min/mi"
