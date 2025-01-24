import string

import lumo_filehandler as l_files
import lumo_formatters as l_formatters
import lumo_animationlibrary as l_animators
import lumo_recurring as l_recurring
import lumo_newcard as l_newcard

letters = string.ascii_lowercase
letters_filtered = [l.upper() for l in letters if not (l == 'q') and not (l == 'x')]

completed_hotkey_feedback_phrases = [
    "Nice Job!"
    , "Go Team!"
    , "Excellent!"
    , "Marked as complete."
    , "Cool!"
    , "Card was moved to archived cards"
]

hotkey_feedback =  {
      "edit card": ("You are editing card: ", 'edit')
    , "edit": ("You are editing card: ", 'edit')
    , "mark": ("You have completed some steps:", 'edit')
    , "change": ("You are editing card: ", 'edit')
    , "open": ("You are editing card: ", 'edit')

    , "show full": ("Showing full card...", 'show full')
    , "show all": ("Showing full card...", 'show full')
    , "see all": ("Showing full card...", 'show full')
    , "full card": ("Showing full card...", 'show full')
    , "full": ("Showing full card...", 'show full')
    , "show": ("Showing full card...", 'show full')

    , "menu": ("menu", "menu")
    , "options": ("menu", "menu")
    , "help": ("menu", "menu")

    , "delete": ("Card set for deletion.", 'delete')
    , "deleted": ("Card set for deletion.", 'delete')

    , "done": (True, 'archive')
    , "complete": (True, 'archive')
    , "completed": (True, 'archive')
    , "archive": (True, 'archive')
    , "finished": (True, 'archive')

    , "mark inactive": ("Card toggled to inactive cards.", 'toggle')
    , "toggle": ("Card toggled to inactive cards.", 'toggle')
    , "make inactive": ("Card toggled to inactive cards.", 'toggle')
    , "inactive": ("Card toggled to inactive cards.", 'toggle')
    , "deactivate": ("Card toggled to inactive cards.", 'toggle')

    , "super quit": ("Super Quit, Goodbye!", 'superquit')
    , "full quit": ("Super Quit, Goodbye!", 'superquit')
    , "superquit": ("Super Quit, Goodbye!", 'superquit')
}

action_open = "Open/Edit card in text editor"
action_modify = "Refocus, Rename, Archive, or Delete"
action_schedule = "Schedule card to ➝ Calendar"
action_set_recurring = "Set/Update ➝ Recurring Card"

action_set_near = "Set card to ➝ Near Focus"
action_set_middle = "Set card to ➝ Middle Focus"
action_set_dist = "Set card to ➝ Distant Focus"

action_archive = "Move card to Archives"
action_delete = "Delete card"
action_mark_delete = "Mark card for deletion"
action_newsearch = "New search"
action_retitle = "Rename card"
action_retitle_B = "Retitle + Change Category card"

action_exit_menu = "➝ Exit Menu"
action_start_over = "➝ Start Over"
action_cancel = "➝ Cancel"
action_quit = "➝ Quit"

# hotkey_exit_menu = {"X": f"{action_exit_menu}"}

focus_menu = [
      "Set as ➝ Near Focus"
    , "Set as ➝ Middle Focus"
    , "Set as ➝ Dist Focus"
]

schedule_menu = [
      "Schedule to ➝ Calendar"
    , "Set as ➝ Recurring Card"
    , "Set as ➝ Checklist Card"
]

recurring_menu = [
      "Day(s)"
    , "Week(s)"
    , "Month(s)"
]

cardsrun_macro_menu_actions = [
      action_open
    , action_modify
    , action_schedule
    , action_set_recurring
]

cardsrun_modify_menu_actions = [
      action_set_near
    , action_set_middle
    , action_set_dist
    , action_retitle
    , action_archive
    , action_mark_delete
]

cardsearch_main_menu_actions = [
          action_open
        , action_modify
        , action_schedule
        , action_set_recurring
    ]

cardsearch_modify_menu_actions = [
      action_set_near
    , action_set_middle
    , action_set_dist
    , action_retitle
    , action_archive
    , action_delete
]

newcard_main_actions = [
      action_open
    , action_modify
    , action_schedule
]


start_over_menu = [f"  [X] {action_start_over}"]
hotkey_start_over_dict = {"X": f"{action_start_over}"}

exit_menu = [f"  [X] {action_exit_menu}"]
hotkey_exit_dict = {"X": f"{action_exit_menu}"}

cancel_menu = [f"  [X] {action_cancel}"]
hotkey_cancel_dict = {"X": f"{action_cancel}" }

quit_menu = [f"  [Q] {action_quit}"]
hotkey_quit_dict = {"Q": f"{action_quit}"}

display_hotkey_exit_menu = [f"  [X] {action_exit_menu}"]
display_hotkey_quit = [f"  [Q] {action_quit}"]


def prep_newcard_menu(var_menu, var_letters, pop_letters=False):
    if pop_letters:
        full_hotkey_set_dict = {f"{var_letters.pop(0)}":f"{match}" for match in var_menu}

    else:
        full_hotkey_set_dict = {f"{ltr}":f"{match}" for ltr, match in zip(letters_filtered, var_menu)}


    full_hotkey_set_list = [f"  [{letter}] {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_menu(var_menu):
    full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(letters_filtered, var_menu)}

    full_hotkey_set_list = [f"  [{letter}] {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_card_run_menu(actions_list):
    hotkey_dict = {}

    for letter, action in zip(letters_filtered, actions_list):
        hotkey_dict[letter] = action

    full_hotkey_set_dict = hotkey_dict

    full_hotkey_set_list = [f"  [{letter}] {action}" for letter, action in zip(
        full_hotkey_set_dict.keys(),
        full_hotkey_set_dict.values())]

    return full_hotkey_set_dict, full_hotkey_set_list


def prep_card_modify_menu(actions_list, card_filename):
    current_focus = l_formatters.get_card_focus(card_filename)

    hotkey_dict = {}

    if current_focus == "near":
        actions_list.remove(action_set_near)
    elif current_focus == "middle":
        actions_list.remove(action_set_middle)
    elif current_focus == "distant":
        actions_list.remove(action_set_dist)

    for letter, action in zip(letters_filtered, actions_list):
        hotkey_dict[letter] = action

    full_hotkey_set_dict = hotkey_dict

    full_hotkey_set_list = [f"  [{letter}] {action}" for letter, action in zip(
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

        if not l_formatters.test_for_float(response):
            print()
            print(f"  It's gotta be just a number")
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

    response = True

    while response not in l_files.negative_user_responses:
        l_animators.standard_interval_printer(var_hotkey_list, speed_interval=0)
        print()
        l_animators.standard_interval_printer(display_hotkey_exit_menu, speed_interval=0)

        response = input("\n  > ")

        if response.upper() in var_hotkey_dict.keys():

            if var_hotkey_dict[response.upper()] == action_set_near:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_formatters.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_near_folder, dst_name=selected_card)
                l_animators.animate_text("  Card set to ➝ Near Focus")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == action_set_middle:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_formatters.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_middle_folder, dst_name=selected_card)
                l_animators.animate_text("  Card set to ➝ Middle Focus")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == action_set_dist:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_formatters.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_dist_folder, dst_name=selected_card)
                l_animators.animate_text("  Card set to ➝ Distant Focus")
                return "CARD REFOCUSED", None

            elif var_hotkey_dict[response.upper()] == action_retitle:
                retitled_card_path = l_newcard.get_card_from_input()
                print()
                # l_animators.animate_text(f"  Card will been renamed from '{selected_card}' → '{retitled_card_path}'")
                l_formatters.card_renamer(curr_name=selected_card, dst_name=retitled_card_path)
                return None, retitled_card_path

            elif var_hotkey_dict[response.upper()] == action_archive:
                l_recurring.remove_recurring_data(json_filename=selected_card)
                l_formatters.card_renamer(curr_name=selected_card, dst_dir=l_files.archived_cards_folder, dst_name=selected_card)
                l_animators.animate_text("  Card Archived")
                return None, None

            elif var_hotkey_dict[response.upper()] == action_delete:
                l_formatters.card_deleter(selected_card)
                return "DELETED CARD", None

            elif var_hotkey_dict[response.upper()] == action_mark_delete:
                return "CARD MARKED FOR DELETION", None


        elif response.upper() in hotkey_exit_dict.keys():
            return None, None

        elif response in l_files.negative_user_responses:
            l_animators.animate_text("Returning to Main Menu")
            return None, None

        else:
            print()
            print("You entered something other than one letter.")
            print()