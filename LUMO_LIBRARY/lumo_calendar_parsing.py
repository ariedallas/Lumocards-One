import datetime
from collections import namedtuple

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

    def __init__(self):
        self.start_time = None
        self.end_time = None


    @staticmethod
    def get_basic_type(string, target):
        if string == "":
            dt_type = "DEFAULT"

        elif test_for_float(string[0:-1]) and \
            string[-1] == "m" and \
                target == "end time":
            dt_type = "TIME, INCREMENT"

        elif test_for_float(string[0:-1]) and \
            string[-1] == "h" and \
            target == "end time":
            dt_type = "TIME, INCREMENT"

        elif string[0].isdigit() \
                and string[-1].isalpha() \
                and 2 <= len(string) <= 4:
            dt_type = "TIME, STANDARD"

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

        elif dt_type == "DEFAULT" and target == "end time":
            dt_obj = self.start_time.dt_obj + relativedelta(minutes=30)
            display = dt_obj.time().strftime("%I:%M %p").lower()
            dt_type = "TIME, INCREMENT"

        elif dt_type == "TIME, STANDARD":
            hour, error = NewEventParser.parse_time_stnd(string)
            if not error:
                dt_obj = datetime.datetime.now().replace(hour=hour,
                                                         minute=0,
                                                         second=0,
                                                         microsecond=0)
                display = dt_obj.time().strftime("%I:%M %p").lower()
            else:
                dt_type = "UNKNOWN"

        elif dt_type == "TIME, ALL DAY" and \
                (target == "start time" or target == "end time"):
            display = "all day"

        elif dt_type == "TIME, INCREMENT":
            min_add, error = NewEventParser.parse_time_increment(string)
            if not error:
                dt_obj = self.start_time.dt_obj + relativedelta(minutes=min_add)
                display = dt_obj.time().strftime("%I:%M %p").lower()
            else:
                dt_type = "UNKNOWN"

        elif dt_type == "UNKNOWN":
            error = "Unknown input"

        Parsed = ParseResult(dt_type, hour, increment, dt_obj, display, error)

        if target == "start time":
            self.start_time = Parsed
        elif target == "end time":
            self.end_time = Parsed


    @staticmethod
    def parse_time_stnd(string):
        num = None
        add = None
        error = "Please see example times"

        if len(string) == 4 and \
                string[:2].isdigit() and \
                string[2:4].isalpha():

            prefix = string[:2]
            suffix = string[-2:]

            if prefix in {"10", "11", "12"} and \
                    suffix in {"am", "pm"}:
                valid = True
                num = int(prefix)
                dt_frmt = NewEventParser.am_pm_addition(num, suffix)

            else:
                error = f"The digits don't make sense with '{suffix}'"
                valid = False


        elif len(string) == 3:

            if string[:2].isdigit() and \
                    string[-1] in {"a", "p"}:

                num = int(string[:2])
                suffix = string[-1]
                if num in range(9, 13):
                    valid = True
                    dt_frmt = NewEventParser.am_pm_addition(num, suffix)

                else:
                    valid = False
                    error = "These digits aren't 10, 11, or 12"

            elif string[0].isdigit() and \
                    string[-2:] in {"am", "pm"}:

                num = int(string[0])
                suffix = string[-2:]
                if num in range(1, 10):
                    valid = True
                    dt_frmt = NewEventParser.am_pm_addition(num, suffix)

                else:
                    valid = False
                    error = "The number 0 doesn't make sense here."

            else:
                valid = False


        elif len(string) == 2 and \
                string[-1] in {"a", "p"}:

            num = int(string[0])
            suffix = string[-1]
            if num in range(1, 10):
                valid = True
                dt_frmt = NewEventParser.am_pm_addition(num, suffix)

            else:
                valid = False
                error = "The number 0 doesn't work here"

        else:
            valid = False

        if valid:
            error = None
            return dt_frmt, error
        else:
            return None, f"Unknown input: {error}"

    @staticmethod
    def parse_time_increment(string):
        increment = None
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
            minutes = round(increment * 60)
        else:
            minutes = int(increment)

        if valid:
            error = None
            return minutes, error
        else:
            return None, f"Error: {error}."


    def extrapolate_time_data(self):

        if self.start_time.type == "TIME, STANDARD" and \
                self.end_time.type == "TIME, STANDARD":
            start = self.start_time.dt_obj
            end = self.end_time.dt_obj

            if start < end:
                return True
            else:
                return False

        if self.start_time.type == "TIME, STANDARD" and \
            self.end_time.type == "TIME, INCREMENT":

            start = self.start_time.dt_obj
            end = self.end_time.dt_obj

            if start.day == end.day:
                return True
            else:
                comparison_error = ("Can only set duration"
                                       "up to the end of the day")
                return False

        elif self.start_time.type == "DEFAULT" and \
                self.end_time.type == "DEFAULT":
            return True

        elif self.start_time.type == "TIME, ALL DAY" and \
                self.end_time.type == "TIME, ALL DAY":
            return True

        else:
            return False


    def extrapolate_date_data(self):
        return False


    @staticmethod
    def am_pm_addition(num, suffix):
        if num == 12 and suffix in {"a", "am"}:
            return 0
        elif num == 12 and suffix in {"p", "pm"}:
            return 12
        else:
            add = 0 if suffix in {"a", "am"} else 12
            dt_num = num + add
            return dt_num


    def parse_startDate(self):
        pass


    def parse_endDate(self):
        pass


if __name__ == "__main__":
    test = "0.1"
    test_b = "12"
    test_c = ".5"
    test_d = "0.1.2"

    print()

    parser = NewEventParser()
    parser.parse_type("2pm", "start time")
    print(parser.start_time)
    parser.parse_type("9h", "end time")
    print(parser.end_time)

    print(parser.extrapolate_time_data())
