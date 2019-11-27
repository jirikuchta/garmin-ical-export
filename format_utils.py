#!/usr/bin/env python3

from typing import Union


def time(seconds: Union[float, int]) -> str:
    hours, remainder = divmod(round(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def distance_metres(distance: Union[float, int]) -> str:
    return f"{round(distance)} m"


def distance_kilometers(distance: Union[float, int]) -> str:
    return f"{round(distance / 1000, 2)} km"


def distance_miles(distance: Union[float, int]) -> str:
    return f"{round((distance / 1000) * 0.62137, 2)} mi"


def speed_kmph(speed: Union[float, int]) -> str:
    return f"{round(speed * 3.6, 1)} km/h"


def speed_mph(speed: Union[float, int]) -> str:
    return f"{round((speed * 3.6) * 0.62137, 1)} mi/h"


def speed_minutes_per_100_metres(speed: Union[float, int]) -> str:
    minutes, seconds = divmod(100 / speed, 60)
    return f"{int(minutes)}:{round(seconds):02} min/100m"
