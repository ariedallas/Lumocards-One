import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_recurring as l_recurring
import LUMO_LIBRARY.lumo_newcard_2 as l_newcard


def proceed(input_text="... "):
    user_input = input(f"{input_text} ")
    return True if user_input not in l_menus_data.NEGATIVE_USER_RESPONSES else False


def prep_newcard_menu(var_menu, var_letters, pop_letters=False):
    if pop_letters:
        full_hotkey_set_dict = {f"{var_letters.pop(0)}": f"{match}" for match in var_menu}

    else:
        full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(l_menus_data.LETTERS_FILTERED, var_menu)}

    full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_menu(var_menu):
    full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(l_menus_data.LETTERS_FILTERED, var_menu)}

    full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_card_run_menu(actions_list):
    hotkey_dict = {}

    for letter, action in zip(l_menus_data.LETTERS_FILTERED, actions_list):
        hotkey_dict[letter] = action

    full_hotkey_set_dict = hotkey_dict

    full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_card_modify_menu(actions_list, card_filename):
    current_focus = l_card_utils.get_card_focus(card_filename)

    hotkey_dict = {}

    if current_focus == "near":
        actions_list.remove(l_menus_data.ACTION_SET_NEAR)
    elif current_focus == "middle":
        actions_list.remove(l_menus_data.ACTION_SET_MIDDLE)
    elif current_focus == "distant":
        actions_list.remove(l_menus_data.ACTION_SET_DIST)

    for letter, action in zip(l_menus_data.LETTERS_FILTERED, actions_list):
        hotkey_dict[letter] = action

    full_hotkey_set_dict = hotkey_dict

    full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_list, full_hotkey_set_dict


def menu_recurrence_settings(var_menu):
    recurrence_settings = None

    while not recurrence_settings:
        print()
        response = input("  Should this recur in days, weeks, or months? > ")
        if response.upper() not in var_menu.keys():
            avlbl = list(var_menu.keys())
            print(f"  Available letters are '{avlbl[0]}' '{avlbl[1]}' and '{avlbl[2]}' (upper or lower case)")
            continue

        units = var_menu[response.upper()]
        response = input(f"  Select a number of {units}? e.g. '2' > ")

        if not l_card_utils.test_for_float(response):
            print()
            print(f"  Please use whole numbers only (no decimals)")
            continue
        else:
            amt = float(response)
            units = units.replace("(s)", "")

        recurrence_settings = (units, amt)
        return recurrence_settings


def menu_modify_card(selected_card, var_hotkey_list, var_hotkey_dict):
    print()
    l_animators.animate_text("MODIFYING CARD")
    print()

    while True:
        l_animators.standard_interval_printer(var_hotkey_list, speed_interval=0)
        print()
        l_animators.standard_interval_printer(l_menus_data.EXIT_MENU_LIST, speed_interval=0)

        response = input("\n  > ")

        if response.upper() in var_hotkey_dict.keys():

            if var_hotkey_dict[response.upper()] == l_menus_data.ACTION_SET_NEAR:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_near_folder,
                                          dst_name=selected_card)
                l_animators.animate_text("  Card set to ➝ Near Focus")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_SET_MIDDLE:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_middle_folder,
                                          dst_name=selected_card)
                l_animators.animate_text("  Card set to ➝ Middle Focus")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_SET_DIST:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_dist_folder,
                                          dst_name=selected_card)
                l_animators.animate_text("  Card set to ➝ Distant Focus")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_RENAME:
                retitled_card_path = l_newcard.get_cardname_from_input()
                print()
                # l_animators.animate_text(f"  Card will been renamed from '{selected_card}' → '{retitled_card_path}'")
                l_card_utils.card_renamer(curr_name=selected_card, dst_name=retitled_card_path)
                return None, retitled_card_path

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_ARCHIVE:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.archived_cards_folder,
                                          dst_name=selected_card)
                l_animators.animate_text("  Card Archived")
                return None, None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_DELETE:
                l_card_utils.card_deleter(selected_card)
                return "DELETED CARD", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_MARK_DELETE:
                return "CARD MARKED FOR DELETION", None


        elif response.upper() in l_menus_data.EXIT_MENU_DICT.keys():
            return None, None

        elif response in l_menus_data.NEGATIVE_USER_RESPONSES:
            l_animators.animate_text("Returning to Main Menu")
            return None, None

        else:
            print()
            print("You entered something other than one letter.")
            print()
