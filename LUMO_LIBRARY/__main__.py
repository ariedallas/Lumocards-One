import argparse
import subprocess
import time

from typing import (Optional,
                    OrderedDict)

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

parser: argparse.ArgumentParser


def get_argument_parser() -> argparse.ArgumentParser:
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
    def __init__(self, name: str, var_dict: OrderedDict[str, str]) -> None:
        self.name = name
        self.menu = var_dict


    def display_main(self) -> None:
        dict_length = len(self.menu)

        LumoMenu.clear()
        print()
        print("LUMOCARDS")
        print("\n")

        for idx, item in enumerate(self.menu.items()):
            if idx == dict_length - 1:
                print()

            k: str
            v: str

            k, v = item
            print(f"  [{k}]  {v}")


    def display_all(self) -> None:
        dict_length = len(self.menu)

        LumoMenu.clear()
        print()
        print("LUMOCARDS ::all:: ")
        print("\n")

        for idx, item in enumerate(self.menu.items()):
            if idx == 3:
                print()
            if idx == dict_length - 3:
                print()
            if idx == dict_length - 1:
                print()

            k: str
            v: str

            k, v = item
            print(f"  [{k}]  {v}")


    @staticmethod
    def clear() -> None:
        subprocess.run(["clear"], shell=True)


    @staticmethod
    def load_dots() -> None:
        print("\033[33;1m", end="")
        l_animators.animate_text(" ...", speed=.1)
        print("\033[0m", end="")


    @staticmethod
    def load_transition() -> None:
        LumoMenu.clear()
        print()
        LumoMenu.load_dots()


main_menu = LumoMenu("main", l_menus_data.LUMO_MAIN_MENU)
all_menu = LumoMenu("all", l_menus_data.LUMO_ALL_MENU)


def _determine_from_cli(orig_input: Optional[argparse.Namespace]) -> bool:
    if not orig_input:
        return False

    choice = orig_input.route
    from_cli = True if choice not in {None, "home"} else False

    return from_cli


def root_loop(cli_parsed_args: argparse.Namespace, unknown: list[str]) -> None:
    menu: LumoMenu
    status: Optional[str]

    menu = main_menu
    status = None

    from_cli: bool
    from_cli = _determine_from_cli(cli_parsed_args)

    # The user either launches a sub_program, i.e. 'cards planner' from the command line
    # or they are put in the home menu loop which links to all sub-programs
    # and can parse lumo_input from there
    if from_cli:
        status, menu = router(cli_input=cli_parsed_args,
                              unknown_args=unknown,
                              lumo_input="_",
                              contextual_menu=main_menu)

    while True:
        if status == "QUIT":
            break

        if status == "RELOOP":
            print()
            l_animators.animate_text_indented("unrecognized option", indent=2, finish_delay=1)

        if status == "LUMO DUPLICATE":
            print()
            l_animators.animate_text_indented("Try typing the keyword without 'lumo' first or use a shortcut letter.", indent=2, finish_delay=1)

        LumoMenu.load_transition()
        if menu.name == "all":
            current_menu = all_menu
            all_menu.display_all()
        else:
            current_menu = main_menu
            main_menu.display_main()

        print()

        user_input: str
        user_input = input("  > ")
        status, menu = router(cli_input=None,
                              unknown_args=[],
                              lumo_input=user_input,
                              contextual_menu=current_menu)


def router(cli_input: Optional[argparse.Namespace],
           unknown_args: list[str],
           lumo_input: str,
           contextual_menu: LumoMenu) -> tuple[Optional[str], LumoMenu]:
    selected_prog: str
    from_cli: bool
    from_cli = _determine_from_cli(cli_input)

    if not from_cli:
        key = lumo_input.upper()
        selected_prog_dict_value = contextual_menu.menu.get(key, "_")

        selected_prog = lumo_input
        cli_prog = "_"


    else:  # from_cli and cli_input is not None
        cli_prog = cli_input.route
        selected_prog = "_"
        selected_prog_dict_value = "_"

    if (selected_prog.lower() in {"about"} or
            cli_prog.lower() in {"about"} or
            selected_prog_dict_value in {":: about ::"}):

        LumoMenu.load_transition()
        print("LUMOCARDS")
        print()
        l_animators.list_printer(["This", "is", "the", "about", "section"])
        print()
        time.sleep(.5)
        return None, main_menu

    elif (selected_prog.lower() in {"all", "more"} or
          cli_prog.lower() in {"all"} or
          selected_prog_dict_value in {":: all | more ::"}):

        return None, all_menu

    elif (selected_prog.lower() in {"calendar"} or
          cli_prog.lower() in {"calendar"} or
          selected_prog_dict_value in {"Calendar"}):

        from LUMO_LIBRARY import lumo_calendar_main as l_calendar

        LumoMenu.load_transition()
        l_calendar.main()
        return None, main_menu

    elif (selected_prog.lower() in {"checklist", "checklists"} or
          cli_prog.lower() in {"checklist"} or
          selected_prog_dict_value in {"Checklist"}):

        LumoMenu.load_transition()
        l_checklist.main()
        return None, main_menu


    elif (selected_prog.lower() in {"journal"} or
          cli_prog.lower() in {"journal"} or
          selected_prog_dict_value in {"Journal"}):

        LumoMenu.load_transition()
        l_journal.main()
        return None, main_menu

    elif (selected_prog.lower() in {"lumo"}):
        return "LUMO DUPLICATE", contextual_menu

    elif (selected_prog.lower() in {"new card", "newcard"} or
          cli_prog.lower() in {"newcard"} or
          selected_prog_dict_value in {"New Card"}):

        if from_cli and (cli_input.card_category and cli_input.card_title):
            category, title = cli_input.card_category, cli_input.card_title
            LumoMenu.load_transition()
            l_newcard.main(category, title, from_lumo_menu=True)
        else:
            LumoMenu.load_transition()
            l_newcard.main(from_lumo_menu=True)

        return None, main_menu

    elif (selected_prog.lower() in {"planner", "cards planner", "cards"} or
          cli_prog.lower() in {"planner"} or
          selected_prog_dict_value in {"Cards Planner"}):

        LumoMenu.load_transition()
        l_cards.main()
        return None, main_menu

    elif (selected_prog.lower() in {"pomodoro"} or
          cli_prog.lower() in {"pomodoro"} or
          selected_prog_dict_value in {"Pomodoro"}):

        if from_cli and (cli_input.minutes_focus and cli_input.minutes_break):
            LumoMenu.load_transition()
            l_pomodoro.main(cli_input)
        else:
            LumoMenu.load_transition()
            l_pomodoro.main()

        return None, main_menu

    elif (selected_prog.lower() in {"search", "find"} or
          cli_prog.lower() in {"search"} or
          selected_prog_dict_value in {"Search"}):

        if from_cli and cli_input.search_term:
            LumoMenu.load_transition()
            l_search.main(cli_input.search_term)
        else:
            LumoMenu.load_transition()
            l_search.main()
        return None, main_menu

    elif (selected_prog.lower() in {"settings"} or
          cli_prog.lower() in {"settings"} or
          selected_prog_dict_value in {":: settings ::"}):

        LumoMenu.load_transition()
        l_settings.main()
        return None, main_menu

    elif (selected_prog.lower() in {"timer"} or
          cli_prog.lower() in {"timer"} or
          selected_prog_dict_value in {"Timer"}):

        if from_cli:
            LumoMenu.load_transition()
            l_timer.main(cli_input.minutes)
        else:
            LumoMenu.load_transition()
            l_timer.main()

        return None, main_menu

    # No need to have a cli_prog.lower() in {"quit"}
    # we only quit from inside the program
    elif (selected_prog.lower() in {"quit", "exit"} or
          selected_prog_dict_value in {"Quit"}):

        return "QUIT", contextual_menu

    else:
        return "RELOOP", contextual_menu


def main() -> None:
    global parser

    parser = get_argument_parser()

    try:
        parsed, unknown = parser.parse_known_args()
    except:
        parsed, unknown = parser.parse_known_args(["home"])

    root_loop(parsed, unknown)


if __name__ == "__main__":
    main()
