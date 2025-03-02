import string
import os

import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_animationlibrary as l_animators

letters = string.ascii_uppercase
letters_filtered = [l.upper() for l in letters if not (l == 'q') and not (l == 'x')]

main_card_path = os.path.join(l_files.internal_cards_folder, "Checklist_Main.txt")
main_card = l_card_utils.fullpath_to_card(main_card_path)
main_card_title, main_card_steps = main_card[0], main_card[1]

errand_card_path = os.path.join(l_files.internal_cards_folder, "Checklist_Errand.txt")
errand_card = l_card_utils.fullpath_to_card(errand_card_path)
errand_card_title, errand_card_steps = errand_card[0], errand_card[1]

checklist_cards = sorted([card for card in os.listdir(l_files.checklist_cards_folder)])

def display_menu(var_list_cards):
    fetched_cards = [l_card_utils.filename_to_card(fn) for fn in var_list_cards]
    formatted_results = [f"[{idx_lttr}] {l_card_utils.format_card_title(card[0])}"
                         for idx_lttr, card in zip(letters_filtered, fetched_cards)]

    l_animators.standard_interval_printer(formatted_results, speed_interval=.15)


def card_select(var_list_cards):
    letter_to_idx = input("\nSelect letter > ")
    match_letters = letters_filtered[0:len(var_list_cards)]

    # change this to a dict lookup
    if letter_to_idx.isalpha() and len(letter_to_idx) == 1 and (letter_to_idx.upper() in match_letters):
        letter_as_listindex = ord(letter_to_idx.lower()) - 97
        outlist_path = var_list_cards[letter_as_listindex]
        outlist_card = l_card_utils.filename_to_card(outlist_path)

        card_title = l_card_utils.format_card_title(outlist_card[0]).upper()
        card_steps = outlist_card[1]

        return card_title, card_steps

    else:
        print("Try again, pls.")


def display_selected_checklist(card_title, card_steps):
    print()
    l_animators.animate_text(card_title)
    print()
    l_card_utils.cycler(card_steps)


def main_checklist_review():
    print()
    rsp = l_files.proceed("Would you like to review the Essentials Checklist? ")
    if rsp:
        main_card_title_formatted = l_card_utils.format_card_title(main_card_title).upper()
        print()
        l_animators.animate_text(main_card_title_formatted)

        print()
        l_card_utils.cycler(main_card_steps)


def errand_checklist_review():
    print()
    rsp = l_files.proceed("Would you like to review the Errands Checklist? ")
    if rsp:
        errand_card_title_formatted = l_card_utils.format_card_title(errand_card_title).upper()
        print()
        l_animators.animate_text(errand_card_title_formatted)

        print()
        l_card_utils.cycler(errand_card_steps)


if __name__ == "__main__":

    print()
    l_animators.animate_text("CHECKLISTS")
    print()

    display_menu(checklist_cards)
    title, steps = card_select(checklist_cards)
    display_selected_checklist(card_title=title, card_steps=steps)

    main_checklist_review()
    errand_checklist_review()
