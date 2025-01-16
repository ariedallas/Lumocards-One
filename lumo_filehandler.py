import os
import datetime
import time
import pathlib
import lumo_json_utilities as l_json_utils

# ---TIME--- #
today = datetime.datetime.today()
today_frmttd = today.strftime("%d%b%Y")
today_frmttd_spaces = today.strftime("%d %b %Y")
today_frmttd_log = today.strftime("%d %m %Y")
today_frmttd_csv = today.strftime("%d %B %Y")
today_dayof_year = today.strftime("%j")
localtime = time.localtime(time.time())
localhour = localtime[3]

is_Sunday = (datetime.date.weekday(today) == 6)
week_from_today = (today + datetime.timedelta(weeks=1)).strftime("%A, %B %d, %Y")

tomrrw = today + datetime.timedelta(days=1)
tomrrw_frmttd = tomrrw.strftime("%d%b %Y")

cur_time = today.strftime("%H:%M:%S")
cur_time_hr = "----------{}----------".format(cur_time)


# ---FILES--- #
home = pathlib.Path.home()
parent = (pathlib.Path(__file__).parent.name)
rootpath = os.getcwd()
desktop = f"{home}/Desktop"

cards_near_folder = os.path.join(rootpath, "CARDS/CARDS_A_FOCUS_NEAR")
cards_middle_folder = os.path.join(rootpath, "CARDS/CARDS_B_FOCUS_MIDDLE")
cards_dist_folder = os.path.join(rootpath, "CARDS/CARDS_C_FOCUS_DISTANT")

archived_cards_folder = os.path.join(rootpath, "CARDS/CARDS_D_ARCHIVED")
checklist_cards_folder = os.path.join(rootpath, "CARDS/CARDS_E_CHECKLISTS")
recurring_cards_folder = os.path.join(rootpath, "CARDS/CARDS_F_RECURRING")

internal_cards_folder = os.path.join(rootpath, "INTERNAL_CARDS")
json_cards = os.path.join(rootpath, "SUPPORT_FILES/JSON_CARDS")
temp_folder = os.path.join(rootpath, "SUPPORT_FILES/TEMP")
logging_folder = os.path.join(rootpath, "LOGS_DATEDATABS")

sounds_folder = os.path.join(rootpath, "SUPPORT_FILES/Z_SOUNDS")

lightwalk_folder = os.path.join(rootpath, "PLANNER")
lightwalk_filename = ("%s_lightwalk.txt") % today_frmttd.upper()
lightwalk_file = os.path.join(lightwalk_folder, lightwalk_filename)

lightwalk_cycles_filename = "_lightwalk_cycles_data.csv"
lightwalk_cycles_file     = os.path.join(logging_folder, lightwalk_cycles_filename)
lightwalk_cycles_temp_filename = "_lightwalk_cycles_temp.csv"
lightwalk_cycles_temp_file     = os.path.join(logging_folder, lightwalk_cycles_temp_filename)


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
    cardsA = [c for (_, _, c) in os.walk(cards_near_folder)]

    cardsB = cardsA[0]
    fetched_cards = list(filter(lambda c: not c.startswith('.'), cardsB))

    return fetched_cards

def get_lumocards_categories():
    json_settings = l_json_utils.read_and_get_json_data('SUPPORT_FILES/settings.json', is_json_card=False)
    categories = list(json_settings['card categories'].keys())

    return sorted(categories)

# —--LUMOCARDS--- #
near_focus_cards = get_near_focus_cards()
near_focus_cards_ordrd = sorted(near_focus_cards)

active_cards_ordrd = sorted(near_focus_cards)

checklist_cards = [card for card in os.listdir(checklist_cards_folder)]
checklist_cards_ordrd = sorted(checklist_cards)

def basic_wrtr(content, file):

    with open(file, "a+") as fin:
        fin.write(content)
        fin.write("\n")


def basic_wrtr_custom_dir(content, file, custom_dir):
    file_abspath = os.path.join(custom_dir, file)

    with open(file_abspath, "a+") as fin:
        fin.write(content)
        fin.write("\n")


def over_wrtr(content, file):

    with open(file, "w+") as fin:
        fin.write(content)
        fin.write("\n")


def over_wrtr_list(list, file):

    with open(file, "w+") as fin:
        for item in list:
            fin.write(item)
            fin.write("\n")


def basic_wrtr_list(list, file):

    with open(file, "a+") as fin:
        for item in list:
            fin.write(item)
            fin.write("\n")


def mk_lightwalk():
    basic_wrtr("LIGHTWALK: {}".format(today_frmttd_spaces.upper()), lightwalk_file)


def exists_lightwalk_file():
    if os.path.exists(lightwalk_file):
        return True


def get_days_from_date(birthyear, birthmonth, birthday):
    d_present = datetime.datetime.today().date()
    d_birth = datetime.date(birthyear, birthmonth, birthday)

    delta = d_present - d_birth
    return delta.days


def proceed(input_text="... "):
    response = input(f"{input_text} ")
    return True if response not in negative_user_responses else False


if __name__ == '__main__':
    print("hello from main")

