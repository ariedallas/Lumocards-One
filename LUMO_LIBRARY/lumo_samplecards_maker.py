import os

import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_newcard as l_newcard
import LUMO_LIBRARY.lumo_recurring as l_recurring

category_letters = l_files.get_lumocards_categories()
sample_steps = ["Step 01\n", "Step 02\n", "Step 03\n"]


def generate_sample_cards():
    # CREATE NEAR CARDS
    near_cards()

    # CREATE MIDDLE CARDS
    middle_cards()

    # CREATE DISTANT CARDS
    distant_cards()

    # CREATE ARCHIVED CARDS
    archived_cards()

    # CREATE RECURRING CARDS
    recurring_cards()

    # CREATE CHECKLIST CARDS
    checklist_cards()


def delete_all_cards():
    print("Deleting all sample cards and initializing folders with nothing.")
    print()

    if l_files.proceed("OK? "):
        delete_cards_from_folder(l_files.cards_near_folder)
        delete_cards_from_folder(l_files.cards_middle_folder)
        delete_cards_from_folder(l_files.cards_dist_folder)
        delete_cards_from_folder(l_files.archived_cards_folder)
        delete_cards_from_folder(l_files.checklist_cards_folder)
        delete_cards_from_folder(l_files.recurring_cards_folder)

        delete_cards_from_folder(l_files.json_cards_folder)


def delete_cards_from_folder(var_dir):

    for card in os.listdir(var_dir):
        print(f"deleted card: {card}")
        os.remove(f"{var_dir}/{card}")


def near_cards():
    for n, ltr in zip(range(1, 9), category_letters):
        filename = f"{ltr}_NearCard{n}.txt"
        l_newcard.write_card_and_json(filename, l_files.cards_near_folder, add_custom_steps=sample_steps)


def middle_cards():
    for n, ltr in zip(range(1, 9), category_letters):
        filename = f"{ltr}_MiddleCard{n}.txt"
        l_newcard.write_card_and_json(filename, l_files.cards_middle_folder, add_custom_steps=sample_steps)


def distant_cards():
    for n, ltr in zip(range(1, 9), category_letters):
        filename = f"{ltr}_DistantCard{n}.txt"
        l_newcard.write_card_and_json(filename, l_files.cards_dist_folder, add_custom_steps=sample_steps)


def archived_cards():
    for n, ltr in zip(range(1, 4), category_letters):
        filename = f"{ltr}_ArchivedCard{n}.txt"
        l_newcard.write_card_and_json(filename, l_files.archived_cards_folder, add_custom_steps=sample_steps)


def checklist_cards():
    for n, ltr in zip(range(1, 4), category_letters):
        filename = f"{ltr}_ChecklistCard{n}.txt"
        l_newcard.write_card_and_json(filename, l_files.checklist_cards_folder, add_custom_steps=sample_steps)


def recurring_cards():
    for n, ltr in zip(range(1, 4), category_letters):
        filename = f"{ltr}_RecurringCard{n}.txt"
        l_newcard.write_card_and_json(filename, l_files.recurring_cards_folder, add_custom_steps=sample_steps)
        l_recurring.update_recurring_data(filename, ("Day", 4), initialized=True)


if __name__ == "__main__":
    # delete_all_cards()
    generate_sample_cards()