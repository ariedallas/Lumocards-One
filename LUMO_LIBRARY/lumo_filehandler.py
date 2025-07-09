import datetime
import itertools
import os
import pathlib
import platform
import string
import subprocess
import time
from os.path import dirname

import LUMO_LIBRARY.lumo_json_utils as l_json_utils

# ---FILES--- #
ROOT_PATH = dirname(dirname(os.path.abspath(__file__)))
USER_FILES = os.path.join(ROOT_PATH, "__USER_FILES__")

cards_near_folder = os.path.join(USER_FILES, "CARDS/CARDS_A_FOCUS_NEAR")
cards_middle_folder = os.path.join(USER_FILES, "CARDS/CARDS_B_FOCUS_MIDDLE")
cards_dist_folder = os.path.join(USER_FILES, "CARDS/CARDS_C_FOCUS_DISTANT")

checklist_cards_folder = os.path.join(USER_FILES, "CARDS/CARDS_E_CHECKLISTS")
recurring_cards_folder = os.path.join(USER_FILES, "CARDS/CARDS_F_RECURRING")
archived_cards_folder = os.path.join(USER_FILES, "CARDS/CARDS_G_ARCHIVED")

journal_folder = os.path.join(USER_FILES, "JOURNAL")
support_files_folder = os.path.join(ROOT_PATH, "__SUPPORT_FILES__")
json_cards_folder = os.path.join(ROOT_PATH, "__SUPPORT_FILES__/JSON_CARDS")
temp_folder = os.path.join(ROOT_PATH, "__SUPPORT_FILES__/TEMP")
credentials_folder = os.path.join(ROOT_PATH, "__SUPPORT_FILES__/Z_CREDENTIALS")

sounds_folder = os.path.join(ROOT_PATH, "__SUPPORT_FILES__/Z_SOUNDS")
settings_fullpath = os.path.join(ROOT_PATH, "__SUPPORT_FILES__/settings.json")

micro = "micro"

# ---TIME--- #
today = datetime.datetime.today()
now = datetime.datetime.now().isoformat() + "Z"
today_frmttd = today.strftime("%d%b%Y")
today_frmttd_spaces = today.strftime("%d %b %Y")
today_frmttd_log = today.strftime("%d %m %Y")
today_dayof_year = today.strftime("%j")
local_time = time.localtime(time.time())
local_hour = local_time[3]

curr_time = today.strftime("%H:%M:%S")
curr_time_hr = "----------{}----------".format(curr_time)


def clear() -> None:
    if platform.system() == "Linux" or platform.system() == "Darwin":
        subprocess.run(["clear"], shell=True)
    elif platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)


def isolate_date_units():
    day = today.strftime("%A")
    day_num = today.strftime("%d")
    month = today.strftime("%b")
    year = today.strftime("%Y")

    return day, day_num, month, year


# ---- PLANNER FILES ---- #
planner_folder = os.path.join(USER_FILES, "PLANNER")

LETTERS_THROUGH_L = string.ascii_lowercase[:12]
curr_month_idx = today.month - 1
curr_month_lttr = LETTERS_THROUGH_L[curr_month_idx].upper()

planner_date = today.strftime(f"%Y_{curr_month_lttr}_%b_%d")
today_planner_file = f"{planner_date}_planner.txt"
today_planner_fullpath = os.path.join(planner_folder, today_planner_file)


# ---- FUCNTIONS ---- #
def get_near_focus_cards():
    cards = [c for c in os.listdir(cards_near_folder)]
    fetched_cards = list(filter(lambda c: c[0].isalpha(), cards))

    return fetched_cards


def get_category_prefixes():
    settings = get_json_settings()
    categories = list(settings["card categories"].keys())

    return sorted(categories)


def get_json_settings():
    json_settings = l_json_utils.read_and_get_json_data(json_filename=None, var_fullpath=settings_fullpath,
                                                        is_json_card=False)
    return json_settings


def get_all_json_cards():
    all_json_cards = set([pathlib.Path(f).stem for f in os.listdir(json_cards_folder)])
    return all_json_cards

def get_all_cards():
    all_txt_cards =  set(itertools.chain(
    [os.path.join(cards_near_folder, f) for f in os.listdir(cards_near_folder)],
    [os.path.join(cards_middle_folder, f) for f in os.listdir(cards_middle_folder)],
    [os.path.join(cards_dist_folder, f) for f in os.listdir(cards_dist_folder)],

    [os.path.join(checklist_cards_folder, f) for f in os.listdir(checklist_cards_folder)],
    [os.path.join(recurring_cards_folder, f) for f in os.listdir(recurring_cards_folder)],
    [os.path.join(archived_cards_folder, f) for f in os.listdir(archived_cards_folder)],
))
    return all_txt_cards

def get_all_cards_by_prefix(search_prefix, check_archives=False):
    matching_paths = list(itertools.chain(
        [f for f in os.listdir(cards_near_folder) if f[0]==search_prefix],
        [f for f in os.listdir(cards_middle_folder) if f[0]==search_prefix],
        [f for f in os.listdir(cards_dist_folder) if f[0]==search_prefix],
        [f for f in os.listdir(checklist_cards_folder) if f[0]==search_prefix],
        [f for f in os.listdir(recurring_cards_folder) if f[0]==search_prefix]
    ))

    if check_archives:
        matching_paths.extend(
            [f for f in os.listdir(archived_cards_folder) if f[0] == search_prefix]
        )

    return matching_paths


def basic_wrtr(content, card_fullpath):
    with open(card_fullpath, "a+") as fin:
        fin.write(content)


def basic_wrtr_custom_dir(content, card_filename, var_dir):
    file_fullpath = os.path.join(var_dir, card_filename)

    with open(file_fullpath, "a+") as fin:
        fin.write(content)
        fin.write("\n")


def over_wrtr(content, card_fullpath):
    with open(card_fullpath, "w+") as fin:
        fin.write(content)
        fin.write("\n")


def over_wrtr_list(var_list, card_fullpath):
    with open(card_fullpath, "w+") as fin:
        for item in var_list:
            fin.write(item)
            fin.write("\n")


def basic_wrtr_list(var_list, card_fullpath):
    with open(card_fullpath, "a+") as fin:
        for item in var_list:
            fin.write(item)
            fin.write("\n")


def make_today_planner():
    basic_wrtr(f"PLANNER: {today_frmttd_spaces.upper()}", today_planner_fullpath)
    basic_wrtr("\n", today_planner_fullpath)


def exists_planner_file():
    if os.path.exists(today_planner_fullpath):
        return True


def get_days_from_date(birth_year, birth_month, birth_day):
    d_present = datetime.datetime.today().date()
    d_birth = datetime.date(birth_year, birth_month, birth_day)

    delta = d_present - d_birth
    return delta.days


if __name__ == '__main__':
    print("hello from main")
    clear()
