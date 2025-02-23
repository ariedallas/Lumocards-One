import os
import argparse
import re
import string
import subprocess
import sys

import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_formatters as l_formatters
import LUMO_LIBRARY.lumo_menus as l_menus
import LUMO_LIBRARY.lumo_recurring as l_recurring
# import lumo_json_utilities as l_json_utils

letters = string.ascii_lowercase
letters_filtered = [l.upper() for l in letters if not (l == "q") and not (l == "x")]
settings = l_files.get_json_settings()

def test_match(queried):

    unique_words =  re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", queried)
    return unique_words


def test_match_digit(queried, search_term):

    digit_match = re.findall(fr"{search_term}\d*", queried)
    return digit_match


def iterate_and_find(searchterm, folder):
    possible_files = []

    for item in os.listdir(folder):
        unique_words = test_match(item)
        digit_match = test_match_digit(queried=item, search_term=searchterm)

        for word in unique_words:
            if searchterm.capitalize() in word:
                possible_files.append(item)
            elif searchterm in word:
                possible_files.append(item)

        if digit_match:
            possible_files.append(item)


    return possible_files


def reshow_match(chosen_file):
    card = l_formatters.filename_to_card(chosen_file)
    l_menus.prep_menu(l_menus.cardsearch_main_menu_actions)
    return card, chosen_file


def big_zipper_prep(searchterm):

    file_matches_near = iterate_and_find(searchterm, l_files.cards_near_folder)
    file_matches_middle = iterate_and_find(searchterm, l_files.cards_middle_folder)
    file_matches_dist = iterate_and_find(searchterm, l_files.cards_dist_folder)

    file_matches_recurring = iterate_and_find(searchterm, l_files.recurring_cards_folder)
    file_matches_checklist = iterate_and_find(searchterm, l_files.checklist_cards_folder)
    file_matches_archived = iterate_and_find(searchterm, l_files.archived_cards_folder)

    found_matches = (sorted(file_matches_near), sorted(file_matches_middle), sorted(file_matches_dist)
                     , sorted(file_matches_recurring), sorted(file_matches_checklist), sorted(file_matches_archived))

    shortcut_file_matches = sorted(file_matches_near) + sorted(file_matches_middle) + sorted(file_matches_dist) \
                            + sorted(file_matches_recurring) + sorted(file_matches_checklist) + sorted(file_matches_archived)


    return found_matches, shortcut_file_matches


def big_zipper(var_total_matches):

    total_amt_matches = sum([len(m) for m in var_total_matches])

    if total_amt_matches > 24:
        return total_amt_matches, None, None

    letters_filtered_copy = letters_filtered.copy()

    print()

    near_matches_setup = [f"  [{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[0]]
    mid_matches_setup = [f"  [{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[1]]
    dist_matches_setup = [f"  [{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[2]]
    recurring_matches_setup = [f"  [{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[3]]
    checklist_matches_setup = [f"  [{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[4]]
    archived_matches_setup = [f"  [{letters_filtered_copy.pop(0)}] ({len(var_total_matches[5])})"] if len(var_total_matches[5]) > 0 else []


    near_matches_formatted = ["  NEAR FOCUS CARDS:"] + near_matches_setup
    mid_matches_formatted = ["  MIDDLE FOCUS CARDS:"] + mid_matches_setup
    dist_matches_formatted = ["  DISTANT FOCUS CARDS:"] + dist_matches_setup
    recurring_matches_formatted = ["  RECURRING CARDS:"] + recurring_matches_setup
    checklist_matches_formatted = ["  CHECKLIST CARDS:"] + checklist_matches_setup
    archived_matches_formatted = ["  ARCHIVED CARDS:"] + archived_matches_setup

    used_letters = [letter for letter in letters_filtered if letter not in letters_filtered_copy]

    big_zipp = [near_matches_formatted, mid_matches_formatted, dist_matches_formatted
                , recurring_matches_formatted, checklist_matches_formatted, archived_matches_formatted]

    return total_amt_matches, big_zipp, used_letters


def select_card_from_found(searchterm):

    found_matches, shortcut_file_matches = big_zipper_prep(searchterm=searchterm)
    total_amt_matches, all_matches_formatted, used_letters  = big_zipper(found_matches)

    if total_amt_matches > 24:
        print(f"More than 24 possible matches for term \'{searchterm}\'... try something more specific.")
        return None, None

    if total_amt_matches == 0:
        print(f"No matches found for your term \'{searchterm}\'... ")
        return None, None

    if len(all_matches_formatted[5]) > 1:
        archived_matches_line = all_matches_formatted[5][1]
        archives_letter = archived_matches_line[3]
    else:
        archives_letter = None

    for matches_list in all_matches_formatted:
        if len(matches_list) > 1:
            l_animators.standard_interval_printer(matches_list, speed_interval=0)
            print()

    print(l_menus.exit_menu[0])
    print(l_menus.quit_menu[0])

    while True:
        response = input("\n  > ")

        if response.upper() == archives_letter:
            print("  Archived cards are not shown in this mode, but"
                  "\n  the number indicator is shown for reference."
                  f"\n  i.e. there is/are ({len(found_matches[5])}) archived cards that pertain.")
            continue

        # change this to be if ... in dict.keys() etc.
        if response.isalpha() and len(response) == 1 and (response.upper() in used_letters):
            letter_as_listindex = ord(response.lower()) - 97

            chosen_file = shortcut_file_matches[letter_as_listindex]
            card = l_formatters.filename_to_card(chosen_file)

            return card, chosen_file

        elif response.lower() == "x":
            return None, None

        elif response.lower() == "q":
            print("Quit")
            print()
            sys.exit(0)

        elif response in l_files.negative_user_responses:
            print("Quit")
            print()
            sys.exit(0)

        else:
            print( "\nYou entered something other than one letter "
                   "\n- or - "
                   "\nYou entered a letter that doesn't match anything.")


def cardsearch_main_options(var_card, var_card_filename, var_hotkey_dict, var_hotkey_list):

    card_fullpath = l_formatters.get_card_abspath(var_card_filename)

    l_formatters.card_header(var_card)

    l_animators.standard_interval_printer(var_hotkey_list, speed_interval=0)
    print()
    l_animators.standard_interval_printer(l_menus.exit_menu, speed_interval=0)
    l_animators.standard_interval_printer(l_menus.quit_menu, speed_interval=0)

    while True:
        response = input("\n  > ")

        if response.upper() in var_hotkey_dict.keys():

            if var_hotkey_dict[response.upper()] == l_menus.action_open:
                subprocess.run([f"{settings.get("text editor")} {card_fullpath}"], shell=True)
                return "RELOOP", var_card_filename

            elif var_hotkey_dict[response.upper()] == l_menus.action_modify:

                hotkey_list, hotkey_dict = l_menus.prep_card_modify_menu(l_menus.cardsearch_modify_menu_actions.copy(),
                                                                         card_filename=var_card_filename)

                possible_status, possible_returned_card = l_menus.menu_modify_card(selected_card=var_card_filename,
                                                                                   var_hotkey_list=hotkey_list,
                                                                                   var_hotkey_dict=hotkey_dict)
                if possible_returned_card:
                    return "RELOOP", possible_returned_card

                elif possible_status == "DELETED CARD":
                    return "NEW SEARCH", None

                else:
                    return "RELOOP", var_card_filename


            elif var_hotkey_dict[response.upper()] == l_menus.action_schedule:
                l_animators.animate_text("  This feature not fully available")
                return "RELOOP", var_card_filename

            elif var_hotkey_dict[response.upper()] == l_menus.action_set_recurring:
                card_title_formatted = l_formatters.format_card_title(var_card_filename.replace(".txt", ""))
                recur_menu_d, recur_menu_l = l_menus.prep_newcard_menu(l_menus.recurring_menu,
                                                                       l_menus.letters_filtered,
                                                                       pop_letters=False)
                print()
                l_animators.standard_interval_printer([card_title_formatted])
                print()
                l_animators.standard_interval_printer(recur_menu_l)

                recurrence_settings = l_menus.menu_recurrence_settings(var_menu=recur_menu_d)

                l_recurring.update_recurring_data(var_card_filename, recurrence_settings, initialized=True)
                l_formatters.card_renamer(curr_name=var_card_filename
                                          , dst_dir=l_files.recurring_cards_folder
                                          , dst_name=var_card_filename)

                return "RELOOP", var_card_filename


        elif response.upper() in l_menus.hotkey_exit_dict.keys():
            return "NEW SEARCH", None

        elif response.upper() in l_menus.hotkey_quit_dict.keys():
            print()
            l_animators.animate_text("Quit Lumocards: Search")
            sys.exit(0)

        elif response.lower() == "quit":
            print()
            l_animators.animate_text("Quit Lumocards: Search")
            sys.exit(0)

        else:
            print()
            print("  In this context your options are hotkey letter such as 'a', 'c', or 'quit'.")


def steps_preview(card_steps, steps_amt, steps_idx):
    if 3 > steps_amt > 0:
        initial = [f" {n} — {l_formatters.step_abbreviator(step)}" for n, step in
                   zip(range(1, steps_idx), card_steps[0:steps_amt])]
        filler = [f" {n} — {step}" for n, step in zip(range(steps_idx, 4), l_formatters.default_card_steps)]
        card_steps_three = initial + filler
    elif steps_amt >= 3:
        card_steps_three = [f" {n} — {l_formatters.step_abbreviator(step)}" for n, step in
                            zip(range(4), card_steps[0:3])]
    else:
        card_steps_three = [f" {n} — {step}" for n, step in l_formatters.default_card_steps]
    return card_steps_three


def main():
    command_line_arg_parser = argparse.ArgumentParser()
    command_line_arg_parser.add_argument(
        "match_term"
        , action="store"
        , metavar="Match Term"
        , help="This is what regex uses to search for...i.e. 'potatoes' ")

    options = command_line_arg_parser.parse_args()

    status = "INITIAL SEARCH"
    response = True
    return_path = None

    while response not in l_files.negative_user_responses:
        print()

        if status == "INITIAL SEARCH":
            print(f"{status} ➝ '{options.match_term}'")

            card, matched_path = select_card_from_found(options.match_term)

            if card:
                hotkey_dict, hotkey_list = l_menus.prep_menu(l_menus.cardsearch_main_menu_actions)
                status, return_path = cardsearch_main_options(card, matched_path, hotkey_dict, hotkey_list)

            else:
                status = "NEW SEARCH"

        elif status == "RELOOP":
            print(status)

            card, return_path = reshow_match(return_path)
            hotkey_dict, hotkey_list = l_menus.prep_menu(l_menus.cardsearch_main_menu_actions)
            status, return_path = cardsearch_main_options(card, return_path, hotkey_dict, hotkey_list)

        elif status == "NEW SEARCH":
            print(status)
            response = input("\nTry entering a new search term or type 'quit' > ")

            if response not in l_files.negative_user_responses:
                card, matched_path = select_card_from_found(response)

                if card:
                    hotkey_dict, hotkey_list = l_menus.prep_menu(l_menus.cardsearch_main_menu_actions)
                    status, return_path = cardsearch_main_options(card, matched_path, hotkey_dict, hotkey_list)


if __name__ == "__main__":
    main()


# ---- ETC. / UNUSED ---- #


# elif var_hotkey_dict[response.upper()] == action_schedule:
#     print("Future function to be created with Google API")
#     return "RELOOP", var_card_path
#
# elif var_hotkey_dict[response.upper()] == action_newsearch:
#     return "NEW SEARCH", var_card_path
#
# elif var_hotkey_dict[response.upper()] == action_retitle:
#     print(var_card_path)
#
#     retitled_card_path = l_newcard.get_card_from_input()
#
#     l_animators.animate_text(f"Card will been renamed from "{var_card_path}" ➝ "{retitled_card_path}"")
#
#     if l_files.proceed("> "):
#         l_animators.animate_text("Card renamed")
#         src = os.path.join(l_files.cards_near_folder, var_card_path)
#         dst = os.path.join(l_files.cards_near_folder, retitled_card_path)
#         os.rename(src, dst)
#
#         return "RELOOP", retitled_card_path
#
#     else:
#         return "RELOOP", var_card_path
