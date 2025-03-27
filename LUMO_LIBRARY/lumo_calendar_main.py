import math
import time
from pprint import pprint as pp

from dateutil.relativedelta import relativedelta

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
from LUMO_LIBRARY.lumo_calendar_utils import (CalendarPageDay,
                                              CalendarPageWeek,
                                              Menus
                                              )


class CalendarInterface:
    default_view: str = "WEEK"
    curr_view_mode: str | None = None


    def __init__(self):
        past_month = l_cal_utils.get_adjacent_month(l_cal_utils.curr_month,
                                        l_cal_utils.curr_year,
                                        "past", 1)

        next_month = l_cal_utils.get_adjacent_month(l_cal_utils.curr_month,
                                        l_cal_utils.curr_year,
                                        "next", 1)

        self.day_blocks_window = l_cal_utils.get_day_blocks()
        self.week_blocks_window = self.separate_by_weeks()

        self.curr_day_idx = self._get_idx_for_today()
        self.curr_week_idx = self._get_idx_for_curr_week()


    def calendar_actions_router(self):
        print("lemon")
        pass

    def view_days(self):
        curr_day_block = self.day_blocks_window[self.curr_day_idx]
        menu_dict, _ = l_menus_funcs.prep_menu(Menus.MAIN_CAL_MENU)

        while True:
            curr_page = CalendarPageDay(curr_day_block)
            curr_page.display_day()
            curr_page.display_menu()

            # print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE + f" {str(self.curr_day_idx)}")
            print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE, end="  ")

            user_input = input(">  ")

            if "]" in user_input or "[" in user_input:
                curr_day_block = self.paginate_days(user_input)

            elif user_input.upper() in menu_dict.keys():
                self.calendar_actions_router(user_input);
                time.sleep(.5)

            elif user_input.lower() in {"t", "toggle"}:
                CalendarInterface.curr_view_mode = "WEEK"
                for idx, group in enumerate(self.week_blocks_window):
                    if curr_day_block in group:
                        self.curr_week_idx = idx
                        break
                return "TOGGLE"

            elif user_input.lower() in {"q", "quit"}:
                return "QUIT"


            else:
                l_animators.animate_text_indented("  Unrecognized option...",
                                                  indent=CalendarPageDay.cursor_indent_amt,
                                                  finish_delay=.5)


    def paginate_days(self, user_input):
        shift, direction = l_cal_utils.parse_brackets(user_input)
        shift = shift if shift < 25 else 25

        if direction == "PAGE RIGHT":
            look_ahead_idx = self.curr_day_idx + shift

            if look_ahead_idx < len(self.day_blocks_window) - 3:
                self.curr_day_idx += shift
                curr_day_block = self.day_blocks_window[self.curr_day_idx]
            else:
                # Means the idx is nearing the right end of the "buffered" events_block and needs to be updated
                # Function grabs a group of 4 isoweeks, "right"/future, relative to the current month in focus
                big_shift = self._roll_forward(amt_weeks=4, context="DAY VIEW")
                self.curr_day_idx -= big_shift
                curr_day_block = self.day_blocks_window[self.curr_day_idx]

        elif direction == "PAGE LEFT":
            look_ahead_idx = self.curr_day_idx - shift

            if look_ahead_idx > 3:
                self.curr_day_idx -= shift
                curr_day_block = self.day_blocks_window[self.curr_day_idx]
            else:
                # Means the idx is nearing the left end of the "buffered" events block and needs to be updated
                # Functions grabs a group of 4 isoweeks, "left"/past, relative to the current date in focus
                big_shift = self._roll_backward(amt_weeks=4, context="DAY VIEW")
                self.curr_day_idx += big_shift
                curr_day_block = self.day_blocks_window[self.curr_day_idx]
        else:
            curr_day_block = self.day_blocks_window[self.curr_day_idx]

        return curr_day_block



    def view_weeks(self):
        curr_week_block = self.week_blocks_window[self.curr_week_idx]
        menu_dict, _ = l_menus_funcs.prep_menu(Menus.MAIN_CAL_MENU)


        while True:
            curr_page = CalendarPageWeek(curr_week_block)
            curr_page.display_week()
            curr_page.display_menu_column()

            # print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE + f" {str(self.curr_week_idx)}")
            print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE, end="  ")

            user_input = input(">  ")

            if "]" in user_input or "[" in user_input:
                curr_week_block = self.paginate_weeks(user_input)

            elif user_input.upper() in menu_dict.keys():
                self.calendar_actions_router(user_input)


            elif l_cal_utils.validate_day_seleciton(user_input, curr_week_block):
                week_in_focus_day_ints = [block.day for block in curr_week_block]
                selected_idx = week_in_focus_day_ints.index(int(user_input))
                selected_day_block = curr_week_block[selected_idx]
                self.curr_day_idx = self.day_blocks_window.index(selected_day_block)

                CalendarInterface.curr_view_mode = "DAY"
                return "TOGGLE"

            elif user_input.lower() in {"t", "toggle"}:
                CalendarInterface.curr_view_mode = "DAY"
                monday_of_curr_week = curr_week_block[0]
                self.curr_day_idx = self.day_blocks_window.index(monday_of_curr_week)
                return "TOGGLE"

            elif user_input.lower() in {"q", "quit"}:
                return "QUIT"


            else:
                l_animators.animate_text_indented("  Unrecognized option...",
                                                  indent=CalendarPageDay.cursor_indent_amt,
                                                  finish_delay=.5)


    def paginate_weeks(self, user_input):
        shift, direction = l_cal_utils.parse_brackets(user_input)
        shift = shift if shift < len(self.week_blocks_window) else len(self.week_blocks_window)

        if direction == "PAGE RIGHT":
            look_ahead_idx = self.curr_week_idx + shift

            if look_ahead_idx <= len(self.week_blocks_window) - 1:
                self.curr_week_idx += shift
                curr_week_block = self.week_blocks_window[self.curr_week_idx]

            else:
                big_shift = self._roll_forward(amt_weeks=4, context="WEEK VIEW")
                self.curr_week_idx -= big_shift
                curr_week_block = self.week_blocks_window[self.curr_week_idx]

        elif direction == "PAGE LEFT":
            look_ahead_idx = self.curr_week_idx - shift

            if look_ahead_idx >= 0:
                self.curr_week_idx -= shift
                curr_week_block = self.week_blocks_window[self.curr_week_idx]

            else:
                big_shift = self._roll_backward(amt_weeks=4, context="WEEK VIEW")
                self.curr_week_idx += big_shift
                curr_week_block = self.week_blocks_window[self.curr_week_idx]

        else:
            print(" " * CalendarPageWeek.l_margin, end=" ")
            print("Use one or more brackets '[' or ']' to navigate.")
            curr_week_block = self.week_blocks_window[self.curr_week_idx]

        return curr_week_block


    def _get_idx_for_today(self):
        total_weeks = len(self.week_blocks_window)
        prior_weeks = round((total_weeks - 1) / 2)
        prior_days = prior_weeks * 7
        idx = prior_days + l_cal_utils.today_date.weekday()

        return idx


    def _get_idx_for_curr_week(self):
        total_weeks = len(self.week_blocks_window)
        center_idx = math.floor(total_weeks / 2)

        return center_idx


    def _roll_forward(self, amt_weeks, context):
        curr_final_monday = self.week_blocks_window[-1][0]
        target_monday = curr_final_monday.date + relativedelta(weeks=1)

        start, end = l_cal_utils.get_time_window_2(target_monday, 4)
        future_events = l_cal_utils.get_day_blocks(time_min=start, time_max=end)

        day_blocks_to_keep = self.day_blocks_window[28:]
        self.day_blocks_window = day_blocks_to_keep + future_events
        self.week_blocks_window = self.separate_by_weeks()

        if context == "DAY VIEW":
            idx_shift = len(future_events) - 1
        else:
            idx_shift = amt_weeks - 1

        return idx_shift


    def _roll_backward(self, amt_weeks, context):
        curr_first_monday = self.week_blocks_window[0][0]
        target_monday = curr_first_monday.date - relativedelta(weeks=amt_weeks)

        start, end = l_cal_utils.get_time_window_2(target_monday, window_size_weeks=amt_weeks)
        past_events = l_cal_utils.get_day_blocks(time_min=start, time_max=end)

        day_blocks_to_keep = self.day_blocks_window[:-28]
        self.day_blocks_window = past_events + day_blocks_to_keep
        self.week_blocks_window = self.separate_by_weeks()

        if context == "DAY VIEW":
            idx_shift = len(past_events) - 1
        else:
            idx_shift = amt_weeks - 1

        return idx_shift


    def separate_by_weeks(self):
        separated_weeks = []
        num_weeks = round(len(self.day_blocks_window) / 7)
        for x in range(num_weeks):
            start = 7 * x
            end = (7 * x) + 7
            separated_weeks.append(self.day_blocks_window[start: end])

        return separated_weeks


def main():
    calendar_interface = CalendarInterface()
    CalendarInterface.curr_view_mode = CalendarInterface.default_view
    status = None

    while True:
        if status == "QUIT":
            return

        if CalendarInterface.curr_view_mode == "DAY":
            status = calendar_interface.view_days()

        elif CalendarInterface.curr_view_mode == "WEEK":
            status = calendar_interface.view_weeks()


if __name__ == "__main__":
    main()
