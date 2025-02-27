import datetime
import os
import string
import subprocess

import LUMO_LIBRARY.lumo_filehandler as l_files

settings = l_files.get_json_settings()
today = datetime.date.today()

LETTERS_THROUGH_L = string.ascii_lowercase[:12]
curr_month_int = datetime.date.today().month
curr_month_idx = curr_month_int - 1
curr_month_lttr = LETTERS_THROUGH_L[curr_month_idx].upper()

journal_title_long = today.strftime("%B %d, %Y")

journal_name = today.strftime(f"%Y_{curr_month_lttr}_%b_%d")
journal_filename = f"{journal_name}__journal.txt"
journal_abspath = os.path.join(l_files.journal_folder, journal_filename)

def make_journal_file():
    with open(journal_abspath, "w+") as journal:
        journal.write(journal_title_long)
        journal.write("\n\n")


def get_or_make_journal():
    if os.path.exists(journal_abspath):
        pass
    else:
        make_journal_file()

def main():
    get_or_make_journal()
    subprocess.run([f"{settings.get("text editor")} +9999999 {journal_abspath}"], shell=True)



if __name__ == "__main__":
    main()