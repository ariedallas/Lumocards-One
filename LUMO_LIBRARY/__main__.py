import argparse
import subprocess
import time

from LUMO_LIBRARY import (
    lumo_animationlibrary as l_animators,
    lumo_journal as l_journal,
    lumo_newcard_refactor as l_newcard,
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
    sub_parser.add_parser(
        "pomodoro"
        , help="A simple timer to use in various ways."
        , description="A simple timer feature."
    )

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

    sub_parser.add_parser(
        "timer"
        , help="A simple timer to use in various ways."
        , description="A simple timer feature."
    )

    return parser


HOME_MENU = {
    "A": "Planner"
    , "B": "New Card"
    , "C": "Calendar"
    , "D": "Journal"
    , "E": ":: more ::"
    , "F": ":: settings::"
}

SUB_MENU = {
    "A": "Timer"
    , "B": "Search Cards"
}

def clear():
    subprocess.run(["clear"], shell=True)

def load_dots():
    l_animators.animate_text(" ...", speed=.1, finish_delay=.2)

def load_transition():
    clear()
    load_dots()
    print()

def display_home(var_dict):
    clear()
    print()
    print("LUMOCARDS")
    print("\n")

    for k, v in var_dict.items():
        print(f"  [{k}]  {v}")

    print()
    print(f"  [Q]  Quit")


def display_submenu(var_dict):
    clear()
    menu_equalize = len(HOME_MENU) - len(SUB_MENU)

    print()
    print("LUMOCARDS ::MORE:: ")
    print("\n")

    for k, v in var_dict.items():
        print(f"  [{k}]  {v}")
    print()
    print(f"  [X]  Back / Exit")

    for _ in range(menu_equalize):
        print()


def root_loop(parsed_args, unknown):
    status = None
    # print(parsed_args, unknown)

    if parsed_args.route == "home" or not parsed_args.route:
        while True:
            if status == "QUIT":
                break

            display_home(HOME_MENU)

            if status == "RELOOP":
                l_animators.animate_text("  unrecognized option")

            print()
            response = input("  > ")
            status = router(response, [])

    else:
        router(parsed_args, unknown)


def submenu_loop():
    status = None

    while True:
        display_submenu(SUB_MENU)

        if status == "RELOOP":
            l_animators.animate_text("  unrecognized option")

        if status == "EXIT":
            break

        print()
        response = input("  > ")
        status = sub_router(response)


def _determine_input_origin(user_input):
    if type(user_input) == argparse.Namespace:
        choice = user_input.route.lower()
        origin = "CLI PARSED"
    else:
        choice = user_input.lower()
        origin = "HOME MENU"

    return choice, origin


def router(user_input, unknown):
    """TODO: refactor, if choice:
            then do func(choice), rather than so much logic in each elif..."""
    choice, origin = _determine_input_origin(user_input)

    if choice in ["a", "planner"]:
        print("planner")
        time.sleep(2)
        root_loop(parser.parse_args(["home"]), [])

    elif choice in ["b", "new card", "newcard"]:
        if origin == "CLI PARSED" and (user_input.card_category and user_input.card_title):
            category, title = user_input.card_category, user_input.card_title
            load_transition()
            l_newcard.main(category, title, from_lumo_menu=True)
        else:
            load_transition()
            l_newcard.main(from_lumo_menu=True)

        root_loop(parser.parse_args(["home"]), [])

    elif choice in ["c", "calendar"]:
        # from LUMO_LIBRARY import lumo_calendar_main
        #
        # lumo_calendar_main.main()
        print("calendar")
        time.sleep(2)
        root_loop(parser.parse_args(["home"]), [])

    elif choice in ["d", "journal"]:
        l_journal.main()
        root_loop(parser.parse_args(["home"]), [])

    elif choice in ["e", "more"]:
        submenu_loop()

    elif choice in ["f", "settings"]:
        load_transition()
        l_settings.main()
        root_loop(parser.parse_args(["home"]), [])

    elif choice in ["timer", "pomodoro"]:
        print("timer")
        time.sleep(2)
        root_loop(parser.parse_args(["home"]), [])

    elif choice == "search":
        if origin == "CLI PARSED" and user_input.search_term:
            load_transition()
            l_search.main(user_input.search_term)
        else:
            load_transition()
            l_search.main()
        root_loop(parser.parse_args(["home"]), [])

    elif choice in ["q", "quit"]:
        return "QUIT"

    else:
        return "RELOOP"


def sub_router(option):
    if option.lower() in ["a", "timer"]:
        # lumo_pomodoro.main()
        time.sleep(2)
        print("timer")
        root_loop(parser.parse_args(["home"]), [])

    elif option.lower() in ["b", "search", "search cards"]:
        l_search.main()
        root_loop(parser.parse_args(["home"]), [])

    elif option.lower() in ["x", "exit", "back"]:
        return "EXIT"

    else:
        return "RELOOP"


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

# ---- ETC./UNUSED ---- #
    # parser.add_argument(
    #     "entry"
    #     , nargs="?"
    #     , action="store"
    #     , default="menu"
    #     , type=str
    #     , help=""
    # )
    # lumo add dinner with john @ today @ 2:00p - 3:00p @ my house


# def safe_parse(parser):
#     try:
#         parsed_args, unknown = parser.parse_known_args()
#         return parsed_args, unknown
#     except argparse.ArgumentError:
#         parsed_args, unknown = parser.parse_known_args(["home"])
#         return parsed_args, unknown
