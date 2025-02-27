import datetime
import os
import pathlib
import time

import LUMO_LIBRARY.lumo_json_utils as l_json_utils

# ---FILES--- #
home = pathlib.Path.home()
parent = pathlib.Path(__file__).parent.name
parents = pathlib.Path(__file__).parents
rootpath = pathlib.Path(__file__).parents[1]
desktop = f"{home}/Desktop"

cards_near_folder = os.path.join(rootpath, "CARDS/CARDS_A_FOCUS_NEAR")
cards_middle_folder = os.path.join(rootpath, "CARDS/CARDS_B_FOCUS_MIDDLE")
cards_dist_folder = os.path.join(rootpath, "CARDS/CARDS_C_FOCUS_DISTANT")
cards_calendar_folder = os.path.join(rootpath, "CARDS/CARDS_D_CALENDAR")

checklist_cards_folder = os.path.join(rootpath, "CARDS/CARDS_E_CHECKLISTS")
recurring_cards_folder = os.path.join(rootpath, "CARDS/CARDS_F_RECURRING")
archived_cards_folder = os.path.join(rootpath, "CARDS/CARDS_G_ARCHIVED")

journal_folder = os.path.join(rootpath, "JOURNAL")
support_files_folder = os.path.join(rootpath, "SUPPORT_FILES")
internal_cards_folder = os.path.join(rootpath, "SUPPORT_FILES/Z_INTERNAL_CARDS")
json_cards_folder = os.path.join(rootpath, "SUPPORT_FILES/JSON_CARDS")
temp_folder = os.path.join(rootpath, "SUPPORT_FILES/TEMP")
credentials_folder = os.path.join(rootpath, "SUPPORT_FILES/Z_CREDENTIALS")

sounds_folder = os.path.join(rootpath, "SUPPORT_FILES/Z_SOUNDS")

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


def isolate_date_units():
    day = today.strftime("%A")
    day_num = today.strftime("%d")
    month = today.strftime("%b")
    year = today.strftime("%Y")

    return day, day_num, month, year


# ---- PLANNER ---- #
planner_folder = os.path.join(rootpath, "PLANNER")
today_planner_file = f"{today_frmttd.upper()}_planner.txt"
today_planner_fullpath = os.path.join(planner_folder, today_planner_file)

# ---- RESPONSES ---- #
negative_user_responses = [
    "no"
    , "exit"
    , "quit"
    , "stop"
    , "cancel"
]


# ---- FUCNTIONS ---- #
def get_near_focus_cards():
    cards = [c for c in os.listdir(cards_near_folder)]
    fetched_cards = list(filter(lambda c: c[0].isalpha(), cards))

    return fetched_cards


def get_lumocards_categories():
    settings = get_json_settings()
    categories = list(settings['card categories'].keys())

    return sorted(categories)


def get_json_settings():
    settings_fullpath = os.path.join(rootpath, 'SUPPORT_FILES/settings.json')
    json_settings = l_json_utils.read_and_get_json_data(json_filename=None, var_fullpath=settings_fullpath,
                                                        is_json_card=False)
    return json_settings


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


def proceed(input_text="... "):
    response = input(f"{input_text} ")
    return True if response not in negative_user_responses else False


if __name__ == '__main__':
    print("hello from main")
    print(get_near_focus_cards())
