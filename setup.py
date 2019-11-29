#!/usr/bin/env python

from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="garmin-ical-export",
    version="0.0.1",
    description="Export Garmin Connect activities to iCalendar file",
    long_description=readme(),
    author="Jiri Kuchta",
    url="https://github.com/jirikuchta/garmin-ical-export",
    packages=["garminicalexport"],
    license="MIT",
    scripts=["bin/garmin-ical-export"],
    install_requires=[
        "vobject",
        "requests",
        "mypy_extensions"
    ],
    include_package_data=True,
    zip_safe=False
)
