import string

LETTERS_CAPS = string.ascii_uppercase
LETTERS_FILTERED = [L for L in LETTERS_CAPS if not (L == 'Q') and not (L == 'X')]

ACTION_OPEN = "Open/Edit card in text editor"
ACTION_MODIFY = "Refocus, Rename, Archive, or Delete"
ACTION_SCHEDULE = "Schedule to ➝ Calendar"
ACTION_SET_RECURRING = "Set as ➝ Recurring Card"
ACTION_SET_RECURRING_2 = "Set/Update ➝ Recurring Card"
ACTION_SET_CHECKLIST = "Set as ➝ Checklist Card"

ACTION_SET_NEAR = "Set as ➝ Near Focus"
ACTION_SET_MIDDLE = "Set as ➝ Middle Focus"
ACTION_SET_DIST = "Set as ➝ Distant Focus"

ACTION_ARCHIVE = "Move card to Archives"
ACTION_DELETE = "Delete card"
ACTION_MARK_DELETE = "Mark card for deletion"
ACTION_NEW_SEARCH = "New search"
ACTION_RENAME = "Rename card"
ACTION_RENAME_2 = "Retitle + Change Category card"

ACTION_EXIT_MENU = "Exit Menu"
ACTION_SIMPLE_EXIT = "Exit"
ACTION_START_OVER = "Start Over"
ACTION_CANCEL = "Cancel"
ACTION_QUIT = "Quit"

FOCUS_MENU = [
    ACTION_SET_NEAR
    , ACTION_SET_MIDDLE
    , ACTION_SET_DIST
]

SCHEDULE_MENU = [
    ACTION_SCHEDULE
    , ACTION_SET_RECURRING
    , ACTION_SET_CHECKLIST
]

RECURRING_MENU = [
    "Day(s)"
    , "Week(s)"
    , "Month(s)"
]

CARDS_PLANNER_MACRO_MENU = [
    ACTION_OPEN
    , ACTION_MODIFY
    , ACTION_SCHEDULE
    , ACTION_SET_RECURRING_2
]

CARDS_PLANNER_MODIFY_MENU = [
    ACTION_SET_NEAR
    , ACTION_SET_MIDDLE
    , ACTION_SET_DIST
    , ACTION_RENAME
    , ACTION_ARCHIVE
    , ACTION_MARK_DELETE
]

SEARCH_MAIN_MENU = [
    ACTION_OPEN
    , ACTION_MODIFY
    , ACTION_SCHEDULE
    , ACTION_SET_RECURRING_2
]

SEARCH_MODIFY_MENU = [
    ACTION_SET_NEAR
    , ACTION_SET_MIDDLE
    , ACTION_SET_DIST
    , ACTION_RENAME
    , ACTION_ARCHIVE
    , ACTION_DELETE
]

NEWCARD_MAIN_MENU = [
    ACTION_OPEN
    , ACTION_MODIFY
    , ACTION_SCHEDULE
]

START_OVER_MENU_LIST = [f"  [X]  {ACTION_START_OVER}"]
START_OVER_MENU_DICT = {"X": f"{ACTION_START_OVER}"}

EXIT_MENU_LIST = [f"  [X]  {ACTION_EXIT_MENU}"]
EXIT_MENU_DICT = {"X": f"{ACTION_EXIT_MENU}"}

SIMPLE_EXIT_LIST = [f"  [X]  {ACTION_SIMPLE_EXIT}"]
SIMPLE_EXIT_DICT = {"X": f"{ACTION_SIMPLE_EXIT}"}

CANCEL_MENU_LIST = [f"  [X]  {ACTION_CANCEL}"]
CANCEL_MENU_DICT = {"X": f"{ACTION_CANCEL}"}

QUIT_MENU_LIST = [f"  [Q]  {ACTION_QUIT}"]
QUIT_MENU_DICT = {"Q": f"{ACTION_QUIT}"}

CARDS_PLANNER_COMPLETED_PHRASES = [
    "Nice!"
    , "Excellent!"
    , "Marked as complete."
    , "Cool!"
    , "Card was moved to archived cards."
]

CARDS_PLANNER_FEEDBACK = {
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

# ---- RESPONSES ---- #
NEGATIVE_USER_RESPONSES = [
    "no"
    , "exit"
    , "quit"
    , "stop"
    , "cancel"
]

# def prep_newcard_menu(var_menu, var_letters, pop_letters=False):
#     if pop_letters:
#         full_hotkey_set_dict = {f"{var_letters.pop(0)}": f"{match}" for match in var_menu}
#
#     else:
#         full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(LETTERS_FILTERED, var_menu)}
#
#     full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
#         full_hotkey_set_dict.keys(),
#         full_hotkey_set_dict.values())]
#
#     return full_hotkey_set_dict, full_hotkey_set_list
#
#
# def prep_menu(var_menu):
#     full_hotkey_set_dict = {f"{ltr}": f"{match}" for ltr, match in zip(LETTERS_FILTERED, var_menu)}
#
#     full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
#         full_hotkey_set_dict.keys(),
#         full_hotkey_set_dict.values())]
#
#     return full_hotkey_set_dict, full_hotkey_set_list
#
#
# def prep_card_run_menu(actions_list):
#     hotkey_dict = {}
#
#     for letter, action in zip(LETTERS_FILTERED, actions_list):
#         hotkey_dict[letter] = action
#
#     full_hotkey_set_dict = hotkey_dict
#
#     full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
#         full_hotkey_set_dict.keys(),
#         full_hotkey_set_dict.values())]
#
#     return full_hotkey_set_dict, full_hotkey_set_list
#
#
# def prep_card_modify_menu(actions_list, card_filename):
#     current_focus = l_card_utils.get_card_focus(card_filename)
#
#     hotkey_dict = {}
#
#     if current_focus == "near":
#         actions_list.remove(ACTION_SET_NEAR)
#     elif current_focus == "middle":
#         actions_list.remove(ACTION_SET_MIDDLE)
#     elif current_focus == "distant":
#         actions_list.remove(ACTION_SET_DIST)
#
#     for letter, action in zip(LETTERS_FILTERED, actions_list):
#         hotkey_dict[letter] = action
#
#     full_hotkey_set_dict = hotkey_dict
#
#     full_hotkey_set_list = [f"  [{letter}]  {action}" for letter, action in zip(
#         full_hotkey_set_dict.keys(),
#         full_hotkey_set_dict.values())]
#
#     return full_hotkey_set_list, full_hotkey_set_dict
#
#
# def proceed(input_text="... "):
#     user_input = input(f"{input_text} ")
#     return True if user_input not in NEGATIVE_USER_RESPONSES else False
#
#
# def menu_recurrence_settings(var_menu):
#     recurrence_settings = None
#
#     while not recurrence_settings:
#         print()
#         response = input("  Should this recur in days, weeks, or months? > ")
#         if response.upper() not in var_menu.keys():
#             avlbl = list(var_menu.keys())
#             print(f"  Available letters are '{avlbl[0]}' '{avlbl[1]}' and '{avlbl[2]}' (upper or lower case)")
#             continue
#
#         units = var_menu[response.upper()]
#         response = input(f"  Select a number of {units}? e.g. '2' > ")
#
#         if not l_card_utils.test_for_float(response):
#             print()
#             print(f"  Please use whole numbers only (no decimals)")
#             continue
#         else:
#             amt = float(response)
#             units = units.replace("(s)", "")
#
#         recurrence_settings = (units, amt)
#         return recurrence_settings
#
#
# def menu_modify_card(selected_card, var_hotkey_list, var_hotkey_dict):
#     print()
#     l_animators.animate_text("MODIFYING CARD")
#     print()
#
#     while True:
#         l_animators.standard_interval_printer(var_hotkey_list, speed_interval=0)
#         print()
#         l_animators.standard_interval_printer(EXIT_MENU_LIST, speed_interval=0)
#
#         response = input("\n  > ")
#
#         if response.upper() in var_hotkey_dict.keys():
#
#             if var_hotkey_dict[response.upper()] == ACTION_SET_NEAR:
#                 l_recurring.remove_recurring_data(json_filename=selected_card)
#                 l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_near_folder,
#                                           dst_name=selected_card)
#                 l_animators.animate_text("  Card set to ➝ Near Focus")
#                 return "CARD REFOCUSED", None
#
#             elif var_hotkey_dict[response.upper()] == ACTION_SET_MIDDLE:
#                 l_recurring.remove_recurring_data(json_filename=selected_card)
#                 l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_middle_folder,
#                                           dst_name=selected_card)
#                 l_animators.animate_text("  Card set to ➝ Middle Focus")
#                 return "CARD REFOCUSED", None
#
#             elif var_hotkey_dict[response.upper()] == ACTION_SET_DIST:
#                 l_recurring.remove_recurring_data(json_filename=selected_card)
#                 l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.cards_dist_folder,
#                                           dst_name=selected_card)
#                 l_animators.animate_text("  Card set to ➝ Distant Focus")
#                 return "CARD REFOCUSED", None
#
#             elif var_hotkey_dict[response.upper()] == ACTION_RENAME:
#                 retitled_card_path = l_newcard.get_card_from_input()
#                 print()
#                 # l_animators.animate_text(f"  Card will been renamed from '{selected_card}' → '{retitled_card_path}'")
#                 l_card_utils.card_renamer(curr_name=selected_card, dst_name=retitled_card_path)
#                 return None, retitled_card_path
#
#             elif var_hotkey_dict[response.upper()] == ACTION_ARCHIVE:
#                 l_recurring.remove_recurring_data(json_filename=selected_card)
#                 l_card_utils.card_renamer(curr_name=selected_card, dst_dir=l_files.archived_cards_folder,
#                                           dst_name=selected_card)
#                 l_animators.animate_text("  Card Archived")
#                 return None, None
#
#             elif var_hotkey_dict[response.upper()] == ACTION_DELETE:
#                 l_card_utils.card_deleter(selected_card)
#                 return "DELETED CARD", None
#
#             elif var_hotkey_dict[response.upper()] == ACTION_MARK_DELETE:
#                 return "CARD MARKED FOR DELETION", None
#
#
#         elif response.upper() in EXIT_MENU_DICT.keys():
#             return None, None
#
#         elif response in NEGATIVE_USER_RESPONSES:
#             l_animators.animate_text("Returning to Main Menu")
#             return None, None
#
#         else:
#             print()
#             print("You entered something other than one letter.")
#             print()
