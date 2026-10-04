import json
import os
import keyring

SETTINGS_FILE = "settings.json"

APP_NAME = "SportsDashboard"


DEFAULT_SETTINGS = {
    "apple_email": "",
    "calendars": [],
    "sports": [
        "NFL",
        "NBA",
        "MLB",
        "NHL",
        "NCAA",
        "NCAAM"
    ],
    "image_folder": "images",
    "score_refresh_seconds": 30,
    "image_rotation_seconds": 5
}


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            saved = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(saved)

        return settings

    except Exception:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )


def save_apple_password(email, password):
    keyring.set_password(
        APP_NAME,
        email,
        password
    )


def get_apple_password(email):
    if not email:
        return None

    return keyring.get_password(
        APP_NAME,
        email
    )


def delete_apple_password(email):
    try:
        keyring.delete_password(
            APP_NAME,
            email
        )
    except keyring.errors.PasswordDeleteError:
        pass