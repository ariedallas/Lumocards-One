import subprocess

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files
import LUMO_LIBRARY.lumo_json_utils as l_json_utils
import LUMO_LIBRARY.lumo_menus_data as l_menus_data
import LUMO_LIBRARY.lumo_menus_funcs as l_menus_funcs

all_category_prefixes = l_files.get_category_prefixes()

manager_menu_d, manager_menu_l = l_menus_funcs.prep_menu_tuple_integers(
    l_menus_data.SETTINGS_CARD_MANAGER)

singleCat_menu_d, singleCat_menu_l = l_menus_funcs.prep_menu_tuple_integers(
    l_menus_data.SETTINGS_CARD_MANAGER_SINGLE)



def main():
    categories_manager()


def categories_manager():
    global first_round
    first_round = True

    while True:

        status = manager_menu()
        if status == "QUIT":
            break


def manager_menu():
    categories_dict = get_categories_copy()
    global first_round

    while True:

        if not first_round:
            l_card_utils.load_transition()
        else:
            first_round = False


        categories_header(categories_dict)
        print()
        l_animators.list_printer(manager_menu_l,
                                 indent_amt=2,
                                 speed_interval=0)
        l_animators.list_printer(l_menus_data.QUIT_MENU_LIST,
                                 indent_amt=2,
                                 speed_interval=0,
                                 finish_delay=.5)

        print()
        l_animators.list_printer(["Select a category using it's prefix letter (except Z)",
                                  "- or -",
                                  "Select a menu option with '1' or '2'"],
                                 indent_amt=7,
                                 speed_interval=0)

        user_input = input("\n  >  ")
        val = user_input.strip().upper()

        if val in categories_dict.keys():
            status = letter_router(categories_dict, val)
            if status == "DELETED" or status == "UPDATED":
                return "RELOOP"
        elif val == "Z":
            print()
            l_animators.animate_text_indented("Z — Default Category, is a fixed category.",
                                              indent_amt=2,
                                              finish_delay=.5)
        elif val == "1":
            valid = create_category(categories_dict)
            if valid:
                return "RELOOP"
        elif val == "2":
            valid = delete_category(categories_dict)
            if valid:
                return "RELOOP"
        elif val == "Q":
            return "QUIT"
        else:
            l_animators.animate_text_indented(
                "Options available are shortcut letters and shortcut numbers.",
                indent_amt=2, finish_delay=.5)


def categories_header(categories_dict):
    print()
    print("CARD CATEGORIES MANAGER")
    print()

    categories_as_list = l_menus_funcs.menu_list_from_dict(categories_dict)
    Z_CATEGORY_LIST = l_menus_funcs.menu_list_from_dict(l_menus_data.Z_CATEGORY_DICT)

    diff_amt = 8 - len(categories_dict)
    empty_slots = get_empty_slots(diff_amt)

    categories_as_list.extend(empty_slots)
    categories_as_list.extend(Z_CATEGORY_LIST)
    l_animators.list_printer(categories_as_list,
                             indent_amt=2,
                             speed_interval=0)




def get_categories_copy():
    categories_dict = {}
    settings = l_files.get_json_settings()

    for k, v in settings.get("card categories").items():
        categories_dict[k] = v

    return dict(sorted(categories_dict.items()))


def get_empty_slots(diff_amt):
    empty_slots = []

    for _ in range(diff_amt):
        empty_slots.append(" .   (empty slot)")

    return empty_slots


def clear() -> None:
    subprocess.run(["clear"], shell=True)


def letter_router(categories_dict, key):
    selected = categories_dict[key].upper()
    format = f"{key} — {selected}"

    while True:
        print()
        l_animators.animate_text(f"{format}")
        print()

        l_animators.list_printer(singleCat_menu_l, indent_amt=2, speed_interval=0)
        print()
        l_animators.list_printer(l_menus_data.EXIT_MENU_LIST, indent_amt=2, speed_interval=0)

        user_input = input("\n  >  ")
        val = user_input.strip()

        if val in singleCat_menu_d.keys():
            if singleCat_menu_d[val] == l_menus_data.ACTION_UPDATE_CATEGORY:
                valid = update_category(categories_dict, key, format)
                if valid:
                    return "UPDATED"
            elif singleCat_menu_d[val] == l_menus_data.ACTION_DELETE_THIS_CATEGORY:
                del categories_dict[key]
                write_new_settings(categories_dict)
                return "DELETED"

        elif val.upper() == "X":
            return "RELOOP"
        else:
            l_animators.animate_text_indented(
                "Options available are shortcut letters and shortcut numbers.",
                indent_amt=2, finish_delay=.5)


def create_category(categories_dict):
    keys = list(categories_dict.keys())

    if categories_filled(categories_dict):
        l_animators.animate_text_indented("Categories currently all filled; one must be deleted.",
                                          indent_amt=2)
        return False

    while True:
        print()
        l_animators.animate_text("CREATE NEW CATEGORY")
        print()

        prefix = get_category_prefix(indent_amt=2)
        name = get_category_name(indent_amt=2)

        valid_prefix, error_prefix = category_prefix_validator(prefix, None, keys)


        if valid_prefix:
            categories_dict[valid_prefix] = name
            l_animators.animate_text_indented(f"Created: {valid_prefix} — {name}",
                                              indent_amt=2,
                                              finish_delay=.5)
            write_new_settings(categories_dict)
            return True
        else:
            l_animators.animate_text_indented(f"{error_prefix}", indent_amt=2, finish_delay=.5)
            return False

def update_category(categories_dict, key, existing):
    keys = list(categories_dict.keys())
    keys.remove(key)
    temp_dict = dict.copy(categories_dict)
    del temp_dict[key]
    categories_as_list = l_menus_funcs.menu_list_from_dict(temp_dict)
    display = ["Existing categories:"]
    display.extend(categories_as_list)

    while True:
        print()
        l_animators.animate_text(f"UPDATE CATEGORY: {existing}")
        print()
        l_animators.list_printer(display,
                                 indent_amt=2,
                                 speed_interval=0,
                                 finish_delay=.5)
        print()
        l_animators.list_printer(["Leaving the category letter or category name blank",
                                  f"will reuse the current letter or name"],
                                 indent_amt=7,
                                 speed_interval=0)
        print()


        prefix = get_category_prefix(indent_amt=2)
        name = get_category_name(indent_amt=2)

        valid_prefix, error = category_prefix_validator(prefix, key, keys)

        if valid_prefix:
            del categories_dict[key]
            categories_dict[valid_prefix] = name
            old = existing.title()
            new = f"{valid_prefix} — {name}"
            print()
            l_animators.animate_text_indented(f"{old} updated to {new}",
                                              indent_amt=2,
                                              finish_delay=.5)
            write_new_settings(categories_dict)
            return True
        else:
            l_animators.animate_text_indented(f"{error}", indent_amt=2, finish_delay=.5)
            return False


def delete_category(categories_dict):
    keys = list(categories_dict.keys())
    categories_as_list = l_menus_funcs.menu_list_from_dict(categories_dict)

    while True:
        print()
        l_animators.animate_text("DELETE A CATEGORY")
        print()

        l_animators.list_printer(categories_as_list,
                                 indent_amt=2,
                                 speed_interval=0)

        print()
        l_animators.list_printer(["(Type 'cancel' or 'exit' to go back)"], indent_amt=2)

        user_input = input("\n  >  ")
        val = user_input.strip().upper()

        if val in keys:
            del categories_dict[val]
            write_new_settings(categories_dict)
            return True
        elif val.lower() in {"cancel", "exit"}:
            l_animators.animate_text_indented("Cancelled",
                                              indent_amt=2,
                                              finish_delay=.5)
            return False
        else:
            l_animators.animate_text_indented("That letter doesn't match a category.",
                                              indent_amt=2,
                                              finish_delay=.5)

def rename_all_matching():
    pass


def category_prefix_validator(new_prefix, old_prefix, keys):
    if not new_prefix and old_prefix:
        return old_prefix, None
    elif not new_prefix:
        return None, "You did not type a letter"
    elif len(new_prefix) > 1:
        return None, "Please use just one letter"
    elif new_prefix == "Z":
        return None, "Z is reserved for the Default Category"
    elif new_prefix not in keys:
        return new_prefix, None
    else:
        return None, f"Letter {new_prefix} is already assigned."

def category_name_validator(new_name):
    if not new_name:
        return None, "You did not type a name"


def get_category_prefix(indent_amt=0, default_for_empty=None):
    space = " " * indent_amt
    if default_for_empty:
        user_input = input(f"{space}Category Letter {default_for_empty} >  ")
    else:
        user_input = input(f"{space}Category Letter >  ")

    return user_input.strip().upper()


def get_category_name(indent_amt=0):
    space = " " * indent_amt

    user_input = input(f"{space}Category Name >  ")
    return user_input.strip().title()


def categories_filled(categories_dict):
    return len(categories_dict) == 8


def write_new_settings(updated_dict):
    settings = l_files.get_json_settings()
    settings["card categories"] = updated_dict

    l_json_utils.write_json(l_files.settings_fullpath, settings)


# update category from letter shortcut
# delete category from letter shortcut
# new category from '1'
# delete category from '2'

# write to settings
# find all matching cards with prefix
# if you delete category with existing cards
# inform user that they will become 'z'
# option to 'cancel' process
# show how many cards will change
# re-prefix all cards / json cards
# when updating existing categories
# ask user to confirm / cancel
# show how many cards will change

if __name__ == "__main__":
    main()
