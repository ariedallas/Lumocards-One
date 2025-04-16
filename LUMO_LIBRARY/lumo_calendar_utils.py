import calendar
import datetime
import os
import subprocess
import sys
from pprint import pprint as pp
from selectors import SelectSelector

import dateutil.tz
from dateutil.relativedelta import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
import LUMO_LIBRARY.lumo_newcard_2 as l_newcard

SCOPES = ["https://www.googleapis.com/auth/calendar"]
creds_file = os.path.join(l_files.credentials_folder, "credentials.json")
token_file = os.path.join(l_files.credentials_folder, "token.json")

cal = calendar.Calendar()
curr_year, curr_month, curr_day = l_files.today.year, l_files.today.month, l_files.today.day
monthdays = [d for d in cal.itermonthdays(year=curr_year, month=curr_month) if d != 0]
curr_month_max = calendar.monthrange(year=curr_year, month=curr_month)[1]
today_date = datetime.date.today()
tz_local = dateutil.tz.gettz("America/Los_Angeles")


def get_creds():
    creds = None

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds


def get_google_event_by_id(credentials, id):
    try:
        service = build("calendar", "v3", credentials=credentials)

        event_result = (service.events().get(
            calendarId="primary"
            , eventId=id)
                        .execute())

        return event_result

    except HttpError as error:
        print("Nothing")
        print("An error has occurred ", error)
        return None


def get_google_events(credentials, time_min, time_max):
    page_token = None

    try:
        service = build("calendar", "v3", credentials=credentials)

        start = datetime.datetime(year=time_min.year, month=time_min.month, day=time_min.day).isoformat() + "Z"
        end = datetime.datetime(year=time_max.year, month=time_max.month, day=time_max.day).isoformat() + "Z"

        event_result = service.events().list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token
        ).execute()

        events = event_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        return events

    except HttpError as error:
        print("Nothing")
        print("An error has occurred ", error)
        return None


def get_google_event_service(credentials, time_min, time_max):
    page_token = None

    try:
        service = build("calendar", "v3", credentials=credentials)

        start = datetime.datetime(year=time_min.year, month=time_min.month, day=time_min.day).isoformat() + "Z"
        end = datetime.datetime(year=time_max.year, month=time_max.month, day=time_max.day).isoformat() + "Z"

        event_result = service.events().list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token
        ).execute()

        if not event_result:
            print("No upcoming events found.")
            return

        return event_result

    except HttpError as error:
        print("Nothing")
        print("An error has occurred ", error)
        return None


def get_google_events_for_times(credentials, time_min, time_max):
    google_month_events = get_google_events(credentials=credentials,
                                            time_min=time_min,
                                            time_max=time_max)

    return google_month_events


def update_event(credentials):
    try:

        service = build("calendar", "v3", credentials=credentials)

        retrieved_id_from_txt = "4v39giucjk61s9q23koofhfekd"

        event = service.events().get(calendarId="primary",
                                     eventId=retrieved_id_from_txt).execute()
        print()
        print("FROM UPDATER FUNCTION")
        print(f"ID {retrieved_id_from_txt} makes ->", event.get("summary"))

        event["colorId"] = 1
        # event["summary"] = "Desiree + Arie Continue to Collab on Little Ditty"

        updated_event = service.events().update(calendarId="primary", eventId=event["id"], body=event).execute()

        google_id = event["id"]
        return google_id


    except HttpError as error:
        print("An error happened: ", error)


def delete_event_from_google(credentials, var_id):
    try:
        service = build("calendar", "v3", credentials=credentials)
        service.events().delete(calendarId="primary", eventId=var_id).execute()

    except HttpError as error:
        print("This event was (likely) already deleted.")
        print(error)


def delete_calendar_card(credentials, card_filename):
    json_data = l_json_utils.read_and_get_json_data(card_filename)
    calendar_card_id = json_data["google calendar data"]["id"]

    delete_event_from_google(credentials, calendar_card_id)

    l_card_utils.card_deleter(card_filename)

    l_animators.animate_text("The card was deleted from the external (Google) calendar.")
    l_animators.animate_text("This Lumo card is deleted.")


def dt_to_time(dt_obj, format):
    if format == "military":
        return datetime.datetime.strftime(dt_obj, "%H:%M")
    elif format == "standard":
        return datetime.datetime.strftime(dt_obj, "%I:%M%p")
    else:
        return datetime.datetime.strftime(dt_obj, "%I:%M%p")


def times_formatter(event_obj, format):
    if event_obj.event_type == "EMPTY EVENT":
        space = " " * 7
        formatted = f"{space} - {space}"


    elif event_obj.event_type == "ALL DAY" or \
            event_obj.event_type == "MULTI DAY":

        formatted = "{0:^{width}}".format("all day", width=17)

    else:  # event_type == "standard"
        start = dt_to_time(event_obj.s, format)
        end = dt_to_time(event_obj.e, format)

        if format == "military":
            start_format = f" {start} "
            end_format = f" {end} "
        else:  # standard time
            start_format = start if len(start) == 7 else f" {start}"
            end_format = end if len(end) == 7 else f" {end}"

        formatted = f"{start_format} - {end_format}"

    return formatted


def military_to_standard(military_time):
    standard_converted = datetime.datetime.strptime(military_time, "%H:%M")
    standard_time_formatted = standard_converted.strftime("%I:%M%p")
    return standard_time_formatted.title()


def standard_to_military(standard_time):
    military_converted = datetime.datetime.strptime(standard_time, "%I:%M%p")
    military_formatted = military_converted.strftime("%H:%M")
    print(military_formatted)


def percenter(percentage, number):
    perc_as_dec = percentage / 100
    return round(number * perc_as_dec)


def is_odd(num):
    return not num % 2 == 0


def parse_brackets(var_input):
    if "]" in var_input:
        return var_input.count("]"), "PAGE RIGHT"
    elif "[" in var_input:
        return (var_input.count("[")), "PAGE LEFT"
    else:
        return 0, None


def get_nearest_recent_monday(dt):
    amt = dt.weekday()
    return dt - relativedelta(days=amt)


def get_time_window_1(var_date, window_size_weeks):
    window_size_weeks = window_size_weeks if is_odd(window_size_weeks) else (window_size_weeks + 1)

    non_current_weeks = window_size_weeks - 1
    max_look_behind = round(non_current_weeks / 2)
    max_look_behind_days = max_look_behind * 7
    window_size_days = (window_size_weeks * 7) - 1

    nearest_monday = get_nearest_recent_monday(var_date)
    window_start = nearest_monday - relativedelta(days=max_look_behind_days)
    window_end = window_start + relativedelta(days=window_size_days)

    return window_start, window_end


def get_time_window_2(var_date: datetime.date,
                      window_size_weeks: int):
    window_size_days = (window_size_weeks * 7) - 1

    window_start = get_nearest_recent_monday(var_date)
    window_end = window_start + relativedelta(days=window_size_days)

    return window_start, window_end


def fill_time_window_dates(window_start, window_end):
    delta = window_end - window_start
    window_size_days = delta.days + 1

    time_window = []
    for d in range(window_size_days):
        next_day = window_start + relativedelta(days=d)
        time_window.append(next_day)

    return time_window


def google_event_to_obj(event):
    """Determine type of event: all-day, standard, recurring"""

    summary = event["summary"]

    s_dt_google = event["start"].get("dateTime")
    s_date_google = event["start"].get("date")

    e_dt_google = event["end"].get("dateTime")
    e_date_google = event["end"].get("date")

    if s_dt_google:
        s_dt_python = datetime.datetime.strptime(s_dt_google, "%Y-%m-%dT%H:%M:%S%z")
        e_dt_python = datetime.datetime.strptime(e_dt_google, "%Y-%m-%dT%H:%M:%S%z")

        is_multi_day = e_dt_python.day > s_dt_python.day
        if is_multi_day:
            event_type = "MULTI DAY"
        else:
            event_type = "STANDARD"

    elif s_date_google:
        s_date_python = datetime.datetime.strptime(s_date_google, "%Y-%m-%d")
        e_date_python = datetime.datetime.strptime(e_date_google, "%Y-%m-%d")

        event_type = "ALL DAY"

    if event_type == "STANDARD":
        event_obj = Event.from_dt(s_dt_python,
                                  e_dt_python,
                                  summary,
                                  event_type)

    elif event_type == "ALL DAY":
        event_obj = Event.from_date(s_date_python,
                                    e_date_python,
                                    summary,
                                    event_type)

    elif event_type == "MULTI DAY":
        event_obj = Event.from_dt(s_dt_python,
                                  e_dt_python,
                                  summary,
                                  event_type)
    return event_obj


def get_adjacent_month(base_month, base_year, direction, months_distance):
    if direction == "past":
        adjacent = datetime.date(day=1, month=base_month, year=base_year) - relativedelta(months=months_distance)
    elif direction == "next":
        adjacent = datetime.date(day=1, month=base_month, year=base_year) + relativedelta(months=months_distance)
    else:
        adjacent = datetime.date(day=1, month=base_month, year=base_year)

    return adjacent


def get_local_calendar_cards(window_start, window_end):
    calendar_cards_found = []
    dt_window_start = datetime.datetime(window_start.year, window_start.month, window_start.day, tzinfo=tz_local)
    dt_window_end = datetime.datetime(window_end.year, window_end.month, window_end.day, tzinfo=tz_local)

    for card in os.listdir(l_files.cards_calendar_folder):
        json_data = l_json_utils.read_and_get_json_data(card)
        dt_google_start = json_data["google calendar data"]["start"]["dateTime"]
        dt_python_start = datetime.datetime.strptime(dt_google_start, "%Y-%m-%dT%H:%M:%S%z")
        within_window = dt_window_start <= dt_python_start <= dt_window_end
        calendar_cards_found.append(card) if within_window else None

    return calendar_cards_found

    # start time > specified start and start time < specified end


def get_day_blocks(var_date=today_date, time_min=None, time_max=None):
    creds = get_creds()

    if time_min and time_max:
        window_start, window_end = time_min, time_max
    else:
        window_start, window_end = get_time_window_1(var_date, 13)

    google_month_events = get_google_events(creds, time_min=window_start, time_max=window_end)

    converted_events = [google_event_to_obj(e) for e in google_month_events]

    day_blocks = []

    window = fill_time_window_dates(window_start, window_end)
    for date in window:
        """Transform whatever events are found from Google into a full list where every day has a placeholder
         Adds an empty list if no Google events exist for date."""
        matched_events = [obj for obj in converted_events if
                          (obj.get_date() == date or obj.spans(date))]
        day_block = DayBlock.from_date(date, matched_events)
        day_blocks.append(day_block)

    return day_blocks


class Event:
    def __init__(self,
                 summary,
                 event_type):
        self.s_date = None
        self.e_date = None
        self.s = None
        self.e = None
        self.summary = summary
        self.event_type = event_type


    def get_date(self):
        if self.event_type == "ALL DAY":
            return self.s_date

        else:  # self.event_type is "multi day" or "standard"
            return self.s.date()


    def spans(self, var_date):
        if self.s_date and self.e_date:
            return self.s_date.date() <= var_date <= self.e_date.date()


    @classmethod
    def from_date(cls,
                  s_date,
                  e_date,
                  summary,
                  event_type):
        event_obj = Event(summary,
                          event_type)

        event_obj.s_date = s_date
        event_obj.e_date = e_date

        return event_obj


    @classmethod
    def from_dt(cls,
                s,
                e,
                summary,
                event_type):
        event_obj = Event(summary,
                          event_type)

        event_obj.s = s
        event_obj.e = e

        return event_obj


class DayBlock:
    def __init__(self, day, dayname, date, events):
        self.day = day
        self.dayname = dayname
        self.date = date
        self.events = events


    @classmethod
    def from_date(cls, var_datetime, events):
        day = var_datetime.day
        day_int = var_datetime.weekday()
        dayname = calendar.Day(day_int).name
        date = var_datetime

        return DayBlock(day, dayname, date, events)


    @staticmethod
    def list_safe_get_item(var_list, idx):
        if len(var_list) >= (idx + 1):
            return var_list[idx]
        else:
            return Event("--- --- ---",
                         "EMPTY EVENT")


class CalendarPageEvent:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)
    content_width = percenter(70, total_width)

    EVENTS_WIDTH = 86
    EVENTS_LINE = "-" * EVENTS_WIDTH
    l_margin_num = round((total_width - EVENTS_WIDTH) / 2) - 1
    l_margin_space = " " * l_margin_num
    l_margin_line = "-" * l_margin_num

    main_line = ("-" * content_width)

    EVENT_TIME = 14
    EVENTS_SELECTOR = 10
    EVENTS_SELECTOR_SPACE = " " * EVENTS_SELECTOR
    EVENTS_BODY = EVENTS_WIDTH - EVENTS_SELECTOR - EVENT_TIME

    MENU_ITEM_INDENT_NUDGE = EVENTS_SELECTOR + 2
    MENU_ITEM_INDENT_SPACE = " " * (MENU_ITEM_INDENT_NUDGE)

    cursor_indent_amt = l_margin_num + MENU_ITEM_INDENT_NUDGE + 3


    def __init__(self, var_event_obj):
        self.event_obj = var_event_obj


    def _row_event_header(self):
        title = f"EVENT: {self.event_obj.summary.upper()}"

        print()
        print("{0:^{width}}".format(title,
                                    width=CalendarPageDay.total_width))
        print()


    def display_event(self):
        self._row_event_header()
        print()
        print()


    def display_menu(self):
        menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.EVENT_MENU)

        wh_sp = CalendarPageDay.l_margin_space + CalendarPageDay.EVENTS_SELECTOR_SPACE
        whitespace_menu = Menus.add_whitespace_menu_list(menu_list, wh_sp)
        whitespace_exit = Menus.add_whitespace_menu_list(l_menus_data.EXIT_MENU_LIST, wh_sp)

        print()
        print(CalendarPageDay.l_margin_space + CalendarPageDay.EVENTS_SELECTOR_SPACE + "EVENT")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(whitespace_exit, indent_amt=2, speed_interval=0)


class CalendarPageDay:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)
    content_width = percenter(70, total_width)

    EVENTS_WIDTH = 86
    EVENTS_LINE = "-" * EVENTS_WIDTH
    l_margin_num = round((total_width - EVENTS_WIDTH) / 2) - 1
    l_margin_space = " " * l_margin_num
    l_margin_line = "-" * l_margin_num

    main_line = ("-" * content_width)

    EVENTS_TIME = 17
    EVENTS_SELECTOR = 10
    EVENTS_SELECTOR_SPACE = " " * EVENTS_SELECTOR
    EVENTS_BODY = EVENTS_WIDTH - EVENTS_SELECTOR - EVENTS_TIME

    MENU_ITEM_INDENT_NUDGE = EVENTS_SELECTOR + 2
    MENU_ITEM_INDENT_SPACE = " " * (MENU_ITEM_INDENT_NUDGE)

    cursor_indent_amt = l_margin_num + MENU_ITEM_INDENT_NUDGE + 3


    def __init__(self, var_dayblock):
        self.header_date = CalendarPageDay._format_date_for_header(var_dayblock.date)
        self.day_block = var_dayblock


    @staticmethod
    def _format_date_for_header(var_date):
        formatted = datetime.date.strftime(var_date, "%A: %B %d, %Y")
        return formatted


    def _row_cal_header(self):
        # under_line = ("-" * len(self.header_date))

        print()
        print("{0:^{width}}".format(self.header_date.upper(), width=CalendarPageDay.total_width))
        # print("{0:^{width}}".format(under_line, width=CalendarPageDay.total_width))
        print()
        print()


    @staticmethod
    def _row_style_event(var_sel, event_obj):
        summary_bullet = "• " + event_obj.summary

        selector = "{:<{width}}".format(var_sel, width=CalendarPageDay.EVENTS_SELECTOR)
        event = "{:<{width}}".format(summary_bullet, width=CalendarPageDay.EVENTS_BODY)
        time_info = times_formatter(event_obj, "military")

        group = selector + event + time_info
        print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))


    @staticmethod
    def _row_style_flexible(var_l, var_m, var_r):
        selector = "{:<{width}}".format(var_l, width=CalendarPageDay.EVENTS_SELECTOR)
        event = "{:<{width}}".format(var_m, width=CalendarPageDay.EVENTS_BODY)
        time_info = "{:<{width}}".format(var_r, width=CalendarPageDay.EVENTS_TIME)

        group = selector + event + time_info
        print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))


    @staticmethod
    def _row_style_menu_dict(var_sel, var_option):
        selector = f"[{var_sel}]  "

        print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT + selector + var_option)


    def display_day(self, events_limit, low):
        subprocess.run(["clear"], shell=True)
        self._row_cal_header()

        empty_event = Event("--- --- ---",
                            "EMPTY EVENT")

        for idx in range(events_limit):
            if idx < len(self.day_block.events):
                CalendarPageDay._row_style_event(f"[{idx + 1}]", self.day_block.events[idx])
            elif len(self.day_block.events) <= idx < low:
                CalendarPageDay._row_style_event(f"[{idx + 1}]", empty_event)

        total_e = len(self.day_block.events)
        remaining_e = 0 if total_e - events_limit <= 0 \
            else total_e - events_limit

        CalendarPageDay._row_style_flexible(" ",
                                            f"+ {remaining_e} more events",
                                            " ")
        print()


    def display_menu(self):
        TOGGLE_DICT = {"T": Menus.ACTION_TOGGLE_DAY}
        TOGGLE_MENU = [f"[{k}]  {v}" for k, v in TOGGLE_DICT.items()]

        menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.MAIN_CAL_MENU)

        wh_sp = CalendarPageDay.l_margin_space + CalendarPageDay.EVENTS_SELECTOR_SPACE
        whitespace_menu = Menus.add_whitespace_menu_list(menu_list, wh_sp)
        whitespace_toggle = Menus.add_whitespace_menu_list(TOGGLE_MENU, wh_sp)
        whitespace_quit = Menus.add_whitespace_menu_list(l_menus_data.QUIT_MENU_LIST, wh_sp)

        print()
        print(CalendarPageDay.l_margin_space + CalendarPageDay.EVENTS_SELECTOR_SPACE + "CALENDAR")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(whitespace_toggle, indent_amt=2, speed_interval=0)
        l_animators.list_printer(whitespace_quit, indent_amt=2, speed_interval=0)


    def display_menu_columns(self, var_dict):
        TOGGLE_DICT = {"T": Menus.ACTION_TOGGLE_DAY}
        TOGGLE_MENU = [f"[{k}]  {v}" for k, v in TOGGLE_DICT.items()]

        menu_list = l_menus_funcs.menu_list_from_dict(var_dict)
        menu_list_left = menu_list[:4]
        menu_list_right = menu_list[4:8]
        menu_columns = CalendarPageWeek.prep_menu_columns(menu_l=menu_list_left,
                                                          menu_r=menu_list_right)

        wh_sp = CalendarPageWeek.l_margin_menu_space
        whitespace_menu = Menus.add_whitespace_menu_list(menu_columns, wh_sp)
        whitespace_toggle = Menus.add_whitespace_menu_list(TOGGLE_MENU, wh_sp)
        whitespace_quit = Menus.add_whitespace_menu_list(l_menus_data.QUIT_MENU_LIST, wh_sp)

        print(CalendarPageWeek.l_margin_menu_space + "CALENDAR")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(whitespace_toggle, indent_amt=2, speed_interval=0)
        l_animators.list_printer(whitespace_quit, indent_amt=2, speed_interval=0)


    @staticmethod
    def valid_event_selection(user_input: str, max_ints: int) -> bool:
        if not l_card_utils.test_for_int(user_input):
            return False

        input_int = int(user_input)
        valid_range = range(1, max_ints + 1)

        if max_ints < input_int <= CalendarPageDay.EVENTS_DISPLAY_LIMIT:
            return False
        if input_int in valid_range:
            return True
        else:
            return False


class CalendarPageWeek:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)

    COL_SPACER = "        "
    COL_WIDTH = 60

    content_width = (2 * COL_WIDTH) + len(COL_SPACER)
    line = ("-" * content_width)

    margins_total = (total_width - content_width) / 2
    indent_margin = margins_total + (COL_WIDTH / 2)
    l_margin_menu = round(indent_margin)
    l_margin_menu_space = " " * int(l_margin_menu)


    def __init__(self, week_of_day_blocks):
        self.day_blocks = week_of_day_blocks
        self.header_date = CalendarPageWeek.get_header_date(week_of_day_blocks)


    @staticmethod
    def get_header_date(var_week_block):
        bucket_1 = []
        bucket_2 = []

        first, last = var_week_block[0], var_week_block[-1]

        if first.date.month == last.date.month:
            month_int = first.date.month

        else:
            for day_block in var_week_block:
                if day_block.date.month == first.date.month:
                    bucket_1.append(day_block.date.month)
                else:
                    bucket_2.append(day_block.date.month)

            larger_bucket = bucket_1 if len(bucket_1) > len(bucket_2) else bucket_2
            month_int = larger_bucket[0]

        header_month = (calendar.Month(month_int).name)
        return header_month


    def cal_header(self):
        print()
        # print("{0:^{width}}".format(CalendarPageDay.line, width=CalendarPageWeek.total_width))
        print("{0:^{width}}".format(self.header_date, width=CalendarPageWeek.total_width))
        print()


    @staticmethod
    def row_style_days(dates):
        dt_1, dt_2 = dates
        dt_1_frmt = "{:02d}".format(dt_1)
        dt_2_frmt = "{:02d}".format(dt_2)

        print("{0:-<{width}}".format(dt_1_frmt, width=CalendarPageWeek.COL_WIDTH)
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(dt_2_frmt, width=CalendarPageWeek.COL_WIDTH))


    @staticmethod
    def row_style_daynames(daynames):
        dayname_1, dayname_2 = daynames

        print("{0:-<{width}}".format(dayname_1, width=CalendarPageWeek.COL_WIDTH)
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(dayname_2, width=CalendarPageWeek.COL_WIDTH))


    @staticmethod
    def line_break():
        print()


    @staticmethod
    def row_style_event(event_1, event_2):
        summary_width = CalendarPageWeek.COL_WIDTH - 17

        summary_1, time_1 = event_1
        summary_2, time_2 = event_2

        print("{0:-<{width}}".format(summary_1, width=summary_width), time_1
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(summary_2, width=summary_width), time_2)

        print("{0:-<{width}}".format(summary_1, width=summary_width), time_1
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(summary_2, width=summary_width), time_2)

        print("{0:-<{width}}".format(summary_1, width=summary_width), time_1
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(summary_2, width=summary_width), time_2)


    @staticmethod
    def row_style_addnl_events(addnl_events_indicators):
        num_1, num_2 = addnl_events_indicators

        formatted_text_1 = "+ {} more events".format(num_1)
        formatted_text_2 = "+ {} more events".format(num_2)

        print("{0:>{width}}".format(formatted_text_1, width=CalendarPageWeek.COL_WIDTH)
              , CalendarPageWeek.COL_SPACER
              , "{0:>{width}}".format(formatted_text_2, width=CalendarPageWeek.COL_WIDTH))


    @staticmethod
    def half_row_style_day(day):
        day_frmt = "{:02d}".format(day)

        return "{0:<{width}}".format(day_frmt, width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def half_row_style_dayname(dayname):
        return "{0:-<{width}}".format(dayname, width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def half_row_style_addnl_events(num):
        formatted_text = "+ {} more events".format(num)

        return "{0:>{width}}".format(formatted_text, width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def half_row_style_editor_header():
        editor_header = ":::"
        editor_header_formatted = "{0:-^{width}}".format(editor_header, width=CalendarPageWeek.COL_WIDTH)
        return editor_header_formatted


    @staticmethod
    def half_row_style_event(event_obj):
        summary_width = CalendarPageWeek.COL_WIDTH - 17

        time_info = times_formatter(event_obj, format="military")

        return "{0:<{width}}".format(event_obj.summary, width=summary_width) + time_info


    @staticmethod
    def half_row_style_line_break():
        return "{0:<{width}}".format("", width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def half_row_style_line():
        return "{0:-<{width}}".format("", width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def half_row_style_menu(menu_item):
        return "  {0:<{width}}".format(menu_item, width=CalendarPageWeek.COL_WIDTH - 2)


    @staticmethod
    def prep_menu_columns(menu_l, menu_r):
        columnified = []

        if len(menu_r) < len(menu_l):
            diff = len(menu_l) - len(menu_r)
            for _ in range(diff):
                menu_r.append(" ")

        for l, r in zip(menu_l, menu_r):
            left_col = "{0:<{width}}".format(l, width=36)
            right_col = "{0:<{width}}".format(r, width=36)
            columnified.append(left_col + right_col)

        return columnified


    @staticmethod
    def make_editor_block_1():
        header = CalendarPageWeek.half_row_style_editor_header()
        summary = CalendarPageWeek.half_row_style_event([None, None, "20:00", "21:00", "Dinner with John"])
        br = CalendarPageWeek.half_row_style_line_break()
        menu_1 = CalendarPageWeek.half_row_style_menu("[A]  Complete card with no additional options")
        menu_2 = CalendarPageWeek.half_row_style_menu("[B]  Set recurring features")
        menu_3 = CalendarPageWeek.half_row_style_menu("[C]  Go back")
        menu_4 = CalendarPageWeek.half_row_style_menu("[X]  Exit")

        return [br
            , header
            , summary
            , br
            , menu_1, menu_2, menu_3
            , br
            , menu_4
                ]


    @staticmethod
    def make_editor_block_2():
        test_edited_event = Event.from_dt(
            datetime.datetime.now(),
            datetime.datetime.now(),
            "",
            event_type="EMPTY EVENT"
        )

        header = CalendarPageWeek.half_row_style_editor_header()
        summary = CalendarPageWeek.half_row_style_event(test_edited_event)
        br = CalendarPageWeek.half_row_style_line_break()

        return [br
            , header
            , br
            , br
            , br
            , br
            , br
            , br
            , br
                ]


    @staticmethod
    def format_day_block(day_block):
        event_obj_1 = DayBlock.list_safe_get_item(day_block.events, 0)
        event_obj_2 = DayBlock.list_safe_get_item(day_block.events, 1)
        event_obj_3 = DayBlock.list_safe_get_item(day_block.events, 2)
        addnl_event_num = len(day_block.events) - 3 if \
            len(day_block.events) > 3 else 0

        day = CalendarPageWeek.half_row_style_day(day_block.day)
        dayname = CalendarPageWeek.half_row_style_dayname(day_block.dayname)
        br = CalendarPageWeek.half_row_style_line_break()
        event_1_row = CalendarPageWeek.half_row_style_event(event_obj_1)
        event_2_row = CalendarPageWeek.half_row_style_event(event_obj_2)
        event_3_row = CalendarPageWeek.half_row_style_event(event_obj_3)
        addl_events = CalendarPageWeek.half_row_style_addnl_events(addnl_event_num)

        return [day
            , dayname
            , br
            , event_1_row, event_2_row, event_3_row
            , br
            , addl_events
            , br]


    @staticmethod
    def block_zipper(block_1, block_2, remove_last_line=False):
        if remove_last_line:
            block_1.pop()
            block_2.pop()

        for l1, l2 in zip(block_1, block_2):
            line = l1 + CalendarPageWeek.COL_SPACER + l2
            print("{0:^{width}}".format(line, width=CalendarPageWeek.total_width))


    def display_week(self):
        self.cal_header()

        editor_block = CalendarPageWeek.make_editor_block_2()
        day_block_1 = CalendarPageWeek.format_day_block(self.day_blocks[0])
        day_block_2 = CalendarPageWeek.format_day_block(self.day_blocks[1])
        day_block_3 = CalendarPageWeek.format_day_block(self.day_blocks[2])
        day_block_4 = CalendarPageWeek.format_day_block(self.day_blocks[3])
        day_block_5 = CalendarPageWeek.format_day_block(self.day_blocks[4])
        day_block_6 = CalendarPageWeek.format_day_block(self.day_blocks[5])
        day_block_7 = CalendarPageWeek.format_day_block(self.day_blocks[6])

        CalendarPageWeek.block_zipper(day_block_1, day_block_4)
        CalendarPageWeek.block_zipper(day_block_2, day_block_5)
        CalendarPageWeek.block_zipper(day_block_3, day_block_6)
        CalendarPageWeek.block_zipper(editor_block, day_block_7, remove_last_line=True)


    def display_menu(self):
        TOGGLE_DICT = {"T": Menus.ACTION_TOGGLE_DAY}
        TOGGLE_MENU = [f"[{k}]  {v}" for k, v in TOGGLE_DICT.items()]

        menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.MAIN_CAL_MENU)

        wh_sp = CalendarPageWeek.l_margin_menu_space
        whitespace_menu = Menus.add_whitespace_menu_list(menu_list, wh_sp)
        whitespace_toggle = Menus.add_whitespace_menu_list(TOGGLE_MENU, wh_sp)
        whitespace_quit = Menus.add_whitespace_menu_list(l_menus_data.QUIT_MENU_LIST, wh_sp)

        print(CalendarPageWeek.l_margin_menu_space + "CALENDAR")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(whitespace_toggle, indent_amt=2, speed_interval=0)
        l_animators.list_printer(whitespace_quit, indent_amt=2, speed_interval=0)


    def display_menu_columns(self):
        TOGGLE_DICT = {"T": Menus.ACTION_TOGGLE_WEEK}
        TOGGLE_MENU = [f"[{k}]  {v}" for k, v in TOGGLE_DICT.items()]

        _, menu_list_short = l_menus_funcs.prep_menu_tuple(Menus.WEEK_MENU_SHORT)
        menu_list_left = menu_list_short[:3]
        menu_list_right = menu_list_short[3:4] + TOGGLE_MENU + l_menus_data.QUIT_MENU_LIST
        menu_columns = CalendarPageWeek.prep_menu_columns(menu_l=menu_list_left,
                                                          menu_r=menu_list_right)

        wh_sp = CalendarPageWeek.l_margin_menu_space
        whitespace_menu = Menus.add_whitespace_menu_list(menu_columns, wh_sp)

        print(CalendarPageWeek.l_margin_menu_space + "CALENDAR")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)


    @staticmethod
    def valid_day_selection(user_input: str, var_weekblock: list[DayBlock]) -> bool:
        valid_day_selections = [block.day for block in var_weekblock]

        if not l_card_utils.test_for_int(user_input):
            return False

        input_int = int(user_input)

        if len(user_input) > 2:
            return False
        if input_int < 1:
            return False
        if input_int not in valid_day_selections:
            return False
        else:
            return True


class Menus:
    ACTION_EMPTY = "..."
    ACTION_HELP = "Help"
    ACTION_LIST_ALL = "List all events"
    ACTION_LIST_FEW = "List fewer events"
    ACTION_MENU_LESS = "Menu: show less"
    ACTION_MENU_MORE = "Menu: show more"
    ACTION_GOTO = "Go to date / day"
    ACTION_HELP_MORE = "Help / More"
    ACTION_MOD_DEL = "Modify / delete event"
    ACTION_NEW_EVENT = "New event"
    ACTION_NEW_QUICK = "New quick event"
    ACTION_SEARCH = "Search events"

    ACTION_TOGGLE_DAY = "Toggle view ➝ Day"
    ACTION_TOGGLE_WEEK = "Toggle view ➝ Week"
    ACTION_EXIT = "Exit"
    ACTION_QUIT = "Quit"

    MAIN_CAL_MENU = [
        ACTION_NEW_EVENT,
        ACTION_NEW_QUICK,
        ACTION_SEARCH,
        ACTION_GOTO,
        ACTION_MOD_DEL,
        ACTION_HELP_MORE,
    ]

    DAY_MENU_SHORT = [
        ACTION_NEW_EVENT,
        ACTION_SEARCH,
        ACTION_GOTO,
        ACTION_MENU_MORE
    ]

    DAY_MENU_LONG = [
        ACTION_NEW_EVENT,
        ACTION_NEW_QUICK,
        ACTION_SEARCH,
        ACTION_MENU_LESS,
        ACTION_GOTO,
        ACTION_LIST_ALL,
        ACTION_EMPTY,
        ACTION_EMPTY
    ]

    WEEK_MENU_SHORT = [
        ACTION_NEW_EVENT,
        ACTION_SEARCH,
        ACTION_GOTO,
        ACTION_HELP_MORE
    ]

    WEEK_MENU_LONG = [
        ACTION_NEW_EVENT,
        ACTION_SEARCH,
        ACTION_GOTO,
        ACTION_HELP_MORE
    ]

    EVENT_MENU = [
        ".",
        "..",
        "..."
    ]

    NEW_EVENT_MENU = [
        ".",
        "..",
        "..."
    ]

    MENU_BAR_1 = " :: MENU :: "


    @staticmethod
    def add_whitespace_menu_list(var_menu, space):
        whitespace_menu = []
        for item in var_menu:
            whitespace_menu.append(
                space + item
            )

        return whitespace_menu


if __name__ == "__main__":
    print("Hello from main")
    print(CalendarPageWeek.l_margin_menu);
    input("???")

    event_page = CalendarPageEvent(
        Event("Hello New Event", "STANDARD")
    )
    event_page.display_event()
    sys.exit()

    creds = get_creds()
    w_start, w_end = get_time_window_2(datetime.date.today(), 2)
    events = get_google_events_for_times(creds, w_start, w_end)
    # pp(events)

    event_obj = get_google_event_service(credentials=creds, time_min=w_start, time_max=w_end)
    pp(event_obj.get('nextPageToken'))
    print(event_obj.keys())

    sys.exit()


    def get_new_single_cards_from_google():
        start, end = get_time_window_2(datetime.date(2025, 3, 26), 2)
        events = get_google_events(creds, start, end)

        single_events = [e for e in events]
        cards_to_create = []

        for e in single_events[:10]:
            test = l_newcard.string_to_filename(e.get("summary"))
            if l_newcard.check_for_calendar_cards(test):
                cards_to_create.append((test, e))

        return cards_to_create


    events = get_new_single_cards_from_google()


    def sync_deleted_from_google():
        pass


    def create_new_local_card_w_sync(credentials, card_file, card_abspath):
        pass


    def create_google_event(credentials, formatted_card_title, card_steps):

        try:
            service_2 = build("calendar", "v3", credentials=credentials)

            now = datetime.datetime.now().isoformat() + "Z"
            card_steps_as_str = "\n".join(card_steps[:3])

            my_event = {
                "summary": formatted_card_title
                , "location": "..."
                , "description": card_steps_as_str
                , "start": {
                    "dateTime": f"{now}"
                    , "timeZone": "America/Los_Angeles"
                }
                , "end": {
                    "dateTime": f"{now}"
                    , "timeZone": "America/Los_Angeles"
                }
                , "colorId": 7
            }

            run_event = service_2.events().insert(calendarId="primary", body=my_event).execute()

            generated_id = run_event.get("id")
            # animators.animate_text(f"Created Google Calendar Event with ID: {generated_id}")
            return generated_id


        except HttpError as error:
            print("Here's the error that has occurred: ", error)
            return None


    def make_local_card_from_google():
        cards_to_create = get_new_single_cards_from_google()
        pp(cards_to_create)
        title, google_data = cards_to_create[2]
        # pp(google_data)

        details = google_data["description"] if google_data.get("description") else "...\n...\n...\n"
        details_as_list = [f"{d}\n" for d in details.split("\n")]
        title = f"A_{title}"

        l_newcard.write_calendar_card_and_json(title, l_files.cards_calendar_folder, google_data, details_as_list)

    # make_local_card_from_google()

    # def instances():
    #     page_token = None
    #     service = build("calendar", "v3", credentials=creds)
    #
    #     while True:
    #         events = service.events().instances(calendarId="primary", eventId="21fpfp3buf3qpp04qbpbjgpffb",
    #                                             pageToken=page_token).execute()
    #         for event in events["items"][:10]:
    #             print(event["summary"], event["id"])
    #         pause = input("<<< pause >>>")
    #         page_token = events.get("nextPageToken")
    #         if not page_token:
    #             break

    # instances()

# print("21fpfp3buf3qpp04qbpbjgpffb_20250220T000000Z" == "21fpfp3buf3qpp04qbpbjgpffb_20250220T000000Z")
# print("21fpfp3buf3qpp04qbpbjgpffb_20250220T000000Z" == "21fpfp3buf3qpp04qbpbjgpffb_20250222T000000Z")

# ------------------------------------- END / MISC BELOW -------------------------------------- #

# print("{:{fill}<50}".format("hello", fill="*"))
# print("{0:{width}}{:<8}{:<}{}".format(
# print("{:^{width}}".format(CalendarPageDay.events_line, width=CalendarPageDay.total_width))

# today_block = DayBlock.from_date(var_datetime=dt_today, events=[
#       ("Dinner and places with Phil", "7:00Pm - 9:30Pm")
#     , ("Dinner and places with Phil", "7:00Pm - 9:30Pm")
#     , ("Dinner and places with Phil", "7:00Pm - 9:30Pm")
# ])

# 2025-02-20T04:52:49.886Z
# 2025-02-20T04:52:49.886Z
