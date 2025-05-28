import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_recurring as l_recurring
import LUMO_LIBRARY.lumo_newcard_2 as l_newcard


def proceed(input_text="... "):
    user_input = input(f"{input_text}")
    user_input_filtered = user_input.lower().strip()
    return True if user_input_filtered not in l_menus_data.NEGATIVE_USER_RESPONSES else False


def prep_newcard_menu(var_menu, var_letters, pop_letters=False):
    if pop_letters:
        full_hotkey_set_dict = {f"{var_letters.pop(0)}": f"{match}" for match in var_menu}

    else:
        full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(
            l_menus_data.LETTERS_FILTERED, var_menu)}

    full_hotkey_set_list = [f"[{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_menu_tuple(var_menu):
    full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(l_menus_data.LETTERS_FILTERED, var_menu)}

    full_hotkey_set_list = [f"[{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list

def menu_list_from_dict(var_dict):
    full_hotkey_set_list = [f"[{letter}]  {action}" for letter, action in zip(
        var_dict.keys(),
        var_dict.values())]

    return full_hotkey_set_list


def prep_card_run_menu(actions_list):
    hotkey_dict = {}

    for letter, action in zip(l_menus_data.LETTERS_FILTERED, actions_list):
        hotkey_dict[letter] = action

    full_hotkey_set_dict = hotkey_dict

    full_hotkey_set_list = [f"[{letter}]  {action}" for letter, action in zip(
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

    full_hotkey_set_list = [f"[{letter}]  {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_list, full_hotkey_set_dict


def menu_recurrence_settings(var_menu):
    recurrence_settings = None

    while not recurrence_settings:
        print()
        response = input("  Should this recur in days, weeks, or months? >  ")
        if response.upper() not in var_menu.keys():
            avlbl = list(var_menu.keys())
            print(f"  Available letters are '{avlbl[0]}' '{avlbl[1]}' and '{avlbl[2]}' (upper or lower case)")
            continue

        units = var_menu[response.upper()]
        response = input(f"  Select a number of {units}? e.g. '2' >  ")

        if not l_card_utils.test_for_float(response):
            print()
            print(f"  Please use whole numbers only (no decimals)")
            continue
        else:
            amt = float(response)
            units = units.replace("(s)", "")

        recurrence_settings = (units, amt)
        return recurrence_settings


def menu_modify_card(selected_card, var_hotkey_list, var_hotkey_dict, indent_amt):
    print()
    l_animators.animate_text_indented("MODIFYING CARD", indent_amt=indent_amt)
    print()

    while True:
        l_animators.list_printer(var_hotkey_list, indent_amt=indent_amt+2, speed_interval=0)
        print()
        l_animators.list_printer(l_menus_data.EXIT_MENU_LIST, indent_amt=indent_amt+2, speed_interval=0)

        input_space = " " * (indent_amt+2)
        response = input(f"\n{input_space}>  ")

        if response.upper() in var_hotkey_dict.keys():

            if var_hotkey_dict[response.upper()] == l_menus_data.ACTION_SET_NEAR:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card,
                                          dst_dir=l_files.cards_near_folder,
                                          dst_name=selected_card)

                l_animators.animate_text_indented("Card set to ➝ Near Focus", indent_amt=2, finish_delay=.5)
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_SET_MIDDLE:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card,
                                          dst_dir=l_files.cards_middle_folder,
                                          dst_name=selected_card)

                l_animators.animate_text_indented("Card set to ➝ Middle Focus", indent_amt=2, finish_delay=.5)
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_SET_DIST:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card,
                                          dst_dir=l_files.cards_dist_folder,
                                          dst_name=selected_card)

                l_animators.animate_text_indented("Card set to ➝ Distant Focus", indent_amt=2, finish_delay=.5)
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_RENAME:
                print()
                l_card_utils.print_card_categories()
                retitled_card_path = l_newcard.input_to_filename()
                print()
                confirmation = l_card_utils.card_renamer(curr_name=selected_card,
                                          dst_name=retitled_card_path,
                                          ask_confirmation=True)

                if confirmation == "CANCELLED":
                    l_animators.animate_text_indented("Cancelled card rename", indent_amt=2, finish_delay=.5)
                    return None, None

                l_animators.animate_text_indented("Card renamed", indent_amt=2, finish_delay=.5)
                return None, retitled_card_path

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_ARCHIVE:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_card_utils.card_renamer(curr_name=selected_card,
                                          dst_dir=l_files.archived_cards_folder,
                                          dst_name=selected_card)

                l_animators.animate_text_indented("Card archived", indent_amt=2, finish_delay=.5)
                return None, None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_DELETE:
                confirmation = l_card_utils.card_deleter(selected_card)

                if confirmation == "CANCELLED":
                    l_animators.animate_text_indented("Card not deleted", indent_amt=2, finish_delay=.5)
                    return None, None

                l_animators.animate_text_indented("Card deleted", indent_amt=2, finish_delay=.5)
                return "DELETED CARD", None

            elif var_hotkey_dict[response.upper()] == l_menus_data.ACTION_MARK_DELETE:
                return "CARD MARKED FOR DELETION", None


        elif response.upper() in l_menus_data.EXIT_MENU_DICT.keys():
            return None, None

        elif response in l_menus_data.NEGATIVE_USER_RESPONSES:
            l_animators.animate_text("Returning to Main Menu", finish_delay=.5)
            return None, None

        else:
            print()
            print("You entered something other than one letter.")
            print()

if __name__ == "__main__":
    print("Hello from main")