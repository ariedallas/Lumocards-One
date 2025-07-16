import datetime
import os
import pathlib
import re
import subprocess

import send2trash

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs
import LUMO_LIBRARY.lumo_recurring as l_recurring

settings = l_files.get_json_settings()

default_card_steps = [
    "..."
    , "..."
    , "..."
]


def t_editor(var_path, cursor_to_eof):
    if not cursor_to_eof:
        subprocess.run(["micro", var_path])
    else:
        subprocess.run(["micro", "+9999999", var_path])


def card_header(var_card, indent_amt=0):
    card_title = var_card[0]
    card_steps = var_card[1]
    steps_amt = len(card_steps)
    steps_idx = steps_amt + 1

    formatted_card_title = format_card_title(card_title)
    card_steps_three = steps_preview(card_steps, steps_amt, steps_idx)
    card_steps_formatted = f"First three items: 1) {card_steps_three[0]}  2) {card_steps_three[1]}  3) {card_steps_three[2]}"

    print()
    l_animators.animate_text_indented(formatted_card_title.upper(), indent_amt=indent_amt)
    print()
    l_animators.list_printer([card_steps_formatted], indent_amt=indent_amt + 2)
    print()


def step_abbreviator(var_step):
    result = (var_step[0:15] + "...") if len(var_step) >= 15 else var_step
    return result


def steps_preview(card_steps, steps_amt, steps_idx):
    if 0 < steps_amt < 3:

        initial = [f"{step_abbreviator(step)}" for n, step in
                   zip(range(1, steps_idx), card_steps[0:steps_amt])]
        filler = [f"{step}" for n, step in
                  zip(range(steps_idx, 4), default_card_steps)]

        card_steps_three = initial + filler

    elif steps_amt >= 3:
        card_steps_three = [f"{step_abbreviator(step)}" for n, step in
                            zip(range(4), card_steps[0:3])]

    elif steps_amt == 0:
        card_steps_three = [f"(empty)" for n in range(4)]

    else:
        card_steps_three = [f"{step}" for n, step in zip(range(4), default_card_steps)]

    return card_steps_three


def print_card_categories(indent_amt):
    indent_space = " " * indent_amt
    iter_settings = sorted(settings.get("card categories").items())

    for k, v in iter_settings:
        print(f"{indent_space}{k} — {v}")

    for k, v in l_menus_data.Z_CATEGORY_DICT.items():
        print(f"{indent_space}{k} — {v}")


def card_renamer(curr_name, dst_name, dst_dir="Same Dir", ask_confirmation=False):
    curr_name_abspath = get_card_abspath(curr_name)
    curr_dir_name = pathlib.Path(str(curr_name_abspath)).parent.name

    if dst_dir == "Same Dir":
        dst_dir = os.path.join(l_files.USER_FILES, "CARDS", curr_dir_name)

    category_change = (curr_name[0] != dst_name[0])
    dst_dir_name = pathlib.Path(dst_dir).name

    source = curr_name_abspath
    dest = os.path.join(dst_dir, dst_name)

    print()
    if curr_dir_name != dst_dir_name:
        print(f"  Moving from '{curr_dir_name}' to '{dst_dir_name}' ")

    elif curr_name != dst_name:
        print(f"  Renaming from '{curr_name}' to '{dst_name}' ")

    if ask_confirmation:
        if not l_menus_funcs.proceed("Type 'no' or 'x' to cancel, otherwise press any key to continue",
                                     indent_amt=2, reference_list=l_menus_data.NEGATIVE_USER_RESPONSES):
            return "CANCELLED"
        os.rename(source, dest)
        l_json_utils.rename_json_card(src_filename=curr_name, dest_filename=dst_name)
        l_json_utils.flexible_json_updater(json_filename=dst_name, location=dst_dir_name,
                                           update_category=category_change)

    else:
        os.rename(source, dest)
        l_json_utils.rename_json_card(src_filename=curr_name, dest_filename=dst_name)
        l_json_utils.flexible_json_updater(json_filename=dst_name, location=dst_dir_name,
                                           update_category=category_change)


def card_prefix_renamer(old_prefix, new_prefix):
    if old_prefix == new_prefix:
        return

    for f in l_files.get_all_cards_by_prefix(old_prefix):
        p, n = f.split("_")
        new_f = "_".join([new_prefix, n])
        source = get_card_abspath(f)
        dest = os.path.join(
            pathlib.Path(source).parent, new_f)

        os.rename(source, dest)
        l_json_utils.rename_json_card(src_filename=f, dest_filename=new_f)
        l_json_utils.flexible_json_updater(json_filename=new_f, update_category=True)


def card_deleter(card_filename):
    print()
    l_animators.list_printer([f"{card_filename} ➝ Type 'no' or 'x' to cancel deletion",
                              "or press any other key to confirm deletion"], indent_amt=2)
    print()
    if not l_menus_funcs.proceed("", indent_amt=2, reference_list=l_menus_data.NEGATIVE_USER_RESPONSES):
        return "CANCELLED"
    card_fullpath = get_card_abspath(card_filename, check_archives=True)
    json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)

    send2trash.send2trash(card_fullpath)
    send2trash.send2trash(json_fullpath)
    l_animators.animate_text_indented(f"Card {card_filename} deleted", indent_amt=2)


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


def default_json_card_handler(filename):
    json_filename = f"{filename}.json"
    card_filename = f"{filename}.txt"

    recurring_set = {c for c in os.listdir(l_files.recurring_cards_folder)}
    is_recurring = card_filename in recurring_set
    sched_data = None

    mk_default_json_card(card_filename=card_filename)

    if is_recurring:
        sched_data = add_default_recurr_data(json_filename=json_filename,
                                             freq=4,
                                             unit="Day")

    feedback(is_recurring, sched_data)


def mk_default_json_card(card_filename):
    card_fullpath = get_card_abspath(card_filename, check_archives=True)
    loc = pathlib.Path(card_fullpath).parent.name
    abbr = card_filename[0]

    default_json = l_json_utils.make_default_json_dict(location=loc, category_letter=abbr)
    json_fullpath = l_json_utils.get_json_card_fullpath(card_filename)
    l_json_utils.write_json(json_filename=json_fullpath, json_data=default_json)


def add_default_recurr_data(json_filename, freq, unit):
    json_data = l_json_utils.read_and_get_json_data(json_filename)

    json_data["recurring freq"] = freq
    json_data["recurring freq time unit"] = unit
    json_data["last occurrence"] = datetime.datetime.strftime(l_files.today, "%b %d %Y, %A")

    l_json_utils.write_json(json_filename=json_filename, json_data=json_data)

    sched_data = f"{freq} {unit} "
    return sched_data


def feedback(is_recurring=False, schedule=None, deleted=False):
    if is_recurring and not deleted:
        print(f"        Recurring card created with defaults: {schedule}")
    elif not deleted and not is_recurring:
        print(f"        Standard card created")
    else:  # deleted
        print(f"        Card deleted")

    print()


def clean_cards_dupes():
    pass


def clean_cards_renamer(var_path):
    p, n = var_path.split("_")
    new_f = "_".join(["Z", n])
    source = get_card_abspath(var_path, check_archives=True)
    dest = os.path.join(
        pathlib.Path(source).parent, new_f)

    print(f"  Card '{var_path}' is getting renamed to '{new_f}'")
    print(f"  This is because '{p}' is not currently a valid card category.")

    os.rename(source, dest)


def clean_cards_prefixes(test_mode):
    if not test_mode:
        program_header("CARD PREFIXES")

    txt_paths = l_files.get_all_cards()

    for full_path in txt_paths:
        file_name = pathlib.Path(full_path).name
        card_prefix = file_name[0]
        if card_prefix not in l_files.get_category_prefixes() \
                and card_prefix != "Z":

            if test_mode:
                return True

            clean_cards_renamer(file_name)

    if not test_mode:
        print()
        l_animators.animate_text("All .txt cards should now have valid prefixes.", finish_delay=.5)


def clean_cards_unpaired(test_mode):
    """Check to make sure that each .txt card is coupled with a .json card
    If not, ask the user to make either a .txt or .json file to pair
    or delete the solo card."""
    if not test_mode:
        program_header("CARD UNPAIRED")

    txt_paths = l_files.get_all_cards()
    txt_cards = {pathlib.Path(card).stem for card in txt_paths}

    json_paths = l_files.get_all_json_cards()
    json_cards = {pathlib.Path(card).stem for card in json_paths}

    unique_txts = txt_cards.difference(json_cards)
    unique_jsons = json_cards.difference(txt_cards)

    if (unique_txts or unique_jsons) and test_mode:
        return True

    if unique_txts:
        l_animators.list_printer([f"{len(unique_txts)} unique .txt file(s) found:\n"]
                                 , indent_amt=2)

        for u in unique_txts:
            l_animators.list_printer([f"Updating json for {u}.txt"], indent_amt=2)
            default_json_card_handler(u)

    if unique_jsons:
        print()
        l_animators.list_printer([f"{len(unique_jsons)} unique .json file found:\n"]
                                 , indent_amt=2)

        for u in unique_jsons:
            l_animators.list_printer([f"Deleting uneeded json file {u}.json"], indent_amt=2)
            json_fullpath = l_json_utils.get_json_card_fullpath(f"{u}.json")
            send2trash.send2trash(json_fullpath)

    if not test_mode:
        print()
        l_animators.animate_text("All cards should now be paired", finish_delay=.5)


def clean_cards_mover(test_mode):
    if not test_mode:
        program_header("CARD MOVED")

    txt_cards = l_files.get_all_cards()
    # json_cards = l_files.get_all_json_cards()

    txt_tuples = [(pathlib.Path(card).parent.name, pathlib.Path(card).name) for card in txt_cards]

    for tuple in txt_tuples:
        txt_loc, card_name = tuple
        txt_prefix = card_name[0]
        try:
            json_data = l_json_utils.read_and_get_json_data(card_name)
            json_path = l_json_utils.get_json_card_fullpath(card_name)
        except:
            return True

        json_loc = json_data["card location"]
        json_cat = json_data["card category abbreviation"]

        if not json_loc == txt_loc:
            if test_mode:
                return True

            if txt_loc == "CARDS_F_RECURRING":
                l_recurring.update_recurring_data(card_name, ("Day", 4), initialized=True)

            if json_loc == "CARDS_F_RECURRING":
                l_recurring.remove_recurring_data(card_name)

            print(f"  Updating json location for '{card_name}' in '{txt_loc}'")
            l_json_utils.flexible_json_updater(json_path, txt_loc)



        if not txt_prefix == json_cat:
            if test_mode:
                return True

            print(f"  Updating json category for '{card_name}'")
            l_json_utils.flexible_json_updater(card_name, location=None, update_category=True)

    if not test_mode:
        print()
        l_animators.animate_text("All moved cards have updated json info.", finish_delay=.5)


def format_card_title(card_filename):
    try:
        subbed_underscores = card_filename.replace("_", " ")

        first, rest = subbed_underscores.split()
        separated_by_caps = camel_case_separator_b(rest).upper()

        result = "{}: {}".format(first, separated_by_caps)

    except ValueError:
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
        stop = breaks[n + 1]

        card_name += "{} ".format(card_filename[start:stop])

    card_name += "{}".format(card_filename[stop:])

    return card_name


def camel_case_separator_b(card_filename):
    breaks = get_capital_letter_idxs_b(card_filename)
    total_words = len(breaks) - 1

    # add this back at the end
    first_nums = re.match(r"\d+", card_filename)

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
        nums = re.search(r"\d+", word)

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


def get_card_abspath(card_filename, check_archives=False):
    folder_route = None

    if card_filename in os.listdir(l_files.cards_near_folder):
        folder_route = l_files.cards_near_folder
    elif card_filename in os.listdir(l_files.cards_middle_folder):
        folder_route = l_files.cards_middle_folder
    elif card_filename in os.listdir(l_files.cards_dist_folder):
        folder_route = l_files.cards_dist_folder
    elif card_filename in os.listdir(l_files.checklist_cards_folder):
        folder_route = l_files.checklist_cards_folder
    elif card_filename in os.listdir(l_files.recurring_cards_folder):
        folder_route = l_files.recurring_cards_folder
    elif check_archives and \
            card_filename in os.listdir(l_files.archived_cards_folder):

        folder_route = l_files.archived_cards_folder

    card_fullpath = os.path.join(folder_route, card_filename)
    return card_fullpath


def filename_to_card(card_filename, check_archives=False):
    card_name_a = card_filename.replace(".txt", "")
    card_name_b = card_name_a.replace("_", " ")
    card_name_c = card_name_b.strip()

    card_fullpath = get_card_abspath(card_filename, check_archives=check_archives)

    with open(card_fullpath, "r") as fin:
        card_steps = [l.strip() for l in fin.readlines()]

    card = (card_name_c, card_steps)
    return card


def fullpath_to_card(card_fullpath):
    card_title_unformatted = os.path.basename(card_fullpath)

    format_a = card_title_unformatted.replace(".txt", "")
    format_b = format_a.replace("_", " ")
    card_title = format_b.strip()

    with open(card_fullpath, "r") as fin:
        card_steps = [l.strip() for l in fin.readlines()]

    card = (card_title, card_steps)
    return card


def add_multiple_steps_from_card(nums):
    if "," in nums:
        new_nums = nums.split(",")
        new_list = [n.strip() for n in new_nums]

    elif " " in nums:
        new_list = nums.split(" ")

    else:
        new_list = [nums]

    filtered_nums = filter(lambda n: n.isnumeric(), new_list)
    passed_list = [int(num) for num in filtered_nums]

    return passed_list


def test_for_float(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


def test_for_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False


def load_dots() -> None:
    print("\033[33;1m", end="")
    l_animators.animate_text(" ...", speed=.1)
    print("\033[0m", end="")


def load_transition() -> None:
    l_files.clear()
    print()
    load_dots()


def program_header(header):
    print()
    print(header)
    print()


def cards_cleaner():
    run_prefixes = clean_cards_prefixes(test_mode=True)
    run_unpaired = clean_cards_unpaired(test_mode=True)
    run_updated = clean_cards_mover(test_mode=True)

    if True in [run_prefixes, run_unpaired, run_updated]:
        l_files.clear()
        l_animators.animate_text("Now running Cards Cleaner...", finish_delay=.5)

        clean_cards_prefixes(False)
        clean_cards_unpaired(False)
        clean_cards_mover(False)

        print("\nType any key to continue to main menu")
        input("\n>  ")


if __name__ == "__main__":
    cards_cleaner()
