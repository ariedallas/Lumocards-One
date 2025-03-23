import argparse
import subprocess
import time
from typing import Dict

from LUMO_LIBRARY import (lumo_animationlibrary as l_animators,
                          lumo_cards_planner as l_cards,
                          lumo_checklist as l_checklist,
                          lumo_journal as l_journal,
                          lumo_menus_data as l_menus_data,
                          lumo_newcard_2 as l_newcard,
                          lumo_pomodoro as l_pomodoro,
                          lumo_search as l_search,
                          lumo_settings as l_settings,
                          lumo_timer as l_timer)


def get_argument_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)

    """many of the same "routes" are aliased to other names for redundancy and flexibility."""
    sub_parser = parser.add_subparsers(
        help=""
        , dest="route"
    )

    sub_parser.add_parser(
        "all"
        , help="Display the full Lumo menu of subprograms"
        , description="Display the full Lumo menu of subprograms"
    )
    sub_parser.add_parser(
        "calendar"
        , help="Display the calendar in Lumo."
        , description="The calendar can be used to schedule events and sync them to Google Calendar."
    )
    sub_parser.add_parser(
        "cardsrun"
        , help="Alternate shortcut name to run Lumocards."
        , description="Alternate shortcut to run Lumocards."
    )
    sub_parser.add_parser(
        "home"
        , help="Defaults to main menu when you type 'lumo' by itself."
        , description="Defaults to main meny when you type 'lumo' by itself."
    )
    sub_parser.add_parser(
        "checklist"
        , help="Cycle through a simple checklist for any regular routine."
        , description="Create a card and set it as a 'checklist' card to use this feature."
    )
    sub_parser.add_parser(
        "journal"
        , help="Opens a text editor to write in."
        , description="Creates a journal file with today's date and saves it to a 'JOURNAL' folder."
    )
    newcard = sub_parser.add_parser(
        "newcard"
        , help="Create a new card."
        , description="""New cards can be events or not depending on how you want to use them.
                           A card always has a category, a title, and a list of steps."""
    )
    newcard.add_argument("card_category", nargs="?")
    newcard.add_argument("card_title", nargs="*")

    sub_parser.add_parser(
        "planner"
        , help="Run Lumocards for today"
        , description="""Lumocards is an interactive tool to manage and plan your day,
                        and manage projects."""
    )
    pomodoro = sub_parser.add_parser(
        "pomodoro"
        , help="A timer with preplanned breaks"
        , description="Emulates a pomodoro (tomato) timer"
    )
    pomodoro.add_argument("minutes_focus", nargs="?")
    pomodoro.add_argument("minutes_break", nargs="?")

    search = sub_parser.add_parser(
        "search"
        , help="Search across everything in the Lumo program: cards, events, etc. "
        , description=""
    )
    search.add_argument("search_term", nargs="?")

    settings = sub_parser.add_parser(
        "settings"
        , help="Open the lumo settings."
        , description="Interactive settings program to adjust program features."
    )

    timer = sub_parser.add_parser(
        "timer"
        , help="A simple timer to use in various ways."
        , description="A simple timer feature."
    )
    timer.add_argument("minutes", nargs="?")

    return parser


class LumoMenu:
    def __init__(self, name: str, var_dict: Dict):
        self.name = name
        self.menu = var_dict


    def display_main(self):
        dict_length = len(self.menu)

        LumoMenu.clear()
        print()
        print("LUMOCARDS")
        print("\n")

        for idx, item in enumerate(self.menu.items()):
            if idx == dict_length - 1:
                print()

            k, v = item
            print(f"  [{k}]  {v}")


    def display_all(self):
        dict_length = len(self.menu)

        LumoMenu.clear()
        print()
        print("LUMOCARDS ::all:: ")
        print("\n")

        for idx, item in enumerate(self.menu.items()):
            if idx == 4:
                print()
            if idx == dict_length - 3:
                print()
            if idx == dict_length - 1:
                print()

            k, v = item
            print(f"  [{k}]  {v}")


    @staticmethod
    def clear():
        subprocess.run(["clear"], shell=True)


    @staticmethod
    def load_dots():
        print("\033[33;1m",end="")
        l_animators.animate_text(" ...", speed=.1, finish_delay=.3)
        print("\033[0m")


    @staticmethod
    def load_transition():
        LumoMenu.clear()
        print()
        LumoMenu.load_dots()


main_menu = LumoMenu("main", l_menus_data.LUMO_MAIN_MENU)
all_menu = LumoMenu("all", l_menus_data.LUMO_ALL_MENU)


def root_loop(parsed_args, unknown):
    status = None
    menu = main_menu

    _, from_cli = _determine_input_origin(parsed_args)

    if from_cli:
        status, menu = router(parsed_args, unknown, main_menu)

    while True:
        if status == "QUIT":
            break

        if status == "RELOOP":
            print()
            l_animators.animate_text("  unrecognized option", finish_delay=.5)

        LumoMenu.load_transition()
        if menu.name == "all":
            current_menu = all_menu
            all_menu.display_all()
        else:
            current_menu = main_menu
            main_menu.display_main()

        print()
        user_input = input("  > ")
        status, menu = router(user_input, [], current_menu)


def _determine_input_origin(user_input):
    if type(user_input) == argparse.Namespace:
        choice = user_input.route
        from_cli = True if choice not in {None, "home"} else False
    else:
        choice = user_input
        from_cli = False

    return choice, from_cli


def router(user_input, unknown, contextual_menu: LumoMenu):
    """TODO: refactor, if choice:
            then do func(choice), rather than so much logic in each elif..."""
    choice, from_cli = _determine_input_origin(user_input)
    key = choice.upper()
    value = contextual_menu.menu[key] if key in contextual_menu.menu.keys() else "_"

    if (choice.lower() in {"about"} or
            value in {":: about ::"}):

        LumoMenu.load_transition()
        print("LUMOCARDS")
        print()
        l_animators.list_printer(["This", "is", "the", "about", "section"])
        print()
        time.sleep(.5)
        return None, main_menu

    elif (choice.lower() in {"all", "more"} or
          value in {":: all | more ::"}):

        return None, all_menu

    elif (choice.lower() in {"checklist", "checklists"} or
          value in {"Checklist"}):

        LumoMenu.load_transition()
        l_checklist.main()
        return None, main_menu

    elif (choice.lower() in {"calendar"} or
          value in {"Calendar"}):

        from LUMO_LIBRARY import lumo_calendar_main as l_calendar

        LumoMenu.load_transition()
        l_calendar.main()
        return None, main_menu

    elif (choice.lower() in {"journal"} or
          value in {"Journal"}):

        LumoMenu.load_transition()
        l_journal.main()
        return None, main_menu

    elif (choice.lower() in {"new card", "newcard"} or
          value in {"New Card"}):

        if from_cli and (user_input.card_category and user_input.card_title):
            category, title = user_input.card_category, user_input.card_title
            LumoMenu.load_transition()
            l_newcard.main(category, title, from_lumo_menu=True)
        else:
            LumoMenu.load_transition()
            l_newcard.main(from_lumo_menu=True)

        return None, main_menu

    elif (choice.lower() in {"planner", "cards planner", "cards"} or
          value in {"Cards Planner"}):

        LumoMenu.load_transition()
        l_cards.main()
        return None, main_menu

    elif (choice.lower() in {"pomodoro"} or
          value in {"Pomodoro"}):

        if from_cli and (user_input.minutes_focus and user_input.minutes_break):
            LumoMenu.load_transition()
            l_pomodoro.main(user_input)
        else:
            LumoMenu.load_transition()
            l_pomodoro.main()

        return None, main_menu

    elif (choice.lower() in {"search", "find"} or
          value in {"Search"}):

        if from_cli and user_input.search_term:
            LumoMenu.load_transition()
            l_search.main(user_input.search_term)
        else:
            LumoMenu.load_transition()
            l_search.main()
        return None, main_menu

    elif (choice.lower() in {"settings"} or
          value in {":: settings ::"}):

        LumoMenu.load_transition()
        l_settings.main()
        return None, main_menu

    elif (choice.lower() in {"timer"} or
          value in {"Timer"}):

        if from_cli:
            LumoMenu.load_transition()
            l_timer.main(user_input.minutes)
        else:
            LumoMenu.load_transition()
            l_timer.main()

        return None, main_menu

    elif (choice.lower() in {"quit", "exit"} or
          value in {"Quit"}):

        return "QUIT", None

    else:
        return "RELOOP", contextual_menu


def main():
    global parser
    parser = get_argument_parser()

    try:
        parsed, unknown = parser.parse_known_args()
    except:
        parsed, unknown = parser.parse_known_args(["home"])

    root_loop(parsed, unknown)


if __name__ == "__main__":
    main()
