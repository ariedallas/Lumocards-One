import collections
import pprint
import string

LETTERS_CAPS = string.ascii_uppercase
LETTERS_FILTERED = [L for L in LETTERS_CAPS if not (L == 'Q') and not (L == 'X')]

INTEGERS_10 = list(range(1, 11))
Z_CATEGORY_DICT = {"Z":  "Default Category"}

ACTION_OPEN = "Open/Edit card in text editor"
ACTION_MODIFY = "Refocus, Rename, Archive, or Delete"
ACTION_SCHEDULE = "Schedule to ➝ Calendar"
ACTION_SET_RECURRING = "Set as ➝ Recurring Card"
ACTION_SET_RECURRING_2 = "Set/Update ➝ Recurring Card"
ACTION_SET_CHECKLIST = "Set as ➝ Checklist Card"

ACTION_SET_NEAR = "Set as ➝ Near Focus"
ACTION_SET_MIDDLE = "Set as ➝ Middle Focus"
ACTION_SET_DIST = "Set as ➝ Distant Focus"

ACTION_ARCHIVE = "Move card to archives"
ACTION_DELETE = "Delete card"
ACTION_MARK_DELETE = "Mark card for deletion"
ACTION_NEW_SEARCH = "New search"
ACTION_RENAME = "Rename card"
ACTION_RENAME_2 = "Retitle + Change Category card"

ACTION_EXIT_MENU = "Exit Menu"
ACTION_EXIT_NO_SAVE = "Exit without saving"
ACTION_SAVE_WITH_EXIT = "Save and exit"
ACTION_SIMPLE_EXIT = "Exit"
ACTION_START_OVER = "Start Over"
ACTION_CANCEL = "Cancel"
ACTION_QUIT = "Quit"

ACTION_NEW_CATEGORY = "New: create new card category"
ACTION_UPDATE_CATEGORY = "Update: this card category"
ACTION_DELETE_CATEGORY = "Delete: a card category"
ACTION_DELETE_THIS_CATEGORY = "Delete: this card category"

LUMO_MAIN = [
    "Cards Planner"
    , "New Card"
    , "Calendar"
    , "Journal"
    , ":: all | more ::"
    , ":: settings ::"
]

LUMO_ALL = [
    "Cards Planner"
    , "New Card"
    , "Calendar"
    , "Journal"
    , "Search"
    , "Checklist"
    , "Timer"
    , "Pomodoro"
    , ":: settings ::"
    , ":: about ::"
]
# ---- LUMO MAIN MENU ---- #
LUMO_MAIN_MENU = collections.OrderedDict([])
LUMO_ALL_MENU = collections.OrderedDict([])

for ltr, item in zip(LETTERS_FILTERED, LUMO_MAIN):
    LUMO_MAIN_MENU.update({ltr: item})

for ltr, item in zip(LETTERS_FILTERED, LUMO_ALL):
    LUMO_ALL_MENU.update({ltr: item})

LUMO_MAIN_MENU.update({"Q": "Quit"})
LUMO_ALL_MENU.update({"Q": "Quit"})

# ---- ALL OTHER MENUS ---- #
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

SETTINGS_CARD_MANAGER = [
    ACTION_NEW_CATEGORY
    , ACTION_DELETE_CATEGORY
]

SETTINGS_CARD_MANAGER_SINGLE = [
    ACTION_UPDATE_CATEGORY
    , ACTION_DELETE_THIS_CATEGORY
]

START_OVER_MENU_LIST = [f"[X]  {ACTION_START_OVER}"]
START_OVER_MENU_DICT = {"X": f"{ACTION_START_OVER}"}

EXIT_MENU_LIST = [f"[X]  {ACTION_EXIT_MENU}"]
EXIT_MENU_DICT = {"X": f"{ACTION_EXIT_MENU}"}

EXIT_NOSAVE_LIST = [f"[X]  {ACTION_EXIT_NO_SAVE}"]
EXIT_NOSAVE_DICT = {"X": f"{ACTION_EXIT_NO_SAVE}"}

SIMPLE_EXIT_LIST = [f"[X]  {ACTION_SIMPLE_EXIT}"]
SIMPLE_EXIT_DICT = {"X": f"{ACTION_SIMPLE_EXIT}"}

CANCEL_MENU_LIST = [f"[X]  {ACTION_CANCEL}"]
CANCEL_MENU_DICT = {"X": f"{ACTION_CANCEL}"}

SAVE_LIST = [f"[S]  {ACTION_SAVE_WITH_EXIT}"]
SAVE_DICT = {"S": f"{ACTION_SAVE_WITH_EXIT}"}

QUIT_MENU_LIST = [f"[Q]  {ACTION_QUIT}"]
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

NEGATIVE_USER_RESPONSES = [
    "n"
    , "no"
    , "exit"
    , "x"
    , "quit"
    , "q"
    , "stop"
    , "cancel"
]
