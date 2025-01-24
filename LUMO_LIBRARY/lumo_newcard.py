import os
import pathlib
import sys
import subprocess
from argparse import ArgumentParser

import lumo_filehandler as l_files
import lumo_formatters as l_formatters
import lumo_animationlibrary as l_animators
import lumo_recurring as l_recurring
import lumo_json_utilities as l_json_utils
import lumo_search_cards as l_search
import lumo_menus as l_menus

settings = l_files.get_json_settings()

all_card_categories = l_files.get_lumocards_categories()
default_text = '\n'.join(('...', '...', '...'))

card_title_already_exists = False


def arg_parser():
    global parser

    parser = ArgumentParser(add_help=False)
    parser.add_argument('-o', '--output', action='store_true',
                        help="shows output")
    parser.add_argument(
        'category'
        , action='store'
        , metavar='Optional card category?'
        , help="Use an abbreviating letter"
    )
    parser.add_argument(
        # '-o'
        # , '--card_name'
        'cardname'
        , action='store'
        , nargs="+"
        , metavar='Optional card name?'
        , default='unnamed'
        , help="…?")


# change this so that it returns the same kind of type, i.e. true / false
def retrieve_available_arguments():
    if len(sys.argv) > 1:
        result = parser.parse_args()
        return result
    else:
        return False


def get_card_from_argv(parsed_options):
    cardname_as_list = [t.title() for t in parsed_options.cardname]
    cardname = "".join(cardname_as_list)

    result = parsed_options.category.upper()
    category = category_check(result)

    card_name = "_".join((category, cardname))
    complete_card_name = f"{card_name}.txt"

    return complete_card_name


def get_cardname_from_input():
    print()
    cardname = input("NEW CARD NAME:  ").title()
    result = cardname.replace(' ', '')
    return result


def get_category_from_input():

    print("\n")

    print("CARD CATEGORIES .......")
    print()
    print("{:<10}{:^10}{:>10}".format("[Aa]_ADIO", "[Pp]_PNTG", "[Rr]_MAKE", "\n"))
    print("{:<10}{:^10}{:>10}".format("[Ee]_ERND", ".....", "[Ff]_SOIL", "\n"))
    print("{:<10}{:^10}{:>10}".format("[Cc]_COMP", "[Dd]_DOMS", "[Ss]_SLFC", "\n"))

    print("\n")
    result = input("Select a category letter > ")

    return category_check(result)


def category_check(card_category):
    if card_category.upper() not in all_card_categories:
        l_animators.animate_text("Category letter currently doesn't exist", speed=.025)
        l_animators.animate_text("- or -", speed=.025)
        l_animators.animate_text("You entered something other than one letter.", speed=.025)
        print()
        l_animators.animate_text("The system defaults the category to [Rr]_MAKE.", speed=.025)
        return 'R'

    else:
        return card_category.upper()


def get_card_name():
    global card_title_already_exists

    outcome = retrieve_available_arguments()

    if outcome and not card_title_already_exists:
        card_filename = get_card_from_argv(outcome)
        check_for_dupes(card_filename)

        if not card_title_already_exists:
            return card_filename
        else:
            return None
    else:
        card_title_already_exists = False

        card_filename = get_card_from_input()
        check_for_dupes(card_filename)

        if not card_title_already_exists:
            return card_filename
        else:
            return None


def get_card_from_input():
    cardname = get_cardname_from_input()
    category = get_category_from_input()
    joined = ("_").join((category, cardname))
    result = f"{joined}.txt"
    return result


def prep_newcard_menu(menu, pop_letters=False):
    if pop_letters:
        full_hotkey_set_dict = {f"{letters_filtered_copy.pop(0)}":f"{match}" for match in menu}

    else:
        full_hotkey_set_dict = {f"{ltr}":f"{match}" for ltr, match in zip(l_menus.letters_filtered, menu)}


    full_hotkey_set_list = [f"  [{letter}] {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def generate_quick_card(card_filename):
    formatted_card_fullpath = os.path.join(l_files.cards_near_folder, card_filename)
    with open(formatted_card_fullpath, "a+") as newcard:
        newcard.write(default_text)

    return formatted_card_fullpath


def check_for_dupes(card_filename):
    global card_title_already_exists
    card_title_already_exists = False

    if card_filename in os.listdir(l_files.cards_near_folder):
        card_title_already_exists = True
    elif card_filename in os.listdir(l_files.cards_middle_folder):
        card_title_already_exists = True
    elif card_filename in os.listdir(l_files.cards_dist_folder):
        card_title_already_exists = True
    elif card_filename in os.listdir(l_files.recurring_cards_folder):
        card_title_already_exists = True
    elif card_filename in os.listdir(l_files.archived_cards_folder):
        card_title_already_exists = True
    elif card_filename in os.listdir(l_files.checklist_cards_folder):
        card_title_already_exists = True


def add_custom_or_default_steps():
    scratchpad_file = os.path.join(l_files.temp_folder, "scratchpad.txt")
    if l_files.proceed("Edit steps? >  "):
        with open(scratchpad_file, "w") as fin:
            fin.write("")

        subprocess.run([f'{settings.get("text editor")} {scratchpad_file}'], shell=True)

        with open(scratchpad_file, "r") as fin:
            steps = [l for l in fin.readlines()]

    else:
        steps = False

    return steps


def create_card():
    global letters_filtered_copy
    letters_filtered_copy = l_menus.letters_filtered.copy()

    card_filename = get_card_name()

    if card_filename:
        card_steps = add_custom_or_default_steps()

    else:
        print()
        l_animators.animate_text("A card with this name already exists...")
        l_animators.animate_text("Try another card name.")
        return "RESTART", None

    focus_menu_d, focus_menu_l = l_menus.prep_newcard_menu(l_menus.focus_menu,
                                                           letters_filtered_copy,
                                                           pop_letters=True)

    schedule_menu_d, schedule_menu_l = l_menus.prep_newcard_menu(l_menus.schedule_menu,
                                                                 letters_filtered_copy,
                                                                 pop_letters=True)

    combined_menus_dict = focus_menu_d | schedule_menu_d

    status = "CREATING CARD"
    response = True

    while response not in l_files.negative_user_responses:
        print()
        print(f"Status: {status}")

        print()
        l_animators.standard_interval_printer(focus_menu_l, speed_interval=0)
        print()
        l_animators.standard_interval_printer(schedule_menu_l, speed_interval=0)
        print()
        l_animators.standard_interval_printer(l_menus.start_over_menu, speed_interval=0)
        l_animators.standard_interval_printer(l_menus.quit_menu, speed_interval=0)
        print()
        response = input("  Select where this card should go > ")

        if response.upper() in combined_menus_dict.keys():

            if combined_menus_dict[response.upper()] == "Set as ➝ Near Focus":

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.cards_near_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text("  Card set to ➝ Near Focus")
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[response.upper()] == "Set as ➝ Middle Focus":

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.cards_middle_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text("  Card set to ➝ Middle Focus")
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[response.upper()] == "Set as ➝ Dist Focus":

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.cards_dist_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text("  Card set to ➝ Distant Focus")
                return "CREATED CARD", card_abspath


            # ---- SCHEDULING MENU ---- #


            elif combined_menus_dict[response.upper()] == "Set as ➝ Checklist Card":

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.checklist_cards_folder,
                                                              add_custom_steps=card_steps)

                l_animators.animate_text("  Card set to ➝ Checklist Cards")
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[response.upper()] == "Make into ➝ Recurring Card":

                card_title_formatted = l_formatters.format_card_title(card_filename.replace(".txt", ""))
                recur_menu_d, recur_menu_l = l_menus.prep_newcard_menu(l_menus.recurring_menu,
                                                                       l_menus.letters_filtered,
                                                                       pop_letters=False)

                print()
                l_animators.standard_interval_printer([card_title_formatted])
                print()
                l_animators.standard_interval_printer(recur_menu_l)

                recurrence_settings = l_menus.menu_recurrence_settings(recur_menu_d)

                card_abspath, json_file = write_card_and_json(card_filename,
                                                              l_files.recurring_cards_folder,
                                                              add_custom_steps=card_steps)

                l_recurring.update_recurring_data(card_filename, recurrence_settings, initialized=True)

                print()
                l_animators.animate_text("  Card created in ➝ Recurring Cards")
                return "CREATED CARD", card_abspath

            elif combined_menus_dict[response.upper()] == "Schedule to ➝ Calendar":
                l_animators.animate_text("  This function currently unavailable...")
                # card_abspath = generate_card(card_filename, l_files.recurring_cards_folder)
                # l_animators.animate_text("Card set to ➝ Recurring Cards")
                # return "CREATED CARD", card_abspath


        elif response.lower() == "x":
            return "RESTART", None

        elif response.lower() == "q":
            l_animators.animate_text("Quitting...")
            sys.exit(0)

        else:
            l_animators.animate_text("  Options available in this context are just shortcut letters.")


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

    default_json = l_json_utils.make_dflt_json_dict(card_folder, c_abbr)
    json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)
    l_json_utils.write_json(json_filename=json_fullpath, json_data=default_json)

    return formatted_card_fullpath, json_fullpath


def card_creation_loop():
    status = "RESTART"
    possible_card_abspath = None

    while status == "RESTART":
        status, possible_card_abspath = create_card()

    if possible_card_abspath:
        card_path = os.path.basename(possible_card_abspath)
        card = l_formatters.filename_to_card(card_path)

        return card, card_path

    else:
        return None, None


def card_menu_loop(result_card, result_path):

    if result_card and result_path:
        hotkey_dict, hotkey_list = l_menus.prep_newcard_menu(l_menus.newcard_main_actions, l_menus.letters_filtered.copy())
        status, return_path = l_search.cardsearch_main_options(var_card=result_card,
                                                               var_card_filename=result_path,
                                                               var_hotkey_dict=hotkey_dict,
                                                               var_hotkey_list=hotkey_list)
        while status == "RELOOP":
            card = l_formatters.filename_to_card(return_path)
            status, return_path = l_search.cardsearch_main_options(var_card=card,
                                                                   var_card_filename=return_path,
                                                                   var_hotkey_dict=hotkey_dict,
                                                                   var_hotkey_list=hotkey_list)
    else:
        print()
        l_animators.animate_text("Quit Lumocards: New Card")
        sys.exit(0)

    print()
    l_animators.animate_text("Quit Lumocards: New Card")


def main():
    arg_parser()
    result_card, result_path = card_creation_loop()
    card_menu_loop(result_card, result_path)


if __name__ == "__main__":
    main()


# ---- ETC. / UNUSED ---- #
#
# def lambda_menu(letter, msg):
#     return [f"  [{letter}] {msg}"]
