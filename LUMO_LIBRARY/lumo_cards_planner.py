import os
import random
import subprocess
import sys
from os.path import exists

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_calendar_utils as l_cal_utils
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_cardsdisplay_boxformatter as l_boxify
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
import LUMO_LIBRARY.lumo_recurring as l_recurring




def cards_intro():
    day, day_num, month, year = l_files.isolate_date_units()

    print()

    l_animators.list_printer([
        f"IT'S: {day.upper()}, {day_num} of {month.upper()}, {year}",
        "RUNNING: NEAR FOCUS CARDS", ], indent_amt=2)


def add_step_via_integers(card_steps, card_title, user_input):
    selected_integers = l_card_utils.add_multiple_steps_from_card(user_input)
    total_cards = len(card_steps)
    selected_integers_filtered = [num for num in selected_integers if (0 < int(num) <= total_cards)]
    for card_step in selected_integers_filtered:
        idx = int(card_step) - 1

        planner_feedback(card_title, card_steps[idx])

    for num in selected_integers:
        if 0 <= int(num) > total_cards:
            l_animators.animate_text_indented(f"Skipping number {num}, it shouldn't correspond to a step...",
                                              indent_amt=2)


def cardsrun_macro_hotwords(card_filename, card, card_idx):
    card_title, card_steps = card[0], card[1]

    user_input = input("\n  >  ")
    user_input_filtered = l_card_utils.add_blank_space(user_input)

    if user_input_filtered == " ":  # I.E. SKIPPED CARD
        l_animators.animate_text_indented("...", speed=.075, indent_amt=2)
        reviewed_cards.append(card_filename)

    elif user_input_filtered in l_menus_data.NEGATIVE_USER_RESPONSES_SHORT:  # I.E. QUIT
        # l_animators.animate_text_indented(text="Quitted card review.",
        #                                   indent_amt=2)
        return False

    elif user_input_filtered[0].isnumeric():
        add_step_via_integers(card_steps, card_title, user_input_filtered)
        reviewed_cards.append(card_filename)

    elif user_input_filtered.lower() in l_menus_data.CARDS_PLANNER_FEEDBACK.keys():  # I.E. PAIR RESPONSE TO SHORTCUTS
        found_tuple = l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered]
        route = found_tuple[1]

        if route == "menu":
            hotkey_dict, hotkey_list = l_menus_funcs.prep_card_run_menu(l_menus_data.CARDS_PLANNER_MACRO_MENU)
            status, possible_card_path = cardsrun_macro_menu(card_filename=card_filename,
                                                             card=card,
                                                             menu_dict=hotkey_dict,
                                                             menu_list=hotkey_list)

            if status == "RELOOP" and possible_card_path:
                return "RELOOP"

            elif status == "EXIT MENU":
                return "RELOOP"

            elif status == "CARD REFOCUSED":
                return "RELOOP"

            elif status == "CARD MARKED FOR DELETION":
                reviewed_cards.append(card_filename)
                deleted_cards.append(card_filename)
                l_animators.animate_text_indented(f"Card {card_filename} marked for deletion; returning to Lumocards.",
                                                  indent_amt=2)
                return "RELOOP"

            elif status == "QUIT":
                return False

            else:
                return "RELOOP"


        elif route == "edit":
            card_fullpath = l_card_utils.get_card_abspath(card_filename)
            l_card_utils.t_editor(card_fullpath, False)

            return "RELOOP"


        elif route == "archive":
            reviewed_cards.append(card_filename)
            archived_cards.append(card_filename)
            l_animators.list_printer(["Card completed: {}".format(l_files.curr_time_hr)],
                                     indent_amt=2
                                     )

        elif route == "delete":
            deleted_cards.append(card_filename)
            reviewed_cards.append(card_filename)
            l_animators.list_printer([l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered][0]],
                                     indent_amt=2)

        elif route == "show full":
            return "SHOW FULL"

        elif route == "superquit":
            found_tuple = l_menus_data.CARDS_PLANNER_FEEDBACK.get(user_input_filtered)
            feedback = found_tuple[0]
            l_animators.animate_text_indented(feedback, indent_amt=2)
            return "SUPER QUIT"

    else:
        reviewed_cards.append(card_filename)

        card_title = card[0]
        planner_feedback(card_title, user_input_filtered)

    return True


def cardsrun_recurring_macro_hotwords(card_filename, card, card_idx):
    card_title, card_steps = card[0], card[1]

    user_input = input("\n  >  ")
    user_input_filtered = l_card_utils.add_blank_space(user_input)

    # ---- START OF MAIN IF/ELIF ---- #

    if user_input_filtered == " ":  # I.E. SKIPPED CARD
        l_animators.animate_text_indented(text="...", speed=.075, indent_amt=2)
        reviewed_recurring_cards.append(card_filename)

    elif user_input_filtered in l_menus_data.NEGATIVE_USER_RESPONSES_SHORT:  # I.E. QUIT
        # l_animators.animate_text_indented(text="Quitted card review.", indent_amt=2)
        return False

    elif user_input_filtered[0].isnumeric():
        add_step_via_integers(card_steps, card_title, user_input_filtered)
        reviewed_recurring_cards.append(card_filename)

    elif user_input_filtered.lower() in l_menus_data.CARDS_PLANNER_FEEDBACK.keys():  # I.E. PAIR RESPONSE TO SHORTCUTS

        found_tuple = l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered]
        route = found_tuple[1]

        if route == "menu":

            hotkey_dict, hotkey_list = l_menus_funcs.prep_card_run_menu(l_menus_data.CARDS_PLANNER_MACRO_MENU)
            status, possible_card_path = cardsrun_macro_menu(card_filename=card_filename,
                                                             card=card,
                                                             menu_dict=hotkey_dict,
                                                             menu_list=hotkey_list)
            if status == "RELOOP" and possible_card_path:
                return "RELOOP"

            elif status == "CARD REFOCUSED":
                reviewed_recurring_cards.append(card_filename)
                return "RELOOP"

            elif status == "CARD MARKED FOR DELETION":
                reviewed_recurring_cards.append(card_filename)
                deleted_cards.append(card_filename)
                l_animators.animate_text_indented(f"Card {card_filename} marked for deletion; returning to Lumocards.",
                                                  indent_amt=2)
                return "RELOOP"

            elif status == "EXIT MENU":
                return "RELOOP"

            elif status == "QUIT":
                return False

            else:
                return "RELOOP"


        elif route == "edit":

            card_fullpath = os.path.join(l_files.recurring_cards_folder, card_filename)

            l_animators.animate_text_indented((l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered.lower()][0]),
                                              indent_amt=2)
            l_card_utils.t_editor(card_fullpath, False)

            return "RELOOP"


        elif route == "archive":
            next_occurrence = l_recurring.update_recurring_data(card_filename)
            reviewed_recurring_cards.append(card_filename)
            l_animators.animate_text_indented(f"Recurring card will reactivate next {next_occurrence}",
                                              indent_amt=2)


        elif route == "delete":
            deleted_cards.append(card_filename)
            reviewed_recurring_cards.append(card_filename)
            print(l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered][0])


        elif route == "show full":
            return "SHOW FULL"

        elif route == "superquit":
            l_animators.animate_text_indented(l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered][0],
                                              indent_amt=2)
            return "SUPER QUIT"

    else:
        reviewed_recurring_cards.append(card_filename)
        planner_feedback(card[0], user_input_filtered)

    return True


def cardsrun_macro_menu(card_filename, card, menu_dict, menu_list):
    card_fullpath = l_card_utils.get_card_abspath(card_filename)

    l_card_utils.card_header(card, indent_amt=2)

    l_animators.list_printer(menu_list, indent_amt=4, speed_interval=0)
    print()
    l_animators.list_printer(l_menus_data.EXIT_MENU_LIST, indent_amt=4, speed_interval=0)
    l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=4, speed_interval=0)

    while True:
        user_input = input("\n    >  ")
        val = user_input.strip()

        if val.upper() in menu_dict.keys() or \
                val.lower() in l_menus_data.CARDS_PLANNER_MACRO_KEYWORDS:
            action = menu_dict.get(val.upper())

            if action == l_menus_data.ACTION_OPEN or \
                    val.lower() in {"open", "edit"}:
                l_card_utils.t_editor(card_fullpath, False)
                return "RELOOP", card_filename


            elif action == l_menus_data.ACTION_MODIFY or \
                    val.lower() in {"modify"}:

                hotkey_list, hotkey_dict = l_menus_funcs.prep_card_modify_menu(
                    actions_list=l_menus_data.CARDS_PLANNER_MODIFY_MENU.copy(),
                    card_filename=card_filename)

                status, possible_returned_card = l_menus_funcs.menu_modify_card(selected_card=card_filename,
                                                                                var_hotkey_list=hotkey_list,
                                                                                var_hotkey_dict=hotkey_dict,
                                                                                indent_amt=2)
                if possible_returned_card:
                    return "RELOOP", possible_returned_card

                elif status == "CARD MARKED FOR DELETION":
                    return "CARD MARKED FOR DELETION", None

                elif status == "CARD REFOCUSED":
                    return "CARD REFOCUSED", None

                else:
                    return "RELOOP", card_filename

            elif action == l_menus_data.ACTION_SCHEDULE or \
                    val.lower() in {"schedule"}:
                print()
                l_animators.animate_text_indented("This feature not fully available..."
                                                  , indent_amt=2
                                                  , finish_delay=.5)
                return "CARD REFOCUSED", None


        elif val.lower() in {"x", "exit"}:
            return "EXIT MENU", None

        elif val.lower() in {"q", "exit"}:
            # Optional feature:
            # print()
            # l_animators.animate_text_indented("Quit", indent_amt=2, finish_delay=.5)
            return "QUIT", None

        else:
            print()
            l_animators.animate_text_indented(f"Unrecognized option '{val}' ..."
                                              , indent_amt=4
                                              , finish_delay=.5)


def iterate_cards(var_list_cards, mode):
    total_cards = len(var_list_cards)

    for idx, card_path in enumerate(var_list_cards):
        status = None

        card_no = idx + 1
        card_counter_feedback_text = "Card ({}) of ({})".format(card_no, total_cards).upper()

        card = l_card_utils.filename_to_card(card_path)

        l_animators.list_printer(["", card_counter_feedback_text], indent_amt=2, speed_interval=0)
        l_boxify.display_card(card)

        if mode == "main cards":
            status = cardsrun_macro_hotwords(card_filename=card_path, card=card, card_idx=card_no - 1)
        elif mode == "recurring cards":
            status = cardsrun_recurring_macro_hotwords(card_filename=card_path, card=card, card_idx=card_no - 1)

        if status == "SHOW FULL" and mode == "main cards":
            l_animators.animate_text_indented("Same card showing up to 20 steps", indent_amt=2)
            l_boxify.display_card(card, 20)
            status = cardsrun_macro_hotwords(card_filename=card_path, card=card, card_idx=card_no - 1)
        elif status == "SHOW FULL" and mode == "recurring cards":
            l_animators.animate_text_indented("Same card showing up to 20 steps", indent_amt=2)
            l_boxify.display_card(card, 20)
            status = cardsrun_recurring_macro_hotwords(card_filename=card_path, card=card, card_idx=card_no - 1)

        if not status:
            return "EXIT CARD LIST"

        elif status == "RELOOP" or status == "SHOW FULL":
            return "RELOOP"

        elif status == "SUPER QUIT":
            return "SUPER QUIT"


def iterate_cards_calendar(var_list_cards):
    total_cards = len(var_list_cards)

    for idx, event_card in enumerate(var_list_cards):
        card_no = idx + 1
        card_counter_feedback_text = f"Calendar Card ({card_no}) of ({total_cards})".upper()

        event_dict = event_card.format_as_editing_dict()
        event_formatted = l_cal_utils.get_formatted_event_info(event_dict)

        l_animators.list_printer(["", card_counter_feedback_text], indent_amt=2, speed_interval=0)
        l_boxify.display_card_event(event_formatted)

        input("\n  >  ")

        l_animators.animate_text_indented(text="...", speed=.075, indent_amt=2)


def run_remaining_cards():
    review_set = set(reviewed_cards)
    near_focus_cards = sorted(l_files.get_near_focus_cards())
    remaining_cards = [x for x in near_focus_cards if x not in review_set]

    if not remaining_cards:
        return "EXIT CARD LIST"

    status = iterate_cards(remaining_cards, "main cards")
    return status


def review_and_write_recurring():
    reactivated_cards = l_recurring.get_recurring_cards()

    if reactivated_cards:
        l_animators.list_printer([
            f"RUNNING: {len(reactivated_cards)} REACTIVATED CARDS", ], indent_amt=2)

        review_set = set(reviewed_recurring_cards)
        remaining_cards = [x for x in reactivated_cards if x not in review_set]

        while len(remaining_cards) > 0:
            status = iterate_cards(remaining_cards, "recurring cards")

            if status == "EXIT CARD LIST":
                return status

            elif status == "SUPER QUIT":
                return status

            review_set = set(reviewed_recurring_cards)
            remaining_cards = [x for x in reactivated_cards if x not in review_set]

    else:
        l_animators.list_printer([
            f"NO RECURRING CARDS TODAY", ], indent_amt=2)


def review_calendar_cards():
    calendar_events = l_cal_utils.get_today_events()

    l_animators.list_printer([
        f"RUNNING: CALENDAR CARDS", ], indent_amt=2)

    iterate_cards_calendar(calendar_events)


def translate_events_to_oneliners():
    oneliners = []
    calendar_events = l_cal_utils.get_today_events()

    for idx, event_obj in enumerate(calendar_events):
        event_dict = event_obj.format_as_editing_dict()
        summary, time_info_f, _, _, descr_list_limited, loc_list_limited = l_cal_utils.get_formatted_event_info(
            event_dict)

        loc_f = "Loc: " + loc_list_limited[0]
        descr_f = "Descr: " + descr_list_limited[0]
        num = f"{idx + 1} - "

        main_info = (", ").join([summary, time_info_f])
        secondary_info = (", ").join([descr_f, loc_f])

        group = num + main_info + "    " + secondary_info
        oneliners.append(group)

    return oneliners


def update_cards():
    print()

    uniq_cal_events = prune_calendar_duplicates(calendar_cards)

    if todays_cards:
        l_animators.animate_text_indented("ADDING TO PLANNER:", indent_amt=2)
        print()
        l_animators.list_printer(todays_cards, indent_amt=4)


    if uniq_cal_events:
        print()
        l_animators.animate_text_indented("ADDING EVENTS TO PLANNER:", indent_amt=2)
        print()
        l_animators.list_printer(uniq_cal_events, indent_amt=4)

    if len(archived_cards) > 0:
        print()
        l_animators.animate_text_indented("The system is now going to archive cards:", indent_amt=2)
        print()
        l_animators.list_printer(archived_cards, indent_amt=4)
        print()

        if l_menus_funcs.proceed("( ➝ yes) >  ", indent_amt=2, reference_list=l_menus_data.NEGATIVE_USER_RESPONSES):
            for card in archived_cards:
                l_card_utils.near_focus_to_archive(card)

    if len(deleted_cards) > 0:
        print()
        l_animators.animate_text_indented("The system is now going to delete cards:", indent_amt=2)
        print()
        l_animators.list_printer(deleted_cards, indent_amt=4)
        print()

        for card in deleted_cards:
            l_card_utils.card_deleter(card)

    if not l_files.exists_planner_file():
        print()
        l_animators.animate_text_indented("Creating planner file for today...", indent_amt=2, finish_delay=.5)
        l_files.make_today_planner()

    if len(todays_cards) > 0:
        l_files.basic_wrtr("\n", l_files.today_planner_fullpath)
        l_files.basic_wrtr(f"NEAR FOCUS CARDS: {l_files.curr_time_hr}", l_files.today_planner_fullpath)
        l_files.basic_wrtr("\n", l_files.today_planner_fullpath)
        l_files.basic_wrtr_list(todays_cards, l_files.today_planner_fullpath)

    if len(uniq_cal_events) > 0 :
        l_files.basic_wrtr("\n", l_files.today_planner_fullpath)
        l_files.basic_wrtr(f"CALENDAR CARDS: {l_files.curr_time_hr}", l_files.today_planner_fullpath)
        l_files.basic_wrtr("\n", l_files.today_planner_fullpath)
        l_files.basic_wrtr_list(uniq_cal_events, l_files.today_planner_fullpath)


    print()
    l_animators.animate_text_indented("This round of cards has completed.", indent_amt=2, finish_delay=1)


def planner_feedback(card_title, card_step):
    formatted_output = f"{card_title}: {card_step}"
    full_message = f"Added: '{formatted_output}.' to planner."
    l_animators.list_printer([full_message], indent_amt=2)
    todays_cards.append(formatted_output)


def prune_calendar_duplicates(cards_list):
    uniq = []

    if not os.path.exists(l_files.today_planner_fullpath):
        return cards_list

    with open(l_files.today_planner_fullpath) as fin:
        all_lines = [l.strip() for l in fin.readlines()]

        for line in cards_list:
            if line not in all_lines:
                uniq.append(line)

    return uniq


def update_calendar_review():
    settings = l_files.get_json_settings()
    day, day_num, month, year = l_files.isolate_date_units()
    settings["calendar cards last review"] = f"{month} {day_num}, {day}"
    l_json_utils.write_json(l_files.settings_fullpath, settings)

def program_header(header):
    print()
    print(header)
    print()

def get_agenda():
    today_has_agenda = os.path.exists(l_files.today_planner_fullpath)

    if not today_has_agenda:
        program_header("AGENDA")
        l_animators.animate_text_indented("No planner file exists yet for today...", indent_amt=2)
        l_animators.animate_text_indented("Returning to main Lumo menu.", indent_amt=2, finish_delay=.5)

    else:
        l_card_utils.t_editor(l_files.today_planner_fullpath, False)

def main():

    global reviewed_cards, reviewed_recurring_cards, todays_cards, calendar_cards, \
        reassigned_cards, reactivated_cards, archived_cards, deleted_cards


    reviewed_cards = []
    reviewed_recurring_cards = []
    todays_cards = []
    calendar_cards = []

    reassigned_cards = []
    archived_cards = []
    deleted_cards = []

    program_header("PLANNER")
    cards_intro()

    while True:
        status = run_remaining_cards()

        if status == "EXIT CARD LIST" or status == "SUPER QUIT":
            break

        print()

    if status == "EXIT CARD LIST":
        print()
        user_input = l_menus_funcs.proceed("Proceed to Recurring Cards? ( ➝ yes) >  "
                                           , indent_amt=2
                                           , reference_list=l_menus_data.NEGATIVE_USER_RESPONSES)

        if user_input:
            review_and_write_recurring()

        print()
        user_input = l_menus_funcs.proceed("Proceed to Calendar Cards ( ➝ yes) >  "
                                           , indent_amt=2
                                           , reference_list=l_menus_data.NEGATIVE_USER_RESPONSES)

        if user_input:

            try:
                review_calendar_cards()
                events_as_oneliners = translate_events_to_oneliners()
                calendar_cards.extend(events_as_oneliners)


            except:
                print()
                l_animators.list_printer(["Calendar is not currently configured -or-",
                                          "the calendar is incorrectly setup -or-",
                                          "other reasons: i.e. there is no internet connection",
                                          "",
                                          "In order to use this feature follow the README at the address below:",
                                          "https://github.com/ariedallas/Lumocards-One",
                                          "and check out the video link for setup."], indent_amt=2)
                print()
                print("  Type any key to continue")
                input("\n  >  ")


        else:
            l_animators.animate_text_indented("Skipping calendar cards",
                                              indent_amt=2,
                                              finish_delay=.5)

    update_cards()


if __name__ == "__main__":
    main()
    update_cards()
