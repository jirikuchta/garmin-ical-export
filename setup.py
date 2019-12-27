#!/usr/bin/env python3

import setuptools  # noqa
from distutils.core import setup


def readme():
    with open("README.md", encoding='utf-8') as f:
        return f.read()


setup(
    name="garmin-ical-export",
    version="1.0.1",
    description="Export Garmin Connect activities to iCalendar file",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Jiri Kuchta",
    author_email="jiri.kuchta@email.cz",
    url="https://github.com/jirikuchta/garmin-ical-export",
    packages=["garminicalexport"],
    license="MIT",
    entry_points={
        "console_scripts": ["garmin-ical-export=garminicalexport.cmd:main"]
    },
    install_requires=["vobject", "requests"],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False
)
