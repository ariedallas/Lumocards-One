import os

import lumo_filehandler as l_files
import lumo_newcard as l_newcard
import lumo_recurring as l_recurring

category_letters = l_files.get_lumocards_categories()
sample_steps = ["Step 01\n", "Step 02\n", "Step 03\n"]

# '''
# CREATE NEAR CARDS
for n, ltr in zip(range(1,9), category_letters):
    filename = f"{ltr}_NearCard{n}.txt"
    l_newcard.write_card_and_json(filename, l_files.cards_near_folder, add_custom_steps=sample_steps)
    
# CREATE MIDDLE CARDS 
for n, ltr in zip(range(1, 9), category_letters):
    filename = f"{ltr}_MiddleCard{n}.txt"
    l_newcard.write_card_and_json(filename, l_files.cards_middle_folder, add_custom_steps=sample_steps)

# CREATE DISTANT CARDS 
for n, ltr in zip(range(1, 9), category_letters):
    filename = f"{ltr}_DistantCard{n}.txt"
    l_newcard.write_card_and_json(filename, l_files.cards_dist_folder, add_custom_steps=sample_steps)

# CREATE ARCHIVED CARDS 
for n, ltr in zip(range(1, 4), category_letters):
    filename = f"{ltr}_ArchivedCard{n}.txt"
    l_newcard.write_card_and_json(filename, l_files.archived_cards_folder, add_custom_steps=sample_steps)

# CREATE CHECKLIST CARDS 
for n, ltr in zip(range(1, 4), category_letters):
    filename = f"{ltr}_ChecklistCard{n}.txt"
    l_newcard.write_card_and_json(filename, l_files.checklist_cards_folder, add_custom_steps=sample_steps)

# CREATE RECURRING CARDS
for n, ltr in zip(range(1, 4), category_letters):
    filename = f"{ltr}_RecurringCard{n}.txt"
    l_newcard.write_card_and_json(filename, l_files.recurring_cards_folder, add_custom_steps=sample_steps)
    l_recurring.update_recurring_data(filename, ("Day", 4), initialized=True)

# '''
