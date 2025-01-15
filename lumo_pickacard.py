import os
import random

import lumo_animationlibrary
import lumo_filehandler as l_files

# all_cards = [c[2] for c in os.walk('lumocards')]
# all_cards_flat = all_cards[0]
# filtered_one = list(filter(lambda c: not c.startswith('.'), all_cards_flat))
# active_cards = list(filter(lambda c: c.startswith('_'), filtered_one))
# inactive_cards = list(set(filtered_one) - set(active_cards))

# def filter_and_choose(sample_list):
#     filtered = []
#
#     for c in sample_list:
#         if ignore(c):
#             filtered.append(c)
#
#     return filtered

# filtered_cards = filter_and_choose(cards)

def ignore(sample_card):
    text = str(sample_card)
    if text.startswith('.'):
        return False
    else:
        return True

def random_archives_card(no_of_cards):
    random_selections = []

    for n in range(no_of_cards):
        random_selections.append(random.choice(l_files.inactive_cards))

    # lumo_animationlibrary.animate_pause(1, .1)
    lumo_animationlibrary.animate_text("RANDOM CARD(S): ", speed=.02)
    lumo_animationlibrary.animate_pause(1, .02)

    lumo_animationlibrary.standard_interval_printer(random_selections, speed_interval=.2, animate_letters=.035)

if __name__ == '__main__':
    random_archives_card(3)
