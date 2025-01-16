import os
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

    formatted_card_tile = format_card_title(card_title)
    card_steps_three = steps_preview(card_steps, steps_amt, steps_idx)

    print()
    l_animators.animate_text(formatted_card_tile.upper())
    print()
    print("  First three items: ", card_steps_three[0], card_steps_three[1], card_steps_three[2])
    print()


def step_abbreviator(var_step):
    result = (var_step[0:15] + "...") if len(var_step) >= 15 else var_step
    return result


def steps_preview(card_steps, steps_amt, steps_idx):

    if steps_amt < 3 and steps_amt > 0:

        initial = [f" {n} — {step_abbreviator(step)}" for n, step in
                   zip(range(1, steps_idx), card_steps[0:steps_amt])]
        filler = [f" {n} — {step}" for n, step in
                  zip(range(steps_idx, 4), default_card_steps)]

        card_steps_three = initial + filler

    elif steps_amt >= 3:
        card_steps_three = [f" {n} — {step_abbreviator(step)}" for n, step in
                            zip(range(4), card_steps[0:3])]

    else:
        card_steps_three = [f" {n} — {step}" for n, step in default_card_steps]
    return card_steps_three


def card_renamer(curr_name, dst_name, dst_dir="Same Dir"):
    curr_name_abspath = get_card_abspath(curr_name)
    curr_dir_name = pathlib.Path(curr_name_abspath).parent.name

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
        print(source, dest)
        l_json_utils.rename_json_card(var_file_src=curr_name, var_file_dst=dst_name)
        l_json_utils.flexible_json_updater(var_file=dst_name, loc=dst_dir_name, update_category=category_change)


def card_deleter(var_card_path):
    card_fullpath = get_card_abspath(var_card_path)
    json_fullpath = l_json_utils.get_json_card_fullpath(var_card_path)

    send2trash.send2trash(card_fullpath)
    send2trash.send2trash(json_fullpath)


def set_card_near_focus(card_path, var_dst_dir):
    new_path = os.path.join(l_files.cards_near_folder, card_path)

    card_renamer(curr_name=card_path, dst_dir=var_dst_dir, dst_name=card_path)
    return new_path


def set_card_middle_focus(card_path):
    new_path = os.path.join(l_files.cards_middle_folder, card_path)

    card_renamer(card_path, new_path)
    return new_path


def set_card_dist_focus(card_path):
    new_path = os.path.join(l_files.cards_dist_folder, card_path)

    card_renamer(card_path, new_path)
    return new_path


def get_card_focus(path):
    focus = None

    if path in os.listdir(l_files.cards_near_folder):
        focus = "near"
    elif path in os.listdir(l_files.cards_middle_folder):
        focus = "middle"
    elif path in os.listdir(l_files.cards_dist_folder):
        focus = "distant"

    return focus


def archiver(card_path):
    source = os.path.join(l_files.cards_near_folder, card_path)
    dest = os.path.join(l_files.archived_cards_folder, card_path)
    os.rename(source, dest)


def cycler(list_of_steps):
    for item in list_of_steps:
        result = l_files.proceed(item)
        if not result:
            sys.exit(0)


def format_card_title(var=str):
    try:
        var = var.replace("_", " ")

        b = var.split()
        c = b[0]
        cc = b[1]
        ccc = camelbreaks_stitch(cc).upper()

        result = "{}  {}".format(c, ccc)

    except:
        var = var.replace("_", " ")
        result = camelbreaks_stitch(var).upper()

    return result


def add_blank_space(response):
    if response == "":
        return " "

    else:
        return response


def camelbreaks(var=str):
    result = []

    for x in range(len(var)):
        if var[x].isupper():
            result.append(x)
    return result


def camelbreaks_stitch(var=str):
    card_name = ""
    breaks = camelbreaks(var)
    stop = 0

    for n in range(len(breaks) - 1):
        start = breaks[n]
        stop = breaks[n+1]

        card_name += "{} ".format(var[start:stop])

    card_name += "{}".format(var[stop:])

    return card_name


def get_card_abspath(path):
    folder_route = None

    if path in os.listdir(l_files.cards_near_folder):
        folder_route = l_files.cards_near_folder
    elif path in os.listdir(l_files.cards_middle_folder):
        folder_route = l_files.cards_middle_folder
    elif path in os.listdir(l_files.cards_dist_folder):
        folder_route = l_files.cards_dist_folder
    elif path in os.listdir(l_files.recurring_cards_folder):
        folder_route = l_files.recurring_cards_folder
    elif path in os.listdir(l_files.archived_cards_folder):
        folder_route = l_files.archived_cards_folder
    elif path in os.listdir(l_files.checklist_cards_folder):
        folder_route = l_files.checklist_cards_folder

    card_fullpath = os.path.join(folder_route, path)
    return card_fullpath


def path_to_card(path):
    card_name_a = path.replace(".txt", "")
    card_name_b = card_name_a.replace("_", " ")
    card_name_c = card_name_b.strip()

    card_fullpath = get_card_abspath(path)

    with open(card_fullpath, 'r') as fin:
        card_steps = [l.strip() for l in fin.readlines()]

    card = (card_name_c, card_steps)
    return card


def abspath_to_card(abspath):
    card_title_unformatted = os.path.basename(abspath)

    format_a = card_title_unformatted.replace(".txt", "")
    format_b = format_a.replace("_", " ")
    card_title = format_b.strip()

    with open(abspath, 'r') as fin:
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


def test_for_float(string):
    try:
        float(string)
        return True
    except:
        return False


if __name__ == "__main__":
    print("Hello from main")
    print(step_abbreviator("house call to the swamp thing"))