import argparse
import collections
import itertools
import os
import pprint

import send2trash

import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import lumo_filehandler as l_files
import lumo_card_utils as l_formatters

def function_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(func.__name__)
        print(end - start)
        return result

    return wrapper


a = set(itertools.chain(range(3,6), range(14, 25), range(30, 35)))

txt_cards = set(itertools.chain(
    [l[:-4] for l in os.listdir(l_files.cards_near_folder)],
    [l[:-4] for l in os.listdir(l_files.cards_middle_folder)],
    [l[:-4] for l in os.listdir(l_files.cards_dist_folder)],
    [l[:-4] for l in os.listdir(l_files.cards_calendar_folder)],

    [l[:-4] for l in os.listdir(l_files.checklist_cards_folder)],
    [l[:-4] for l in os.listdir(l_files.recurring_cards_folder)],
    [l[:-4] for l in os.listdir(l_files.archived_cards_folder)],

))

json_cards = set([c[:-5] for c in os.listdir(l_files.json_cards_folder)])

diff_sym = txt_cards.symmetric_difference(json_cards)
unique_txts = txt_cards.difference(json_cards)
unique_jsons = json_cards.difference(txt_cards)

# add or delete for .json
# add or delete for .txt

if unique_txts:
    print(f"{len(unique_txts)} unique .txt file found:\n")

    for u in unique_txts:
        print(f"  {u}.txt", end=" ")
        response = input("——> [D]elete this or [C]reate .json files to pair it? >  ")
        if response.lower() == 'd':
            card_fullpath = l_formatters.get_card_abspath(f"{u}.txt")
            send2trash.send2trash(card_fullpath)
        elif response.lower() == 'c':
            pass
        else:
            print("        (You skipped this card for now.)")


print()

if unique_jsons:
    print(f"{len(unique_jsons)} unique .json file found:\n")

    for u in unique_jsons:
        print(f"  {u}.json", end=" ")
        response = input("——> [D]elete this or [C]reate .txt files to pair it? >  ")
        if response.lower() == 'd':
            json_fullpath = l_json_utils.get_json_card_fullpath(f"{u}.json")
            send2trash.send2trash(json_fullpath)
        elif response.lower() == 'c':
            pass
        else:
            print("        (You skipped this card for now.)")



# def card_deleter(card_filename):
#     card_fullpath = get_card_abspath(card_filename)
#     json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)
#
#     send2trash.send2trash(card_fullpath)
#     send2trash.send2trash(json_fullpath)

# print(unique_txts, unique_jsons)

# pprint.pprint(b)
# pprint.pprint(c)

