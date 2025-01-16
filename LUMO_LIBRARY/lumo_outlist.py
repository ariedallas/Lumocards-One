import string
import os

import lumo_filehandler as l_files
import lumo_formatters as l_formatters
import lumo_animationlibrary as l_animators

letters = string.ascii_uppercase
letters_filtered = [l.upper() for l in letters if not (l == 'q') and not (l == 'x')]

main_card_path = os.path.join(l_files.internal_cards_folder, "Outlist_Main.txt")
main_card = l_formatters.abspath_to_card(main_card_path)
main_card_title = main_card[0]
main_card_steps = main_card[1]

errand_card_path = os.path.join(l_files.internal_cards_folder, "Outlist_Errand.txt")
errand_card = l_formatters.abspath_to_card(errand_card_path)
errand_card_title = errand_card_path[0]
errand_card_steps = errand_card_path[1]

checklist_cards = l_files.checklist_cards_ordrd
checklist_cards_filtered = []

for path in checklist_cards:

    if (path == main_card_path or path == errand_card_path):
        continue
    else:
        checklist_cards_filtered.append(path)

def display_menu(list_of_cards):
    fetched_cards = [l_formatters.path_to_card(path) for path in list_of_cards]
    formatted_results = [f"[{idx_lttr}] {l_formatters.format_card_title(card[0])}"
                         for idx_lttr, card in zip(letters_filtered, fetched_cards)]

    l_animators.standard_interval_printer(formatted_results, speed_interval=.15)


def card_select(list_of_cards):
    letter_to_idx = input("\nSelect letter > ")
    match_letters = letters_filtered[0:len(list_of_cards)]

    if letter_to_idx.isalpha() and len(letter_to_idx) == 1 and (letter_to_idx.upper() in match_letters):
        letter_as_listindex = ord(letter_to_idx.lower()) - 97
        outlist_path = list_of_cards[letter_as_listindex]
        outlist_card = l_formatters.path_to_card(outlist_path)

        title = l_formatters.camelbreaks_stitch(outlist_card[0]).upper()
        list_of_steps = outlist_card[1]

        if "HOME" in title:
            location = False
        else:
            location = True

        return title, list_of_steps, location

    else:
        print("Try again, pls.")

def display_selected_outlist(var_title, var_steps):
    print()
    l_animators.animate_text(title)
    print()
    l_formatters.cycler(var_steps)


def main_outlist_review(var_location):
    if var_location:
        print()
        main_card_title_formatted = l_formatters.camelbreaks_stitch(main_card_title).upper()

        l_animators.animate_text(main_card_title_formatted)
        print()
        l_formatters.cycler(main_card_steps)


def errand_outlist_review(var_location):
    if var_location:
        print()
        main_card_title_formatted = l_formatters.camelbreaks_stitch(main_card_title).upper()

        rsp = l_files.proceed("Would you like to review the Errands Card? ")
        if rsp:
            print()
            l_animators.animate_text(main_card_title_formatted)
            print()
            l_formatters.cycler(main_card_steps)


if __name__ == "__main__":

    print()
    l_animators.animate_text("OUTLISTS")
    print()

    display_menu(checklist_cards_filtered)
    title, steps, location = card_select(checklist_cards_filtered)
    display_selected_outlist(var_title=title, var_steps=steps)

    main_outlist_review(var_location=location)
    errand_outlist_review(var_location=location)





