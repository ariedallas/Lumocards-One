import calendar
import datetime
import sys
from collections import namedtuple

import dateutil.parser
from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta

from LUMO_LIBRARY.lumo_card_utils import test_for_float

ParseResult = namedtuple("ParseResult",
                         [
                             "type",
                             "hour",
                             "increment",
                             "dt_obj",
                             "display",
                             "error"])


class NewEventParser:

    def __init__(self, date_in_focus):
        self.date_in_focus = date_in_focus

        self.start_time = None
        self.end_time = None
        self.start_date = None
        self.end_date = None


    @staticmethod
    def get_basic_type(string, target):
        if string == "":
            dt_type = "DEFAULT"

        elif NewEventParser.test_for_increment(string) and \
                target != "start time":
            dt_type = "TIME, INCREMENT"

        elif NewEventParser.test_for_dateutil(string):
            if target in {"start time", "end time"}:
                dt_type = "DATEUTIL, TIME"
            elif target in {"start date", "end date"}:
                dt_type = "DATEUTIL, DATE"
            else:
                dt_type = "UNKNOWN"

        elif string == "all day":
            dt_type = "TIME, ALL DAY"

        else:
            dt_type = "UNKNOWN"

        return dt_type


    def parse_type(self, input_string, target):
        string = input_string.strip().lower()

        hour = None
        increment = None
        dt_obj = None
        display = None
        error = None

        dt_type = NewEventParser.get_basic_type(string, target)

        if dt_type == "DEFAULT" and target == "start time":
            display = "all day"

        elif dt_type == "DEFAULT" and target == "end time" and \
                self.start_time.type != "UNKNOWN":
            if self.start_time.display == "all day":
                display = "all day"

            else:
                dt_obj = self.start_time.dt_obj + relativedelta(minutes=30)
                display = dt_obj.strftime("%I:%M %p").lower()
                dt_type = "TIME, INCREMENT"

        elif dt_type == "DEFAULT" and target == "start date":
            dt_obj = self.date_in_focus
            display = dt_obj.strftime("%d of %b, %Y")
            dt_type = "DATE, FROM FOCUS"

        elif dt_type == "DEFAULT" and target == "end date":
            dt_obj = self.start_date.dt_obj
            display = self.start_date.display
            dt_type = self.start_date.type

        elif dt_type == "DATEUTIL, TIME":
            parsed = NewEventParser.parse_time(string)

            if parsed:
                dt_obj = parsed
                display = dt_obj.strftime("%I:%M %p").lower()
            else:
                dt_type = "UNKNOWN"
                error = f"Not valid here: '{string}'"

        elif dt_type == "DATEUTIL, DATE":
            parsed = NewEventParser.parse_date(string)

            if parsed:
                dt_obj = parsed
                display = dt_obj.strftime("%d of %b, %Y")
            else:
                dt_type = "UNKNOWN"
                error = f"Not valid here: {string}"

        elif dt_type == "TIME, INCREMENT" and \
              self.start_time.type != "UNKNOWN":

            min_add, error = self.parse_time_increment(string)
            if not error:
                dt_obj = self.start_time.dt_obj + relativedelta(minutes=min_add)
                display = dt_obj.time().strftime("%I:%M %p").lower()
            else:
                dt_type = "UNKNOWN"

        elif dt_type == "UNKNOWN":
            error = f"'{input_string}' not valid as: {target.title()}"

        Parsed = ParseResult(dt_type, hour, increment, dt_obj, display, error)

        if target == "start time":
            self.start_time = Parsed
        elif target == "end time":
            self.end_time = Parsed
        elif target == "start date":
            self.start_date = Parsed
        elif target == "end date":
            self.end_date = Parsed


    def extrapolate_time_data(self, get_errors=False):

        if self.start_time.type == "DATEUTIL, TIME" and \
                self.end_time.type == "DATEUTIL, TIME":
            start = self.start_time.dt_obj
            end = self.end_time.dt_obj

            if start < end:
                return True, "No Error"
            else:
                error = "Start time not before end time"
                return False, error

        if self.start_time.type == "DATEUTIL, TIME" and \
                self.end_time.type == "TIME, INCREMENT":

            return True, "No Error"

        elif self.start_time.type == "DEFAULT" and \
                self.end_time.type == "DEFAULT":
            return True, "No Error"

        elif self.start_time.type == "TIME, ALL DAY" and \
                self.end_time.type == "TIME, ALL DAY":
            return True, "No Error"

        else:
            error = "Info doesn't make sense together"
            return False, error


    def extrapolate_date_data(self):
        if not self.start_date or not self.end_date:
            return False, "_"

        elif self.start_date.type == "UNKNOWN" or \
                self.end_date.type == "UNKNOWN":
            return False, "Date Error"
        else:
            return True, "No Error"


    # TODO: fix this broken membership testing
    @staticmethod
    def parse_time(string):
        time_obj = dateutil.parser.parse(string)

        if time_obj.hour == 0 and time_obj.minute == 0 and \
                not string in {"0:00",
                               "12a",
                               "12am",
                               "12:00a",
                               "12:00am",
                               "12:00 a",
                               "12:00 am"}:
            return None

        elif NewEventParser.test_for_increment(string):
            return None

        return time_obj


    @staticmethod
    def parse_date(string):
        date_obj = dateutil.parser.parse(string)
        return date_obj


    def parse_time_increment(self, string):
        error = ("Example durations:\n"
                 "'5h' = 5 hours\n"
                 "'2.5h' = 2 hours 30 minutes"
                 "'30m' = 30 minutes")

        increment = float(string[0:-1])
        suffix = string[-1]

        time_notation = "minute" if suffix == "m" else "hour"

        if increment < 5 and time_notation == "minute":
            valid = False
            error = "Cannot make events shorter than 5 minutes."

        elif increment < .1 and time_notation == "hour":
            valid = False
            error = "Cannot make events shorter than .1 hours."

        elif increment >= 24 and time_notation == "hour":
            valid = False
            error = "Cannot set duration greater than 23.99 hours"

        elif increment >= 1440 and time_notation == "minute":
            valid = False
            error = "Cannot set duration greater than 1439 minutes"

        elif increment == 0:
            valid = False
            error = "Cannot set duration of 0"

        else:
            valid = True

        if time_notation == "hour":
            min_add = round(increment * 60)
        else:
            min_add = int(increment)

        curr_dt = self.start_time.dt_obj
        futr_dt = self.start_time.dt_obj + relativedelta(minutes=min_add)

        same_day = True if curr_dt.day == futr_dt.day else False
        if not same_day:
            valid = False
            error = "Duration can only be set up to the end of one day."

        if valid:
            error = None
            return min_add, error
        else:
            return None, f"Error: {error}."


    @staticmethod
    def test_for_dateutil(string):
        try:
            dateutil.parser.parse(string)
            return True
        except:
            return False


    @staticmethod
    def test_for_increment(string):
        if test_for_float(string[0:-1]) and \
                string[-1] == "h":
            return True

        elif test_for_float(string[0:-1]) and \
                string[-1] == "m":
            return True

        else:
            return False


    def get_error(self):
        if self.start_time:
            valid, error = self.extrapolate_time_data()

            if self.start_time.error:
                return self.start_time.error
            elif self.end_time.error:
                return self.end_time.error
            elif not valid:
                return error

        if self.start_date:
            valid, error = self.extrapolate_date_data()

            if self.start_date.error:
                return self.start_date.error
            elif self.end_date.error:
                return self.end_date.error
            elif not valid:
                return error

        else:
            return "Basic error"
        # etc. etc.


if __name__ == "__main__":
    parser = NewEventParser(datetime.datetime.now(tzlocal()))
    parser.parse_type("12a", "start time")
    print(parser.start_time)
    parser.parse_type("2p", "end time")
    print(parser.end_time)
    parser.parse_type("may 21", "start date")
    print(parser.start_date)
    parser.parse_type("may 22", "end date")
    print(parser.end_date)
