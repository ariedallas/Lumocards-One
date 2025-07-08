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
    l_animators.list_printer(var_menu, indent_amt=2, speed_interval=0)
    print()
    l_animators.list_printer(l_menus_data.QUIT_MENU_LIST, indent_amt=2, speed_interval=0)


def card_select(var_dict):
    user_input = input("\n  > ")
    val = user_input.strip()

    if val.upper() in var_dict.keys():
        selected = var_dict[val.upper()]
        card_title = l_card_utils.format_card_title(selected[0])
        card_steps = selected[1]

        return card_title, card_steps, None, None

    elif val.lower() in {"q", "quit"}:
        return None, None, "QUIT", None

    else:
        return None, None, None, val


def display_selected_checklist(card_title, card_steps):
    print()
    l_animators.animate_text(card_title)
    print()
    cycler(card_steps)
    print()

    l_animators.animate_text_indented("Checklist done, press any key to to continue...", indent_amt=2)
    input("\n  >  ")



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
        title, steps, status, val = card_select(formatted_results_dict)
        if title and steps:
            break
        elif status == "QUIT":
            break
        else:
            print()
            l_animators.animate_text_indented(f"Unrecognized option '{val}' ...", indent_amt=2, finish_delay=.5)
            l_files.clear()
            print("\n")

    if status == "QUIT":
        print()
        # Optional feature:
        # l_animators.animate_text("Quit Lumo: Checklist", finish_delay=.5)
        return

    display_selected_checklist(card_title=title, card_steps=steps)
    print()


if __name__ == "__main__":
    main()
