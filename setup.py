#!/usr/bin/env python3

import setuptools  # noqa
from distutils.core import setup


def readme():
    with open("README.md", encoding='utf-8') as f:
        return f.read()


setup(
    name="garmin-ical-export",
    version="0.0.5",
    description="Export Garmin Connect activities to iCalendar file",
    long_description=readme(),
    author="Jiri Kuchta",
    author_email="jiri.kuchta@email.cz",
    url="https://github.com/jirikuchta/garmin-ical-export",
    packages=["garminicalexport"],
    license="MIT",
    scripts=["bin/garmin-ical-export"],
    install_requires=[
        "vobject",
        "requests"
    ],
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
