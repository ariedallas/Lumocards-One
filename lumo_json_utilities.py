import datetime
import os
import json
import pathlib

import lumo_filehandler as l_files
import lumo_formatters
from lumo_recurring import remove_recurring_data


def flexible_json_pathfinder(var_file, is_json_card=True):
    file_prefix = os.path.splitext(var_file)[0]
    file_suffix = os.path.splitext(var_file)[1]

    if is_json_card:
        json_file = var_file if not file_suffix == ".txt" else (file_prefix + ".json")
        json_fullpath = os.path.join(l_files.json_cards, json_file)
    else:
        json_fullpath = os.path.join(l_files.rootpath, var_file)

    return json_fullpath


def read_and_get_json_data(var_file, is_json_card=True):
    json_fullpath = flexible_json_pathfinder(var_file, is_json_card=is_json_card)

    with open(json_fullpath) as fin:
        json_data = json.load(fin)

    return json_data


def write_json(var_file, json_data):

    json_fullpath = flexible_json_pathfinder(var_file)

    with open(json_fullpath, "w+") as fout:
        fout.write(json.dumps(json_data, indent=2))


def get_category_from_json_settings(var_ltr):
    with open('settings.json') as fin:
        data = json.load(fin)

    card_settings = data['card categories']
    selected_category = card_settings[var_ltr.upper()][1]

    return selected_category


def make_dflt_json_dict(loc, abbr):
    category = get_category_from_json_settings(abbr)

    dict_for_json = {
            "card location": loc,
            "card category abbreviation": abbr.upper(),
            "card category": category,
            "calender event": None,
            "calendar repeating event": None,
            "recurring freq": 0,
            "recurring freq time unit": None,
            "last occurrence": None,
            "card created": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            "tags":
                [ "default tag a"
                , "default tag b"
                , "default tag c"]
        }

    return dict_for_json


def flexible_json_updater(var_file, loc=None, update_category=False):

    if loc:
        json_data = read_and_get_json_data(var_file)

        json_data['card location'] = loc
        write_json(var_file, json_data)

    if update_category:
        json_data = read_and_get_json_data(var_file)

        c_abbr = var_file[0]
        new_category = get_category_from_json_settings(c_abbr)
        json_data['card category abbreviation'] = c_abbr
        json_data['card category'] = new_category
        write_json(var_file, json_data)


def rename_json_card(var_file_src, var_file_dst):
    source = flexible_json_pathfinder(var_file_src)
    dest = flexible_json_pathfinder(var_file_dst)

    os.rename(source, dest)


def make_json_for_unpaired_card(var_card_path):
    card_fullpath = lumo_formatters.get_card_abspath(var_card_path)
    loc = pathlib.Path(card_fullpath).parent.name
    abbr = var_card_path[0]

    default_json = make_dflt_json_dict(loc=loc, abbr=abbr)
    json_fullpath = flexible_json_pathfinder(var_card_path)
    write_json(var_file=json_fullpath, json_data=default_json)


if __name__ == "__main__":
    print("Hello from main")

