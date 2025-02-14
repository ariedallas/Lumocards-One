import calendar
import datetime
import os
import subprocess


def percenter(percentage, number):

    perc_as_dec = percentage / 100
    return round(number * perc_as_dec)

class DayBlock:
    def __init__(self, day, dayname, events):
        self.day = day
        self.dayname = dayname
        self.events = events

        self.event_1 = events[0]
        self.event_2 = events[1]
        self.event_3 = events[2]

    @classmethod
    def from_date(cls, var_datetime, events):
        day = var_datetime.day
        day_int = var_datetime.weekday()
        dayname = calendar.Day(day_int).name

        return DayBlock(day, dayname, events)


class CalendarPageWeek:
    t_size = os.get_terminal_size()
    total_width = int(t_size.columns)
    content_width = percenter(80, total_width)
    line = ("-" * content_width)

    COL_SPACER = "        "
    COL_WIDTH = 60

    # EVENTS_WIDTH = 86
    # EVENTS_LINE = "-" * EVENTS_WIDTH
    # l_margin = round((total_width - EVENTS_WIDTH) / 2)
    # l_margin_line = "-" * l_margin
    # full_line = ("-" * total_width)


    def __init__(self, header_date, events):
        self.header_date = header_date
        self.events = events


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
        summary_width = CalendarPageWeek.COL_WIDTH - 14

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
        summary_width = CalendarPageWeek.COL_WIDTH - 15

        summary, time = event

        return "{0:<{width}}".format(summary, width=summary_width) + time

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
        summary = CalendarPageWeek.half_row_style_event(("Dinner with John", "8:00Pm - 9:00Pm"))
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
    def make_day_block(day_block):
        day = CalendarPageWeek.half_row_style_day(day_block.day)
        dayname = CalendarPageWeek.half_row_style_dayname(day_block.dayname)
        br = CalendarPageWeek.half_row_style_line_break()
        event_1 = CalendarPageWeek.half_row_style_event(day_block.event_1)
        event_2 = CalendarPageWeek.half_row_style_event(day_block.event_2)
        event_3 = CalendarPageWeek.half_row_style_event(day_block.event_3)
        addl_events = CalendarPageWeek.half_row_style_addnl_events(3)

        return [ day
                ,dayname
                ,br
                ,event_1, event_2, event_3
                ,br
                ,addl_events
                ,br]

    @staticmethod
    def block_zipper(block_1, block_2):
        for l1, l2 in zip(block_1, block_2):
            line = l1 + CalendarPageWeek.COL_SPACER + l2
            print("{0:^{width}}".format(line, width=CalendarPageWeek.total_width))

    def display_week(self):
        # subprocess.run(['clear'], shell=True)

        dt_today = datetime.date.today()
        today_block = DayBlock.from_date(var_datetime=dt_today, events=[
              ("Dinner and places with Phil", "7:00Pm - 9:30Pm")
            , ("Dinner and places with Phil", "7:00Pm - 9:30Pm")
            , ("Dinner and places with Phil", "7:00Pm - 9:30Pm")
        ])

        self.cal_header()
        # CalendarPageWeek.row_style_days((2, 30))
        # CalendarPageWeek.row_style_daynames(("MONDAY--JAN", "THURSDAY"))
        # CalendarPageWeek.line_break()
        # CalendarPageWeek.row_style_event(("Places with Cameron and Phil", "14:00 - 15:00")
        #                                  , ("Places with Cameron and Phil", "14:00 - 15:00"))
        # CalendarPageWeek.line_break()
        # CalendarPageWeek.row_style_addnl_events((2, 6))
        # CalendarPageWeek.line_break()

        editor_block = CalendarPageWeek.make_editor_block()
        day_block_7 = CalendarPageWeek.make_day_block(today_block)

        CalendarPageWeek.block_zipper(day_block_7, day_block_7)
        CalendarPageWeek.block_zipper(day_block_7, day_block_7)
        CalendarPageWeek.block_zipper(day_block_7, day_block_7)
        CalendarPageWeek.block_zipper(editor_block, day_block_7)
        CalendarPageWeek.line_break()
        print("                                                         ", end='')
        usr = input(">")


    def cal_header(self):
        print()
        print('{0:^{width}}'.format(self.header_date, width=CalendarPageWeek.total_width))
        print()


if __name__ == "__main__":
    week_viewer = CalendarPageWeek("DECEMBER", [])
    week_viewer.display_week()