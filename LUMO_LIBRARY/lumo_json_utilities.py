import datetime
import os
import json
import pathlib

import lumo_filehandler as l_files
import lumo_formatters as l_formatters


def get_json_card_fullpath(var_file):
    file_prefix = os.path.splitext(var_file)[0]
    file_suffix = os.path.splitext(var_file)[1]

    json_file = var_file if not file_suffix == ".txt" else (file_prefix + ".json")
    json_fullpath = os.path.join(l_files.json_cards_folder, json_file)

    return json_fullpath


def read_and_get_json_data(var_rel_filename, var_file_abspath=None, is_json_card=True):
    if is_json_card:
        json_fullpath = get_json_card_fullpath(var_rel_filename)
    elif var_file_abspath and is_json_card == False:
        json_fullpath = var_file_abspath

    with open(json_fullpath) as fin:
        json_data = json.load(fin)

    return json_data


def write_json(var_file, json_data):

    json_fullpath = get_json_card_fullpath(var_file)

    with open(json_fullpath, "w+") as fout:
        fout.write(json.dumps(json_data, indent=2))


def get_category_from_json_settings(var_ltr):
    settings_fullpath = os.path.join(l_files.rootpath, 'SUPPORT_FILES/settings.json')
    with open(settings_fullpath) as fin:
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
    source = get_json_card_fullpath(var_file_src)
    dest = get_json_card_fullpath(var_file_dst)

    os.rename(source, dest)


def make_json_for_unpaired_card(var_card_path):
    card_fullpath = l_formatters.get_card_abspath(var_card_path)
    loc = pathlib.Path(card_fullpath).parent.name
    abbr = var_card_path[0]

    default_json = make_dflt_json_dict(loc=loc, abbr=abbr)
    json_fullpath = get_json_card_fullpath(var_card_path)
    write_json(var_file=json_fullpath, json_data=default_json)


if __name__ == "__main__":
    print("Hello from main")

