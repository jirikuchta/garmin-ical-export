# Garmin iCAL Export
Garmin Connect only allows you to publish calendar with planned workouts for upcoming 30 days ([source](https://support.garmin.com/ms-MY/?faq=UVAoDoRAgl1d75WQc4aGEA)).
There is no way how to export/publish your passed activities. This package provides a CLI tool that fills the gap.

The package will export your activities to [iCalendar](https://en.wikipedia.org/wiki/ICalendar) file that can be imported into any calendar client.

To keep your calendar always synced with Garmin Connect you will have to:
1) schedule a periodical job to run the CLI tool
2) publish iCalendar file to an URL
3) create new calencdar in your client connected to the URL


## Installation
```bash
pip3 install garmin-ical-export
```

## Usage
```
usage: garmin-ical-export [-h]
                          [--activity_type {running,cycling,swimming,multi_sport,fitness_equipment,hiking,walking,winter_sports,other,all}]
                          [--limit LIMIT]
                          [--measurement_system {metric,imperial}]
                          [--target_file TARGET_FILE]
                          login_email password

Exports Garmin Connect activities to iCalendar file.

positional arguments:
  login_email           your Garmin Connect login e-mail
  password              your Garmin Connect login password

optional arguments:
  -h, --help            show this help message and exit
  --activity_type {running,cycling,swimming,multi_sport,fitness_equipment,hiking,walking,winter_sports,other,all}
                        export only specific type of activity
  --limit LIMIT         max. number of activities to export
  --measurement_system {metric,imperial}
                        which system to use to calculate activity properties
  --target_file TARGET_FILE
                        target .ics file (prints to stdout if not passed)

```

## Examples
Export all activities, print the result.
```bash
garmin-ical-export <GARMIN_CONNECT_EMAIL> <GARMIN_CONNECT_PASSWORD>
```
Export only `running` activities, save the result to `garmin_activities.ics` file inside home folder.
```bash
garmin-ical-export <GARMIN_CONNECT_EMAIL> <GARMIN_CONNECT_PASSWORD> --activity_type running --target_file ~/garmin_activities.ics
```

