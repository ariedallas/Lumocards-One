import calendar
import datetime
import os
import subprocess
import sys
import textwrap
from pprint import pprint as pp

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


def get_google_service():
    creds = get_creds()

    try:
        service = build("calendar", "v3", credentials=creds)
        return service

    except HttpError as error:
        print("An error has occurred ", error)
        return None


def get_google_events(credentials, time_min, time_max):
    page_token = None

    try:
        service = build("calendar", "v3", credentials=credentials)

        start = datetime.datetime(year=time_min.year, month=time_min.month, day=time_min.day
                                  , hour=0, minute=0, second=0,
                                  tzinfo=dateutil.tz.tzlocal()
                                  ).isoformat()

        end = datetime.datetime(year=time_max.year, month=time_max.month, day=time_max.day
                                , hour=0, minute=0, second=0,
                                tzinfo=dateutil.tz.tzlocal()
                                ).isoformat()

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
            return

        return events

    except HttpError as error:
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


def get_google_setting(setting_id):
    service = get_google_service()
    try:
        result = service.settings().get(setting=setting_id).execute()
        return result.get("value")
    except:
        return None


def split_at_max(var_str, col_width):
    sub_rows = []

    amt_sub_rows = len(var_str) // col_width
    if amt_sub_rows == 0:
        sub_rows.append(var_str)
        return sub_rows

    for num in range(amt_sub_rows + 1):
        idx_start, idx_end = num * col_width, (num + 1) * col_width
        sub_row = var_str[idx_start:idx_end]
        sub_rows.append(sub_row)

    return sub_rows


def list_limiter(var_list, col_width, row_limit):
    limited_list = []

    limited_rows = var_list if len(var_list) <= row_limit else var_list[:row_limit]

    for string in limited_rows:
        sub_rows = split_at_max(string, col_width)

        for sub_row in sub_rows:
            if len(limited_list) < row_limit:
                limited_list.append(sub_row)
            elif len(limited_list) == row_limit:
                break

        if len(limited_list) == row_limit:
            break

    return limited_list


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

    summary = event.get("summary", "(no title)")

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

    event_obj._add_event_details(id=event["id"],
                                 description=event.get("description"),
                                 location=event.get("location"),
                                 reminders=event.get("reminders")
                                 )

    return event_obj


def get_adjacent_month(base_month, base_year, direction, months_distance):
    if direction == "past":
        adjacent = datetime.date(day=1, month=base_month, year=base_year) - relativedelta(months=months_distance)
    elif direction == "next":
        adjacent = datetime.date(day=1, month=base_month, year=base_year) + relativedelta(months=months_distance)
    else:
        adjacent = datetime.date(day=1, month=base_month, year=base_year)

    return adjacent


def get_day_blocks(var_date=today_date, time_min=None, time_max=None):
    creds = get_creds()

    if time_min and time_max:
        window_start, window_end = time_min, time_max
    else:
        window_start, window_end = get_time_window_1(var_date, 13)

    google_month_events = get_google_events(creds,
                                            time_min=window_start,
                                            time_max=window_end)

    if not google_month_events:
        google_month_events = []

    converted_events = [google_event_to_obj(e) for e in google_month_events]

    day_blocks = []

    window = fill_time_window_dates(window_start, window_end)
    for date in window:
        """Transform whatever events are found from Google into a full list where every day has a placeholder
         Adds an empty list if no Google events exist for date."""
        matched_events = [obj for obj in converted_events if
                          obj.get_date() == date]
        day_block = DayBlock.from_date(date, matched_events)
        day_blocks.append(day_block)

    return day_blocks


def get_today_events():
    creds = get_creds()

    time_min = today_date
    time_max = today_date + relativedelta(days=1)

    today_events = get_google_events(creds,
                                     time_min=time_min,
                                     time_max=time_max)

    if not today_events:
        today_events = []

    converted_events = [google_event_to_obj(e) for e in today_events]

    return converted_events


def get_formatted_event_info(event_dict):
    summary = event_dict.get("summary", "")

    s_time = event_dict.get("s")
    e_time = event_dict.get("e")
    s_date = event_dict.get("s_date")
    e_date = event_dict.get("e_date")

    description = event_dict.get("description")
    location = event_dict.get("location")

    if not s_time and not e_time:
        time_info_f = "..."

    elif s_time == "all day":
        time_info_f = s_time

    else:
        time_info_f = f"{s_time} - {e_time}"

    if not s_date and not e_date:
        start_date_f = "..."
        end_date_f = "..."

    else:
        start_date_f = s_date
        end_date_f = e_date

    if not description:
        desc_list_limited = ["..."]
    else:
        descr_split = description.split("\n")
        desc_list_limited = list_limiter(descr_split,
                                         col_width=CalendarPageEvent.EVENT_VALUE,
                                         row_limit=5)

    if not location:
        loc_list_limited = ["..."]
    else:
        loc_split = location.split("\n")
        loc_list_limited = list_limiter(loc_split,
                                        col_width=CalendarPageEvent.EVENT_VALUE,
                                        row_limit=5)

    return (summary,
            time_info_f,
            start_date_f,
            end_date_f,
            desc_list_limited,
            loc_list_limited)


class Event:
    def __init__(self,
                 summary,
                 event_type):
        self.s = None
        self.e = None
        self.s_date = None
        self.e_date = None
        self.summary = summary
        self.event_type = event_type

        self.id = None
        self.description = None
        self.location = None
        self.reminders = None


    def _add_event_details(self,
                           id,
                           description,
                           location,
                           reminders):
        self.id = id
        self.description = description
        self.location = location
        self.reminders = reminders


    @staticmethod
    def _string_split_newln(string):
        list_from_string = string.split("\n")
        return list_from_string


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


    def get_date(self):
        if self.event_type == "ALL DAY":
            return self.s_date.date()

        else:  # self.event_type is "multi day" or "standard"
            return self.s.date()


    def format_as_editing_dict(self):
        editing_event = {}

        editing_event["summary"] = self.summary

        if self.event_type == "ALL DAY":
            editing_event["s"] = "all day"
            editing_event["e"] = "all day"

            editing_event["s_date"] = self.s_date.strftime("%d of %b, %Y")
            editing_event["e_date"] = self.e_date.strftime("%d of %b, %Y")

        else:
            editing_event["s"] = self.s.strftime("%I:%M %p").lower()
            editing_event["e"] = self.e.strftime("%I:%M %p").lower()

            editing_event["s_date"] = self.s.strftime("%d of %b, %Y")
            editing_event["e_date"] = self.e.strftime("%d of %b, %Y")

        editing_event["description"] = self.description
        editing_event["location"] = self.location

        return editing_event


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

    EVENT_WIDTH = 60
    EVENT_FIELD = 30
    EVENT_VALUE = 30
    EVENT_LINE = "-" * EVENT_WIDTH

    l_margin_num = round((total_width - EVENT_WIDTH) / 2)
    l_margin_space = " " * l_margin_num
    l_margin_line = "-" * l_margin_num

    main_line = ("-" * content_width)

    EVENT_MENU_NUDGE = 2
    EVENT_MENU_SPACE = " " * (EVENT_MENU_NUDGE)

    cursor_indent_space = l_margin_space + EVENT_MENU_SPACE

    msg_indent_1 = l_margin_num + EVENT_MENU_NUDGE + 5
    msg_indent_2 = l_margin_num + EVENT_MENU_NUDGE


    def __init__(self, var_event_obj):
        self.event_obj = var_event_obj


    def _row_event_header(self):
        if not self.event_obj.summary:
            summary_limited = "(no title)"
        else:
            summary_limited = textwrap.shorten(self.event_obj.summary, width=70, placeholder="...")

        title = f"EVENT: {summary_limited}"

        print()
        print("{0:^{width}}".format(title,
                                    width=CalendarPageEvent.total_width))
        print()


    def _row_editing_event_header(self, summary, header):
        summary_limited = textwrap.shorten(summary, width=70, placeholder="...")

        if header == "EDIT":
            title = f"EDITING EVENT: {summary_limited}"
        else:  # header == "NEW"
            title = f"NEW EVENT: {summary_limited}"

        print()
        print("{0:^{width}}".format(title,
                                    width=CalendarPageEvent.total_width))
        print("{0:^{width}}".format(CalendarPageEvent.EVENT_LINE,
                                    width=CalendarPageEvent.total_width))
        print()


    @staticmethod
    def _row_event_data(col_l, col_r, use_new_line=True):
        event_field = "{:<{width}}".format(col_l, width=CalendarPageEvent.EVENT_FIELD)
        event_value = "{:<{width}}".format(col_r, width=CalendarPageEvent.EVENT_VALUE)

        group = event_field + event_value
        # print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))
        print(CalendarPageEvent.l_margin_space + group)
        if use_new_line:
            print()


    @staticmethod
    def _row_prompt_subheader(col_l, col_lw, col_r, col_rw):
        subheader = "{:<{width}}".format(col_l, width=col_lw)
        context_date = "{:>{width}}".format(col_r, width=col_rw)

        group = subheader + context_date
        # print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))
        print(CalendarPageEvent.l_margin_space + group)


    @staticmethod
    def _rows_event_list_data(col_l, var_list):
        single_row = True if len(var_list) <= 1 else False

        CalendarPageEvent._row_event_data(col_l, var_list[0], single_row)

        end = len(var_list)
        for remaining in var_list[1:end]:
            CalendarPageEvent._row_event_data("", remaining, False)

        if not single_row:
            print()


    def display_event(self, event_obj: Event) -> None:
        if not event_obj.s and event_obj.event_type != "ALL DAY":
            time_info_formatted = "..."

        else:
            time_info = times_formatter(event_obj, "military")
            time_info_formatted = time_info.lstrip(" ")

        if not event_obj.s and not event_obj.s_date:
            date_info_formatted = "..."

        else:
            date_info = event_obj.s if event_obj.s else event_obj.s_date
            date_info_formatted = CalendarPageEvent.dates_formatter(date_info,
                                                                    event_obj.event_type)

        if not event_obj.description:
            desc_list_limited = ["..."]
        else:
            desc_list = event_obj._string_split_newln(event_obj.description)
            desc_list_limited = list_limiter(desc_list,
                                             col_width=CalendarPageEvent.EVENT_VALUE,
                                             row_limit=5)
        if not event_obj.location:
            loc_list_limited = ["..."]
        else:
            location_list = event_obj._string_split_newln(event_obj.location)
            loc_list_limited = list_limiter(location_list,
                                            col_width=CalendarPageEvent.EVENT_VALUE,
                                            row_limit=5)

        if not event_obj.reminders:
            reminder_info = "..."
        else:
            reminder_info = "Default" if event_obj.reminders["useDefault"] == True else "..."

        self._row_event_header()
        print()
        CalendarPageEvent._row_event_data("Times:", time_info_formatted)
        CalendarPageEvent._row_event_data("Date:", date_info_formatted)
        CalendarPageEvent._rows_event_list_data("Description:", desc_list_limited)
        CalendarPageEvent._rows_event_list_data("Location:", loc_list_limited)
        CalendarPageEvent._row_event_data("Reminders:", reminder_info)
        print()


    def display_editing_event(self, event_dict, header):
        (summary,
        time_info_f,
        start_date_f,
        end_date_f,
        desc_list_limited,
        loc_list_limited) = get_formatted_event_info(event_dict)

        self._row_editing_event_header(summary, header)
        print()
        CalendarPageEvent._row_event_data("Times:", time_info_f)
        CalendarPageEvent._row_event_data("Start Date:", start_date_f)
        CalendarPageEvent._row_event_data("End Date:", end_date_f)
        CalendarPageEvent._rows_event_list_data("Description:", desc_list_limited)
        CalendarPageEvent._rows_event_list_data("Location:", loc_list_limited)
        print()


    # def display_menu(self):
    #     menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.EVENT_MENU_LONG)
    #
    #     wh_sp = CalendarPageEvent.l_margin_space
    #     whitespace_menu = Menus.add_whitespace_menu_list(menu_list, wh_sp)
    #     whitespace_exit = Menus.add_whitespace_menu_list(l_menus_data.EXIT_MENU_LIST, wh_sp)
    #
    #     print()
    #     print(wh_sp + "EVENT")
    #     print()
    #     l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)
    #     print()
    #     l_animators.list_printer(whitespace_exit, indent_amt=2, speed_interval=0)

    def display_menu_columns(self, var_dict):
        menu_list = l_menus_funcs.menu_list_from_dict(var_dict)
        menu_list_left = menu_list[:4]
        menu_list_right = menu_list[4:8]
        menu_columns = Menus.prep_menu_columns(menu_l=menu_list_left,
                                               menu_r=menu_list_right)

        wh_sp = CalendarPageEvent.l_margin_space
        print(wh_sp + "CALENDAR")

        print()
        l_animators.list_printer(menu_columns,
                                 indent_amt=CalendarPageEvent.msg_indent_2,
                                 speed_interval=0)
        print()
        l_animators.list_printer(l_menus_data.SIMPLE_EXIT_LIST,
                                 indent_amt=CalendarPageEvent.msg_indent_2,
                                 speed_interval=0)


    def display_menu_confirmation(self):
        menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.EDITING_EVENT_CONFIRMATION)

        l_animators.list_printer(menu_list,
                                 indent_amt=CalendarPageEvent.msg_indent_2,
                                 speed_interval=0)

        l_animators.list_printer(l_menus_data.EXIT_NOSAVE_LIST,
                                 indent_amt=CalendarPageEvent.msg_indent_2,
                                 speed_interval=0)


    def display_prompts_subheader(self,
                                  subheader_name,
                                  date_in_focus: datetime.datetime):

        date_in_focus_formatted = date_in_focus.strftime("%d of %b (%a) %Y ")
        date_formatted = f"IN FOCUS: {date_in_focus_formatted}"

        self._row_prompt_subheader(subheader_name, 20,
                                   date_formatted, 40)


    @staticmethod
    def dates_formatter(dt_obj, event_type):
        if event_type == "STANDARD":
            month_abbr = calendar.month_abbr[dt_obj.month]
            return f"{dt_obj.day} of {month_abbr}, {dt_obj.year}"

        else:
            month_abbr = calendar.month_abbr[dt_obj.month]
            return f"{dt_obj.day} of {month_abbr}, {dt_obj.year}"


class CalendarPageDay:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)
    content_width = percenter(70, total_width)

    DAY_WIDTH = 86
    DAY_LINE = "-" * DAY_WIDTH
    l_margin_num = int((total_width - DAY_WIDTH) / 2)
    l_margin_space = " " * l_margin_num
    l_margin_line = "-" * l_margin_num

    main_line = ("-" * content_width)

    DAY_FIELD_SEL = 10
    DAY_FIELD_TIME = 17
    DAY_FIELD_EVENTS = DAY_WIDTH - DAY_FIELD_SEL - DAY_FIELD_TIME
    SELECTOR_SPACE = " " * DAY_FIELD_SEL

    DAY_MENU_NUDGE = DAY_FIELD_SEL + 2
    DAY_MENU_SPACE = " " * (DAY_MENU_NUDGE)

    cursor_indent_space = l_margin_space + DAY_MENU_SPACE

    msg_indent_num = l_margin_num + DAY_MENU_NUDGE + 5


    def __init__(self, var_dayblock):
        self.header_date = CalendarPageDay._format_date_for_header(var_dayblock.date)
        self.day_block = var_dayblock


    def _row_day_header(self):
        # under_line = ("-" * len(self.header_date))

        print()
        print("{0:^{width}}".format(self.header_date.upper(), width=CalendarPageDay.total_width))
        # print("{0:^{width}}".format(under_line, width=CalendarPageDay.total_width))
        print()
        print()


    @staticmethod
    def _row_day_events(var_sel, event_obj):
        summary_limited = textwrap.shorten(event_obj.summary, width=35, placeholder="...")
        summary_bullet = "• " + summary_limited

        selector = "{:<{width}}".format(var_sel, width=CalendarPageDay.DAY_FIELD_SEL)
        event = "{:<{width}}".format(summary_bullet, width=CalendarPageDay.DAY_FIELD_EVENTS)
        time_info = times_formatter(event_obj, "military")

        group = selector + event + time_info
        print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))


    @staticmethod
    def _row_flexible(col_l, col_m, col_r):
        col_l = "{:<{width}}".format(col_l, width=CalendarPageDay.DAY_FIELD_SEL)
        col_m = "{:<{width}}".format(col_m, width=CalendarPageDay.DAY_FIELD_EVENTS)
        col_r = "{:<{width}}".format(col_r, width=CalendarPageDay.DAY_FIELD_TIME)

        group = col_l + col_m + col_r
        print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))


    @staticmethod
    def _row_day_menu(var_sel, var_option):
        selector = f"[{var_sel}]  "

        print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT + selector + var_option)


    def display_day(self, events_limit, low):
        l_files.clear()
        self._row_day_header()

        empty_event = Event("--- --- ---",
                            "EMPTY EVENT")

        for idx in range(events_limit):
            if idx < len(self.day_block.events):
                CalendarPageDay._row_day_events(f"[{idx + 1}]", self.day_block.events[idx])
            elif len(self.day_block.events) <= idx < low:
                CalendarPageDay._row_day_events(f"[{idx + 1}]", empty_event)

        total_e = len(self.day_block.events)
        remaining_e = 0 if total_e - events_limit <= 0 \
            else total_e - events_limit

        CalendarPageDay._row_flexible(" ",
                                      f"+ {remaining_e} more events",
                                      " ")
        print()


    def display_menu(self):
        TOGGLE_DICT = {"T": Menus.ACTION_TOGGLE_DAY}
        TOGGLE_MENU = [f"[{k}]  {v}" for k, v in TOGGLE_DICT.items()]

        menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.DAY_MENU_LONG)

        wh_sp = CalendarPageDay.l_margin_space + CalendarPageDay.SELECTOR_SPACE
        whitespace_menu = Menus.add_whitespace_menu_list(menu_list, wh_sp)
        whitespace_toggle = Menus.add_whitespace_menu_list(TOGGLE_MENU, wh_sp)
        whitespace_quit = Menus.add_whitespace_menu_list(l_menus_data.QUIT_MENU_LIST, wh_sp)

        print()
        print(wh_sp + "CALENDAR")
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
        menu_columns = Menus.prep_menu_columns(menu_l=menu_list_left,
                                               menu_r=menu_list_right)

        wh_sp = CalendarPageDay.l_margin_space + CalendarPageDay.SELECTOR_SPACE
        whitespace_menu = Menus.add_whitespace_menu_list(menu_columns, wh_sp)
        whitespace_toggle = Menus.add_whitespace_menu_list(TOGGLE_MENU, wh_sp)
        whitespace_quit = Menus.add_whitespace_menu_list(l_menus_data.QUIT_MENU_LIST, wh_sp)

        print(wh_sp + "CALENDAR")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(whitespace_toggle, indent_amt=2, speed_interval=0)
        l_animators.list_printer(whitespace_quit, indent_amt=2, speed_interval=0)


    @staticmethod
    def valid_event_selection(user_input: str,
                              max_ints: int,
                              curr_limit: int) -> bool:

        if not l_card_utils.test_for_int(user_input):
            return False

        input_int = int(user_input)
        valid_range = range(1, max_ints + 1)

        if input_int in valid_range and input_int <= curr_limit:
            return True
        else:
            return False


    @staticmethod
    def _format_date_for_header(var_date):
        formatted = datetime.date.strftime(var_date, "%A: %B %d, %Y")
        return formatted


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

    msg_indent_num = l_margin_menu + 7


    def __init__(self, week_of_day_blocks):
        self.day_blocks = week_of_day_blocks
        self.header_date = CalendarPageWeek.get_header_date(week_of_day_blocks)


    def _row_week_header(self):
        print()
        # print("{0:^{width}}".format(CalendarPageDay.line, width=CalendarPageWeek.total_width))
        print("{0:^{width}}".format(self.header_date, width=CalendarPageWeek.total_width))
        print()


    @staticmethod
    def _row_week_days(dates):
        dt_1, dt_2 = dates
        dt_1_frmt = "{:02d}".format(dt_1)
        dt_2_frmt = "{:02d}".format(dt_2)

        print("{0:-<{width}}".format(dt_1_frmt, width=CalendarPageWeek.COL_WIDTH)
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(dt_2_frmt, width=CalendarPageWeek.COL_WIDTH))


    @staticmethod
    def _row_week_daynames(daynames):
        dayname_1, dayname_2 = daynames

        print("{0:-<{width}}".format(dayname_1, width=CalendarPageWeek.COL_WIDTH)
              , CalendarPageWeek.COL_SPACER
              , "{0:-<{width}}".format(dayname_2, width=CalendarPageWeek.COL_WIDTH))


    @staticmethod
    def _row_week_events(event_1, event_2):
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
    def _row_addnl_events(addnl_events_indicators):
        num_1, num_2 = addnl_events_indicators

        formatted_text_1 = "+ {} more events".format(num_1)
        formatted_text_2 = "+ {} more events".format(num_2)

        print("{0:>{width}}".format(formatted_text_1, width=CalendarPageWeek.COL_WIDTH)
              , CalendarPageWeek.COL_SPACER
              , "{0:>{width}}".format(formatted_text_2, width=CalendarPageWeek.COL_WIDTH))


    @staticmethod
    def _row_week_days_half(day):
        day_frmt = "{:02d}".format(day)

        return "{0:<{width}}".format(day_frmt, width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def _row_week_dnames_half(dayname):
        return "{0:-<{width}}".format(dayname, width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def _row_week_addnl_half(num):
        formatted_text = "+ {} more events".format(num)

        return "{0:>{width}}".format(formatted_text, width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def _row_week_event_half(event_obj):
        summary_width = CalendarPageWeek.COL_WIDTH - 17
        summary_limited = textwrap.shorten(event_obj.summary, width=35, placeholder="...")

        time_info = times_formatter(event_obj, format="military")

        return "{0:<{width}}".format(summary_limited, width=summary_width) + time_info


    @staticmethod
    def _row_week_line_break():
        return "{0:<{width}}".format("", width=CalendarPageWeek.COL_WIDTH)


    @staticmethod
    def _row_week_editor_header():
        editor_header = ":::"
        editor_header_formatted = "{0:-^{width}}".format(editor_header, width=CalendarPageWeek.COL_WIDTH)
        return editor_header_formatted


    @staticmethod
    def _row_week_editor_menu(menu_item):
        return "  {0:<{width}}".format(menu_item, width=CalendarPageWeek.COL_WIDTH - 2)


    @staticmethod
    def make_editor_block_1():
        header = CalendarPageWeek._row_week_editor_header()
        summary = CalendarPageWeek._row_week_event_half([None, None, "20:00", "21:00", "Dinner with John"])
        br = CalendarPageWeek._row_week_line_break()
        menu_1 = CalendarPageWeek._row_week_editor_menu("[A]  Complete card with no additional options")
        menu_2 = CalendarPageWeek._row_week_editor_menu("[B]  Set recurring features")
        menu_3 = CalendarPageWeek._row_week_editor_menu("[C]  Go back")
        menu_4 = CalendarPageWeek._row_week_editor_menu("[X]  Exit")

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

        header = CalendarPageWeek._row_week_editor_header()
        summary = CalendarPageWeek._row_week_event_half(test_edited_event)
        br = CalendarPageWeek._row_week_line_break()

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

        day = CalendarPageWeek._row_week_days_half(day_block.day)
        dayname = CalendarPageWeek._row_week_dnames_half(day_block.dayname)
        br = CalendarPageWeek._row_week_line_break()
        event_1_row = CalendarPageWeek._row_week_event_half(event_obj_1)
        event_2_row = CalendarPageWeek._row_week_event_half(event_obj_2)
        event_3_row = CalendarPageWeek._row_week_event_half(event_obj_3)
        addl_events = CalendarPageWeek._row_week_addnl_half(addnl_event_num)

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
        self._row_week_header()

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

        menu_dict, menu_list = l_menus_funcs.prep_menu_tuple(Menus.WEEK_MENU_SHORT)

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
        menu_columns = Menus.prep_menu_columns(menu_l=menu_list_left,
                                               menu_r=menu_list_right)

        wh_sp = CalendarPageWeek.l_margin_menu_space
        whitespace_menu = Menus.add_whitespace_menu_list(menu_columns, wh_sp)

        print(CalendarPageWeek.l_margin_menu_space + "CALENDAR")
        print()
        l_animators.list_printer(whitespace_menu, indent_amt=2, speed_interval=0)


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
    ACTION_EDIT_DESCRIPTION = "Notes (edit description)"
    ACTION_EDIT_LOCATION = "Location (edit)"
    ACTION_EDIT_TITLE = "Title (edit)"
    ACTION_EDIT_TIME_DATE = "Time / Date (edit)"
    # ACTION_REPEAT_EVENT = "Repeat: event"
    ACTION_DELETE_EVENT = "Delete: event"

    ACTION_EMPTY = "..."
    ACTION_GOTO = "Go to: date / day"
    ACTION_HELP = "Help"
    ACTION_HELP_KEYWORDS = "Help / Keywords"
    ACTION_HELP_MORE = "Help / More"
    ACTION_LIST_ALL = "All: list all events"
    ACTION_LIST_FEW = "Few: list fewer events"
    ACTION_MENU_LESS = "Menu: show less"
    ACTION_MENU_MORE = "Menu: show more"
    ACTION_MOD_DEL = "Modify / delete event"
    ACTION_NEW_EVENT = "New: event"
    ACTION_NEW_QUICK = "Quick: event"
    ACTION_SEARCH = "Search: events"

    ACTION_TOGGLE_DAY = "Toggle view ➝ Day"
    ACTION_TOGGLE_WEEK = "Toggle view ➝ Week"
    ACTION_EXIT = "Exit"
    ACTION_QUIT = "Quit"

    ACTION_SAVE = "Save ➝ (Default action)"
    ACTION_TRY_AGAIN = "Edit again?"
    ACTION_EXIT_NO_SAVE = "Exit without saving"

    P_TITLE = "Title ( ➝ no title) :"
    P_S_TIME = "Start time ( ➝ all day) :"
    P_E_TIME = "End time"
    P_S_DATE = "Start date"
    P_E_DATE = "End date"
    P_DESCRIPTION = "Edit description? ( ➝ no) :"
    P_LOCATION = "Edit location? ( ➝ no) :"

    EVENT_MENU_SHORT = [
        ACTION_EDIT_TITLE,
        ACTION_EDIT_TIME_DATE,
        ACTION_EDIT_DESCRIPTION,
        ACTION_MENU_MORE
    ]

    EVENT_MENU_LONG = [
        ACTION_EDIT_TITLE,
        ACTION_EDIT_TIME_DATE,
        ACTION_EDIT_DESCRIPTION,
        ACTION_MENU_LESS,

        ACTION_EDIT_LOCATION,
        ACTION_DELETE_EVENT
    ]

    PROMPT_TITLE = {"summary": P_TITLE}
    PROMPT_S_TIME = {"s": P_S_TIME}
    PROMPT_E_TIME = {"e": P_E_TIME}
    PROMPT_S_DATE = {"s_date": P_S_DATE}
    PROMPT_E_DATE = {"e_date": P_E_DATE}
    PROMPT_DESCRIPTION = {"description": P_DESCRIPTION}
    PROMPT_LOCATION = {"location": P_LOCATION}

    NEW_EVENT_CATEGORIES = [
        [PROMPT_TITLE],
        [PROMPT_S_TIME, PROMPT_E_TIME],
        [PROMPT_S_DATE, PROMPT_E_DATE],
        [PROMPT_DESCRIPTION],
        [PROMPT_LOCATION]
    ]

    EDITING_EVENT_DT = [
        [PROMPT_S_TIME, PROMPT_E_TIME],
        [PROMPT_S_DATE, PROMPT_E_DATE]
    ]

    EDITING_EVENT_CONFIRMATION = [
        ACTION_SAVE,
        ACTION_TRY_AGAIN,
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
        ACTION_HELP_MORE,
        ACTION_DELETE_EVENT
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

    MENU_BAR_1 = " :: MENU :: "


    @staticmethod
    def add_whitespace_menu_list(var_menu, space):
        whitespace_menu = []
        for item in var_menu:
            whitespace_menu.append(
                space + item
            )

        return whitespace_menu


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


if __name__ == "__main__":
    print("Hello from main")

    dt = datetime.datetime.now()
    print(datetime.datetime(dt.year, dt.month, dt.day,
                            dt.hour, dt.minute, dt.second,
                            tzinfo=dateutil.tz.tzlocal()).isoformat())
