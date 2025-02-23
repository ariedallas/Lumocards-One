import pprint
import subprocess
import sys
from argparse import ArgumentParser

import lumo_filehandler as l_files

import SUPPORT_FILES.TEMP.scratch_2 as scratch_2
import SUPPORT_FILES.TEMP.scratch_3 as scratch_3
import SUPPORT_FILES.TEMP.scratch_4 as scratch_4

parser = ArgumentParser(add_help=False)

parser.add_argument(
    "route"
    , action="store"
    , metavar=""
    , nargs="?"
    , default="show menu"
    , help=""
)



args = parser.parse_args()

def root_loop(option):

    if option != "show menu":
        router(option)

    while True:
        subprocess.run(['clear'], shell=True)
        print(); print(); print()
        for l in ["a", "b", "c"]:
            print(l)

        print("You can also run these by typing 'lumo newcard', 'lumo cards', 'lumo search' ")
        print()
        usr_response = input("  > ")

        router(usr_response)


def router(option):

    if option == 'a':
        scratch_2.call_from_2()
        usr_response = input("> ")

    elif option == 'b':
        scratch_3.call_from_3()
        usr_response = input("> ")

    elif option == 'c':
        scratch_4.call_from_4()
        usr_response = input("> ")

    else:
        print("hey you have just those options...")
        usr_response = input("> ")


if __name__ == "__main__":
    root_loop(args.route)