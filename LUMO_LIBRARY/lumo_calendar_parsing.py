import datetime
from dateutil.relativedelta import relativedelta


class CalendarDTParser:
    def __init__(self, string_1):
        self.s = string_1
        self.string = self.s.strip().lower()


    def get_basic_type(self):
        if self.string[0].isdigit() \
                and self.string[-1].isalpha() \
                and 2 <= len(self.string) <= 4:
            dt_type = "TIME, STANDARD"

        else:
            dt_type = "UNKNOWN"

        return dt_type


    def parse_type(self):
        dt_type = self.get_basic_type()

        if dt_type == "TIME, STANDARD":
            parsed = self.parse_startTime_stnd()

        elif dt_type == "UNKNOWN":
            parsed = "Unknown input"

        return dt_type, parsed


    def parse_startTime_stnd(self):
        num = None
        add = None
        error = "Please see example times"

        if len(self.string) == 4 and \
                self.string[:2].isdigit() and \
                self.string[2:4].isalpha():

            prefix = self.string[:2]
            suffix = self.string[-2:]

            if prefix in {"10", "11", "12"} and \
                    suffix in {"am", "pm"}:
                valid = True
                num = int(prefix)
                add = 0 if suffix == "am" else 12
                dt_frmt = num + add


            else:
                error = f"The digits don't make sense with '{suffix}'"
                valid = False


        elif len(self.string) == 3:

            if self.string[:2].isdigit() and \
                    self.string[-1] in {"a", "p"}:

                num = int(self.string[:2])

                if num in range(9, 13):
                    valid = True
                    add = 0 if self.string[-1] == "a" else 12
                    dt_frmt = num + add


                else:
                    valid = False
                    error = "These digits aren't 10, 11, or 12"



            elif self.string[0].isdigit() and \
                    self.string[-2:] in {"am", "pm"}:

                num = int(self.string[0])
                if num in range(1, 10):
                    valid = True
                    add = 0 if self.string[-2:] == "am" else 12
                    dt_frmt = num + add


                else:
                    valid = False
                    error = "The number 0 doesn't make sense here."

            else:
                valid = False


        elif len(self.string) == 2 and \
                self.string[-1] in {"a", "p"}:

            num = int(self.string[0])
            if num in range(1, 10):
                valid = True
                add = 0 if self.string[-1] == "a" else 12
                dt_frmt = num + add


            else:
                valid = False
                error = "The number 0 doesn't work here"


        else:
            valid = False


        if valid:
            return self.string, num, add, dt_frmt
        else:
            return f"Unknown input: {error}"


    @classmethod
    def parse_for_am_pm(ltr):
        return True if ltr in {"a", "p"} else False


    def parse_endTime(self):
        pass


    def parse_startDate(self):
        pass


    def parse_endDate(self):
        pass


parser = CalendarDTParser('1pm', '2pm')
print(parser.parse_type())
