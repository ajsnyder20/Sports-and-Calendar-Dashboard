import os

from datetime import datetime, date, time
from zoneinfo import ZoneInfo

from caldav import get_davclient
from tzlocal import get_localzone

from settings import (
    load_settings,
    get_apple_password
)

LOCAL_TIMEZONE = get_localzone()


CALENDARS_TO_USE = [
    "Home",
    "Work",
    # "Family",   # temporarily disabled because it is throwing Errno 22
]


def normalize_datetime(value):
    if isinstance(value, datetime):
        if value.tzinfo is None:
            # Assume naive datetimes are in local timezone
            value = value.replace(
                tzinfo=LOCAL_TIMEZONE
            )

        return value.astimezone(
            LOCAL_TIMEZONE
        )

    elif isinstance(value, date):
        # Convert date to datetime at midnight
        return datetime.combine(
            value,
            time.min,
            tzinfo=LOCAL_TIMEZONE
        )

    else:
        return None

def connect():
    settings = load_settings()
    email = settings.get("apple_email")
    password = get_apple_password(email)

    if not email:
        raise RuntimeError(
            "Apple Calendar email is missing."
        )
    
    if not password:
        raise RuntimeError(
            "Apple Calendar password is missing."
        )

    return get_davclient(
        url="https://caldav.icloud.com/",
        username=email,
        password=password,
        auth_type="basic"
    )


def get_apple_calendars():
    with connect() as client:
        principal = client.get_principal()
        calendars = (principal.get_calendars())

        names = []

        for cal in calendars:
            try: 
                name = (
                    cal.get_display_name()
                )

                names.append(name)
            except Exception:
                pass
        return names

def get_apple_events(
    start_date,
    end_date
):

    settings = load_settings()

    selected_calendars = settings.get("calendars", [])

    events = []

    with connect() as client:
        principal = client.get_principal()

        calendars = (principal.get_calendars())

        for cal in calendars:
            try:
                calendar_name = (cal.get_display_name())
            except Exception:
                continue
            if(selected_calendars and calendar_name not in selected_calendars):
                continue
            try:
                results = cal.search(
                    event=True,
                    start=start_date,
                    end=end_date,
                    expand=True
                )
            except Exception as error:
                print(
                    f"Skipping "
                    f"{calendar_name}: "
                    f"{error}"
                )

                continue
        for result in results:
            try:
                component = result.icalendar_component
                start_value = component.get("DTSTART").dt
                all_day = (
                    isinstance(start_value, date) and not isinstance(start_value, datetime)
                )

                start_time = normalize_datetime(start_value)

                end_property = component.get("DTEND")

                if end_property:
                    end_value = end_property.dt
                else:
                    end_value = start_value

                end_time = normalize_datetime(end_value)

                if start_time is None:
                    continue
                if end_time is None:
                    end_time = start_time

                events.append({
                    "title": str(component.get("SUMMARY", "Untitled Event")),
                    "start": start_time,
                    "end": end_time,
                    "location": str(component.get("LOCATION", "")),
                    "calendar": calendar_name,
                    "all_day": all_day
                })
            except Exception as error:
                print("Skipping event:", error)

    events.sort(key=lambda event: event["start"])
    
    return events
