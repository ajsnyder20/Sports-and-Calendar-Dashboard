import tkinter as tk
from tkinter import messagebox

from caldav import get_davclient

from settings import (
    load_settings,
    save_settings,
    save_apple_password
)


class SetupWindow:

    def __init__(
        self,
        root,
        on_complete
    ):

        self.root = root
        self.on_complete = on_complete

        self.window = tk.Toplevel(
            root
        )

        self.window.title(
            "Sports Central Setup"
        )

        self.window.geometry(
            "500x450"
        )

        self.window.resizable(
            False,
            False
        )

        self.window.grab_set()

        self.settings = (
            load_settings()
        )

        self.calendar_vars = {}

        self.build_login()

    def clear(self):

        for widget in (
            self.window
            .winfo_children()
        ):
            widget.destroy()

    def build_login(self):

        self.clear()

        tk.Label(
            self.window,
            text="Sports Central",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        ).pack(
            pady=(30, 5)
        )

        tk.Label(
            self.window,
            text=(
                "Connect your "
                "Apple Calendar"
            ),
            font=(
                "Segoe UI",
                12
            )
        ).pack(
            pady=(0, 25)
        )

        tk.Label(
            self.window,
            text="Apple Account Email"
        ).pack(
            anchor="w",
            padx=60
        )

        self.email_entry = tk.Entry(
            self.window,
            width=45
        )

        self.email_entry.pack(
            padx=60,
            pady=(5, 15)
        )

        self.email_entry.insert(
            0,
            self.settings.get(
                "apple_email",
                ""
            )
        )

        tk.Label(
            self.window,
            text=(
                "App-Specific Password"
            )
        ).pack(
            anchor="w",
            padx=60
        )

        self.password_entry = tk.Entry(
            self.window,
            width=45,
            show="•"
        )

        self.password_entry.pack(
            padx=60,
            pady=(5, 25)
        )

        tk.Button(
            self.window,
            text="Connect",
            width=20,
            command=self.connect
        ).pack()

    def connect(self):

        email = (
            self.email_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
            .strip()
        )

        if not email or not password:

            messagebox.showerror(
                "Missing Information",
                "Enter your email and "
                "app-specific password."
            )

            return

        try:

            with get_davclient(
                url=(
                    "https://"
                    "caldav.icloud.com/"
                ),
                username=email,
                password=password,
                auth_type="basic"
            ) as client:

                principal = (
                    client
                    .get_principal()
                )

                calendars = (
                    principal
                    .get_calendars()
                )

                calendar_names = []

                for cal in calendars:

                    try:

                        name = (
                            cal
                            .get_display_name()
                        )

                        calendar_names.append(
                            name
                        )

                    except Exception:
                        pass

            self.settings[
                "apple_email"
            ] = email

            save_settings(
                self.settings
            )

            save_apple_password(
                email,
                password
            )

            self.build_calendar_picker(
                calendar_names
            )

        except Exception as error:

            messagebox.showerror(
                "Connection Failed",
                str(error)
            )

    def build_calendar_picker(
        self,
        calendars
    ):

        self.clear()

        tk.Label(
            self.window,
            text="Choose Calendars",
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        ).pack(
            pady=25
        )

        tk.Label(
            self.window,
            text=(
                "Select the calendars "
                "you want displayed."
            )
        ).pack(
            pady=(0, 15)
        )

        self.calendar_vars = {}

        frame = tk.Frame(
            self.window
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=80
        )

        existing = (
            self.settings.get(
                "calendars",
                []
            )
        )

        for name in calendars:

            var = tk.BooleanVar(
                value=(
                    name in existing
                    or not existing
                )
            )

            self.calendar_vars[
                name
            ] = var

            tk.Checkbutton(
                frame,
                text=name,
                variable=var
            ).pack(
                anchor="w",
                pady=3
            )

        tk.Button(
            self.window,
            text="Save & Continue",
            width=20,
            command=self.finish
        ).pack(
            pady=20
        )

    def finish(self):

        selected = []

        for name, var in (
            self.calendar_vars.items()
        ):

            if var.get():
                selected.append(name)

        self.settings[
            "calendars"
        ] = selected

        save_settings(
            self.settings
        )

        self.window.destroy()

        self.on_complete()