import datetime
import os
import json
import pathlib

import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_formatters as l_formatters


def get_json_card_fullpath(json_filename):
    file_prefix = os.path.splitext(json_filename)[0]
    file_suffix = os.path.splitext(json_filename)[1]

    json_file = json_filename if not file_suffix == ".txt" else (file_prefix + ".json")
    json_fullpath = os.path.join(l_files.json_cards_folder, json_file)

    return json_fullpath


def read_and_get_json_data(json_filename, var_fullpath=None, is_json_card=True):
    if is_json_card:
        json_fullpath = get_json_card_fullpath(json_filename)
    # Else if you are reading json data that's not specifically a 'json card', i.e. settings.json
    elif var_fullpath and is_json_card == False:
        json_fullpath = var_fullpath
    else:
        json_fullpath = None

    if json_fullpath:
        with open(json_fullpath) as fin:
            json_data = json.load(fin)

    return json_data


def write_json(json_filename, json_data):

    json_fullpath = get_json_card_fullpath(json_filename)

    with open(json_fullpath, "w+") as fout:
        fout.write(json.dumps(json_data, indent=2))


def get_category_from_json_settings(var_ltr):
    settings_fullpath = os.path.join(l_files.rootpath, "SUPPORT_FILES/settings.json")
    with open(settings_fullpath) as fin:
        data = json.load(fin)

    card_settings = data["card categories"]
    selected_category = card_settings[var_ltr.upper()][1]

    return selected_category


def make_dflt_json_dict(location, category_letter, google_calendar_data=None):
    category = get_category_from_json_settings(category_letter)

    dict_for_json = {
            "card location": location,
            "card category abbreviation": category_letter.upper(),
            "card category": category,
            "recurring freq": 0,
            "recurring freq time unit": None,
            "last occurrence": None,
            "card created": datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            "tags":
                [ "default tag a"
                , "default tag b"
                , "default tag c"],
            "google calender data": google_calendar_data
        }

    return dict_for_json


def flexible_json_updater(json_filename, location=None, update_category=False):

    if location:
        json_data = read_and_get_json_data(json_filename)

        json_data["card location"] = location
        write_json(json_filename, json_data)

    if update_category:
        json_data = read_and_get_json_data(json_filename)

        c_abbr = json_filename[0]
        new_category = get_category_from_json_settings(c_abbr)
        json_data["card category abbreviation"] = c_abbr
        json_data["card category"] = new_category
        write_json(json_filename, json_data)


def rename_json_card(src_filename, dest_filename):
    source = get_json_card_fullpath(src_filename)
    dest = get_json_card_fullpath(dest_filename)

    os.rename(source, dest)


def make_json_for_unpaired_card(json_filename):
    card_fullpath = l_formatters.get_card_abspath(json_filename)
    loc = pathlib.Path(card_fullpath).parent.name
    abbr = json_filename[0]

    default_json = make_dflt_json_dict(location=loc, category_letter=abbr)
    json_fullpath = get_json_card_fullpath(json_filename)
    write_json(json_filename=json_fullpath, json_data=default_json)


if __name__ == "__main__":
    print("Hello from main")

