import argparse
import os
import re
import string
import subprocess

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
import LUMO_LIBRARY.lumo_recurring as l_recurring

letters = string.ascii_lowercase
letters_filtered = [l.upper() for l in letters if not (l == "q") and not (l == "x")]
settings = l_files.get_json_settings()


def test_match(queried):
    unique_words = re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", queried)
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
    card = l_card_utils.filename_to_card(chosen_file, check_archives=True)
    l_menus_funcs.prep_menu_tuple(l_menus_data.SEARCH_MAIN_MENU)
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
                            + sorted(file_matches_recurring) + sorted(file_matches_checklist) + sorted(
        file_matches_archived)

    return found_matches, shortcut_file_matches


def big_zipper(var_total_matches):
    total_amt_matches = sum([len(m) for m in var_total_matches])

    if total_amt_matches > 24:
        return total_amt_matches, None, None

    letters_filtered_copy = letters_filtered.copy()

    print()

    near_matches_setup = [f"[{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[0]]
    mid_matches_setup = [f"[{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[1]]
    dist_matches_setup = [f"[{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[2]]
    recurring_matches_setup = [f"[{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[3]]
    checklist_matches_setup = [f"[{letters_filtered_copy.pop(0)}] {match}" for match in var_total_matches[4]]
    archived_matches_setup = [f"[{letters_filtered_copy.pop(0)}] ({len(var_total_matches[5])})"] if len(
        var_total_matches[5]) > 0 else []

    near_matches_formatted = ["NEAR FOCUS CARDS:"] + near_matches_setup
    mid_matches_formatted = ["MIDDLE FOCUS CARDS:"] + mid_matches_setup
    dist_matches_formatted = ["DISTANT FOCUS CARDS:"] + dist_matches_setup
    recurring_matches_formatted = ["RECURRING CARDS:"] + recurring_matches_setup
    checklist_matches_formatted = ["CHECKLIST CARDS:"] + checklist_matches_setup
    archived_matches_formatted = ["ARCHIVED CARDS:"] + archived_matches_setup

    used_letters = [letter for letter in letters_filtered if letter not in letters_filtered_copy]

    big_zipp = [near_matches_formatted, mid_matches_formatted, dist_matches_formatted
        , recurring_matches_formatted, checklist_matches_formatted, archived_matches_formatted]

    return total_amt_matches, big_zipp, used_letters


def select_card_from_found(searchterm):
    found_matches, shortcut_file_matches = big_zipper_prep(searchterm=searchterm)
    total_amt_matches, all_matches_formatted, used_letters = big_zipper(found_matches)

    if total_amt_matches > 24:
        print()
        l_animators.list_printer([f"More than 24 possible matches for term \'{searchterm}\'...",
                                  "Try something more specific."]
                                 , indent_amt=2)

        return None, None, False

    if total_amt_matches == 0:
        l_animators.animate_text_indented(f"No matches found for your term \'{searchterm}\'... "
                                          , indent_amt=2
                                          , finish_delay=.5)
        print()
        return None, None, False

    if len(all_matches_formatted[5]) > 1:
        archived_matches_line = all_matches_formatted[5][1]
        archives_letter = archived_matches_line[1]
    else:
        archives_letter = None

    for matches_list in all_matches_formatted:
        if len(matches_list) > 1:
            l_animators.list_printer(matches_list, indent_amt=2, speed_interval=0)
            print()

    l_animators.list_printer(l_menus_data.EXIT_MENU_LIST, indent_amt=2, speed_interval=0)
    l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=2, speed_interval=0)

    while True:
        user_input = input("\n  > ")
        val = user_input.strip()

        if val.upper() == archives_letter:
            print()
            l_animators.list_printer(["Archived cards are not shown in this mode, but",
                                      "the number indicator is shown for reference.",
                                      f"i.e. there is/are ({len(found_matches[5])}) archived cards that match."]
                                     , indent_amt=2
                                     , speed_interval=0)
            continue

        # TODO: change this to be if ... in dict.keys() etc.
        if val.isalpha() and len(val) == 1 and (val.upper() in used_letters):
            letter_as_idx = ord(val.lower()) - 97

            chosen_file = shortcut_file_matches[letter_as_idx]
            card = l_card_utils.filename_to_card(chosen_file, check_archives=True)

            return card, chosen_file, False

        elif val.lower() in {"x", "exit"}:
            return None, None, False

        elif val.lower() in {"q", "quit"}:
            return None, None, True

        else:
            print()
            l_animators.list_printer(["You entered something other than one letter ",
                                      "- or - ",
                                      "You entered a letter that doesn't match anything."],
                                     indent_amt=2,
                                     speed_interval=0)


def cardsearch_main_options(var_card, var_card_filename, var_hotkey_dict, var_hotkey_list):
    card_fullpath = l_card_utils.get_card_abspath(var_card_filename)

    l_card_utils.card_header(var_card)

    l_animators.list_printer(var_hotkey_list, indent_amt=2, speed_interval=0)
    print()
    l_animators.list_printer(l_menus_data.EXIT_MENU_LIST, indent_amt=2, speed_interval=0)
    l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=2, speed_interval=0)

    while True:
        user_input = input("\n  > ")
        val = user_input.strip()

        if val.upper() in var_hotkey_dict.keys():

            action = var_hotkey_dict.get(val.upper())

            if action == l_menus_data.ACTION_OPEN:
                subprocess.run([f"{l_files.micro} {card_fullpath}"], shell=True)
                return "RELOOP", var_card_filename

            elif action == l_menus_data.ACTION_MODIFY:

                hotkey_list, hotkey_dict = l_menus_funcs.prep_card_modify_menu(l_menus_data.SEARCH_MODIFY_MENU.copy(),
                                                                               card_filename=var_card_filename)

                possible_status, possible_returned_card = l_menus_funcs.menu_modify_card(
                    selected_card=var_card_filename,
                    var_hotkey_list=hotkey_list,
                    var_hotkey_dict=hotkey_dict,
                    indent_amt=0)

                if possible_returned_card:
                    return "RELOOP", possible_returned_card

                elif possible_status == "DELETED CARD":
                    return "NEW SEARCH", None

                else:
                    return "RELOOP", var_card_filename


            elif action == l_menus_data.ACTION_SCHEDULE:
                l_animators.animate_text_indented("This feature not fully available", indent_amt=2, finish_delay=.4)
                print()
                return "RELOOP", var_card_filename

            elif action == l_menus_data.ACTION_SET_RECURRING_2:
                card_title_formatted = l_card_utils.format_card_title(var_card_filename.replace(".txt", ""))
                recur_menu_d, recur_menu_l = l_menus_funcs.prep_newcard_menu(l_menus_data.RECURRING_MENU,
                                                                             l_menus_data.LETTERS_FILTERED,
                                                                             pop_letters=False)
                print()
                l_animators.animate_text(card_title_formatted)
                print()
                l_animators.list_printer(recur_menu_l, indent_amt=2, speed_interval=0)

                recurrence_settings = l_menus_funcs.menu_recurrence_settings(var_menu=recur_menu_d)

                l_recurring.update_recurring_data(var_card_filename, recurrence_settings, initialized=True)
                l_card_utils.card_renamer(curr_name=var_card_filename
                                          , dst_dir=l_files.recurring_cards_folder
                                          , dst_name=var_card_filename)

                return "RELOOP", var_card_filename


        elif val.lower() in {"x", "exit"}:
            return "NEW SEARCH", None

        elif val.lower() in {"q", "quit"}:
            return "QUIT", None

        else:
            print()
            l_animators.list_printer(["Your options are hotkey letters:", "such as 'a', 'c'; or quit/exit", ""]
                                     , indent_amt=2
                                     , finish_delay=.5)


def steps_preview(card_steps, steps_amt, steps_idx):
    if 3 > steps_amt > 0:
        initial = [f" {n} — {l_card_utils.step_abbreviator(step)}" for n, step in
                   zip(range(1, steps_idx), card_steps[0:steps_amt])]
        filler = [f" {n} — {step}" for n, step in zip(range(steps_idx, 4), l_card_utils.default_card_steps)]
        card_steps_three = initial + filler
    elif steps_amt >= 3:
        card_steps_three = [f" {n} — {l_card_utils.step_abbreviator(step)}" for n, step in
                            zip(range(4), card_steps[0:3])]
    else:
        card_steps_three = [f" {n} — {step}" for n, step in l_card_utils.default_card_steps]
    return card_steps_three


def main(initial_search_from_cli=None):
    status = "INITIAL SEARCH" if initial_search_from_cli else "NEW SEARCH"
    return_path = None

    print()
    while True:
        if status == "INITIAL SEARCH":
            print(f"{status}: '{initial_search_from_cli}'")
            card, matched_path, user_quit = select_card_from_found(initial_search_from_cli)

            if card:
                hotkey_dict, hotkey_list = l_menus_funcs.prep_menu_tuple(l_menus_data.SEARCH_MAIN_MENU)
                status, return_path = cardsearch_main_options(card, matched_path, hotkey_dict, hotkey_list)
            elif user_quit:
                status = "QUIT"
            else:
                status = "NEW SEARCH"

        elif status == "RELOOP":
            card, return_path = reshow_match(return_path)
            hotkey_dict, hotkey_list = l_menus_funcs.prep_menu_tuple(l_menus_data.SEARCH_MAIN_MENU)
            status, return_path = cardsearch_main_options(card, return_path, hotkey_dict, hotkey_list)

        elif status == "NEW SEARCH":
            if initial_search_from_cli:
                print()

            print(status)
            user_input = input(
                "\n"
                "                  (Type 'quit' to quit)"
                "\n  Enter a single search term i.e. 'hat'  >  ")

            val = user_input.strip()
            if val.lower() == "quit":
                status = "QUIT"
                continue

            card, matched_path, user_quit = select_card_from_found(val)

            if card:
                hotkey_dict, hotkey_list = l_menus_funcs.prep_menu_tuple(l_menus_data.SEARCH_MAIN_MENU)
                status, return_path = cardsearch_main_options(card, matched_path, hotkey_dict, hotkey_list)
            elif user_quit:
                status = "QUIT"


        else:  # status == "QUIT"
            break

            # Optional feature: show quit message.
            # l_animators.animate_text("Quit Lumo: Search", finish_delay=.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "match_term"
        , action="store"
        , metavar="Match Term"
        , help="This is what regex uses to search for...i.e. 'potatoes' ")

    parsed = parser.parse_args()

    main(parsed.match_term)
