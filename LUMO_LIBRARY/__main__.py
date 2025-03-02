import argparse
import collections
import subprocess
from typing import Dict

from LUMO_LIBRARY import (
    lumo_animationlibrary as l_animators,
    lumo_cardsrun as l_cards,
    lumo_journal as l_journal,
    lumo_newcard_refactor as l_newcard,
    lumo_pomodoro as l_pomodoro,
    lumo_search_cards as l_search,
    lumo_settings as l_settings
)


def get_argument_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)

    """many of the same "routes" are aliased to other names for redundancy and flexibility"""
    sub_parser = parser.add_subparsers(
        help=""
        , dest="route"
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
        , help="Defaults to main menu when you type 'lumo' by itself"
        , description="Defaults to main meny when you type 'lumo' by itself"
    )
    sub_parser.add_parser(
        "journal"
        , help="Opens a text editor to write in"
        , description="Creates a journal file with today's date and saves it to a 'JOURNAL' folder"
    )
    newcard = sub_parser.add_parser(
        "newcard"
        , help="Create a new card"
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
        , help="A simple timer to use in various ways."
        , description="A simple timer feature."
    )
    pomodoro.add_argument("minutes", nargs="?")

    search = sub_parser.add_parser(
        "search"
        , help="Search across everything in the Lumo program: cards, events, etc. "
        , description=""
    )
    search.add_argument("search_term", nargs="?")

    settings = sub_parser.add_parser(
        "settings"
        , help="Open the lumo settings"
        , description="Interactive settings program to adjust program features"
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

        clear()
        print()
        print("LUMOCARDS")
        print("\n")

        for idx, item in enumerate(self.menu.items()):
            if idx == dict_length - 1:
                print()

            k, v = item
            print(f"  [{k.upper()}]  {v}")


    def display_all(self):
        dict_length = len(self.menu)

        clear()

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
            print(f"  [{k.upper()}]  {v}")


MAIN_MENU = collections.OrderedDict([
    ("a", "Planner")
    , ("b", "New Card")
    , ("c", "Calendar")
    , ("d", "Journal")
    , ("e", ":: all | more ::")
    , ("f", ":: settings ::")
    , ("q", "Quit")
])

ALL_MENU = collections.OrderedDict([
    ("a", "Planner")
    , ("b", "New Card")
    , ("c", "Calendar")
    , ("d", "Journal")
    , ("e", "Search")
    , ("f", "Timer")
    , ("g", ":: settings ::")
    , ("h", ":: about ::")
    , ("q", "Quit")
])


def clear():
    subprocess.run(["clear"], shell=True)


def load_dots():
    l_animators.animate_text(" ...", speed=.1, finish_delay=.2)


def load_transition():
    clear()
    load_dots()
    print()


main_menu = LumoMenu("main", MAIN_MENU)
all_menu = LumoMenu("all", ALL_MENU)


def root_loop(parsed_args, unknown):
    status = None
    menu = main_menu

    _, from_cli = _determine_input_origin(parsed_args)

    if from_cli:
        router(parsed_args, unknown, main_menu)

    while True:
        if status == "QUIT":
            break

        if menu.name == "all":
            current_menu = all_menu
            all_menu.display_all()
        else:
            current_menu = main_menu
            main_menu.display_main()

        if status == "RELOOP":
            l_animators.animate_text("  unrecognized option")

        print()
        response = input("  > ")
        status, menu = router(response, [], current_menu)


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
    key = choice.lower()
    value = contextual_menu.menu[key] if key in contextual_menu.menu.keys() else "_"

    if (choice.lower() in {"planner", "agenda"} or
            value.lower() in {"planner", "agenda"}):

        load_transition()
        l_cards.main()
        return None, main_menu

    elif (choice.lower() in {"new card", "newcard"} or
          value.lower() in {"new card", "newcard"}):

        if from_cli and (user_input.card_category and user_input.card_title):
            category, title = user_input.card_category, user_input.card_title
            load_transition()
            l_newcard.main(category, title, from_lumo_menu=True)
        else:
            load_transition()
            l_newcard.main(from_lumo_menu=True)

        return None, main_menu

    elif (choice.lower() in {"calendar"} or
          value.lower() in {"calendar"}):

        from LUMO_LIBRARY import lumo_calendar_main

        load_transition()
        lumo_calendar_main.main()
        return None, main_menu

    elif (choice.lower() in {"journal"} or
          value.lower() in {"journal"}):

        l_journal.main()
        return None, main_menu

    elif (choice.lower() in {"all", "more"} or
          value.lower() in {":: all | more ::"}):

        load_transition()
        return None, all_menu

    elif (choice.lower() in {"settings"} or
          value.lower() in {":: settings ::"}):

        load_transition()
        l_settings.main()
        return None, main_menu

    elif (choice.lower() in {"pomodoro", "timer"} or
          value.lower() in {"pomodoro", "timer"}):

        if from_cli:
            load_transition()
            l_pomodoro.main(user_input.minutes)
        else:
            load_transition()
            l_pomodoro.main()

        return None, main_menu

    elif (choice.lower() in {"search", "find"} or
          value.lower() in {"search", "find"}):

        if from_cli and user_input.search_term:
            load_transition()
            l_search.main(user_input.search_term)
        else:
            load_transition()
            l_search.main()
        return None, main_menu

    elif (choice.lower() in {"quit", "exit"} or
          value.lower() in {"quit", "exit"}):

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
