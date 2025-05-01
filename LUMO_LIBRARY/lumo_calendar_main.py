import datetime
import math
import subprocess
from itertools import chain
from typing import Optional, reveal_type

from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_calendar_actions as l_cal_actions
import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils
import LUMO_LIBRARY.lumo_calendar_parsing as l_cal_parse
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
from LUMO_LIBRARY.lumo_calendar_utils import (CalendarPageDay, CalendarPageEvent, CalendarPageWeek, DayBlock, Event,
                                              Menus)


def clear() -> None:
    subprocess.run(["clear"], shell=True)


class CalendarInterface:
    default_view: str = "WEEK"
    EVENTS_LIMIT_LOW: int = 6
    EVENTS_LIMIT_HIGH: int = 40


    def __init__(self):
        self.curr_view_mode = CalendarInterface.default_view

        self.day_blocks_window: list[DayBlock] = l_cal_utils.get_day_blocks()
        self.week_blocks_window: list[list[DayBlock]] = self._separate_by_weeks()

        self.curr_day_idx: int = self._get_idx_for_today()
        self.curr_week_idx: int = self._get_idx_for_curr_week()
        self.today = datetime.datetime.now(
            tzlocal()).replace(
            minute=0, second=0, microsecond=0)

        self.menu_size: Optional[str] = None

        self.events_limit: int = CalendarInterface.EVENTS_LIMIT_LOW

        self.custom_error_msg: Optional[str] = None

        self.creds = l_cal_utils.get_creds()


    def _refresh_DayBlock(self, curr_page: CalendarPageDay) -> None:
        curr_start = curr_page.day_block.date
        curr_end = curr_start + relativedelta(days=1)

        selected_events = l_cal_utils.get_google_events(self.creds, curr_start, curr_end)
        refreshed_events = [l_cal_utils.google_event_to_obj(e) for
                            e in selected_events]
        curr_page.day_block.events = refreshed_events


    def _event_actions_router(self,
                              user_input: str,
                              actions_dict: dict[str, str],
                              event_obj: Event):

        action = actions_dict[user_input.upper()]

        if action == Menus.ACTION_EDIT_TITLE:
            l_animators.animate_text_indented("Edited event",
                                              indent=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)
            return False, None, None, "UPDATED EVENT"

        elif action == Menus.ACTION_EDIT_TIMES:
            l_animators.animate_text_indented("Edited times",
                                              indent=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)
            return False, None, None, "UPDATED EVENT"

        elif action == Menus.ACTION_EDIT_DATE:
            l_animators.animate_text_indented("Edited date",
                                              indent=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)
            return False, None, None, "UPDATED EVENT"


        elif action == Menus.ACTION_EDIT_NOTES:
            l_animators.animate_text_indented("Edited notes",
                                              indent=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)
            return False, None, None, "UPDATED DESCRIPTION"

        elif action == Menus.ACTION_MENU_LESS:
            self.menu_size = "EVENT SHORT"
            return True, None, None, "RELOOP"

        elif action == Menus.ACTION_MENU_MORE:
            self.menu_size = "EVENT LONG"
            return True, None, None, "RELOOP"

        elif action == Menus.ACTION_EDIT_LOCATION:
            l_animators.animate_text_indented("Edited locations",
                                              indent=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)
            return False, None, None, "UPDATED EVENT"

        elif action == Menus.ACTION_DELETE_EVENT:
            l_cal_actions.delete_event(event_obj.id)
            l_animators.animate_text_indented("Deleted event",
                                              indent=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)

            return False, None, None, "DELETED EVENT"


    def _day_actions_router(self,
                            user_input: str,
                            actions_dict: dict[str, str]
                            ) -> Optional[
        tuple[bool, Optional[str], Optional[str]]
    ]:

        action = actions_dict[user_input.upper()]

        if action == Menus.ACTION_NEW_EVENT:
            self.make_new_event()
            return False, None, None

        elif action == Menus.ACTION_LIST_ALL:
            self.events_limit = CalendarInterface.EVENTS_LIMIT_HIGH
            old_val = action
            new_val = Menus.ACTION_LIST_FEW
            return True, old_val, new_val

        elif action == Menus.ACTION_LIST_FEW:
            self.events_limit = CalendarInterface.EVENTS_LIMIT_LOW
            old_val = action
            new_val = Menus.ACTION_LIST_ALL
            return True, old_val, new_val

        elif action == Menus.ACTION_MENU_LESS:
            self.menu_size = "DAY SHORT"
            return True, None, None

        elif action == Menus.ACTION_MENU_MORE:
            self.menu_size = "DAY LONG"
            return True, None, None


    def _week_actions_router(self,
                             user_input: str,
                             actions_dict: dict[str, str]) -> None:

        status = None
        action = actions_dict[user_input.upper()]

        if action == Menus.ACTION_NEW_EVENT:
            self.make_new_event(default_use_today=True)
            return status


    def view_event(self, event_obj: Event) -> None:
        event_page = CalendarPageEvent(event_obj)
        menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.EVENT_MENU_LONG)
        menu_dict = self._contextualize(menu_dict,
                                        None,
                                        None,
                                        self.menu_size)
        menu_update = False

        while True:
            if menu_update:
                menu_dict = self._contextualize(menu_dict,
                                                None,
                                                None,
                                                self.menu_size)
                menu_update = False

            clear()
            event_page.display_event(event_obj)
            event_page.display_menu_columns(menu_dict)
            print()

            print(CalendarPageEvent.cursor_indent_space, end="  ")
            user_input = input(">  ")

            if user_input.upper() in menu_dict.keys():
                menu_update, _, _, status = self._event_actions_router(user_input,
                                                                       menu_dict,
                                                                       event_obj)
                if status == "DELETED EVENT":
                    return status


            elif user_input.lower() in {"x", "exit"}:
                break

            elif user_input.lower() in {"s", "save"}:
                l_animators.animate_text_indented("Saved event",
                                                  indent=CalendarPageEvent.msg_indent_1,
                                                  finish_delay=.5)
                break

            else:
                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent=CalendarPageEvent.msg_indent_1,
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
                menu_dict = self._contextualize(menu_dict, old_val, new_val, self.menu_size)
                old_val, new_val = None, None
                menu_update = False

            curr_page = CalendarPageDay(curr_day_block)
            clear()
            curr_page.display_day(self.events_limit, CalendarInterface.EVENTS_LIMIT_LOW)
            curr_page.display_menu_columns(menu_dict)

            print()
            print(CalendarPageDay.cursor_indent_space, end="  ")

            user_input = input(">  ")

            if "]" in user_input or "[" in user_input:
                curr_day_block = self.paginate_days(user_input)

            elif curr_page.valid_event_selection(user_input,
                                                 len(curr_day_block.events),
                                                 self.events_limit):
                selection = int(user_input) - 1
                selected_event = curr_day_block.events[selection]

                status = self.view_event(selected_event)

                if status == "DELETED EVENT":
                    self._refresh_DayBlock(curr_page)
                    break


            elif user_input.upper() in menu_dict.keys():
                menu_update, old_val, new_val = self._day_actions_router(user_input, menu_dict)

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
                custom_error = self.parse_for_error(user_input)

                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent=CalendarPageDay.msg_indent_num,
                                                  finish_delay=.5)

                if custom_error:
                    l_animators.animate_text_indented(custom_error,
                                                      indent=CalendarPageDay.msg_indent_num,
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
        menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.WEEK_MENU_SHORT)

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
                status = self._week_actions_router(user_input, menu_dict)


            elif curr_page.valid_day_selection(user_input=user_input, var_weekblock=curr_week_block):
                week_in_focus_day_ints = [block.day for block in curr_week_block]
                selected_idx = week_in_focus_day_ints.index(int(user_input))
                selected_day_block = curr_week_block[selected_idx]
                self.curr_day_idx = self.day_blocks_window.index(selected_day_block)

                self.curr_view_mode = "DAY"
                return "TOGGLE"

            elif user_input.lower() in {"t", "toggle"}:
                self.curr_view_mode = "DAY"
                monday_DayBlock = curr_week_block[0]
                target_date = monday_DayBlock.date
                self.curr_day_idx = self._day_index_lookup(target_date)

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


    def make_new_event(self, default_use_today=False):
        # 2: parse, then ask user for corrections
        # parse the dictionary
        # either it passes or fails

        # if it passes, create object, create event, refresh, display
        # if it fails display errors, use dictionary for updates, prompt

        # how do atomic updates show fails?
        if not default_use_today:
            curr_day_block = self.day_blocks_window[self.curr_day_idx]
            date_in_focus = curr_day_block.date
        else:
            date_in_focus = self.today

        new_event_dict = {}
        event_page = CalendarPageEvent(None)
        dt_parser = l_cal_parse.NewEventParser(date_in_focus)
        event_created = False

        while not event_created:
            continue_forLoop = False
            end_idx = len(Menus.NEW_EVENT_CATEGORIES) - 1

            clear()
            event_page.display_new_event(new_event_dict)
            event_page.display_prompts_subheader(date_in_focus)
            print()

            for idx, prompt_set in enumerate(Menus.NEW_EVENT_CATEGORIES):
                keys_iter = chain.from_iterable(d.keys() for d in prompt_set)
                keys = list(keys_iter)

                if continue_forLoop:
                    continue

                if idx == end_idx:
                    key = keys[0]
                    value = new_event_dict.get(key)
                    if value:
                        event_created = True

                single_prompt = False if len(prompt_set) > 1 else True

                if single_prompt:
                    key = keys[0]
                    value = new_event_dict.get(key)
                    if value:
                        continue
                else:
                    key_a, key_b = keys
                    value_a, value_b = (new_event_dict.get(key_a),
                                        new_event_dict.get(key_b))

                    if value_a and value_b:
                        continue

                if single_prompt:
                    prompt = prompt_set[0].get(key)
                    result = self.prompter_single(prompt)
                    new_event_dict[key] = result
                    continue_forLoop = True
                else:
                    prompt_one = prompt_set[0].get(key_a)
                    prompt_two = prompt_set[1].get(key_b)

                    target_1, target_2 = ("start time", "end time") \
                        if prompt_one == Menus.P_S_TIME \
                        else ("start date", "end date")

                    # I think you need to split this up so that you can handle
                    # errors/and confirmations in dates as it's own function
                    # OR, try it first with prompter_dateTime
                    result_a, result_b = self.prompter_double(prompt_one,
                                                              prompt_two,
                                                              date_in_focus)


                    dt_parser.parse_type(result_a, target_1)
                    dt_parser.parse_type(result_b, target_2)

                    print(dt_parser.start_date, dt_parser.end_date); input("???")

                    if dt_parser.extrapolate_time_data() and \
                            not dt_parser.extrapolate_date_data():
                        new_event_dict[key_a] = dt_parser.start_time.display

                        new_event_dict[key_b] = dt_parser.end_time.display

                        continue_forLoop = True

                    elif dt_parser.extrapolate_date_data() and \
                            dt_parser.extrapolate_date_data():
                        new_event_dict[key_a] = dt_parser.end_date.display
                        new_event_dict[key_b] = dt_parser.start_date.display
                        continue_forLoop = True

                    else:
                        continue_forLoop = True
                        continue

        print(new_event_dict);
        input("???")


    def prompter_single(self, prompt):
        wh_sp = l_cal_utils.CalendarPageEvent.l_margin_space + "  "
        full_prompt = wh_sp + prompt + "  "

        user_input = input(full_prompt)

        if prompt == Menus.P_TITLE:
            user_input_validated = "(no title)" if user_input == "" else user_input
            # animators use error msg

        elif prompt == Menus.P_DESCRIPTION:
            if (user_input.lower()
                    in l_menus_data.NEGATIVE_USER_RESPONSES
                    or user_input == ""):
                user_input_validated = "none"

            else:
                user_input_validated = user_input

        elif prompt == Menus.P_LOCATION:
            if (user_input.lower()
                    in l_menus_data.NEGATIVE_USER_RESPONSES
                    or user_input == ""):
                user_input_validated = "none"

            else:
                user_input_validated = user_input

        return user_input_validated


    def prompter_dateTime(self, prompt, prev_context, date_in_focus):
        prompt_with_context = self._contextualize_prompt(prompt, prev_context, date_in_focus)
        wh_sp = l_cal_utils.CalendarPageEvent.l_margin_space + "  "
        wh_sp_num = l_cal_utils.CalendarPageEvent.msg_indent_2
        full_prompt = wh_sp + prompt_with_context + "  "

        if prompt == Menus.P_E_TIME:
            if prev_context == "":
                return ""
            elif prev_context == "all day":
                return "all day"

        user_input = input(full_prompt)
        return user_input


    def prompter_double(self, prompt_one, prompt_two, date_in_focus):
        user_input_one = self.prompter_dateTime(prompt_one, None, date_in_focus)
        user_input_two = self.prompter_dateTime(prompt_two, user_input_one, None)

        return user_input_one, user_input_two


    def _contextualize_prompt(self, prompt, prev_context, date_in_focus):
        if prompt == Menus.P_S_TIME:
            prompt_with_context = prompt

        elif prompt == Menus.P_E_TIME:
            if prev_context == "all day" or prev_context == "":
                prompt_with_context = f"{prompt} ( ➝ same day) :"
            else:
                prompt_with_context = f"{prompt} ( + 30 mins) :"

        elif prompt == Menus.P_S_DATE:
            default_date = date_in_focus.strftime("( ➝ in focus)")
            prompt_with_context = f"{prompt}  {default_date} :"

        elif prompt == Menus.P_E_DATE:
            default_date = "( ➝ etc.)"
            prompt_with_context = f"{prompt}  {default_date} :"

        else:
            prompt_with_context = prompt

        return prompt_with_context


    def get_default_action(self):
        pass


    def update_default_action(self):
        pass


    # you'll need to parse previous inputs
    # to update the default context action
    # if the parsing breaks the default action is (???)

    def _day_index_lookup(self, target_date):
        for idx, db in enumerate(self.day_blocks_window):
            if db.date == target_date:
                return idx


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
        self.week_blocks_window = self._separate_by_weeks()

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
        self.week_blocks_window = self._separate_by_weeks()

        if context == "DAY VIEW":
            idx_shift = len(past_events) - 1
        else:
            idx_shift = amt_weeks - 1

        return idx_shift


    def _separate_by_weeks(self) -> list[list[DayBlock]]:
        separated_weeks = []
        num_weeks = round(len(self.day_blocks_window) / 7)
        for x in range(num_weeks):
            start = 7 * x
            end = (7 * x) + 7
            separated_weeks.append(self.day_blocks_window[start: end])

        return separated_weeks


    def _contextualize(self, var_dict, old_val, new_val, menu_size):
        if old_val and new_val:
            return self._update_menu_item(var_dict, old_val, new_val)

        elif menu_size == "EVENT SHORT":
            menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.EVENT_MENU_SHORT)
            return menu_dict
        elif menu_size == "EVENT LONG":
            menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.EVENT_MENU_LONG)
            return menu_dict
        elif menu_size == "DAY SHORT":
            menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.DAY_MENU_SHORT)
            return menu_dict
        elif menu_size == "DAY LONG":
            menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.DAY_MENU_LONG)
            return menu_dict
        elif menu_size == "WEEK SHORT":
            menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.WEEK_MENU_SHORT)
            return menu_dict
        elif menu_size == "WEEK LONG":
            menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.WEEK_MENU_LONG)
            return menu_dict

        else:
            return var_dict


    def _update_menu_item(self, var_dict, old_val, new_val):
        keys = [k for k, v in var_dict.items() if v == old_val]
        key = keys[0]
        var_dict.update({key: new_val})

        return var_dict


    def parse_for_error(self, user_input: str) -> Optional[str]:
        return "custom error message"


def main() -> None:
    cal_interface = CalendarInterface()
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
