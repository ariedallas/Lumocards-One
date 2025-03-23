import math
import time

from dateutil.relativedelta import relativedelta

import LUMO_LIBRARY.lumo_animationlibrary as l_animators

from LUMO_LIBRARY.lumo_calendar_utils import (CalendarPageDay,
                                              CalendarPageWeek,
                                              Menus,
                                              curr_month,
                                              curr_year,
                                              get_adjacent_month,
                                              get_day_blocks,
                                              get_time_window_2,
                                              parse_brackets,
                                              today_date
                                              )


class CalendarInterface:
    curr_day_in_focus = None
    curr_week_in_focus = None
    curr_view = "DAY"


    def __init__(self):
        past_month = get_adjacent_month(curr_month, curr_year, "past", 1)
        next_month = get_adjacent_month(curr_month, curr_year, "next", 1)

        self.day_blocks_window = get_day_blocks()
        self.week_blocks_window = self.separate_by_weeks()

        self.day_idx = None


    def view_days(self):
        self.day_idx = self._get_idx_for_today()
        curr_day_block = self.day_blocks_window[self.day_idx]
        menu_dict, _ = Menus.main_cal_menus

        while True:
            curr_page = CalendarPageDay(curr_day_block)
            curr_page.display_day()
            curr_page.display_menu()

            print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT + f" {str(self.day_idx)}")
            print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT, end="  ")

            user_input = input(">  ")


            if "]" in user_input or "[" in user_input:
                curr_day_block = self.paginate_days(user_input)

            elif user_input.upper() in menu_dict.keys():
                self.calendar_actions_router(user_input); time.sleep(.5)

            elif user_input.lower() in {"x", "exit"}:
                print("Exit"); time.sleep(.5)

            elif user_input.lower() in {"q", "quit"}:
                print("Quit"); time.sleep(.5)

            elif user_input.lower() in {"t", "toggle, toggle view, change view"}:
                print("Quit"); time.sleep(.5)

            else:
                l_animators.animate_text_indented("  Unrecognized option...", indent=30,  finish_delay=.5)


    def paginate_days(self, user_input):
        shift, direction = parse_brackets(user_input)
        shift = shift if shift < 25 else 25

        if direction == "PAGE RIGHT":
            look_ahead_idx = self.day_idx + shift

            if look_ahead_idx < len(self.day_blocks_window) - 3:
                self.day_idx += shift
                curr_day_block = self.day_blocks_window[self.day_idx]
            else:
                # Means the idx is nearing the right end of the "buffered" events_block and needs to be updated
                # Function grabs a group of 4 isoweeks, "right"/future, relative to the current month in focus
                big_shift = self._roll_forward(amt_weeks=4, context="DAY VIEW")
                self.day_idx -= big_shift
                curr_day_block = self.day_blocks_window[self.day_idx]

        elif direction == "PAGE LEFT":
            look_ahead_idx = self.day_idx - shift

            if look_ahead_idx > 3:
                self.day_idx -= shift
                curr_day_block = self.day_blocks_window[self.day_idx]
            else:
                # Means the idx is nearing the left end of the "buffered" events block and needs to be updated
                # Functions grabs a group of 4 isoweeks, "left"/past, relative to the current date in focus
                big_shift = self._roll_backward(amt_weeks=4, context="DAY VIEW")
                self.day_idx += big_shift
                curr_day_block = self.day_blocks_window[self.day_idx]
        else:
            curr_day_block = self.day_blocks_window[self.day_idx]

        return curr_day_block

    def calendar_actions_router(self):
        print("lemon")
        pass

    def view_week(self):
        idx = self._get_idx_for_curr_week()
        curr_week_block = self.week_blocks_window[idx]

        while True:
            curr_page = CalendarPageWeek(curr_week_block)
            curr_page.display_week()

            print(" " * CalendarPageWeek.l_margin, idx)
            print(" " * CalendarPageWeek.l_margin, end=" ")

            user_input = input(">  ")

            shift, direction = parse_brackets(user_input)
            shift = shift if shift < len(self.week_blocks_window) else len(self.week_blocks_window)

            if direction == "PAGE RIGHT":
                look_ahead_idx = idx + shift

                if look_ahead_idx <= len(self.week_blocks_window) - 1:
                    idx += shift
                    curr_week_block = self.week_blocks_window[idx]

                else:
                    big_shift = self._roll_forward(amt_weeks=4, context="WEEK VIEW")
                    idx -= big_shift
                    curr_week_block = self.week_blocks_window[idx]

            elif direction == "PAGE LEFT":
                look_ahead_idx = idx - shift

                if look_ahead_idx >= 0:
                    idx -= shift
                    curr_week_block = self.week_blocks_window[idx]

                else:
                    big_shift = self._roll_backward(amt_weeks=4, context="WEEK VIEW")
                    idx += big_shift
                    curr_week_block = self.week_blocks_window[idx]

            else:
                print(" " * CalendarPageWeek.l_margin, end=" ")
                print("Use one or more brackets '[' or ']' to navigate.")
                curr_week_block = self.week_blocks_window[idx]


    def _get_idx_for_today(self):
        total_weeks = len(self.week_blocks_window)
        prior_weeks = round((total_weeks - 1) / 2)
        prior_days = prior_weeks * 7
        idx = prior_days + today_date.weekday()

        return idx


    def _get_idx_for_curr_week(self):
        total_weeks = len(self.week_blocks_window)
        center_idx = math.floor(total_weeks / 2)

        return center_idx


    def _roll_forward(self, amt_weeks, context):
        curr_final_monday = self.week_blocks_window[-1][0]
        target_monday = curr_final_monday.date + relativedelta(weeks=1)

        start, end = get_time_window_2(target_monday, 4)
        future_events = get_day_blocks(time_min=start, time_max=end)

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

        start, end = get_time_window_2(target_monday, window_size_weeks=amt_weeks)
        past_events = get_day_blocks(time_min=start, time_max=end)

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
    # calendar_interface.paginate_days()
    calendar_interface.view_days()


if __name__ == "__main__":
    main()
