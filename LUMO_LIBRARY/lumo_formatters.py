import os
import re
import pathlib
import sys
import send2trash

import lumo_filehandler as l_files
import lumo_json_utilities as l_json_utils
import lumo_animationlibrary as l_animators


default_card_steps = ["..."
                     ,"..."
                     ,"..."]


def card_header(var_card):
    card_title = var_card[0]
    card_steps = var_card[1]
    steps_amt = len(card_steps)
    steps_idx = steps_amt + 1

    formatted_card_title = format_card_title(card_title)
    card_steps_three = steps_preview(card_steps, steps_amt, steps_idx)

    print()
    l_animators.animate_text(formatted_card_title.upper())
    print()
    print("  First three items: ", card_steps_three[0], card_steps_three[1], card_steps_three[2])
    print()


def step_abbreviator(var_step):
    result = (var_step[0:15] + "...") if len(var_step) >= 15 else var_step
    return result


def steps_preview(card_steps, steps_amt, steps_idx):

    if 0 < steps_amt < 3:

        initial = [f" {n} — {step_abbreviator(step)}" for n, step in
                   zip(range(1, steps_idx), card_steps[0:steps_amt])]
        filler = [f" {n} — {step}" for n, step in
                  zip(range(steps_idx, 4), default_card_steps)]

        card_steps_three = initial + filler

    elif steps_amt >= 3:
        card_steps_three = [f" {n} — {step_abbreviator(step)}" for n, step in
                            zip(range(4), card_steps[0:3])]

    elif steps_amt == 0:
        card_steps_three = [f" {n} — (empty)" for n in range(4)]

    else:
        card_steps_three = [f" {n} — {step}" for n, step in zip(range(4), default_card_steps)]

    return card_steps_three


def card_renamer(curr_name, dst_name, dst_dir="Same Dir"):
    curr_name_abspath = get_card_abspath(curr_name)
    curr_dir_name = pathlib.Path(str(curr_name_abspath)).parent.name

    if dst_dir == "Same Dir":
        dst_dir = os.path.join(l_files.rootpath, "CARDS", curr_dir_name)

    category_change = (curr_name[0] != dst_name[0])
    dst_dir_name = pathlib.Path(dst_dir).name

    source = curr_name_abspath
    dest = os.path.join(dst_dir, dst_name)

    print()
    if curr_dir_name != dst_dir_name:
        l_animators.animate_text(f"  Moving from '{curr_dir_name}' to '{dst_dir_name}' ")

    elif curr_name != dst_name:
        l_animators.animate_text(f"  Renaming from '{curr_name}' to '{dst_name}' ")

    if l_files.proceed("  Type 'cancel' to stop or press any key to continue > "):
        os.rename(source, dest)
        l_json_utils.rename_json_card(src_filename=curr_name, dest_filename=dst_name)
        l_json_utils.flexible_json_updater(json_filename=dst_name, location=dst_dir_name, update_category=category_change)


def card_deleter(card_filename):
    card_fullpath = get_card_abspath(card_filename)
    json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)

    send2trash.send2trash(card_fullpath)
    send2trash.send2trash(json_fullpath)


def set_card_near_focus(card_filename, var_dst_dir):
    new_path = os.path.join(l_files.cards_near_folder, card_filename)

    card_renamer(curr_name=card_filename, dst_dir=var_dst_dir, dst_name=card_filename)
    return new_path


def set_card_middle_focus(card_filename):
    new_path = os.path.join(l_files.cards_middle_folder, card_filename)

    card_renamer(card_filename, new_path)
    return new_path


def set_card_dist_focus(card_filename):
    new_path = os.path.join(l_files.cards_dist_folder, card_filename)

    card_renamer(card_filename, new_path)
    return new_path


def get_card_focus(card_filename):
    focus = None

    if card_filename in os.listdir(l_files.cards_near_folder):
        focus = "near"
    elif card_filename in os.listdir(l_files.cards_middle_folder):
        focus = "middle"
    elif card_filename in os.listdir(l_files.cards_dist_folder):
        focus = "distant"

    return focus


def near_focus_to_archive(card_filename):
    source = os.path.join(l_files.cards_near_folder, card_filename)
    dest = os.path.join(l_files.archived_cards_folder, card_filename)
    os.rename(source, dest)


def cycler(list_of_steps):
    for item in list_of_steps:
        result = l_files.proceed(item)
        if not result:
            sys.exit(0)


def format_card_title(card_filename):
    try:
        subbed_underscores = card_filename.replace("_", " ")

        first, rest = subbed_underscores.split()
        separated_by_caps = camel_case_separator_b(rest).upper()

        result = "{}: {}".format(first, separated_by_caps)

    except ValueError:
        print("exception runs")
        subbed_underscores = card_filename.replace("_", " ")
        result = camel_case_separator_b(subbed_underscores).upper()

    return result


def add_blank_space(usr_input):
    if usr_input == "":
        return " "

    else:
        return usr_input


def get_capital_letter_idxs(card_filename):
    result = []

    for x in range(len(card_filename)):
        if card_filename[x].isupper():
            result.append(x)
    return result


def get_capital_letter_idxs_b(card_filename):
    result = []

    for n in range(len(card_filename)):
        if card_filename[n].isupper():
            result.append(n)

    result.append(len(card_filename))

    return result


def camel_case_separator(card_filename):
    card_name = ""
    breaks = get_capital_letter_idxs(card_filename)
    stop = 0

    for n in range(len(breaks) - 1):
        start = breaks[n]
        stop = breaks[n+1]

        card_name += "{} ".format(card_filename[start:stop])

    card_name += "{}".format(card_filename[stop:])

    return card_name


def camel_case_separator_b(card_filename):
    breaks = get_capital_letter_idxs_b(card_filename)
    total_words = len(breaks) - 1

    # add this back at the end
    first_nums = re.match(r'\d+', card_filename)

    initial_group = []

    for n in range(total_words):
        start, stop = breaks[n], (breaks[n + 1])
        word = card_filename[start:stop]
        initial_group.append(word)


    additions = recursive_parser(initial_group)

    card_name = " ".join(additions)

    if first_nums:
        updated_card_name = f"{first_nums.group()} {card_name}"
        return updated_card_name


    return card_name


def recursive_parser(var_list):
    additions = []

    for word in var_list:
        nums = re.search(r'\d+', word)

        if nums:
            m = nums.group()
            result = word.split(m, 1)
            first, second = result[0], result[1]
            additions.append(first)
            additions.append(m)

            if second:
                additions += recursive_parser([second])

        else:
            additions.append(word)

    return additions


def get_card_abspath(card_filename):
    folder_route = None

    if card_filename in os.listdir(l_files.cards_near_folder):
        folder_route = l_files.cards_near_folder
    elif card_filename in os.listdir(l_files.cards_middle_folder):
        folder_route = l_files.cards_middle_folder
    elif card_filename in os.listdir(l_files.cards_dist_folder):
        folder_route = l_files.cards_dist_folder
    elif card_filename in os.listdir(l_files.cards_calendar_folder):
        folder_route = l_files.cards_calendar_folder
    elif card_filename in os.listdir(l_files.checklist_cards_folder):
        folder_route = l_files.checklist_cards_folder
    elif card_filename in os.listdir(l_files.recurring_cards_folder):
        folder_route = l_files.recurring_cards_folder
    elif card_filename in os.listdir(l_files.archived_cards_folder):
        folder_route = l_files.archived_cards_folder

    card_fullpath = os.path.join(folder_route, card_filename)
    return card_fullpath


def filename_to_card(card_filename):
    card_name_a = card_filename.replace(".txt", "")
    card_name_b = card_name_a.replace("_", " ")
    card_name_c = card_name_b.strip()

    card_fullpath = get_card_abspath(card_filename)

    with open(card_fullpath, 'r') as fin:
        card_steps = [l.strip() for l in fin.readlines()]

    card = (card_name_c, card_steps)
    return card


def fullpath_to_card(card_fullpath):
    card_title_unformatted = os.path.basename(card_fullpath)

    format_a = card_title_unformatted.replace(".txt", "")
    format_b = format_a.replace("_", " ")
    card_title = format_b.strip()

    with open(card_fullpath, 'r') as fin:
        card_steps = [l.strip() for l in fin.readlines()]

    card = (card_title, card_steps)
    return card


def add_multiple_steps_from_card(nums):
    if "," in nums:
        new_nums = nums.split(',')
        new_list = [n.strip() for n in new_nums]

    elif " " in nums:
        new_list = nums.split(" ")

    else:
        new_list = [nums]

    filtered_nums = filter(lambda n: n.isnumeric(), new_list)
    passed_list = [int(num) for num in filtered_nums]

    return passed_list


def test_for_float(text):
    try:
        float(text)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print("Hello from main")
