import os
import datetime
import time
import pathlib
import lumo_json_utilities as l_json_utils

# ---FILES--- #
home = pathlib.Path.home()
parent = pathlib.Path(__file__).parent.name
parents = pathlib.Path(__file__).parents
rootpath = pathlib.Path(__file__).parents[1]
desktop = f"{home}/Desktop"

cards_near_folder = os.path.join(rootpath, "CARDS/CARDS_A_FOCUS_NEAR")
cards_middle_folder = os.path.join(rootpath, "CARDS/CARDS_B_FOCUS_MIDDLE")
cards_dist_folder = os.path.join(rootpath, "CARDS/CARDS_C_FOCUS_DISTANT")

archived_cards_folder = os.path.join(rootpath, "CARDS/CARDS_D_ARCHIVED")
checklist_cards_folder = os.path.join(rootpath, "CARDS/CARDS_E_CHECKLISTS")
recurring_cards_folder = os.path.join(rootpath, "CARDS/CARDS_F_RECURRING")

support_files_folder = os.path.join(rootpath, "SUPPORT_FILES")
internal_cards_folder = os.path.join(rootpath, "SUPPORT_FILES/Z_INTERNAL_CARDS")
json_cards_folder = os.path.join(rootpath, "SUPPORT_FILES/JSON_CARDS")
temp_folder = os.path.join(rootpath, "SUPPORT_FILES/TEMP")

sounds_folder = os.path.join(rootpath, "SUPPORT_FILES/Z_SOUNDS")


# ---TIME--- #
today = datetime.datetime.today()
today_frmttd = today.strftime("%d%b%Y")
today_frmttd_spaces = today.strftime("%d %b %Y")
today_frmttd_log = today.strftime("%d %m %Y")
today_frmttd_csv = today.strftime("%d %B %Y")
today_dayof_year = today.strftime("%j")
localtime = time.localtime(time.time())
localhour = localtime[3]


cur_time = today.strftime("%H:%M:%S")
cur_time_hr = "----------{}----------".format(cur_time)

def isolate_date_units():
    day = today.strftime("%A")
    day_num = today.strftime("%d")
    month = today.strftime("%b")
    year = today.strftime("%Y")

    return day, day_num, month, year
# ---- PLANNER ---- #
planner_folder = os.path.join(rootpath, "PLANNER")
today_outline_file = f"{today_frmttd.upper()}_outline.txt"
today_outline_fullpath = os.path.join(planner_folder, today_outline_file)


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
    settings = get_json_settings()
    categories = list(settings['card categories'].keys())

    return sorted(categories)


def get_json_settings():
    settings_fullpath = os.path.join(rootpath, 'SUPPORT_FILES/settings.json')
    json_settings = l_json_utils.read_and_get_json_data(var_rel_filename=None, var_file_abspath=settings_fullpath,
                                                        is_json_card=False)
    return json_settings



def basic_wrtr(content, file):

    with open(file, "a+") as fin:
        fin.write(content)


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


def mk_planner():
    basic_wrtr(f"LIGHTWALK: {today_frmttd_spaces.upper()}", today_outline_fullpath)
    basic_wrtr("\n", today_outline_fullpath)


def exists_planner_file():
    if os.path.exists(today_outline_fullpath):
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

# ---- ETC ---- #
# is_Sunday = (datetime.date.weekday(today) == 6)
# week_from_today = (today + datetime.timedelta(weeks=1)).strftime("%A, %B %d, %Y")
#
# tomrrw = today + datetime.timedelta(days=1)
# tomrrw_frmttd = tomrrw.strftime("%d%b %Y")
