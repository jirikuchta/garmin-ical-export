# Garmin iCAL Export
Garmin Connect currently only supports publishing a calendar of planned workouts for the next 30 days ([source](https://support.garmin.com/ms-MY/?faq=UVAoDoRAgl1d75WQc4aGEA)).
Unfortunately, there is no native way to export or publish your past activities. This package provides a CLI tool designed to bridge that gap.

The tool exports your activity history into an [iCalendar](https://en.wikipedia.org/wiki/ICalendar) (.ics) file, which can be imported into any calendar application.

To keep your calendar synchronized with Garmin Connect, you will need to:
1. Schedule a periodic job to run the CLI tool.
2. Host the generated iCalendar file at a public or accessible URL.
3. Subscribe to that URL from your preferred calendar client.



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
                          [login_email] [password]

Exports Garmin Connect activities to iCalendar file.

positional arguments:
  login_email           your Garmin Connect login e-mail (falls back to the
                        GARMIN_ICAL_EXPORT_EMAIL env var, then an interactive
                        prompt)
  password              your Garmin Connect login password (falls back to
                        the GARMIN_ICAL_EXPORT_PASSWORD env var, then an
                        interactive, hidden prompt)

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
Export all activities, print the result (password prompted interactively).
```bash
garmin-ical-export <GARMIN_CONNECT_EMAIL>
```
Export only `running` activities, save the result to `garmin_activities.ics` file inside home folder.
```bash
garmin-ical-export <GARMIN_CONNECT_EMAIL> <GARMIN_CONNECT_PASSWORD> --activity_type running --target_file ~/garmin_activities.ics
```
Run non-interactively, e.g. from a cron job, without exposing credentials as command-line arguments.
```bash
GARMIN_ICAL_EXPORT_EMAIL=<GARMIN_CONNECT_EMAIL> GARMIN_ICAL_EXPORT_PASSWORD=<GARMIN_CONNECT_PASSWORD> garmin-ical-export --target_file ~/garmin_activities.ics
```

## Security note
`login_email` and `password` are optional. If omitted, they're read from the `GARMIN_ICAL_EXPORT_EMAIL` / `GARMIN_ICAL_EXPORT_PASSWORD` env vars, and if those aren't set either, you'll be prompted interactively (the password prompt is hidden). Passing credentials as plain command-line arguments still works, but is discouraged since they may end up in your shell history or be visible to other users on the machine via the process list (`ps`) — prefer the env vars for scheduled/non-interactive runs.

After a successful login, the tool caches your session (not your password) in a `garmin-ical-export-session` file in your system's temp directory, so you won't be prompted for MFA on every run. Delete that file to force a fresh login.

## Development
See [AGENTS.md](./AGENTS.md) for local setup and running tests.

## License
[MIT](./LICENSE)
