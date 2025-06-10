import datetime
import math
import subprocess
import textwrap

from itertools import chain
from typing import Optional, reveal_type

from dateutil.tz import tzlocal
from dateutil.relativedelta import relativedelta

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_calendar_actions as l_cal_actions
import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils
import LUMO_LIBRARY.lumo_calendar_parsing_2 as l_cal_parse
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
from LUMO_LIBRARY.lumo_calendar_utils import (CalendarPageDay,
                                              CalendarPageEvent,
                                              CalendarPageWeek,
                                              DayBlock,
                                              Event,
                                              get_google_setting,
                                              Menus)


def clear() -> None:
    subprocess.run(["clear"], shell=True)


def feedback_not_implemented(indent_context):
    l_animators.animate_text_indented("This feature not yet implemented yet...",
                                      indent_amt=indent_context,
                                      finish_delay=.5)


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

        self.creds = l_cal_utils.get_creds()


    def _refresh_DayBlock(self, curr_page: CalendarPageDay) -> None:
        curr_start = curr_page.day_block.date
        curr_end = curr_start + relativedelta(days=1)

        selected_events = l_cal_utils.get_google_events(self.creds, curr_start, curr_end)

        if not selected_events:
            refreshed_events = [l_cal_utils.google_event_to_obj(e) for
                                e in list()]
        else:
            refreshed_events = [l_cal_utils.google_event_to_obj(e) for
                                e in selected_events]

        curr_page.day_block.events = refreshed_events


    def _refresh_all(self):
        self.day_blocks_window: list[DayBlock] = l_cal_utils.get_day_blocks()
        self.week_blocks_window: list[list[DayBlock]] = self._separate_by_weeks()


    def _event_actions_router(self,
                              val: str,
                              val_str: str,
                              actions_dict: dict[str, str],
                              event_obj: Event):

        action = actions_dict[val.upper()] if actions_dict.get(val.upper()) else val_str

        if action == Menus.ACTION_EDIT_TITLE or \
                action in {"title", "summary"}:
            start = event_obj.s if event_obj.s else event_obj.s_date

            status = self.update_event_one_val(event_obj,
                                               "summary",
                                               "title",
                                               start)

            return False, None, None, status

        elif action == Menus.ACTION_EDIT_TIME_DATE or \
                action in {"time", "times", "date", "dates"}:

            start = event_obj.s if event_obj.s else event_obj.s_date

            status = self.update_event_dt_vals(event_obj,
                                               start)

            return False, None, None, status


        elif action == Menus.ACTION_EDIT_DESCRIPTION or \
                action in {"description", "notes"}:
            start = event_obj.s if event_obj.s else event_obj.s_date

            status = self.update_event_one_val(event_obj,
                                               "description",
                                               "description",
                                               start)

            return False, None, None, status

        elif action == Menus.ACTION_MENU_LESS or \
                action in {"less", "show less"} or \
                (action == "menu" and self.menu_size == "EVENT LONG"):
            self.menu_size = "EVENT SHORT"
            return True, None, None, "RELOOP"

        elif action == Menus.ACTION_MENU_MORE or \
                action in {"more", "show more"} or \
                (action == "menu" and self.menu_size == "EVENT SHORT"):
            self.menu_size = "EVENT LONG"
            return True, None, None, "RELOOP"

        elif action == Menus.ACTION_EDIT_LOCATION or \
                action in {"location"}:
            start = event_obj.s if event_obj.s else event_obj.s_date

            status = self.update_event_one_val(event_obj,
                                               "location",
                                               "location",
                                               start)

            return False, None, None, status

        elif action == Menus.ACTION_DELETE_EVENT or \
                action in {"delete"}:
            l_cal_actions.delete_event(event_obj.id)
            l_animators.animate_text_indented("Deleted event",
                                              indent_amt=CalendarPageEvent.msg_indent_1,
                                              finish_delay=.5)

            return False, None, None, "DELETE EVENT"


    def _day_actions_router(self,
                            user_input: str,
                            actions_dict: dict[str, str]
                            ) -> Optional[tuple[bool, Optional[str], Optional[str]]]:

        action = actions_dict[user_input.upper()]

        if action == Menus.ACTION_NEW_EVENT:
            self.create_new_event()
            return False, None, None

        elif action == Menus.ACTION_NEW_QUICK:
            feedback_not_implemented(CalendarPageDay.msg_indent_num)
            return False, None, None

        elif action == Menus.ACTION_SEARCH:
            feedback_not_implemented(CalendarPageDay.msg_indent_num)
            return False, None, None

        elif action == Menus.ACTION_MENU_LESS:
            self.menu_size = "DAY SHORT"
            return True, None, None

        elif action == Menus.ACTION_MENU_MORE:
            self.menu_size = "DAY LONG"
            return True, None, None

        elif action == Menus.ACTION_GOTO:
            feedback_not_implemented(CalendarPageDay.msg_indent_num)
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

        elif action == Menus.ACTION_HELP_MORE:
            feedback_not_implemented(CalendarPageDay.msg_indent_num)
            return False, None, None

        elif action == Menus.ACTION_DELETE_EVENT:
            feedback_not_implemented(CalendarPageDay.msg_indent_num)
            return False, None, None


    def _week_actions_router(self,
                             user_input: str,
                             actions_dict: dict[str, str]) -> None:

        action = actions_dict[user_input.upper()]

        if action == Menus.ACTION_NEW_EVENT:
            self.create_new_event(default_use_today=True)

        elif action == Menus.ACTION_SEARCH:
            feedback_not_implemented(CalendarPageWeek.msg_indent_num)

        elif action == Menus.ACTION_GOTO:
            feedback_not_implemented(CalendarPageWeek.msg_indent_num)

        elif action == Menus.ACTION_HELP_MORE:
            feedback_not_implemented(CalendarPageWeek.msg_indent_num)


    def view_event(self, event_idx: int) -> None:
        valid_str_actions = {"title", "summary",
                             "time", "times", "date", "dates",
                             "description", "note", "notes",
                             "menu", "less", "show less", "more", "show more",
                             "location",
                             "delete"
                             }

        self.menu_size = "EVENT LONG"
        menu_update = False
        menu_dict = self._contextualize(None,
                                        None,
                                        None,
                                        self.menu_size)

        while True:
            event_obj = self.day_blocks_window[self.curr_day_idx].events[event_idx]
            event_page = CalendarPageEvent(event_obj)

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
            val = user_input.strip()
            val_str = user_input.strip().lower()

            if val.upper() in menu_dict.keys() or val_str in valid_str_actions:
                menu_update, _, _, status = self._event_actions_router(val,
                                                                       val_str,
                                                                       menu_dict,
                                                                       event_obj)
                if status == "DELETE EVENT":
                    curr_page = CalendarPageDay(self.day_blocks_window[self.curr_day_idx])
                    self._refresh_DayBlock(curr_page)
                    return status

                elif status == "UPDATE EVENT":
                    curr_page = CalendarPageDay(self.day_blocks_window[self.curr_day_idx])
                    self._refresh_DayBlock(curr_page)
                    return status

                else:
                    continue


            elif val.lower() in {"x", "exit"}:
                break


            else:
                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent_amt=CalendarPageEvent.msg_indent_1,
                                                  finish_delay=.5)


    def view_days(self) -> str:
        curr_day_block: DayBlock

        curr_day_block = self.day_blocks_window[self.curr_day_idx]
        menu_dict, _ = l_menus_funcs.prep_menu_tuple(Menus.DAY_MENU_LONG)
        menu_update = False
        old_val = None
        new_val = None
        show_refreshed_event = False

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
            val = user_input.strip()
            val_str = user_input.strip().lower()

            if "]" in val or "[" in val:
                curr_day_block = self.paginate_days(val)

            elif curr_page.valid_event_selection(val,
                                                 len(curr_day_block.events),
                                                 self.events_limit):
                selection = int(val) - 1
                status = self.view_event(selection)

                if status == "UPDATE EVENT":
                    self._refresh_all()
                    curr_day_block = self.day_blocks_window[self.curr_day_idx]

            elif val.upper() in menu_dict.keys():
                menu_update, old_val, new_val = self._day_actions_router(val, menu_dict)

            elif val_str in {"t", "toggle"}:
                self.curr_view_mode = "WEEK"
                for idx, group in enumerate(self.week_blocks_window):
                    if curr_day_block in group:
                        self.curr_week_idx = idx
                        break
                return "TOGGLE"

            elif val_str in {"q", "quit"}:
                return "QUIT"


            else:
                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent_amt=CalendarPageDay.msg_indent_num,
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
            val = user_input.strip()
            val_str = user_input.strip().lower()

            if "]" in val or "[" in val:
                curr_week_block = self.paginate_weeks(val)

            elif val.upper() in menu_dict.keys():
                self._week_actions_router(val, menu_dict)


            elif curr_page.valid_day_selection(user_input=val, var_weekblock=curr_week_block):
                week_in_focus_day_ints = [block.day for block in curr_week_block]
                selected_idx = week_in_focus_day_ints.index(int(val))
                selected_day_block = curr_week_block[selected_idx]
                self.curr_day_idx = self.day_blocks_window.index(selected_day_block)

                self.curr_view_mode = "DAY"
                return "TOGGLE"

            elif val_str in {"t", "toggle"}:
                self.curr_view_mode = "DAY"
                monday_DayBlock = curr_week_block[0]
                target_date = monday_DayBlock.date
                self.curr_day_idx = self._day_index_lookup(target_date)

                return "TOGGLE"


            elif val_str in {"q", "quit"}:
                return "QUIT"


            else:
                indent = CalendarPageWeek.msg_indent_num
                l_animators.animate_text_indented("Unrecognized option...",
                                                  indent_amt=indent,
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

        return curr_week_block


    # Figure out how to split this up into some smaller chunks:
    # Basic idea: Each field of the new event is its own function.
    # Each function gets parsed for an error, and if so it triggers the
    # While loop to repeat again.
    # Possibly, each function takes the new-event dict and hands back the dictionary
    def create_new_event(self, default_use_today=False):
        if not default_use_today:
            curr_day_block = self.day_blocks_window[self.curr_day_idx]
            date_in_focus = datetime.datetime.combine(
                curr_day_block.date, datetime.time(hour=0, minute=0, second=0))
        else:
            date_in_focus = self.today.replace(hour=0, minute=0, tzinfo=None)

        new_event_dict = {}

        event_page = CalendarPageEvent(None)
        dt_parser = l_cal_parse.NewEventParser(date_in_focus)
        event_ready = False
        end_idx = len(Menus.NEW_EVENT_CATEGORIES) - 1

        while not event_ready:
            finish_forLoop = False

            clear()
            event_page.display_editing_event(new_event_dict, "NEW")
            event_page.display_prompts_subheader("NEW CALENDAR EVENT", date_in_focus)
            print()

            for idx, prompt_set in enumerate(Menus.NEW_EVENT_CATEGORIES):
                keys_iter = chain.from_iterable(d.keys() for d in prompt_set)
                keys = list(keys_iter)

                # Each time we add new values to our new_event_dict, we
                # finish out the loop, so that we can clear the screen and check each update
                # along the way. This way is a bit janky, but hopefully explains what is happening.
                if finish_forLoop:
                    continue

                if idx == end_idx:
                    key = keys[0]
                    value = new_event_dict.get(key)
                    if value:
                        event_ready = True

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
                    finish_forLoop = True
                else:
                    prompt_one = prompt_set[0].get(key_a)
                    prompt_two = prompt_set[1].get(key_b)

                    target_a, target_b = ("start time", "end time") \
                        if prompt_one == Menus.P_S_TIME \
                        else ("start date", "end date")

                    valid_times = (new_event_dict.get("s") != "all day" and
                                   new_event_dict.get("s") is not None)

                    result_a, result_b = self.prompter_double(prompt_one,
                                                              prompt_two,
                                                              date_in_focus,
                                                              valid_times)

                    dt_info_a, dt_info_b = self.parse_datetime_info(dt_parser,
                                                                    result_a,
                                                                    result_b,
                                                                    target_a,
                                                                    target_b)

                    if dt_info_a and dt_info_b:
                        new_event_dict[key_a] = dt_info_a
                        new_event_dict[key_b] = dt_info_b

                    finish_forLoop = True

        time_zone = get_google_setting("timezone")
        dt_parser.format_data_for_sync(time_zone)
        outcome = l_cal_actions.create_event(new_event_dict, dt_parser)

        if outcome:
            summary = new_event_dict.get("summary")
            summary_short = textwrap.shorten(summary, 20)
            feedback = f"Created event: {summary_short}"

            l_animators.animate_text_indented(feedback,
                                              indent_amt=CalendarPageEvent.l_margin_num,
                                              finish_delay=1)

            dt_parser.format_data_for_search()
            page_to_update = self._find_DayBlock_from_dt(dt_parser.search_format)

            if page_to_update:
                self._refresh_DayBlock(CalendarPageDay(page_to_update))


        else:
            feedback = "The event failed when creating, try again?"
            l_animators.animate_text_indented(feedback,
                                              indent_amt=CalendarPageEvent.l_margin_num,
                                              finish_delay=1)


    # Figure out how to split this up into some smaller chunks
    def update_event_one_val(self,
                             existing_event,
                             target_key,
                             target_name,
                             date_in_focus):

        existing_id = existing_event.id
        editing_event = existing_event.format_as_editing_dict()
        prev_value = editing_event[target_key]
        del editing_event[target_key]

        event_page = CalendarPageEvent(None)
        event_ready = False
        initial_round = True

        while not event_ready:
            clear()
            event_page.display_editing_event(editing_event, "EDIT")
            event_page.display_prompts_subheader("EDIT EVENT", date_in_focus)
            print()

            if initial_round:
                wh_sp = l_cal_utils.CalendarPageEvent.cursor_indent_space
                prompt = f"New {target_name}:"
                full_prompt = wh_sp + prompt + "  "

                user_input = input(full_prompt)
                val = user_input.strip() if user_input else prev_value

                editing_event[target_key] = val
                initial_round = False

            else:
                event_page.display_menu_confirmation()
                print()
                print(CalendarPageEvent.cursor_indent_space, end="  ")
                user_input = input(">  ")

                val = user_input.strip().lower()

                if val == "a" or val in {"save"} or \
                        val == "":
                    print()
                    l_animators.animate_text_indented("Saving event...",
                                                      indent_amt=CalendarPageEvent.msg_indent_1,
                                                      finish_delay=.5
                                                      )
                    event_ready = True

                elif val == "b" or val in {"edit again",
                                           "edit",
                                           "again"}:

                    initial_round = True
                    del editing_event[target_key]

                elif val == "x" or val in {"exit"}:
                    print()
                    l_animators.animate_text_indented("Back to un-edited event",
                                                      indent_amt=CalendarPageEvent.msg_indent_1,
                                                      finish_delay=.5
                                                      )
                    return "RELOOP"

                else:
                    print()
                    l_animators.animate_text_indented("Unrecognized option",
                                                      indent_amt=CalendarPageEvent.msg_indent_1,
                                                      finish_delay=.5
                                                      )

        outcome, msg = l_cal_actions.update_event_simple(editing_event,
                                                         existing_id,
                                                         target_key)

        if outcome:
            feedback = f"Updated event: {msg}"

            print()
            l_animators.animate_text_indented(feedback,
                                              indent_amt=CalendarPageEvent.msg_indent_2,
                                              finish_delay=1)

            return "UPDATE EVENT"


        else:
            feedback = "The event failed when syncing. Try again?"

            print()
            l_animators.animate_text_indented(feedback,
                                              indent_amt=CalendarPageEvent.msg_indent_2,
                                              finish_delay=1)
            print(msg)

            return "RELOOP"


    # Figure out how to split this up into some smaller chunks
    def update_event_dt_vals(self,
                             existing_event,
                             date_in_focus):

        existing_id = existing_event.id
        # prev_event = existing_event.format_as_editing_dict()
        editing_event = existing_event.format_as_editing_dict()

        del editing_event["s"]
        del editing_event["e"]
        del editing_event["s_date"]
        del editing_event["e_date"]

        event_page = CalendarPageEvent(None)
        dt_parser = l_cal_parse.NewEventParser(date_in_focus)
        event_ready = False
        initial_round = True

        end_idx = len(Menus.EDITING_EVENT_DT) - 1

        while not event_ready:
            clear()
            event_page.display_editing_event(editing_event, "EDIT")
            event_page.display_prompts_subheader("EDIT EVENT DATE/TIME", date_in_focus)
            print()

            if initial_round:
                for idx, prompt_set in enumerate(Menus.EDITING_EVENT_DT):
                    keys_iter = chain.from_iterable(d.keys() for d in prompt_set)
                    keys = list(keys_iter)

                    key_a, key_b = keys
                    value_a, value_b = (editing_event.get(key_a),
                                        editing_event.get(key_b))

                    if value_a and value_b:
                        continue

                    prompt_one = prompt_set[0].get(key_a)
                    prompt_two = prompt_set[1].get(key_b)

                    target_a, target_b = ("start time", "end time") \
                        if prompt_one == Menus.P_S_TIME \
                        else ("start date", "end date")

                    valid_times = (editing_event.get("s") != "all day" and
                                   editing_event.get("s") is not None)

                    result_a, result_b = self.prompter_double(prompt_one,
                                                              prompt_two,
                                                              date_in_focus,
                                                              valid_times)

                    dt_info_a, dt_info_b = self.parse_datetime_info(dt_parser,
                                                                    result_a,
                                                                    result_b,
                                                                    target_a,
                                                                    target_b)

                    if dt_info_a and dt_info_b:
                        editing_event[key_a] = dt_info_a
                        editing_event[key_b] = dt_info_b

                    if idx == end_idx and \
                            editing_event.get(key_a) and \
                            editing_event.get(key_b):
                        initial_round = False

                    break

            else:
                event_page.display_menu_confirmation()
                print()
                print(CalendarPageEvent.cursor_indent_space, end="  ")
                user_input = input(">  ")

                val = user_input.strip().lower()

                if val == "a" or val in {"save"} or \
                        val == "":
                    print()
                    l_animators.animate_text_indented("Saving event...",
                                                      indent_amt=CalendarPageEvent.msg_indent_1,
                                                      finish_delay=.5
                                                      )
                    event_ready = True

                elif val == "b" or val in {"edit again",
                                           "edit",
                                           "again"}:

                    initial_round = True

                    del editing_event["s"]
                    del editing_event["e"]
                    del editing_event["s_date"]
                    del editing_event["e_date"]

                elif val == "x" or val in {"exit"}:
                    print()
                    l_animators.animate_text_indented("Back to un-edited event",
                                                      indent_amt=CalendarPageEvent.msg_indent_1,
                                                      finish_delay=.5
                                                      )
                    return "RELOOP"

                else:
                    print()
                    l_animators.animate_text_indented("Unrecognized option",
                                                      indent_amt=CalendarPageEvent.msg_indent_1,
                                                      finish_delay=.5
                                                      )
        time_zone = get_google_setting("timezone")
        dt_parser.format_data_for_sync(time_zone)
        outcome, msg = l_cal_actions.update_event_dt(existing_id,
                                                     dt_parser)

        if outcome:
            feedback = f"Updated event: {msg}"

            print()
            l_animators.animate_text_indented(feedback,
                                              indent_amt=CalendarPageEvent.msg_indent_2,
                                              finish_delay=1)

            return "UPDATE EVENT"


        else:
            feedback = "The event failed when syncing. Try again?"

            print()
            l_animators.animate_text_indented(feedback,
                                              indent_amt=CalendarPageEvent.msg_indent_2,
                                              finish_delay=1)
            print(msg)

            return "RELOOP"


    def parse_datetime_info(self,
                            dt_parser,
                            result_a,
                            result_b,
                            target_a,
                            target_b
                            ):

        dt_parser.parse_type(result_a, target_a)
        dt_parser.parse_type(result_b, target_b)

        valid_time, _ = dt_parser.extrapolate_time_data()
        valid_date, _ = dt_parser.extrapolate_date_data()

        # We need to include "target_a" == "start time"
        # so that it will only use the right key value
        # at the correct moment
        if valid_time and not valid_date and \
                target_a == "start time":
            return dt_parser.start_time.display, dt_parser.end_time.display

        elif valid_time and valid_date:
            return dt_parser.start_date.display, dt_parser.end_date.display

        else:
            error = dt_parser.get_error()
            print()
            l_animators.animate_text_indented(error,
                                              indent_amt=CalendarPageEvent.msg_indent_2,
                                              finish_delay=1)

            return None, None


    def prompter_single(self, prompt):
        wh_sp = l_cal_utils.CalendarPageEvent.cursor_indent_space
        full_prompt = wh_sp + prompt + "  "

        user_input = input(full_prompt)
        val = user_input.strip()

        if prompt == Menus.P_TITLE:
            user_input_validated = "(no title)" if val == "" else val

        elif prompt == Menus.P_DESCRIPTION:
            if (val in l_menus_data.NEGATIVE_USER_RESPONSES
                    or val == ""):
                user_input_validated = "none"

            else:
                user_input_validated = val

        elif prompt == Menus.P_LOCATION:
            if (val in l_menus_data.NEGATIVE_USER_RESPONSES
                    or val == ""):
                user_input_validated = "none"

            else:
                user_input_validated = val

        return user_input_validated


    def prompter_dateTime(self, prompt, prev_context, date_in_focus, valid_times):
        prompt_with_context = self._contextualize_prompt(prompt, prev_context, date_in_focus)
        wh_sp = l_cal_utils.CalendarPageEvent.l_margin_space + "  "
        full_prompt = wh_sp + prompt_with_context + "  "

        if prompt == Menus.P_E_TIME:
            if prev_context == "":
                return ""
            elif prev_context == "all day":
                return "all day"

        elif prompt == Menus.P_E_DATE and valid_times:
            return ""

        user_input = input(full_prompt)
        val = user_input.strip()
        return val


    def prompter_double(self, prompt_one, prompt_two, date_in_focus, valid_times):
        user_input_one = self.prompter_dateTime(prompt_one, None, date_in_focus, valid_times)
        user_input_two = self.prompter_dateTime(prompt_two, user_input_one, None, valid_times)

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
            default_date = "( ➝ start date)"
            prompt_with_context = f"{prompt}  {default_date} :"

        else:
            prompt_with_context = prompt

        return prompt_with_context


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


    def _find_DayBlock_from_dt(self, dt):
        for d in self.day_blocks_window:
            match = d.date.strftime("%Y-%m-%d")
            if match == dt:
                return d


    def parse_for_error(self, user_input: str) -> Optional[str]:
        return None


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
