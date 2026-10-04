# Sports Central

Sports Central is a Python desktop dashboard that combines live sports scores, an Apple Calendar schedule, and a rotating photo gallery in one interface.

The dashboard currently supports:

- NFL
- NBA
- MLB
- NHL
- College Football
- Men's College Basketball
- College Baseball
- Apple/iCloud Calendar
- Rotating local photos
- Live scrolling score ticker
- Monthly calendar
- Weekly event view
- Configurable refresh rates
- User-selectable sports and photo folders

## Features

### Live Sports Scores

Sports Central retrieves current sports scores and displays them in a scrolling ticker along the bottom of the dashboard.

Users can choose which leagues they want displayed from the Settings window.

### Apple Calendar Integration

The dashboard can connect to an Apple/iCloud Calendar using CalDAV.

Calendar events are displayed in two ways:

- A monthly calendar showing which days contain events
- A weekly schedule showing event names, times, and locations

### Photo Gallery

Users can choose a folder containing images.

The dashboard automatically rotates through those images while maintaining a consistent display size regardless of the original image aspect ratio.

### Settings

The Settings window allows users to configure:

- Sports leagues
- Photo folder
- Score refresh interval
- Photo rotation interval

More settings may be added in future versions.

---

# Requirements

Sports Central requires Python 3 and the following Python packages:

```bash
pip install requests Pillow caldav keyring tzlocal
```

If you plan to build a Windows executable, also install:

```bash
pip install pyinstaller
```

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project folder:

```bash
cd sports-dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python main.py
```

---

# Apple Calendar Setup

Sports Central can connect to your Apple/iCloud Calendar using CalDAV.

## Create an App-Specific Password

Do not use your normal Apple Account password.

Sign in to your Apple Account and create an app-specific password.

1. Go to your Apple Account settings.
2. Open **Sign-In and Security**.
3. Select **App-Specific Passwords**.
4. Create a password for Sports Central.
5. Save the generated password temporarily so you can enter it during setup.

Your normal Apple Account password should never be stored in this application.

## Apple Calendar Authentication

When configuring the program, use:

- Your Apple Account email address
- Your Apple app-specific password

The password should be stored through the operating system's credential manager rather than directly in the source code.

On Windows, Python's `keyring` package uses Windows Credential Manager.

---

# Calendar Selection

After connecting to iCloud, the program may discover several calendars, such as:

```text
Home
Work
Family
Reminders
```

Users can select which calendars should appear in the dashboard.

Some Apple system calendars may not behave like standard calendars. If a particular calendar produces an error, it can simply be disabled.

---

# Photos

By default, the program can use the `images` folder:

```text
sports-dashboard/
└── images/
```

You can also choose another folder from the Settings menu.

Supported image formats include:

```text
.png
.jpg
.jpeg
.webp
```

Personal photos are intentionally excluded from this GitHub repository.

---

# Running the Program

Start Sports Central with:

```bash
python main.py
```

The application displays:

```text
┌───────────────────────────────────────────────────────┐
│                    SPORTS CENTRAL                     │
├──────────────────┬──────────────────┬─────────────────┤
│ MONTH CALENDAR   │ WEEK SCHEDULE    │ PHOTO GALLERY   │
│                  │                  │                 │
│                  │                  │                 │
├──────────────────┴──────────────────┴─────────────────┤
│ LIVE SCORES                                           │
└───────────────────────────────────────────────────────┘
```

---

# Building a Windows Executable

PyInstaller can be used to create a standalone Windows executable.

Install PyInstaller:

```bash
pip install pyinstaller
```

During development, it is easier to test with a console-enabled folder build:

```powershell
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --console `
    --collect-all caldav `
    --collect-all keyring `
    --collect-all tzlocal `
    main.py
```

The executable will be created inside:

```text
dist/main/
```

Once everything is working correctly, create the final single-file version:

```powershell
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --collect-all caldav `
    --collect-all keyring `
    --collect-all tzlocal `
    main.py
```

The final executable will be located at:

```text
dist/main.exe
```

The `--collect-all` options are important because some dependencies load modules dynamically and PyInstaller may not detect them automatically.

---

# Security

Never commit any of the following to GitHub:

- Apple Account passwords
- Apple app-specific passwords
- Environment variables containing credentials
- `settings.json` if it contains personal account information
- Credential files
- Personal calendar exports
- Personal photos

These files are excluded through `.gitignore`.

---

# Project Structure

```text
sports-dashboard/
│
├── main.py
│
├── sports_data.py
│├── calendar_data.py
├── settings.py
├── setup_window.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── images/
    └── .gitkeep
```

### `main.py`

Contains the main Tkinter interface, including:

- Calendar display
- Weekly schedule
- Photo gallery
- Score ticker
- Settings interface

### `sports_data.py`

Handles retrieving and processing sports information.

### `calendar_data.py`

Handles Apple Calendar / CalDAV connections and converts calendar events into a format the dashboard can display.

### `settings.py`

Handles application settings and secure credential storage.

### `setup_window.py`

Optional first-run setup interface for configuring accounts and preferences.

---

# Troubleshooting

## `ModuleNotFoundError: caldav.davclient`

When building with PyInstaller, make sure CalDAV submodules are included:

```powershell
--collect-all caldav
```

A recommended build command is:

```powershell
python -m PyInstaller `
    --onefile `
    --windowed `
    --collect-all caldav `
    --collect-all keyring `
    --collect-all tzlocal `
    main.py
```

## Apple Calendar returns HTTP 401

HTTP `401` means Apple rejected the credentials.

Check that:

- You are using your Apple Account sign-in email.
- You are using an app-specific password.
- The app-specific password is still valid.

## Apple Calendar returns HTTP 207

HTTP `207 Multi-Status` is normal for CalDAV and indicates the request succeeded.

## Calendar timezone errors

Apple Calendar may return timezone-aware dates while other events use normal Python dates.

The application converts calendar values into the user's local timezone before displaying or sorting them.

---


# Disclaimer

Sports Central is an independent personal project.

It is not affiliated with Apple, ESPN, the NFL, NBA, MLB, NHL, NCAA, or any other sports organization.
