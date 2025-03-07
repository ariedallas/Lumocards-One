import os
import string
import subprocess
import time

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_menus as l_menus

letters = string.ascii_lowercase
letters_filtered = [l for l in letters if not (l == 'q') and not (l == 'x')]

main_card_path = os.path.join(l_files.internal_cards_folder, "Checklist_Main.txt")
main_card = l_card_utils.fullpath_to_card(main_card_path)
main_card_title, main_card_steps = main_card[0], main_card[1]

errand_card_path = os.path.join(l_files.internal_cards_folder, "Checklist_Errand.txt")
errand_card = l_card_utils.fullpath_to_card(errand_card_path)
errand_card_title, errand_card_steps = errand_card[0], errand_card[1]

checklist_cards = sorted([card for card in os.listdir(l_files.checklist_cards_folder)])

fetched = [l_card_utils.filename_to_card(file) for file in checklist_cards]
fetched_titles = [l_card_utils.format_card_title(card[0]) for card in fetched]
formatted_results_dict = {f"{ltr}": card for ltr, card in zip(letters_filtered, fetched)}
formatted_results_menu = [f"  [{ltr.upper()}]  {card_title}"
                          for ltr, card_title in zip(letters_filtered, fetched_titles)]


def cycler(list_of_steps):
    for item in list_of_steps:
        input(f"  {item} ?  ")


def display_menu():
    full_menu = formatted_results_menu + [""] + l_menus.simple_exit + l_menus.quit_menu
    for line in full_menu:
        print(line)


def card_select(var_dict):
    lookup = input("\n  > ")
    match_letters = [ltr for ltr in formatted_results_dict.keys()]

    # TODO: change this to a dict lookup
    if lookup in {"q", "x"}:
        return (None, None, "EXIT") if lookup == "x" else (None, None, "QUIT")

    elif lookup in match_letters:
        selected = var_dict[lookup]
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


def main_checklist_review():
    print()
    rsp = l_files.proceed("Would you like to review the Essentials Checklist? ")
    if rsp:
        main_card_title_formatted = l_card_utils.format_card_title(main_card_title).upper()
        print()
        l_animators.animate_text(main_card_title_formatted)

        print()
        cycler(main_card_steps)


def errand_checklist_review():
    print()
    rsp = l_files.proceed("Would you like to review the Errands Checklist? ")
    if rsp:
        errand_card_title_formatted = l_card_utils.format_card_title(errand_card_title).upper()
        print()
        l_animators.animate_text(errand_card_title_formatted)

        print()
        cycler(errand_card_steps)


def program_header():
    print("CHECKLIST(S)")
    print()


def main():
    while True:
        program_header()
        display_menu()
        title, steps, status = card_select(formatted_results_dict)
        if title and steps:
            break
        elif status == "EXIT" or status == "QUIT":
            break
        else:
            print()
            l_animators.animate_text(" unrecognized option", finish_delay=.5)
            subprocess.run(["clear"], shell=True)
            print("\n\n")

    if status == "QUIT":
        print()
        l_animators.animate_text("  Quit Lumo: Checklist", finish_delay=.5)
        return

    if status != "EXIT":
        display_selected_checklist(card_title=title, card_steps=steps)

    main_checklist_review()
    errand_checklist_review()
    print()
    l_animators.animate_text("  Quit Lumo: Checklist", finish_delay=.5)


if __name__ == "__main__":
    main()
