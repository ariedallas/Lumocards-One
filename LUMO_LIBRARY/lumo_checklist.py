import os
import subprocess

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus_data as l_menus_data


def cycler(list_of_steps):
    for item in list_of_steps:
        if item != "\n" and item != "" and item:
            input(f"  {item} ?  ")
        else:
            print()


def display_menu(var_menu):
    exit_and_quit = l_menus_data.SIMPLE_EXIT_LIST + l_menus_data.QUIT_MENU_LIST

    l_animators.list_printer(var_menu, indent_amt=2, speed_interval=0)
    print()
    l_animators.list_printer(exit_and_quit, indent_amt=2, speed_interval=0)


def card_select(var_dict):
    lookup = input("\n  > ")

    # TODO: change this to a dict lookup
    if lookup.lower() in {"q", "x"}:
        return (None, None, "EXIT") if lookup.lower() == "x" else (None, None, "QUIT")

    # Note that var_dict.keys() are capitals; they are created from the base string.ascii_uppercase
    # this is a style choice which could later be a feature in settings to toggle upper/lower case
    elif lookup.upper() in var_dict.keys():
        selected = var_dict[lookup.upper()]
        card_title = l_card_utils.format_card_title(selected[0])
        card_steps = selected[1]

        return card_title, card_steps, None

    else:
        return None, None, None


def display_selected_checklist(card_title, card_steps):
    print()
    l_animators.animate_text(card_title)
    print()
    cycler(card_steps)


def program_header():
    print()
    print("CHECKLIST(S)")
    print()


def main():
    checklist_cards = sorted([card for card in os.listdir(l_files.checklist_cards_folder)])
    fetched = [l_card_utils.filename_to_card(file) for file in checklist_cards]
    fetched_titles = [l_card_utils.format_card_title(card[0]) for card in fetched]
    formatted_results_dict = {f"{ltr}": card for ltr, card in zip(l_menus_data.LETTERS_FILTERED, fetched)}
    formatted_results_menu = [f"[{ltr.upper()}]  {card_title}"
                              for ltr, card_title in zip(l_menus_data.LETTERS_FILTERED, fetched_titles)]

    while True:
        program_header()
        display_menu(formatted_results_menu)
        title, steps, status = card_select(formatted_results_dict)
        if title and steps:
            break
        elif status == "EXIT" or status == "QUIT":
            break
        else:
            print()
            l_animators.animate_text_indented("Unrecognized option", indent=2, finish_delay=.5)
            subprocess.run(["clear"], shell=True)
            print("\n\n")

    if status == "QUIT":
        print()
        l_animators.animate_text("Quit Lumo: Checklist", finish_delay=.5)
        return

    if status != "EXIT":
        display_selected_checklist(card_title=title, card_steps=steps)

    print()
    l_animators.animate_text("Quit Lumo: Checklist", finish_delay=.5)


if __name__ == "__main__":
    main()
