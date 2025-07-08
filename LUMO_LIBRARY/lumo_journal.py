import datetime
import os
import pathlib
import string
import subprocess
import time

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils
import LUMO_LIBRARY.lumo_filehandler as l_files

settings = l_files.get_json_settings()


def make_journal_file():
    today = datetime.date.today()

    journal_abspath = get_journal_path()
    journal_title_long = today.strftime("%B %d, %Y")

    if not os.path.exists(l_files.journal_folder):
        l_animators.animate_text("Creating 'JOURNAL' folder", finish_delay=.5)
        pathlib.Path(l_files.journal_folder).mkdir()

    with open(journal_abspath, "w+") as journal:
        journal.write(journal_title_long)
        journal.write("\n\n")


def get_or_make_journal():
    journal_abspath = get_journal_path()

    if os.path.exists(journal_abspath):
        with open(journal_abspath, "r") as journal:
            lines = journal.readlines()

        with open(journal_abspath, "a") as journal:

            if lines[-1] != ("\n") and len(lines) > 3:
                journal.write("\n")

    else:
        make_journal_file()

    return journal_abspath


def get_journal_path():
    today = datetime.date.today()

    LETTERS_THROUGH_L = string.ascii_lowercase[:12]
    curr_month_int = datetime.date.today().month
    curr_month_idx = curr_month_int - 1
    curr_month_lttr = LETTERS_THROUGH_L[curr_month_idx].upper()

    journal_name = today.strftime(f"%Y_{curr_month_lttr}_%b_%d")
    journal_filename = f"{journal_name}__journal.txt"
    journal_abspath = os.path.join(l_files.journal_folder, journal_filename)

    return journal_abspath


def program_header():
    print()
    print("JOURNAL")
    print()
    time.sleep(.5)


def main():
    journal_abspath = get_or_make_journal()
    l_card_utils.t_editor(journal_abspath, True)


if __name__ == "__main__":
    main()
