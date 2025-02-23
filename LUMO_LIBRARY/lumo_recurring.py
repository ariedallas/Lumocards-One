import os
import datetime
import json

import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_json_utilities as l_json_utils
import LUMO_LIBRARY.lumo_animationlibrary as l_animators

reactivated_cards = []


def test_for_reactivation(json_filename):
    json_fullpath = l_json_utils.get_json_card_fullpath(json_filename)

    with open(json_fullpath) as fin:
        json_data = json.load(fin)

    last = json_data["last occurrence"]
    last_occurrence = datetime.datetime.strptime(last, '%b %d %Y, %A')

    cur_y, cur_m, cur_d = datetime.datetime.today().year, datetime.datetime.today().month, datetime.datetime.today().day

    delta = datetime.datetime(year=cur_y, month=cur_m, day=cur_d) - last_occurrence

    if json_data['recurring freq time unit'] == 'Day':
        return delta.days >= json_data["recurring freq"]

    elif json_data['recurring freq time unit'] == 'Week':
        return (delta.days / 7) >= json_data["recurring freq"]

    elif json_data['recurring freq time unit'] == 'Month':
        return (delta.days / 30) >= json_data["recurring freq"]


def get_recurring_cards():
    for card in os.listdir(l_files.recurring_cards_folder):
        if test_for_reactivation(card):
            reactivated_cards.append(card)

    return reactivated_cards


def remove_recurring_data(json_filename):
    json_data = l_json_utils.read_and_get_json_data(json_filename)

    json_data["recurring freq"] = 0
    json_data["recurring freq time unit"] = None
    json_data["last occurrence"] = None

    l_json_utils.write_json(json_filename, json_data)

    return json_data


def update_recurring_data(json_filename, var_settings=None, initialized=False):
    json_fullpath = l_json_utils.get_json_card_fullpath(json_filename)

    with open(json_fullpath) as fin:
        json_data = json.load(fin)

    today = datetime.datetime.today()

    if not var_settings:
        unit, freq = json_data['recurring freq time unit'], json_data['recurring freq']
    else:
        unit, freq = var_settings[0], var_settings[1]

    if unit == 'Day' and not initialized:
        json_data['recurring freq'] = freq
        json_data['recurring freq time unit'] = unit
        json_data['last occurrence'] = datetime.datetime.strftime(today, '%b %d %Y, %A')
        next_occurrence = today + datetime.timedelta(days=freq)

    elif unit == 'Week' and not initialized:
        json_data['recurring freq'] = freq
        json_data['recurring freq time unit'] = unit
        json_data['last occurrence'] = datetime.datetime.strftime(today, '%b %d %Y, %A')
        next_occurrence = today + datetime.timedelta(weeks=freq)

    elif unit == 'Month' and not initialized:
        json_data['recurring freq'] = freq
        json_data['recurring freq time unit'] = unit
        json_data['last occurrence'] = datetime.datetime.strftime(today, '%b %d %Y, %A')
        next_occurrence = today + datetime.timedelta(days=
                                                     (30 * freq)
                                                      )

    # ---- INITIALIZED CARDS ---- #

    elif unit == 'Day' and initialized:
        json_data['recurring freq'] = freq
        json_data['recurring freq time unit'] = unit

        set_past_date = today - datetime.timedelta(days=freq)
        json_data['last occurrence'] = datetime.datetime.strftime(set_past_date, '%b %d %Y, %A')

        next_occurrence = today

    elif unit == 'Week' and initialized:
        json_data['recurring freq'] = freq
        json_data['recurring freq time unit'] = unit

        set_past_date = today - datetime.timedelta(weeks=freq)

        print(datetime.datetime.strftime(set_past_date, '%b %d %Y, %A'))
        json_data['last occurrence'] = datetime.datetime.strftime(set_past_date, '%b %d %Y, %A')

        next_occurrence = today

    elif unit == 'Month' and initialized:
        json_data['recurring freq'] = freq
        json_data['recurring freq time unit'] = unit

        set_past_date = today - datetime.timedelta(days=freq*30)
        json_data['last occurrence'] = datetime.datetime.strftime(set_past_date, '%b %d %Y, %A')

        next_occurrence = today

    else:
        json_data["recurring freq"]: 0
        json_data["recurring freq time unit"]: None
        json_data["last occurrence"]: None

        l_animators.animate_text("  Oops! Something is funky...")
        next_occurrence = today

    with open (json_fullpath, "w+") as fin:
        fin.write(json.dumps(json_data, indent=2))

    return datetime.datetime.strftime(next_occurrence, '%A, %b %d')


def main():
    reactivated = get_recurring_cards()
    print(reactivated)


if __name__ == "__main__":
    c = get_recurring_cards()