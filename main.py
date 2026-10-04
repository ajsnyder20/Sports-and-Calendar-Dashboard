import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from datetime import datetime, date, timedelta
import calendar
import os
import random
from calendar_data import get_apple_events
import settings
from sports_data import get_scores
from settings import load_settings, save_settings
from tkinter import filedialog
from setup_window import SetupWindow




# ============================================================
# SPORTS LEAGUES
# ============================================================

LEAGUES = [
    "NFL",
    "NBA",
    "MLB",
    "NHL",
    "NCAA",
    "NCAAM",
    "NCAA Baseball"
]


# ============================================================
# LOAD SPORTS
# ============================================================

def load_all_games():
    settings = load_settings()
    leagues = settings.get("sports", [])
    all_games = []

    for league in leagues:
        try:
            games = get_scores(league)
            all_games.extend(games)
        except Exception as error:
            print(f"Error loading {league} scores: {error}")
    return all_games


# ============================================================
# MAIN DASHBOARD
# ============================================================

class SportsDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title("Sports Central")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = int(screen_width * 0.9)
        height = int(screen_height * 0.9)
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(1000, 650)
        self.settings = load_settings()

        # ====================================================
        # COLORS
        # ====================================================

        self.bg = "#111318"
        self.panel = "#1c1f26"
        self.panel_alt = "#252932"
        self.border = "#343945"

        self.text = "#f5f5f5"
        self.muted = "#a1a7b3"

        self.accent = "#2f80ed"
        self.accent_hover = "#4c97f2"

        self.live = "#e63946"

        self.root.configure(bg=self.bg)

        # ====================================================
        # DATA
        # ====================================================

        self.games = []

        # Currently selected calendar date
        self.selected_date = date.today()

        # Month currently displayed
        self.display_year = self.selected_date.year
        self.display_month = self.selected_date.month

        # Load personal/calendar events
        self.events = self.load_calendar_events()

        # ====================================================
        # HEADER
        # ====================================================

        self.header = tk.Frame(
            root,
            bg=self.panel,
            height=75
        )

        self.header.pack(fill="x")

        self.header.pack_propagate(False)

        self.logo_label = tk.Label(
            self.header,
            text="SPORTS CENTRAL",
            font=("Segoe UI", 24, "bold"),
            fg=self.text,
            bg=self.panel
        )

        self.logo_label.pack(
            side="left",
            padx=25
        )

        self.live_label = tk.Label(
            self.header,
            text="● LIVE",
            font=("Segoe UI", 11, "bold"),
            fg=self.live,
            bg=self.panel
        )

        self.live_label.pack(
            side="left",
            padx=10
        )

        self.time_label = tk.Label(
            self.header,
            text="",
            font=("Segoe UI", 11),
            fg=self.muted,
            bg=self.panel
        )

        self.time_label.pack(
            side="right",
            padx=25
        )

        self.settings_button = tk.Button(
            self.header,
            text="⚙",
            font=("Segoe UI", 10, "bold"),
            fg=self.text,
            bg = self.panel_alt,
            activebackground=self.accent,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_settings
        )

        self.settings_button.pack(
            side="right",
            padx=(5, 15),
            pady=18
        )

        # ====================================================
        # MAIN CONTENT AREA
        # ====================================================

        self.content = tk.Frame(
            root,
            bg=self.bg
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Month calendar
        self.content.columnconfigure(
            0,
            weight=3,
            uniform="main"
        )

        # Week schedule
        self.content.columnconfigure(
            1,
            weight=3,
            uniform="main"
        )

        # Photos
        self.content.columnconfigure(
            2,
            weight=5,
            uniform="main"
        )

        self.content.rowconfigure(
            0,
            weight=1
        )

        # ====================================================
        # MONTH CALENDAR CARD
        # ====================================================

        self.calendar_card = tk.Frame(
            self.content,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.calendar_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # Calendar header
        self.calendar_header = tk.Frame(
            self.calendar_card,
            bg=self.panel
        )

        self.calendar_header.pack(
            fill="x",
            padx=15,
            pady=(15, 5)
        )

        self.previous_month_button = tk.Button(
            self.calendar_header,
            text="‹",
            command=self.previous_month,
            font=("Segoe UI", 18, "bold"),
            fg=self.text,
            bg=self.panel_alt,
            activebackground=self.accent,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            width=2,
            cursor="hand2"
        )

        self.previous_month_button.pack(
            side="left"
        )

        self.calendar_title = tk.Label(
            self.calendar_header,
            text="",
            font=("Segoe UI", 16, "bold"),
            fg=self.text,
            bg=self.panel
        )

        self.calendar_title.pack(
            side="left",
            expand=True
        )

        self.next_month_button = tk.Button(
            self.calendar_header,
            text="›",
            command=self.next_month,
            font=("Segoe UI", 18, "bold"),
            fg=self.text,
            bg=self.panel_alt,
            activebackground=self.accent,
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            width=2,
            cursor="hand2"
        )

        self.next_month_button.pack(
            side="right"
        )

        # Actual calendar grid
        self.calendar_grid = tk.Frame(
            self.calendar_card,
            bg=self.panel
        )

        self.calendar_grid.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(5, 15)
        )

        # ====================================================
        # WEEK VIEW CARD
        # ====================================================

        self.week_card = tk.Frame(
            self.content,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.week_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        self.week_header = tk.Frame(
            self.week_card,
            bg=self.panel
        )

        self.week_header.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        self.week_title = tk.Label(
            self.week_header,
            text="THIS WEEK",
            font=("Segoe UI", 17, "bold"),
            fg=self.text,
            bg=self.panel
        )

        self.week_title.pack(
            side="left"
        )

        self.week_range_label = tk.Label(
            self.week_header,
            text="",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.panel
        )

        self.week_range_label.pack(
            side="right"
        )

        # ----------------------------------------------------
        # Scrollable week view
        # ----------------------------------------------------

        self.week_canvas = tk.Canvas(
            self.week_card,
            bg=self.panel,
            highlightthickness=0
        )

        self.week_scrollbar = tk.Scrollbar(
            self.week_card,
            orient="vertical",
            command=self.week_canvas.yview
        )

        self.week_canvas.configure(
            yscrollcommand=self.week_scrollbar.set
        )

        self.week_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.week_canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=(0, 15)
        )

        self.week_inner = tk.Frame(
            self.week_canvas,
            bg=self.panel
        )

        self.week_window = self.week_canvas.create_window(
            (0, 0),
            window=self.week_inner,
            anchor="nw"
        )

        self.week_inner.bind(
            "<Configure>",
            self.update_week_scrollregion
        )

        self.week_canvas.bind(
            "<Configure>",
            self.resize_week_frame
        )

        # ====================================================
        # PHOTO CARD
        # ====================================================

        self.photo_card = tk.Frame(
            self.content,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        self.photo_card.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

        # Prevent photo contents from influencing overall layout
        self.photo_card.grid_propagate(False)
        self.photo_card.pack_propagate(False)

        self.photo_header = tk.Frame(
            self.photo_card,
            bg=self.panel
        )

        self.photo_header.pack(
            fill="x",
            padx=20,
            pady=(15, 10)
        )

        tk.Label(
            self.photo_header,
            text="FEATURED",
            font=("Segoe UI", 17, "bold"),
            fg=self.text,
            bg=self.panel
        ).pack(
            side="left"
        )

        self.photo_status = tk.Label(
            self.photo_header,
            text="Rotating Gallery",
            font=("Segoe UI", 9),
            fg=self.muted,
            bg=self.panel
        )

        self.photo_status.pack(
            side="right"
        )

        self.image_container = tk.Frame(
            self.photo_card,
            bg=self.panel_alt
        )

        self.image_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.image_container.pack_propagate(False)

        self.image_label = tk.Label(
            self.image_container,
            bg=self.panel_alt
        )

        self.image_label.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # SCORE TICKER
        # ====================================================

        self.ticker_frame = tk.Frame(
            root,
            bg="#08090c",
            height=65
        )

        self.ticker_frame.pack(
            fill="x",
            side="bottom"
        )

        self.ticker_frame.pack_propagate(False)

        self.ticker_tag = tk.Label(
            self.ticker_frame,
            text="LIVE SCORES",
            bg=self.accent,
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20
        )

        self.ticker_tag.pack(
            side="left",
            fill="y"
        )

        self.ticker_canvas = tk.Canvas(
            self.ticker_frame,
            bg="#08090c",
            height=65,
            highlightthickness=0
        )

        self.ticker_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.ticker_text = self.ticker_canvas.create_text(
            0,
            32,
            text="Loading live scores...",
            fill=self.text,
            font=("Segoe UI", 13, "bold"),
            anchor="w"
        )

        # ====================================================
        # LOAD IMAGES
        # ====================================================

        self.image_folder = "images"

        self.images = []

        if os.path.exists(self.image_folder):

            for file in os.listdir(
                self.image_folder
            ):

                if file.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".webp"
                    )
                ):

                    self.images.append(
                        os.path.join(
                            self.image_folder,
                            file
                        )
                    )

        # ====================================================
        # START DASHBOARD
        # ====================================================

        self.update_clock()

        self.build_calendar()

        self.build_week_view()

        self.rotate_image()

        self.update_scores()

        self.scroll_ticker()

    # ========================================================
    # SAMPLE CALENDAR EVENTS
    # ========================================================

    def load_calendar_events(self):

        from datetime import date, timedelta

        start_date = date.today() - timedelta(days=90)
        end_date = date.today() + timedelta(days=90)

        try:
            return get_apple_events(start_date, end_date)
        except Exception as error:
            print(f"Error loading calendar events: {error}")
            return []

    # ========================================================
    # CLOCK
    # ========================================================

    def update_clock(self):

        now = datetime.now()

        self.time_label.config(
            text=now.strftime(
                "%A, %B %d   •   %I:%M:%S %p"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )

    # ========================================================
    # SPORTS SCORES
    # ========================================================

    def update_scores(self):

        self.games = load_all_games()

        ticker_parts = []

        for game in self.games:

            ticker_parts.append(
                f"{game['league']}   "
                f"{game['away_abbr']} "
                f"{game['away_score']}  -  "
                f"{game['home_score']} "
                f"{game['home_abbr']}   "
                f"{game['detail']}"
            )

        if ticker_parts:

            ticker = "     ◆     ".join(
                ticker_parts
            )

        else:
            ticker = "No games currently available"

        self.ticker_canvas.itemconfig(
            self.ticker_text,
            text=ticker
        )


        refresh_ms = self.settings.get("score_refresh_seconds", 30) * 1000
        self.root.after(
            refresh_ms,
            self.update_scores
        )

    # ========================================================
    # SCROLL SCORE TICKER
    # ========================================================

    def scroll_ticker(self):

        self.ticker_canvas.move(
            self.ticker_text,
            -2,
            0
        )

        bbox = self.ticker_canvas.bbox(
            self.ticker_text
        )

        if bbox:

            if bbox[2] < 0:

                width = (
                    self.ticker_canvas.winfo_width()
                )

                self.ticker_canvas.coords(
                    self.ticker_text,
                    width,
                    32
                )

        self.root.after(
            20,
            self.scroll_ticker
        )

    # ========================================================
    # PREVIOUS MONTH
    # ========================================================

    def previous_month(self):

        self.display_month -= 1

        if self.display_month < 1:

            self.display_month = 12
            self.display_year -= 1

        self.build_calendar()

    # ========================================================
    # NEXT MONTH
    # ========================================================

    def next_month(self):

        self.display_month += 1

        if self.display_month > 12:

            self.display_month = 1
            self.display_year += 1

        self.build_calendar()

    # ========================================================
    # BUILD MONTH CALENDAR
    # ========================================================

    def build_calendar(self):

        # Delete old calendar tiles
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()

        month_name = calendar.month_name[
            self.display_month
        ]

        self.calendar_title.config(
            text=f"{month_name} {self.display_year}"
        )

        weekdays = [
            "MON",
            "TUE",
            "WED",
            "THU",
            "FRI",
            "SAT",
            "SUN"
        ]

        for column, weekday in enumerate(
            weekdays
        ):

            self.calendar_grid.columnconfigure(
                column,
                weight=1
            )

            tk.Label(
                self.calendar_grid,
                text=weekday,
                font=("Segoe UI", 8, "bold"),
                fg=self.muted,
                bg=self.panel
            ).grid(
                row=0,
                column=column,
                sticky="nsew",
                pady=(0, 5)
            )

        month_weeks = calendar.monthcalendar(
            self.display_year,
            self.display_month
        )

        row = 1

        for week in month_weeks:

            self.calendar_grid.rowconfigure(
                row,
                weight=1
            )

            for column, day in enumerate(
                week
            ):

                if day == 0:

                    blank = tk.Frame(
                        self.calendar_grid,
                        bg=self.panel
                    )

                    blank.grid(
                        row=row,
                        column=column,
                        sticky="nsew",
                        padx=2,
                        pady=2
                    )

                    continue

                current_date = date(
                    self.display_year,
                    self.display_month,
                    day
                )

                event_count = self.events_on_day(
                    current_date
                )

                is_today = (
                    current_date == date.today()
                )

                is_selected = (
                    current_date
                    == self.selected_date
                )

                if is_selected:
                    tile_color = self.accent

                elif is_today:
                    tile_color = "#315b88"

                else:
                    tile_color = self.panel_alt

                tile = tk.Frame(
                    self.calendar_grid,
                    bg=tile_color,
                    highlightbackground=self.border,
                    highlightthickness=1,
                    cursor="hand2"
                )

                tile.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )

                date_label = tk.Label(
                    tile,
                    text=str(day),
                    font=("Segoe UI", 11, "bold"),
                    fg=self.text,
                    bg=tile_color,
                    cursor="hand2"
                )

                date_label.pack(
                    pady=(7, 1)
                )

                if event_count > 0:

                    event_label = tk.Label(
                        tile,
                        text=(
                            f"● {event_count}"
                            if event_count > 1
                            else "●"
                        ),
                        font=("Segoe UI", 8),
                        fg=(
                            "white"
                            if is_selected
                            else self.accent_hover
                        ),
                        bg=tile_color,
                        cursor="hand2"
                    )

                    event_label.pack()

                else:

                    spacer = tk.Label(
                        tile,
                        text="",
                        bg=tile_color
                    )

                    spacer.pack()

                # Make entire tile clickable
                tile.bind(
                    "<Button-1>",
                    lambda event,
                    selected=current_date:
                    self.select_date(selected)
                )

                date_label.bind(
                    "<Button-1>",
                    lambda event,
                    selected=current_date:
                    self.select_date(selected)
                )

                for child in tile.winfo_children():

                    child.bind(
                        "<Button-1>",
                        lambda event,
                        selected=current_date:
                        self.select_date(selected)
                    )

            row += 1

    # ========================================================
    # SELECT DATE
    # ========================================================

    def select_date(self, selected_date):

        self.selected_date = selected_date

        self.display_year = selected_date.year
        self.display_month = selected_date.month

        self.build_calendar()

        self.build_week_view()

    # ========================================================
    # EVENTS ON A DATE
    # ========================================================

    def events_on_day(self, target_date):

        count = 0

        for event in self.events:

            if event["start"].date() == target_date:
                count += 1

        return count

    # ========================================================
    # EVENTS FOR DATE
    # ========================================================

    def get_events_for_date(
        self,
        target_date
    ):

        day_events = []

        for event in self.events:

            if event["start"].date() == target_date:

                day_events.append(
                    event
                )

        day_events.sort(
            key=lambda event:
            event["start"]
        )

        return day_events

    # ========================================================
    # BUILD WEEK VIEW
    # ========================================================

    def build_week_view(self):

        # Remove existing week items
        for widget in self.week_inner.winfo_children():
            widget.destroy()

        # Find Monday containing selected date
        monday = (
            self.selected_date
            - timedelta(
                days=self.selected_date.weekday()
            )
        )

        sunday = monday + timedelta(
            days=6
        )

        self.week_range_label.config(
            text=(
                f"{monday.strftime('%b %d')} - "
                f"{sunday.strftime('%b %d')}"
            )
        )

        for day_number in range(7):

            current_date = (
                monday
                + timedelta(
                    days=day_number
                )
            )

            day_events = (
                self.get_events_for_date(
                    current_date
                )
            )

            # --------------------------------------------
            # Day header
            # --------------------------------------------

            day_header = tk.Frame(
                self.week_inner,
                bg=self.panel_alt
            )

            day_header.pack(
                fill="x",
                pady=(0, 5)
            )

            if (
                current_date
                == self.selected_date
            ):

                header_bg = self.accent

                day_header.config(
                    bg=header_bg
                )

            else:

                header_bg = self.panel_alt

            tk.Label(
                day_header,
                text=current_date.strftime(
                    "%A"
                ).upper(),
                font=("Segoe UI", 10, "bold"),
                fg=self.text,
                bg=header_bg
            ).pack(
                side="left",
                padx=10,
                pady=6
            )

            tk.Label(
                day_header,
                text=current_date.strftime(
                    "%b %d"
                ),
                font=("Segoe UI", 9),
                fg=(
                    "white"
                    if current_date
                    == self.selected_date
                    else self.muted
                ),
                bg=header_bg
            ).pack(
                side="right",
                padx=10
            )

            # --------------------------------------------
            # No events
            # --------------------------------------------

            if not day_events:

                tk.Label(
                    self.week_inner,
                    text="No events",
                    font=("Segoe UI", 9),
                    fg=self.muted,
                    bg=self.panel,
                    anchor="w"
                ).pack(
                    fill="x",
                    padx=12,
                    pady=(2, 10)
                )

            # --------------------------------------------
            # Events
            # --------------------------------------------

            else:

                for event in day_events:

                    event_card = tk.Frame(
                        self.week_inner,
                        bg="#20242c",
                        highlightbackground=self.border,
                        highlightthickness=1
                    )

                    event_card.pack(
                        fill="x",
                        padx=5,
                        pady=(2, 7)
                    )

                    if event.get("all_day"):
                        time_text = "All Day"
                    else:
                        time_text = (
                            f"{event['start'].strftime('%I:%M %p')} - "
                            f"{event['end'].strftime('%I:%M %p')}"
                        )

                    tk.Label(
                        event_card,
                        text=time_text,
                        font=("Segoe UI", 8, "bold"),
                        fg=self.accent_hover,
                        bg="#20242c",
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=10,
                        pady=(8, 2)
                    )

                    tk.Label(
                        event_card,
                        text=event["title"],
                        font=("Segoe UI", 11, "bold"),
                        fg=self.text,
                        bg="#20242c",
                        anchor="w"
                    ).pack(
                        fill="x",
                        padx=10
                    )

                    location = event.get(
                        "location",
                        ""
                    )

                    if location:

                        tk.Label(
                            event_card,
                            text=location,
                            font=("Segoe UI", 8),
                            fg=self.muted,
                            bg="#20242c",
                            anchor="w"
                        ).pack(
                            fill="x",
                            padx=10,
                            pady=(2, 8)
                        )

        # Return week view to top
        self.week_canvas.yview_moveto(0)

    # ========================================================
    # WEEK SCROLL REGION
    # ========================================================

    def update_week_scrollregion(
        self,
        event=None
    ):

        self.week_canvas.configure(
            scrollregion=(
                self.week_canvas.bbox("all")
            )
        )

    # ========================================================
    # WEEK FRAME WIDTH
    # ========================================================

    def resize_week_frame(
        self,
        event
    ):

        self.week_canvas.itemconfig(
            self.week_window,
            width=event.width
        )

    # ========================================================
    # ROTATE PHOTOS
    # ========================================================

    def rotate_image(self):

        if self.images:

            image_path = random.choice(
                self.images
            )

            image = Image.open(
                image_path
            )

            # Get available display dimensions
            width = (
                self.image_container.winfo_width()
            )

            height = (
                self.image_container.winfo_height()
            )

            # Window may not have rendered yet
            if width < 100:
                width = 650

            if height < 100:
                height = 500

            # Force every image into the same display size
            # while preserving aspect ratio by cropping
            image = ImageOps.fit(
                image,
                (width, height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )

            photo = ImageTk.PhotoImage(
                image
            )

            self.image_label.config(
                image=photo,
                text=""
            )

            self.image_label.image = photo

            self.photo_status.config(
                text=os.path.basename(
                    image_path
                )
            )

        else:

            self.image_label.config(
                image="",
                text=(
                    "Add images to the\n"
                    "'images' folder"
                ),
                fg=self.muted,
                font=("Segoe UI", 16),
                bg=self.panel_alt
            )
        rotation_ms = self.settings.get("image_rotation_seconds", 5) * 1000
        self.root.after(
            rotation_ms,
            self.rotate_image
        )

    # ========================================================
    # OPEN SETTINGS WINDOW
    # ========================================================
    def open_settings(self):
        
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("550x700")
        settings_window.configure(bg=self.bg)
        settings_window.transient(self.root)
        settings_window.grab_set()

        settings = self.settings

        canvas = tk.Canvas(
            settings_window,
            bg=self.bg,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            settings_window,
            orient="vertical",
            command=canvas.yview
        )

        settings_frame = tk.Frame(
            canvas,
            bg=self.bg
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=settings_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        settings_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfig(
                canvas_window,
                width=event.width
            )
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        def mouse_scroll(event):
            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        canvas.bind_all(
            "<MouseWheel>",
            mouse_scroll
        )

        def close_settings():
            canvas.unbind_all("<MouseWheel>")
            settings_window.destroy()
        settings_window.protocol("WM_DELETE_WINDOW", close_settings)

        #Title
        tk.Label(
            settings_frame,
            text="Settings",
            font=("Segoe UI", 24, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack(pady=(25,20))

        #Sports
        tk.Label(
            settings_frame,
            text="Sports",
            font=("Segoe UI", 15, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack(
            anchor="w",
            padx=40,
            pady=(10, 5)
        )
        sport_frame = tk.Frame(
            settings_frame,
            bg=self.panel
        )

        sport_frame.pack(
            fill="x",
            padx=40,
            pady=5
        )

        available_sports = [
            "MLB",
            "NBA",
            "NFL",
            "NHL",
            "NCAA",
            "NCAAM",
            "NCAA Baseball"
        ]

        selected_sports = self.settings.get("sports", [])

        sport_vars = {}

        for sport in available_sports:
            var = tk.BooleanVar(value=sport in selected_sports)
            sport_vars[sport] = var
            checkbox = tk.Checkbutton(
                sport_frame,
                text=sport,
                variable=var,
                font=("Segoe UI", 10),
                fg=self.text,
                bg=self.panel,
                selectcolor=self.panel_alt,
                activebackground=self.panel,
                activeforeground=self.text
            )

            checkbox.pack(
                anchor="w",
                padx=15,
                pady=3
            )

        # ============================================================
        # UPLOAD IMAGES BUTTON
        # ============================================================
        tk.Label(
            settings_frame,
            text="Photo Folder",
            font=("Segoe UI", 15, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack(
            anchor="w",
            padx=40,
            pady=(20, 5)
        )
        photo_folder_var = tk.StringVar(value=settings.get("image_folder", "images"))

        photo_entry = tk.Entry(
            settings_frame,
            textvariable=photo_folder_var,
            width=45
        )
        photo_entry.pack(padx=40, pady=5)

        def choose_folder():
            folder = filedialog.askdirectory()
            if folder:
                photo_folder_var.set(folder)

        tk.Button(
            settings_frame,
            text="Choose Folder",
            command=choose_folder,
        ).pack(pady=5)

        #Score Refresh
        tk.Label(
            settings_frame,
            text="Score Refresh (seconds):",
            font=("Segoe UI", 15, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack(
            anchor="w",
            padx=40,
            pady=(25,5)
        )

        score_refresh_var = tk.IntVar(value=settings.get("score_refresh_seconds", 30))

        tk.Spinbox(
            settings_frame,
            from_=10,
            to=300,
            textvariable=score_refresh_var
        ).pack(pady=5)

        tk.Label(
            settings_frame,
            text="Photo Rotation (seconds):",
            font=("Segoe UI", 15, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack(
            anchor="w",
            pady=(15,0)
        )

        photo_rotation_var = tk.IntVar(value=settings.get("image_rotation_seconds", 5))

        tk.Spinbox(
            settings_frame,
            from_=2,
            to=50,
            textvariable=photo_rotation_var
        ).pack(pady=5)

        # ============================================================
        # SAVE BUTTON
        # ============================================================    
        
        def save():
            selected = []
        
            for sport, var in sport_vars.items():
                if var.get():
                    selected.append(sport)
                self.settings["sports"] = selected
                self.settings["image_folder"] = photo_folder_var.get()
                self.settings["image_rotation_seconds"] = photo_rotation_var.get()
                self.settings["score_refresh_seconds"] = score_refresh_var.get()
                save_settings(self.settings)
                close_settings()                
                tk.Button(
                    settings_frame,
                    text="Save",
                    command=save,
                    font=("Segoe UI", 11, "bold"),
                    fg="white",
                    bg=self.accent,
                    activebackground=self.accent_hover,
                    activeforeground="white",
                    relief="flat",
                    borderwidth=0,
                    cursor="hand2",
                    padx=20,
                    pady=8
                ).pack(
                    pady=30
                )


# ============================================================
# RUN PROGRAM
# ============================================================

root = tk.Tk()
root.title("Sports Central")

settings = load_settings()


def start_dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    root.deiconify()

    SportsDashboard(root)


if not settings.get("apple_email"):

    root.withdraw()

    def setup_complete():
        root.deiconify()
        start_dashboard()

    setup = SetupWindow(
        root,
        setup_complete
    )
    settings["setup_complete"] = True
    save_settings(settings)
    setup.window.deiconify()

else:
    start_dashboard()


root.mainloop()
root.mainloop()
