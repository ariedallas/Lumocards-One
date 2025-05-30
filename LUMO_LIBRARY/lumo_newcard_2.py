import os
import pathlib
import subprocess
import sys
from argparse import ArgumentParser

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
import LUMO_LIBRARY.lumo_recurring as l_recurring
import LUMO_LIBRARY.lumo_search as l_search

settings = l_files.get_json_settings()

all_category_prefixes = l_files.get_category_prefixes()
default_text = "\n".join(("...", "...", "..."))

parser = ArgumentParser(add_help=False)
parser.add_argument("-o", "--output", action="store_true",
                    help="shows output")
parser.add_argument(
    "category"
    , action="store"
    , metavar="Optional card category?"
    , help="Use an abbreviating letter"
)
parser.add_argument(
    "title"
    , action="store"
    , nargs="+"
    , metavar="Optional card name?"
    , default="Make a title for the card"
    , help="…?")


def test_for_local_args():
    if len(sys.argv) > 1 and __name__ == "__main__":
        return True
    else:
        return False


def get_cardname_from_input(indent=0):
    if indent > 0:
        print(" " * indent, end="")

    cardname = input("Card Name >  ").title()
    result = cardname.replace(" ", "")
    return result


def get_category_from_input(indent=0):
    if indent > 0:
        print(" " * indent, end="")

    result = input("Card Category >  ")
    return category_check(result)


def category_check(card_category):
    valid_cat = card_category.strip().upper()

    if valid_cat not in all_category_prefixes and \
            valid_cat != "Z":
        print()
        l_animators.list_printer([
            "That category letter currently doesn't exist"
            , "- or -"
            , "You entered something other than one letter."
            , "The system defaults the category to Z — Default Category."]
            , indent_amt=2
            , speed_interval=.5)
        print()
        return "Z"
    elif valid_cat == "Z":
        return "Z"
    else:
        return valid_cat


def validate_from_local_parser():
    parsed_args = parser.parse_args()
    card_filename = parsed_to_filename(parsed_args.category, parsed_args.title)
    exists_card_already = check_for_dupes(card_filename)

    if not exists_card_already:
        return card_filename
    else:
        return None


def validate_from_lumo_parser(category, title):
    card_filename = parsed_to_filename(category, title)
    exists_card_already = check_for_dupes(card_filename)

    if not exists_card_already:
        return card_filename
    else:
        return None


def validate_from_input():
    card_filename = input_to_filename()
    exists_card_already = check_for_dupes(card_filename)

    if not exists_card_already:
        return card_filename
    else:
        return None


def parsed_to_filename(card_category, card_title):
    card_title_as_list = [t.title() for t in card_title]
    formatted_title = "".join(card_title_as_list)

    formatted_category = card_category.upper()
    valid_category = category_check(formatted_category)

    categorized_card = "_".join((valid_category, formatted_title))
    card_filename = f"{categorized_card}.txt"

    return card_filename


def input_to_filename():
    print()
    card_category = get_category_from_input(indent=2)
    card_title = get_cardname_from_input(indent=2)
    joined = "_".join((card_category, card_title))
    card_filename = f"{joined}.txt"
    return card_filename


def check_for_dupes(card_filename):
    card_exists = False

    if card_filename in os.listdir(l_files.cards_near_folder):
        card_exists = True
    elif card_filename in os.listdir(l_files.cards_middle_folder):
        card_exists = True
    elif card_filename in os.listdir(l_files.cards_dist_folder):
        card_exists = True
    elif card_filename in os.listdir(l_files.cards_calendar_folder):
        card_exists = True
    elif card_filename in os.listdir(l_files.checklist_cards_folder):
        card_exists = True
    elif card_filename in os.listdir(l_files.recurring_cards_folder):
        card_exists = True

    return card_exists


def add_custom_or_default_steps():
    scratchpad_file = os.path.join(l_files.temp_folder, "scratchpad.txt")
    print()

    if l_menus_funcs.proceed("Edit steps? ( ➝ yes) >  ", indent_amt=2):
        with open(scratchpad_file, "w") as fin:
            fin.write("")

        subprocess.run([f"{settings.get("text editor")} {scratchpad_file}"], shell=True)

        with open(scratchpad_file, "r") as fin:
            steps = [l for l in fin.readlines()]

    else:
        steps = False

    return steps


def retry_loop_card_filename(card_filename):
    if not card_filename:
        print()
        l_animators.animate_text_indented("A card with this name already exists...", indent_amt=2)
        # TODO: to continue type any key but [q]; [q] for quit
        # TODO: -OR- inform user they can undo after next step and to make a dummy card

        while True:
            retry_card_filename = validate_from_input()
            if retry_card_filename:
                return retry_card_filename
            else:
                print()
                l_animators.animate_text_indented("A card with this name already exists...", indent_amt=2)

    return card_filename


def write_card(card_filename, card_steps):
    letters_filtered_copy = l_menus_data.LETTERS_FILTERED.copy()
    focus_menu_d, focus_menu_l = l_menus_funcs.prep_newcard_menu(l_menus_data.FOCUS_MENU,
                                                                 letters_filtered_copy,
                                                                 pop_letters=True)

    schedule_menu_d, schedule_menu_l = l_menus_funcs.prep_newcard_menu(l_menus_data.SCHEDULE_MENU,
                                                                       letters_filtered_copy,
                                                                       pop_letters=True)

    combined_menus_dict = focus_menu_d | schedule_menu_d

    while True:
        print()
        l_animators.animate_text(f"CREATING CARD: {card_filename}", finish_delay=.5)

        print()
        l_animators.list_printer(focus_menu_l, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(schedule_menu_l, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(l_menus_data.START_OVER_MENU_LIST, indent_amt=2, speed_interval=0)
        l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=2, speed_interval=0)
        print()
        user_input = input("  Select where this card should go >  ")

        if user_input.upper() in combined_menus_dict.keys():

            if combined_menus_dict[user_input.upper()] == l_menus_data.ACTION_SET_NEAR:

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.cards_near_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text_indented("Card set to ➝ Near Focus", indent_amt=2, finish_delay=.5)
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[user_input.upper()] == l_menus_data.ACTION_SET_MIDDLE:

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.cards_middle_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text_indented("Card set to ➝ Middle Focus", indent_amt=2, finish_delay=.5)
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[user_input.upper()] == l_menus_data.ACTION_SET_DIST:

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.cards_dist_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text_indented("Card set to ➝ Distant Focus", indent_amt=2, finish_delay=.5)
                return "CREATED CARD", card_abspath


            # ---- SCHEDULING MENU ---- #

            elif combined_menus_dict[user_input.upper()] == l_menus_data.ACTION_SCHEDULE:
                l_animators.animate_text_indented("This function currently unavailable...", indent_amt=2)

            elif combined_menus_dict[user_input.upper()] == l_menus_data.ACTION_SET_RECURRING:

                card_title_formatted = l_card_utils.format_card_title(card_filename.replace(".txt", ""))
                recur_menu_d, recur_menu_l = l_menus_funcs.prep_newcard_menu(l_menus_data.RECURRING_MENU,
                                                                             l_menus_data.LETTERS_FILTERED,
                                                                             pop_letters=False)

                print()
                l_animators.list_printer([card_title_formatted])
                print()
                l_animators.list_printer(recur_menu_l, indent_amt=2)

                recurrence_settings = l_menus_funcs.menu_recurrence_settings(recur_menu_d)

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.recurring_cards_folder,
                                                              add_custom_steps=card_steps)

                l_recurring.update_recurring_data(card_filename, recurrence_settings, initialized=True)

                print()
                l_animators.animate_text_indented("Card created in ➝ Recurring Cards", indent_amt=2, finish_delay=.5)
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[user_input.upper()] == l_menus_data.ACTION_SET_CHECKLIST:

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.checklist_cards_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text_indented("Card set to ➝ Checklist Cards", indent_amt=2, finish_delay=.5)
                return "CREATED CARD", card_abspath

        elif user_input.lower() in {"x", "exit"}:
            return "RELOOP", None

        elif user_input.lower() in {"q", "quit"}:
            print()
            l_animators.animate_text("Quit Lumo: New Card", finish_delay=.5)
            return "QUIT", None

        else:
            l_animators.animate_text_indented("Options available in this context are just shortcut letters.",
                                              indent_amt=2, finish_delay=.5)


def write_card_and_json(card_filename, folder, add_custom_steps=None):
    formatted_card_fullpath = os.path.join(folder, card_filename)
    card_folder = pathlib.Path(folder).name
    c_abbr = card_filename[0]

    if add_custom_steps:
        with open(formatted_card_fullpath, "w+") as newcard:
            for line in add_custom_steps:
                newcard.write(line)

    else:
        with open(formatted_card_fullpath, "w+") as newcard:
            newcard.write(default_text)

    default_json = l_json_utils.make_default_json_dict(card_folder, c_abbr)
    json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)
    l_json_utils.write_json(json_filename=json_fullpath, json_data=default_json)

    return formatted_card_fullpath, json_fullpath


def card_write_loop(card_filename, card_steps):
    status = None
    round_one = True
    possible_card_abspath = None

    while not status or status == "RELOOP":
        if round_one:
            status, possible_card_abspath = write_card(card_filename, card_steps)
            round_one = False
        else:
            possible_card_filename = validate_from_input()
            new_card_filename = retry_loop_card_filename(possible_card_filename)
            new_card_steps = add_custom_or_default_steps()
            status, possible_card_abspath = write_card(new_card_filename, new_card_steps)

    return status, possible_card_abspath


def card_menu_loop(result_card, result_path):
    hotkey_dict, hotkey_list = l_menus_funcs.prep_newcard_menu(l_menus_data.NEWCARD_MAIN_MENU,
                                                               l_menus_data.LETTERS_FILTERED.copy())

    status, return_path = l_search.cardsearch_main_options(var_card=result_card,
                                                           var_card_filename=result_path,
                                                           var_hotkey_dict=hotkey_dict,
                                                           var_hotkey_list=hotkey_list)
    while status == "RELOOP":
        card = l_card_utils.filename_to_card(return_path)
        status, return_path = l_search.cardsearch_main_options(var_card=card,
                                                               var_card_filename=return_path,
                                                               var_hotkey_dict=hotkey_dict,
                                                               var_hotkey_list=hotkey_list)


# ---- LUMO CALENDAR FUNCTIONS ---- #
def check_for_calendar_cards(card_filename):
    for card in os.listdir(l_files.cards_middle_folder):
        if card[2:] == card_filename:
            return False
    return True


def string_to_filename(var_str):
    split_string = str.split(var_str)
    cardname_as_list = [w.title() for w in split_string]
    cardname = "".join(cardname_as_list)

    cardname_txt = f"{cardname}.txt"
    return cardname_txt


def write_calendar_card_and_json(card_filename, folder, google_calendar_data, add_custom_steps=None):
    formatted_card_fullpath = os.path.join(folder, card_filename)
    card_folder = pathlib.Path(folder).name
    c_abbr = card_filename[0]

    if add_custom_steps:
        with open(formatted_card_fullpath, "w+") as newcard:
            for line in add_custom_steps:
                newcard.write(line)

    else:
        with open(formatted_card_fullpath, "w+") as newcard:
            newcard.write(default_text)

    default_json = l_json_utils.make_default_json_dict(card_folder, c_abbr, google_calendar_data)
    json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)
    l_json_utils.write_json(json_filename=json_fullpath, json_data=default_json)

    return formatted_card_fullpath, json_fullpath


def program_header():
    print()
    print("NEW CARD")
    print()
    l_card_utils.print_card_categories(indent_amt=2)


def main(card_category=None, card_title=None, from_lumo_menu=False):
    from_local_args = test_for_local_args()
    locally_run = (__name__ == "__main__")
    program_header()

    if from_lumo_menu and card_category and card_title:
        possible_card_filename = validate_from_lumo_parser(card_category, card_title)
    elif from_local_args:
        possible_card_filename = validate_from_local_parser()
    else:  # get from input
        possible_card_filename = validate_from_input()

    card_filename = retry_loop_card_filename(possible_card_filename)
    card_steps = add_custom_or_default_steps()
    status, possible_card_abspath = card_write_loop(card_filename, card_steps)

    if status == "QUIT" and locally_run:
        sys.exit(0)
    elif status == "QUIT" and from_lumo_menu:
        return
    else:  # status == "CREATED CARD":
        card_path = os.path.basename(possible_card_abspath)
        card = l_card_utils.filename_to_card(card_path)
        card_menu_loop(card, card_path)


if __name__ == "__main__":
    main()
