import os
import random
import subprocess
import sys

import lumo_filehandler as l_files
import lumo_recurring as l_recurring
import lumo_animationlibrary as l_animators
import lumo_formatters as l_formatters
import lumo_cardsdisplay_boxformatter as l_boxify
import lumo_menus as l_menus

reviewed_cards = []
reviewed_recurring_cards = []
cards_for_lightwalk = []

reassigned_cards = []
reactivated_cards = l_recurring.get_recurring_cards()
archived_cards = []
deleted_cards = []


def cards_intro():
    print(f"You're using Lumocards {l_files.parent[-6:]}, Just FYI")
    print()

    days_since_birth = l_files.get_days_from_date(1988, 6, 12)
    l_animators.animate_text(f"IT'S DAY: {days_since_birth}", finish_delay=.25, speed=.075)
    l_animators.animate_text("      ")
    l_animators.animate_text("ACTIVE CARDS", speed=.075)
    l_animators.standard_interval_printer([""])


def add_step_via_integers(card_steps, card_title, response_filtered):
    selected_integers = l_formatters.add_multiple_steps_from_card(response_filtered)
    max = len(card_steps)
    selected_integers_filtered = [num for num in selected_integers if
                                  (int(num) <= max and int(num) > 0)]
    if selected_integers_filtered:
        l_animators.animate_text("ADDING STEPS FROM NUMBER SHORTCUTS")
    for card_step in selected_integers_filtered:
        idx = int(card_step) - 1

        formatted_output = "{}: {}".format(card_title, card_steps[idx])
        full_message = ("'{}' was added to Lightwalk.".format(formatted_output))
        l_animators.animate_text(full_message)
        cards_for_lightwalk.append(formatted_output)
    for num in selected_integers:
        if int(num) > max or int(num) <= 0:
            l_animators.animate_text(f"Skipping number {num}, it shouldn't correspond to a step...")


def cardsrun_macro_hotwords(card_path, card, card_idx):

    card_title, card_steps = card[0], card[1]

    response = input("    \n> ")
    response_filtered = l_formatters.add_blank_space(response)

    # ---- START OF MAIN IF/ELIF ---- #

    if response_filtered == " ": # I.E. SKIPPED CARD
        l_animators.animate_text(" ...", speed=.075)
        reviewed_cards.append(card_path)

    elif response_filtered in l_files.negative_user_responses: # I.E. QUIT
        l_animators.animate_text(text="Quitted card review.", speed=.075)
        return False

    elif response_filtered[0].isnumeric():
        add_step_via_integers(card_steps, card_title, response_filtered)
        reviewed_cards.append(card_path)

    elif response_filtered.lower() in l_menus.hotkey_feedback.keys(): # I.E. PAIR RESPONSE TO SHORTCUTS
        found_tuple = l_menus.hotkey_feedback[response_filtered]
        route = found_tuple[1]

        if route == 'menu':

            hotkey_dict, hotkey_list = l_menus.prep_card_run_menu(l_menus.cardsrun_macro_menu_actions)
            status = None

            while True:

                if not status:
                    status, possible_card_path = cardsrun_macro_menu(var_card=card,
                                                                     var_card_path=card_path,
                                                                     var_hotkey_dict=hotkey_dict,
                                                                     var_hotkey_list=hotkey_list)
                elif status == "RELOOP" and possible_card_path:
                    return "RELOOP"

                elif status == "EXIT MENU":
                    return "RELOOP"

                elif status == "CARD REFOCUSED":
                    return "RELOOP"

                elif status == "CARD MARKED FOR DELETION":
                    reviewed_cards.append(card_path)
                    deleted_cards.append(card_path)
                    l_animators.animate_text(f"Card {card_path} marked for deletion; returning to Lumocards.")
                    return "RELOOP"


        elif route == 'edit':
            fullpath_to_card = l_formatters.get_card_abspath(card_path)
            l_animators.animate_text((l_menus.hotkey_feedback[response_filtered.lower()][0]))
            subprocess.run(['micro {}'.format(fullpath_to_card)], shell=True, executable='/bin/bash')

            return "RELOOP"


        elif route == 'archive':
            reviewed_cards.append(card_path)
            archived_cards.append(card_path)
            print("Card completed: {}".format(l_files.cur_time_hr))
            print(random.choice(l_menus.completed_hotkey_feedback_phrases))


        elif route == 'delete':
            deleted_cards.append(card_path)
            reviewed_cards.append(card_path)
            print(l_menus.hotkey_feedback[response_filtered][0])


        elif route == 'superquit':
            found_tuple = l_menus.hotkey_feedback.get(response_filtered)
            feedback = found_tuple[0]
            l_animators.animate_text(feedback, speed=.075)
            return "SUPER QUIT"

    else:
        reviewed_cards.append(card_path)

        formatted_output = "{}: {}".format(card[0], response_filtered)
        full_message = ("'{}' was added to Lightwalk.".format(formatted_output))
        cards_for_lightwalk.append(formatted_output)
        l_animators.animate_text(full_message)

    return True

def cardsrun_recurring_macro_hotwords(card_path, card, card_idx):

    card_title, card_steps = card[0], card[1]

    response = input("    \n> ")
    response_filtered = l_formatters.add_blank_space(response)


    # ---- START OF MAIN IF/ELIF ---- #

    if response_filtered == " ": # I.E. SKIPPED CARD
        l_animators.animate_text(text=" ...", speed=.075)
        reviewed_recurring_cards.append(card_path)

    elif response_filtered in l_files.negative_user_responses: # I.E. QUIT
        l_animators.animate_text(text="Quitted card review.", speed=.075)
        return False

    elif response_filtered[0].isnumeric():
        add_step_via_integers(card_steps, card_title, response_filtered)
        reviewed_recurring_cards.append(card_path)

    elif response_filtered.lower() in l_menus.hotkey_feedback.keys(): # I.E. PAIR RESPONSE TO SHORTCUTS

        found_tuple = l_menus.hotkey_feedback[response_filtered]
        route = found_tuple[1]

        if route == 'menu':

            hotkey_dict, hotkey_list = l_menus.prep_card_run_menu(l_menus.cardsrun_macro_menu_actions)
            status = None

            while True:

                if not status:
                    status, possible_card_path = cardsrun_macro_menu(var_card=card,
                                                                              var_card_path=card_path,
                                                                              var_hotkey_dict=hotkey_dict,
                                                                              var_hotkey_list=hotkey_list)
                elif status == "RELOOP" and possible_card_path:
                    return "RELOOP"

                elif status == "EXIT MENU":
                    return "RELOOP"

                elif status == "CARD REFOCUSED":
                    return "RELOOP"

                elif status == "CARD MARKED FOR DELETION":
                    reviewed_recurring_cards.append(card_path)
                    deleted_cards.append(card_path)
                    l_animators.animate_text(f"Card {card_path} marked for deletion; returning to Lumocards.")
                    return "RELOOP"


        elif route == 'edit':

            fullpath_to_card = os.path.join(l_files.cards_near_folder, card_path)

            l_animators.animate_text((l_menus.hotkey_feedback[response_filtered.lower()][0]))
            subprocess.run(['micro {}'.format(fullpath_to_card)], shell=True, executable='/bin/bash')

            return "RELOOP"


        elif route == 'archive':
            next_occurrence = l_recurring.update_recurring_data(card_path)
            reviewed_recurring_cards.append(card_path)
            l_animators.animate_text(f"Recurring card will reactivate next {next_occurrence}")


        elif route == 'delete':
            deleted_cards.append(card_path)
            reviewed_recurring_cards.append(card_path)
            print(l_menus.hotkey_feedback[response_filtered][0])


        elif route == 'superquit':
            l_animators.animate_text(l_menus.hotkey_feedback[response_filtered][0], speed=.075)
            return "SUPER QUIT"

    else:
        reviewed_recurring_cards.append(card_path)

        formatted_output = "{}: {}".format(card[0], response_filtered)
        full_message = ("'{}' was added to Lightwalk.".format(formatted_output))
        cards_for_lightwalk.append(formatted_output)
        print(full_message)

    return True


def cardsrun_macro_menu(var_card, var_card_path, var_hotkey_dict, var_hotkey_list):

    card_fullpath = l_formatters.get_card_abspath(var_card_path)

    l_formatters.card_header(var_card)

    l_animators.standard_interval_printer(var_hotkey_list, speed_interval=0)
    print()
    l_animators.standard_interval_printer(l_menus.exit_menu, speed_interval=0)
    l_animators.standard_interval_printer(l_menus.quit_menu, speed_interval=0)

    while True:
        response = input("\n  > ")

        if response.upper() in var_hotkey_dict.keys():

            if var_hotkey_dict[response.upper()] == l_menus.action_open:
                subprocess.run([f'micro {card_fullpath}'], shell=True, executable='/bin/bash')
                return "RELOOP", var_card_path


            elif var_hotkey_dict[response.upper()] == l_menus.action_modify:

                hotkey_list, hotkey_dict = l_menus.prep_card_modify_menu(
                                                            actions_set=l_menus.cardsrun_modify_menu_actions.copy(),
                                                            var_submenu_cardpath=var_card_path)

                status, possible_returned_card = l_menus.menu_modifying_card(selected_card=var_card_path,
                                                                             var_hotkey_list=hotkey_list,
                                                                             var_hotkey_dict=hotkey_dict)
                if possible_returned_card:
                    return "RELOOP", possible_returned_card

                elif status == "CARD MARKED FOR DELETION":
                    return "CARD MARKED FOR DELETION", None

                elif status == "CARD REFOCUSED":
                    return "CARD REFOCUSED", None

                else:
                    return "RELOOP", var_card_path

            elif var_hotkey_dict[response.upper()] == l_menus.action_schedule:
                l_animators.animate_text("  This feature not fully available")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus.action_set_recurring:
                card_title_formatted = l_formatters.format_card_title(var_card_path.replace(".txt", ""))
                recur_menu_d, recur_menu_l = l_menus.prep_newcard_menu(l_menus.recurring_menu,
                                                                       l_menus.letters_filtered,
                                                                       pop_letters=False)
                print()
                l_animators.standard_interval_printer([card_title_formatted])
                print()
                l_animators.standard_interval_printer(recur_menu_l)

                recurrence_settings = l_menus.menu_recurrence_settings(var_menu=recur_menu_d)

                l_recurring.update_recurring_data(var_card_path, recurrence_settings, initialized=True)
                l_formatters.card_renamer(curr_name=var_card_path
                                          , dst_dir=l_files.recurring_cards_folder
                                          , dst_name=var_card_path)

                return "CARD REFOCUSED", None


        elif response.upper() in l_menus.hotkey_exit_dict.keys():
            return "EXIT MENU", None

        elif response.upper() in l_menus.hotkey_quit_dict.keys():
            l_animators.animate_text("Quit")
            sys.exit(0)

        elif response.lower() == 'quit':
            l_animators.animate_text("Quit")
            sys.exit(0)

        else:
            print("In this context your options are hotkey letter such as 'a', 'c', or 'quit'.")


def iterate_cards(list_of_cards, mode):
    total_cards = len(list_of_cards)

    for idx, card_path in enumerate(list_of_cards):
        status = None

        card_no = idx + 1
        card_counter_feedback_text = "Card ({}) of ({})".format(card_no, total_cards).upper()

        card = l_formatters.path_to_card(card_path)

        l_animators.standard_interval_printer(["", card_counter_feedback_text], speed_interval=0)
        l_boxify.display_card(card)

        if mode == "main cards":
            status = cardsrun_macro_hotwords(card_path=card_path, card=card, card_idx=card_no - 1)
        elif mode == "recurring cards":
            status = cardsrun_recurring_macro_hotwords(card_path=card_path, card=card, card_idx=card_no - 1)


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
        l_animators.animate_text(f'{len(reactivated_cards)} cards were reactivated...', speed=.075)

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


def update_cards():
    print()
    l_animators.animate_text("ADDING TO LIGHTWALK:")
    l_animators.standard_interval_printer(cards_for_lightwalk)
    print()

    if len(archived_cards) > 0:
        print()
        l_animators.animate_text("The system is now going to archive cards:")
        l_animators.standard_interval_printer(archived_cards)

        if l_files.proceed("> "):
            for card in archived_cards:
                l_formatters.archiver(card)


    if len(deleted_cards) > 0:
        print()
        l_animators.animate_text("The system is now going to delete cards:")
        l_animators.standard_interval_printer(deleted_cards)

        if l_files.proceed("> "):
            for card in deleted_cards:
                l_formatters.card_deleter(card)

    if not l_files.exists_lightwalk_file():
        l_animators.animate_text("Creating Lightwalk file for today...")
        l_files.mk_lightwalk()

    if len(cards_for_lightwalk) > 0:
        l_files.basic_wrtr("\n\n", l_files.lightwalk_file)
        l_files.basic_wrtr(f"ACTIVE CARD REVIEW: {l_files.cur_time_hr}", l_files.lightwalk_file)
        l_files.basic_wrtr_list(cards_for_lightwalk, l_files.lightwalk_file)


    print()
    l_animators.animate_text("This round of cards has completed.")
    print()


def main():
    cards_intro()

    while True:
        status = run_remaining_cards()

        if status == "EXIT CARD LIST" or status == "SUPER QUIT":
            break

        print()
        l_animators.animate_text(f"Status: {status}")

    if status == "EXIT CARD LIST":
        response = l_files.proceed("Proceed to Recurring Cards? ")

        if response:
            review_and_write_recurring()

    elif status == "SUPER QUIT":
        update_cards()
        sys.exit(0)


if __name__ == "__main__":
    main()
    update_cards()



# ---- ETC. ---- #
# completed_hotkey_feedback_phrases = [
#     "Nice Job!"
#     , "Go Team!"
#     , "Excellent!"
#     , "Marked as complete."
#     , "Cool!"
#     , "Card was moved to archived cards"
# ]
#
# hotkey_feedback =  {
#       "edit card": ("You are editing card: ", 'edit')
#     , "edit": ("You are editing card: ", 'edit')
#     , "mark": ("You have completed some steps:", 'edit')
#     , "change": ("You are editing card: ", 'edit')
#     , "open": ("You are editing card: ", 'edit')
#
#     , "show full": ("Showing full card...", 'show full')
#     , "show all": ("Showing full card...", 'show full')
#     , "see all": ("Showing full card...", 'show full')
#     , "full card": ("Showing full card...", 'show full')
#     , "full": ("Showing full card...", 'show full')
#     , "show": ("Showing full card...", 'show full')
#
#     , "menu": ("menu", "menu")
#     , "options": ("menu", "menu")
#     , "help": ("menu", "menu")
#
#     , "delete": ("Card set for deletion.", 'delete')
#     , "deleted": ("Card set for deletion.", 'delete')
#
#     , "done": (True, 'archive')
#     , "complete": (True, 'archive')
#     , "completed": (True, 'archive')
#     , "archive": (True, 'archive')
#     , "finished": (True, 'archive')
#
#     , "mark inactive": ("Card toggled to inactive cards.", 'toggle')
#     , "toggle": ("Card toggled to inactive cards.", 'toggle')
#     , "make inactive": ("Card toggled to inactive cards.", 'toggle')
#     , "inactive": ("Card toggled to inactive cards.", 'toggle')
#     , "deactivate": ("Card toggled to inactive cards.", 'toggle')
#
#     , "super quit": ("Super Quit, Goodbye!", 'superquit')
#     , "full quit": ("Super Quit, Goodbye!", 'superquit')
#     , "superquit": ("Super Quit, Goodbye!", 'superquit')
# }
