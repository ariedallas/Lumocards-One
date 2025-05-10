import os
import random
import subprocess
import sys

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_cardsdisplay_boxformatter as l_boxify
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
import LUMO_LIBRARY.lumo_recurring as l_recurring

settings = l_files.get_json_settings()

reviewed_cards = []
reviewed_recurring_cards = []
todays_cards = []

reassigned_cards = []
reactivated_cards = l_recurring.get_recurring_cards()
archived_cards = []
deleted_cards = []
days_since_birth = l_files.get_days_from_date(1988, 6, 12)
day, day_num, month, year = l_files.isolate_date_units()


def cards_intro():
    print()

    l_animators.list_printer([
        f"IT'S DAY: {days_since_birth}",
        f"IT'S: {day.upper()}, {day_num} of {month.upper()}, {year}",
        f"VERSION: {l_files.parents[1].name}",
        "",
        "RUNNING: NEAR FOCUS CARDS"])


def add_step_via_integers(card_steps, card_title, user_input):
    selected_integers = l_card_utils.add_multiple_steps_from_card(user_input)
    total_cards = len(card_steps)
    selected_integers_filtered = [num for num in selected_integers if (0 < int(num) <= total_cards)]
    for card_step in selected_integers_filtered:
        idx = int(card_step) - 1

        planner_feedback(card_title, card_steps[idx])

    for num in selected_integers:
        if 0 <= int(num) > total_cards:
            l_animators.animate_text(f"Skipping number {num}, it shouldn't correspond to a step...")


def cardsrun_macro_hotwords(card_filename, card, card_idx):
    card_title, card_steps = card[0], card[1]

    user_input = input("    \n> ")
    user_input_filtered = l_card_utils.add_blank_space(user_input)

    # ---- START OF MAIN IF/ELIF ---- #

    if user_input_filtered == " ":  # I.E. SKIPPED CARD
        l_animators.animate_text(" ...", speed=.075)
        reviewed_cards.append(card_filename)

    elif user_input_filtered in l_menus_data.NEGATIVE_USER_RESPONSES:  # I.E. QUIT
        l_animators.animate_text(text="Quitted card review.", speed=.075)
        return False

    elif user_input_filtered[0].isnumeric():
        add_step_via_integers(card_steps, card_title, user_input_filtered)
        reviewed_cards.append(card_filename)

    elif user_input_filtered.lower() in l_menus_data.CARDS_PLANNER_FEEDBACK.keys():  # I.E. PAIR RESPONSE TO SHORTCUTS
        found_tuple = l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered]
        route = found_tuple[1]

        if route == 'menu':
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
                l_animators.animate_text(f"Card {card_filename} marked for deletion; returning to Lumocards.")
                return "RELOOP"
            else:
                return "RELOOP"


        elif route == 'edit':
            card_fullpath = l_card_utils.get_card_abspath(card_filename)
            l_animators.animate_text((l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered.lower()][0]))
            subprocess.run([f'{settings.get("text editor")} {card_fullpath}'], shell=True)

            return "RELOOP"


        elif route == 'archive':
            reviewed_cards.append(card_filename)
            archived_cards.append(card_filename)
            print("Card completed: {}".format(l_files.curr_time_hr))
            print(random.choice(l_menus_data.CARDS_PLANNER_COMPLETED_PHRASES))


        elif route == 'delete':
            deleted_cards.append(card_filename)
            reviewed_cards.append(card_filename)
            print(l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered][0])


        elif route == 'superquit':
            found_tuple = l_menus_data.CARDS_PLANNER_FEEDBACK.get(user_input_filtered)
            feedback = found_tuple[0]
            l_animators.animate_text(feedback, speed=.075)
            return "SUPER QUIT"

    else:
        reviewed_cards.append(card_filename)

        card_title = card[0]
        planner_feedback(card_title, user_input_filtered)

    return True


def cardsrun_recurring_macro_hotwords(card_filename, card, card_idx):
    card_title, card_steps = card[0], card[1]

    user_input = input("    \n> ")
    user_input_filtered = l_card_utils.add_blank_space(user_input)

    # ---- START OF MAIN IF/ELIF ---- #

    if user_input_filtered == " ":  # I.E. SKIPPED CARD
        l_animators.animate_text(text=" ...", speed=.075)
        reviewed_recurring_cards.append(card_filename)

    elif user_input_filtered in l_menus_data.NEGATIVE_USER_RESPONSES:  # I.E. QUIT
        l_animators.animate_text(text="Quitted card review.", speed=.075)
        return False

    elif user_input_filtered[0].isnumeric():
        add_step_via_integers(card_steps, card_title, user_input_filtered)
        reviewed_recurring_cards.append(card_filename)

    elif user_input_filtered.lower() in l_menus_data.CARDS_PLANNER_FEEDBACK.keys():  # I.E. PAIR RESPONSE TO SHORTCUTS

        found_tuple = l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered]
        route = found_tuple[1]

        if route == 'menu':

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
                reviewed_recurring_cards.append(card_filename)
                deleted_cards.append(card_filename)
                l_animators.animate_text(f"Card {card_filename} marked for deletion; returning to Lumocards.")
                return "RELOOP"
            else:
                return "RELOOP"


        elif route == 'edit':

            card_fullpath = os.path.join(l_files.recurring_cards_folder, card_filename)

            l_animators.animate_text((l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered.lower()][0]))
            subprocess.run([f'{settings.get("text editor")} {card_fullpath}'], shell=True)

            return "RELOOP"


        elif route == 'archive':
            next_occurrence = l_recurring.update_recurring_data(card_filename)
            reviewed_recurring_cards.append(card_filename)
            l_animators.animate_text(f"Recurring card will reactivate next {next_occurrence}")


        elif route == 'delete':
            deleted_cards.append(card_filename)
            reviewed_recurring_cards.append(card_filename)
            print(l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered][0])


        elif route == 'superquit':
            l_animators.animate_text(l_menus_data.CARDS_PLANNER_FEEDBACK[user_input_filtered][0], speed=.075)
            return "SUPER QUIT"

    else:
        reviewed_recurring_cards.append(card_filename)
        planner_feedback(card[0], user_input_filtered)

    return True


def cardsrun_macro_menu(card_filename, card, menu_dict, menu_list):
    card_fullpath = l_card_utils.get_card_abspath(card_filename)

    l_card_utils.card_header(card)

    l_animators.list_printer(menu_list, speed_interval=0)
    print()
    l_animators.list_printer(l_menus_data.EXIT_MENU_LIST, speed_interval=0)
    l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, speed_interval=0)

    while True:
        user_input = input("\n  > ")

        if user_input.upper() in menu_dict.keys():

            if menu_dict[user_input.upper()] == l_menus_data.ACTION_OPEN:
                subprocess.run([f'{settings.get("text editor")} {card_fullpath}'], shell=True)
                return "RELOOP", card_filename


            elif menu_dict[user_input.upper()] == l_menus_data.ACTION_MODIFY:

                hotkey_list, hotkey_dict = l_menus_funcs.prep_card_modify_menu(
                    actions_list=l_menus_data.CARDS_PLANNER_MODIFY_MENU.copy(),
                    card_filename=card_filename)

                status, possible_returned_card = l_menus_funcs.menu_modify_card(selected_card=card_filename,
                                                                                var_hotkey_list=hotkey_list,
                                                                                var_hotkey_dict=hotkey_dict)
                if possible_returned_card:
                    return "RELOOP", possible_returned_card

                elif status == "CARD MARKED FOR DELETION":
                    return "CARD MARKED FOR DELETION", None

                elif status == "CARD REFOCUSED":
                    return "CARD REFOCUSED", None

                else:
                    return "RELOOP", card_filename

            elif menu_dict[user_input.upper()] == l_menus_data.ACTION_SCHEDULE:
                l_animators.animate_text("  This feature not fully available")
                return "CARD REFOCUSED", None

            elif menu_dict[user_input.upper()] == l_menus_data.ACTION_SET_RECURRING_2:
                card_title_formatted = l_card_utils.format_card_title(card_filename.replace(".txt", ""))
                recur_menu_d, recur_menu_l = l_menus_funcs.prep_newcard_menu(l_menus_data.RECURRING_MENU,
                                                                             l_menus_data.LETTERS_FILTERED,
                                                                             pop_letters=False)
                print()
                l_animators.list_printer([card_title_formatted])
                print()
                l_animators.list_printer(recur_menu_l)

                recurrence_settings = l_menus_funcs.menu_recurrence_settings(var_menu=recur_menu_d)

                l_recurring.update_recurring_data(card_filename, recurrence_settings, initialized=True)
                l_card_utils.card_renamer(curr_name=card_filename
                                          , dst_dir=l_files.recurring_cards_folder
                                          , dst_name=card_filename)

                return "CARD REFOCUSED", None


        elif user_input.upper() in l_menus_data.EXIT_MENU_DICT.keys():
            return "EXIT MENU", None

        elif user_input.upper() in l_menus_data.QUIT_MENU_DICT.keys():
            l_animators.animate_text("Quit")
            sys.exit(0)

        elif user_input.lower() == 'quit':
            l_animators.animate_text("Quit")
            sys.exit(0)

        else:
            print("In this context your options are hotkey letter such as 'a', 'c', or 'quit'.")


def iterate_cards(var_list_cards, mode):
    total_cards = len(var_list_cards)

    for idx, card_path in enumerate(var_list_cards):
        status = None

        card_no = idx + 1
        card_counter_feedback_text = "Card ({}) of ({})".format(card_no, total_cards).upper()

        card = l_card_utils.filename_to_card(card_path)

        l_animators.list_printer(["", card_counter_feedback_text], speed_interval=0)
        l_boxify.display_card(card)

        if mode == "main cards":
            status = cardsrun_macro_hotwords(card_filename=card_path, card=card, card_idx=card_no - 1)
        elif mode == "recurring cards":
            status = cardsrun_recurring_macro_hotwords(card_filename=card_path, card=card, card_idx=card_no - 1)

        if not status:
            return "EXIT CARD LIST"

        elif status == "RELOOP":
            return status

        elif status == "SUPER QUIT":
            return "SUPER QUIT"


def run_remaining_cards():
    review_set = set(reviewed_cards)
    near_focus_cards = sorted(l_files.get_near_focus_cards())
    remaining_cards = [x for x in near_focus_cards if x not in review_set]

    if not remaining_cards:
        return "EXIT CARD LIST"

    status = iterate_cards(remaining_cards, "main cards")
    return status


def review_and_write_recurring():
    if reactivated_cards:
        l_animators.animate_text(f'{len(reactivated_cards)} cards were reactivated...', finish_delay=.5)

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
        l_animators.animate_text(f'No recurring cards for today...', finish_delay=.5)


def planner_feedback(card_title, card_step):
    formatted_output = f"{card_title}: {card_step}"
    full_message = f"Added: '{formatted_output}.' to planner."
    l_animators.list_printer([full_message])
    todays_cards.append(formatted_output)


def update_cards():
    print()
    if todays_cards:
        l_animators.animate_text("ADDING TO PLANNER:")
        l_animators.list_printer(todays_cards)

    if len(archived_cards) > 0:
        print()
        l_animators.animate_text("The system is now going to archive cards:")
        l_animators.list_printer(archived_cards)

        if l_menus_funcs.proceed("> "):
            for card in archived_cards:
                l_card_utils.near_focus_to_archive(card)

    if len(deleted_cards) > 0:
        print()
        l_animators.animate_text("The system is now going to delete cards:")
        l_animators.list_printer(deleted_cards)

        if l_menus_funcs.proceed("> "):
            for card in deleted_cards:
                l_card_utils.card_deleter(card)

    if not l_files.exists_planner_file():
        l_animators.animate_text("Creating Planner file for today...")
        l_files.make_today_planner()

    if len(todays_cards) > 0:
        l_files.basic_wrtr("\n", l_files.today_planner_fullpath)
        l_files.basic_wrtr(f"NEAR FOCUS CARDS: {l_files.curr_time_hr}", l_files.today_planner_fullpath)
        l_files.basic_wrtr("\n", l_files.today_planner_fullpath)
        l_files.basic_wrtr_list(todays_cards, l_files.today_planner_fullpath)

    print()
    l_animators.animate_text("This round of cards has completed.", finish_delay=.5)


def program_header():
    print()
    print("PLANNER")
    print()


def main():
    program_header()
    cards_intro()

    while True:
        status = run_remaining_cards()

        if status == "EXIT CARD LIST" or status == "SUPER QUIT":
            break

        print()

    if status == "EXIT CARD LIST":
        print()
        user_input = l_menus_funcs.proceed("Proceed to Recurring Cards? ")

        if user_input:
            review_and_write_recurring()

    update_cards()


if __name__ == "__main__":
    main()
    update_cards()
