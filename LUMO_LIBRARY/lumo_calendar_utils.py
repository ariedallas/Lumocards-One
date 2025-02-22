import os
import datetime
import subprocess
import calendar

from pprint import pprint as pp

import dateutil.tz
from dateutil.relativedelta import relativedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import lumo_filehandler as l_files
import lumo_formatters as l_formatters
import lumo_newcard_refactor as l_newcard
import lumo_animationlibrary as animators
import lumo_json_utilities as l_json_utils

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
    try:
        service = build("calendar", "v3", credentials=credentials)

        start = datetime.datetime(year=time_min.year, month=time_min.month, day=time_min.day).isoformat() + "Z"
        end   = datetime.datetime(year=time_max.year, month=time_max.month, day=time_max.day).isoformat() + "Z"


        event_result = service.events().list(
            calendarId="primary",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime"
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


def get_google_events_for_times(credentials, time_min, time_max):
    google_month_events = get_google_events(credentials=credentials, time_min=time_min, time_max=time_max)

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

    l_formatters.card_deleter(card_filename)

    animators.animate_text("The card was deleted from the external (Google) calendar.")
    animators.animate_text("This Lumo card is deleted.")


def times_formatter(start, end, format):
    if format == "military":
        start = f" {start} "
        end = f" {end} "
    else:
        # format is standard
        start = start if len(start) == 7 else f" {start}"
        end = end if len(end) == 7 else f" {end}"

    formatted = f"{start} - {end}"
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


def get_nearest_monday(dt):
    amt = dt.weekday()
    return dt - relativedelta(days=amt)


def get_time_window_1(var_date, window_size_weeks):
    window_size_weeks = window_size_weeks if is_odd(window_size_weeks) else (window_size_weeks + 1)

    non_current_weeks = window_size_weeks - 1
    max_look_behind = round(non_current_weeks / 2)
    max_look_behind_days = max_look_behind * 7
    window_size_days = (window_size_weeks * 7) - 1

    nearest_monday = get_nearest_monday(var_date)
    window_start = nearest_monday - relativedelta(days=max_look_behind_days)
    window_end = window_start + relativedelta(days=window_size_days)

    return window_start, window_end


def get_time_window_2(var_date, window_size_weeks):
    window_size_days = (window_size_weeks * 7) - 1

    window_start = get_nearest_monday(var_date)
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


def google_event_to_local(event):
    dt_google_start = (event["start"].get("dateTime"))
    dt_google_end = (event["end"].get("dateTime"))
    dt_python_start = datetime.datetime.strptime(dt_google_start, "%Y-%m-%dT%H:%M:%S%z")
    dt_python_end = datetime.datetime.strptime(dt_google_end, "%Y-%m-%dT%H:%M:%S%z")

    date = dt_python_start.date()
    day = dt_python_start.day
    start_time = dt_python_start.strftime("%H:%M")
    end_time = dt_python_end.strftime("%H:%M")
    summary = event["summary"]

    return date, day, start_time, end_time, summary


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

    converted_events = [google_event_to_local(e) for e in google_month_events]
    expanded_events = []

    window = fill_time_window_dates(window_start, window_end)
    for date in window:
       """Transform whatever events are found from Google into a full list where every day has a placeholder
        Adds an empty list if no Google events exist for date."""
       matched_events = [e for e in converted_events if e[0] == date]
       day_block = DayBlock.from_date(date, matched_events)
       expanded_events.append(day_block)

    return expanded_events


class DayBlock:
    def __init__(self, day, dayname, date, events):
        self.day = day
        self.dayname = dayname
        self.date = date
        self.events = events

        # self.event_1 = DayBlock.list_safe_idx_get(self.events, 0, "--- --- ---")
        # self.event_2 = DayBlock.list_safe_idx_get(self.events, 1, "--- --- ---")
        # self.event_3 = DayBlock.list_safe_idx_get(self.events, 2, "--- --- ---")

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
            return [None, None, "     ", "     ", "--- --- ---"]


class CalendarPageDay:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)
    content_width = percenter(70, total_width)
    left_margin = round((total_width - content_width) / 2)

    EVENTS_WIDTH = 86
    EVENTS_LINE = "-" * EVENTS_WIDTH
    l_margin = round((total_width - EVENTS_WIDTH) / 2)
    l_margin_line = "-" * l_margin

    line = ("-" * content_width)

    def __init__(self, var_dayblock):
        self.header_date = CalendarPageDay.format_date_for_header(var_dayblock.date)
        self.events = var_dayblock.events

    @staticmethod
    def format_date_for_header(var_date):
        formatted = datetime.date.strftime(var_date, "%A: %B %d, %Y")
        return formatted

    def row_cal_header(self):
        print("{0:^{width}}\n".format(self.header_date.upper(), width=CalendarPageDay.total_width))
        print("{0:^{width}}".format(CalendarPageDay.line, width=CalendarPageDay.total_width))
        print()

    @staticmethod
    def _row_style_2(var_sel, var_event, var_start_t, var_end_t):
        selector = "{:<{width}}".format(var_sel, width=10)
        event = "• {:<{width}}".format(var_event, width=60)
        time = "{} —— {}".format(var_start_t, var_end_t)

        group = selector + event + time
        print("{0:^{width}}\n".format(group, width=CalendarPageDay.total_width))

    def display_day(self):
        start, end = (self.events[0][2], self.events[0][3]) if self.events else ("     ", "     ")
        summary = self.events[0][4] if self.events else "--- --- ---"

        subprocess.run(["clear"], shell=True)

        self.row_cal_header()
        CalendarPageDay._row_style_2("[A]", summary, start, end)
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[A]", summary, start, end)
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[-]", "--- --- ---", "     ", "     ")
        CalendarPageDay._row_style_2("[A]", "something I'll do another time", start, end)
        CalendarPageDay._row_style_2("[A]", "something I'll do soon", start, end)


class CalendarPageWeek:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)

    COL_SPACER = "        "
    COL_WIDTH = 60

    content_width = (2 * COL_WIDTH) + len(COL_SPACER)
    line = ("-" * content_width)
    l_margin = round((total_width - content_width) / 2) + 15


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
              ,"{0:-<{width}}".format(summary_2, width=summary_width), time_2)

        print("{0:-<{width}}".format(summary_1, width=summary_width), time_1
              , CalendarPageWeek.COL_SPACER
              ,"{0:-<{width}}".format(summary_2, width=summary_width), time_2)

        print("{0:-<{width}}".format(summary_1, width=summary_width), time_1
              , CalendarPageWeek.COL_SPACER
              ,"{0:-<{width}}".format(summary_2, width=summary_width), time_2)

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
        editor_header = "EDITING--02-DEC-2025"
        editor_header_formatted = "{0:-^{width}}".format(editor_header, width=CalendarPageWeek.COL_WIDTH)
        return editor_header_formatted

    @staticmethod
    def half_row_style_event(event):
        summary_width = CalendarPageWeek.COL_WIDTH - 17

        _, _, start, end, summary = event
        # times = times_formatter(start, end)
        times = times_formatter(start, end, format="military")

        return "{0:<{width}}".format(summary, width=summary_width) + times

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
    def make_editor_block():
        header = CalendarPageWeek.half_row_style_editor_header()
        summary = CalendarPageWeek.half_row_style_event([None, None, "20:00", "21:00", "Dinner with John"])
        br = CalendarPageWeek.half_row_style_line_break()
        menu_1 = CalendarPageWeek.half_row_style_menu("[A]  Complete card with no additional options")
        menu_2 = CalendarPageWeek.half_row_style_menu("[B]  Set recurring features")
        menu_3 = CalendarPageWeek.half_row_style_menu("[C]  Go back")
        menu_4 = CalendarPageWeek.half_row_style_menu("[X]  Exit")

        return [ br
                ,header
                ,summary
                ,br
                ,menu_1, menu_2, menu_3
                ,br
                ,menu_4
                ]
    @staticmethod
    def format_day_block(day_block):
        event_1 = DayBlock.list_safe_get_item(day_block.events, 0)
        event_2 = DayBlock.list_safe_get_item(day_block.events, 1)
        event_3 = DayBlock.list_safe_get_item(day_block.events, 2)

        day = CalendarPageWeek.half_row_style_day(day_block.day)
        dayname = CalendarPageWeek.half_row_style_dayname(day_block.dayname)
        br = CalendarPageWeek.half_row_style_line_break()
        event_1_row = CalendarPageWeek.half_row_style_event(event_1)
        event_2_row = CalendarPageWeek.half_row_style_event(event_2)
        event_3_row = CalendarPageWeek.half_row_style_event(event_3)
        addl_events = CalendarPageWeek.half_row_style_addnl_events(3)

        return [ day
                ,dayname
                ,br
                ,event_1_row, event_2_row, event_3_row
                ,br
                ,addl_events
                ,br]

    @staticmethod
    def block_zipper(block_1, block_2):
        for l1, l2 in zip(block_1, block_2):
            line = l1 + CalendarPageWeek.COL_SPACER + l2
            print("{0:^{width}}".format(line, width=CalendarPageWeek.total_width))

    def display_week(self):
        # subprocess.run(["clear"], shell=True)

        self.cal_header()

        editor_block = CalendarPageWeek.make_editor_block()
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
        CalendarPageWeek.block_zipper(editor_block, day_block_7)
        CalendarPageWeek.line_break()





if __name__ == "__main__":
    print("Hello from main")
    creds = get_creds()

    start, end = get_time_window_2(today_date, 8)
    get_local_calendar_cards(start, end)

    # delete_calendar_card(creds, "A_SingleEvent.txt")

    def get_new_single_cards_from_google():
        start, end = get_time_window_2(today_date, 2)
        events = get_google_events(creds, start, end)

        single_events = [e for e in events if not e.get("recurringEventId")]
        cards_to_create = []

        for e in single_events[:5]:
            test = l_newcard.string_to_filename(e.get("summary"))
            if l_newcard.check_for_calendar_cards(test):
                cards_to_create.append((test, e))

        return cards_to_create


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

    make_local_card_from_google()

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