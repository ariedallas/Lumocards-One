import datetime
from collections import namedtuple

from dateutil.relativedelta import relativedelta

ParseResult = namedtuple("ParseResult",
                         [
                             "type",
                             "hour",
                             "increment",
                             "error"])


class CalendarDTParser:

    def __init__(self, string_1, string_2):
        self.string_1 = string_1.strip().lower() if string_1 else None
        self.string_2 = string_2.strip().lower() if string_2 else None


    @staticmethod
    def get_basic_type(string):
        if string[0].isdigit() \
                and string[-1].isalpha() \
                and 2 <= len(string) <= 4:
            dt_type = "TIME, STANDARD"

        else:
            dt_type = "UNKNOWN"

        return dt_type


    @staticmethod
    def parse_type(string):
        dt_type = CalendarDTParser.get_basic_type(string)

        if dt_type == "TIME, STANDARD":
            hour, error = CalendarDTParser.parse_time_stnd(string)
            increment = None

        elif dt_type == "UNKNOWN":
            hour = None
            increment = None
            error = "Unknown input"

        Parsed = ParseResult(dt_type, hour, increment, error)
        return Parsed


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
                dt_frmt = CalendarDTParser.am_pm_addition(num, suffix)

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
                    dt_frmt = CalendarDTParser.am_pm_addition(num, suffix)



                else:
                    valid = False
                    error = "These digits aren't 10, 11, or 12"



            elif string[0].isdigit() and \
                    string[-2:] in {"am", "pm"}:

                num = int(string[0])
                suffix = string[-2:]
                if num in range(1, 10):
                    valid = True
                    dt_frmt = CalendarDTParser.am_pm_addition(num, suffix)



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
                dt_frmt = CalendarDTParser.am_pm_addition(num, suffix)


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


    def compare_time_data(self):
        Parse_1 = CalendarDTParser.parse_type(self.string_1)
        Parse_2 = CalendarDTParser.parse_type(self.string_2)

        if Parse_1.type == "TIME, STANDARD" and \
                Parse_2.type == "TIME, STANDARD":
            time_obj_1 = datetime.time(hour=Parse_1.hour)
            time_obj_2 = datetime.time(hour=Parse_2.hour)


        print(Parse_1, Parse_2)
        print(time_obj_1, time_obj_2)


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


    def parse_endTime(self):
        pass


    def parse_startDate(self):
        pass


    def parse_endDate(self):
        pass


parser = CalendarDTParser("12a", "2am")
parser.compare_time_data()
