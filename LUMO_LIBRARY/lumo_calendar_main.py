import math
import subprocess
import time
from pprint import pprint as pp
from typing import Optional, reveal_type

from dateutil.relativedelta import relativedelta

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
from LUMO_LIBRARY.lumo_calendar_utils import (CalendarPageDay,
                                              CalendarPageWeek,
                                              CalendarPageEvent,
                                              DayBlock,
                                              Event,
                                              Menus
                                              )


def clear():
    subprocess.run(["clear"], shell=True)


class CalendarInterface:
    default_view: str = "DAY"
    EVENTS_LIMIT_LOW: int = 6
    EVENTS_LIMIT_HIGH: int = 40


    def __init__(self):
        past_month = l_cal_utils.get_adjacent_month(l_cal_utils.curr_month,
                                                    l_cal_utils.curr_year,
                                                    "past", 1)

        next_month = l_cal_utils.get_adjacent_month(l_cal_utils.curr_month,
                                                    l_cal_utils.curr_year,
                                                    "next", 1)

        curr_view_mode: Optional[str] = None

        self.day_blocks_window: list[DayBlock]
        self.day_blocks_window = l_cal_utils.get_day_blocks()
        self.week_blocks_window = self.separate_by_weeks()

        self.curr_day_idx = self._get_idx_for_today()
        self.curr_week_idx = self._get_idx_for_curr_week()

        self.menu_size = "DAY LONG"
        self.events_limit = CalendarInterface.EVENTS_LIMIT_LOW

        self.custom_error_msg = None


    def _event_actions_router(self, user_input) -> None:
        print(user_input)
        print("lemon")
        pass


    def _view_day_actions_router(self,
                                 user_input: str,
                                 actions_dict: dict[str, str]
                                 ) -> Optional[tuple[bool, str, str]]:

        action = actions_dict[user_input.upper()]

        if action == Menus.ACTION_LIST_ALL:
            self.events_limit = CalendarInterface.EVENTS_LIMIT_HIGH
            update_menu = True
            old_val = action
            new_val = Menus.ACTION_LIST_FEW
            return update_menu, old_val, new_val

        elif action == Menus.ACTION_LIST_FEW:
            self.events_limit = CalendarInterface.EVENTS_LIMIT_LOW
            update_menu = True
            old_val = action
            new_val = Menus.ACTION_LIST_ALL
            return update_menu, old_val, new_val


    def _view_week_actions_router(self,
                                  user_input: str,
                                  actions_dict: dict[str, str]) -> None:

        print(actions_dict[user_input.upper()])
        print("lemon")


    def view_event(self, var_event_obj: Event) -> None:
        event_page = CalendarPageEvent(var_event_obj)
        menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.MAIN_CAL_MENU)

        while True:
            clear()
            event_page.display_event()
            event_page.display_menu()
            print()
            print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE, end="  ")

            user_input = input(">  ")

            if False:
                pass

            elif user_input.upper() in menu_dict.keys():
                self._event_actions_router(user_input);
                time.sleep(.5)

            elif user_input.lower() in {"x", "exit"}:
                break

            else:
                indent = int(CalendarPageDay.cursor_indent_amt) + 2
                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent=indent,
                                                  finish_delay=.5)


    def view_days(self) -> str:
        curr_day_block: DayBlock

        curr_day_block = self.day_blocks_window[self.curr_day_idx]
        menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.DAY_MENU_LONG)
        menu_update = False
        old_val = None
        new_val = None

        while True:
            if menu_update:
                menu_dict = self.contextualize(menu_dict, old_val, new_val, self.menu_size)
                menu_update = False

            curr_page = CalendarPageDay(curr_day_block)
            clear()
            curr_page.display_day(self.events_limit, CalendarInterface.EVENTS_LIMIT_LOW)
            curr_page.display_menu_columns(menu_dict)

            # print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE + f" {str(self.curr_day_idx)}")
            print()
            print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE, end="  ")

            user_input = input(">  ")

            if "]" in user_input or "[" in user_input:
                curr_day_block = self.paginate_days(user_input)

            elif curr_page.valid_event_selection(user_input,
                                                 len(curr_day_block.events)):
                selection = int(user_input) - 1
                selected_event = curr_day_block.events[selection]

                self.view_event(selected_event)


            elif user_input.upper() in menu_dict.keys():
                menu_update, old_val, new_val = self._view_day_actions_router(user_input, menu_dict)

            elif user_input.lower() in {"t", "toggle"}:
                self.curr_view_mode = "WEEK"
                for idx, group in enumerate(self.week_blocks_window):
                    if curr_day_block in group:
                        self.curr_week_idx = idx
                        break
                return "TOGGLE"

            elif user_input.lower() in {"q", "quit"}:
                return "QUIT"


            else:
                indent = int(CalendarPageDay.cursor_indent_amt) + 2
                custom_error = self.parse_for_error(user_input)

                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent=indent,
                                                  finish_delay=.5)

                if custom_error:
                    l_animators.animate_text_indented(custom_error,
                                                      indent=indent,
                                                      finish_delay=.5)


    def paginate_days(self, user_input: str) -> DayBlock:
        shift: int
        direction: Optional[str]

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


    def view_weeks(self) -> str:
        curr_week_block: list[DayBlock]

        curr_week_block = self.week_blocks_window[self.curr_week_idx]
        menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.MAIN_CAL_MENU)

        while True:
            curr_page = CalendarPageWeek(curr_week_block)
            clear()
            curr_page.display_week()
            curr_page.display_menu_columns()

            # print(CalendarPageDay.l_margin_space + CalendarPageDay.MENU_ITEM_INDENT_SPACE + f" {str(self.curr_week_idx)}")
            print()
            print(CalendarPageWeek.l_margin_menu_space, end="    ")

            user_input = input(">  ")

            if "]" in user_input or "[" in user_input:
                curr_week_block = self.paginate_weeks(user_input)

            elif user_input.upper() in menu_dict.keys():
                self._view_week_actions_router(user_input, menu_dict)
                time.sleep(.5)


            elif curr_page.valid_day_selection(user_input=user_input, var_weekblock=curr_week_block):
                week_in_focus_day_ints = [block.day for block in curr_week_block]
                selected_idx = week_in_focus_day_ints.index(int(user_input))
                selected_day_block = curr_week_block[selected_idx]
                self.curr_day_idx = self.day_blocks_window.index(selected_day_block)

                self.curr_view_mode = "DAY"
                return "TOGGLE"

            elif user_input.lower() in {"t", "toggle"}:
                self.curr_view_mode = "DAY"
                monday_of_curr_week = curr_week_block[0]
                self.curr_day_idx = self.day_blocks_window.index(monday_of_curr_week)
                return "TOGGLE"

            elif user_input.lower() in {"q", "quit"}:
                return "QUIT"


            else:
                indent = int(CalendarPageWeek.l_margin_menu) + 7
                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent=indent,
                                                  finish_delay=.5)


    def paginate_weeks(self,
                       user_input: str) -> list[DayBlock]:
        shift: int
        direction: Optional[str]

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
            print(" " * CalendarPageWeek.l_margin_menu, end=" ")
            print("Use one or more brackets '[' or ']' to navigate.")
            curr_week_block = self.week_blocks_window[self.curr_week_idx]

        print(reveal_type(curr_week_block));
        return curr_week_block


    def _get_idx_for_today(self) -> int:
        total_weeks = len(self.week_blocks_window)
        prior_weeks = round((total_weeks - 1) / 2)
        prior_days = prior_weeks * 7
        idx = prior_days + l_cal_utils.today_date.weekday()

        return idx


    def _get_idx_for_curr_week(self) -> int:
        total_weeks = len(self.week_blocks_window)
        center_idx = math.floor(total_weeks / 2)

        return center_idx


    def _roll_forward(self,
                      amt_weeks: int,
                      context: str) -> int:
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


    def _roll_backward(self,
                       amt_weeks: int,
                       context: str) -> int:
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


    def separate_by_weeks(self) -> list[list[DayBlock]]:
        separated_weeks = []
        num_weeks = round(len(self.day_blocks_window) / 7)
        for x in range(num_weeks):
            start = 7 * x
            end = (7 * x) + 7
            separated_weeks.append(self.day_blocks_window[start: end])

        return separated_weeks


    def contextualize(self, var_dict, old_val, new_val, menu_size):
        if old_val and new_val:
            return self.update_menu_item(var_dict, old_val, new_val)

        elif menu_size == "DAY SHORT":
            return Menus.DAY_MENU_SHORT
        elif menu_size == "DAY LONG":
            return Menus.DAY_MENU_LONG
        elif menu_size == "WEEK SHORT":
            return Menus.WEEK_MENU_SHORT
        elif menu_size == "WEEK LONG":
            return Menus.WEEK_MENU_LONG

        else:
            return var_dict


    def update_menu_item(self, var_dict, old_val, new_val):
        keys = [k for k, v in var_dict.items() if v == old_val]
        key = keys[0]
        var_dict.update({key: new_val})

        return var_dict


    def parse_for_error(self, user_input: str) -> Optional[str]:
        return "custom error message"


def main() -> None:
    cal_interface = CalendarInterface()
    cal_interface.curr_view_mode = CalendarInterface.default_view
    status = None

    while True:
        if status == "QUIT":
            return

        if cal_interface.curr_view_mode == "DAY":
            status = cal_interface.view_days()

        elif cal_interface.curr_view_mode == "WEEK":
            status = cal_interface.view_weeks()


if __name__ == "__main__":
    main()
