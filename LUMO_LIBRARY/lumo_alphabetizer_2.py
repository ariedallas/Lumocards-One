import argparse
import subprocess
import time
import sys
import pathlib

import lumo_filehandler as l_files

home = pathlib.Path.home()

parser = argparse.ArgumentParser()
parser.add_argument(
		'file_fullpath'
		, action='store'
		, metavar='Fullpath File'
		, help="require an absolute path to a filename")

parser_options = parser.parse_args()

fullpath = parser_options.file_fullpath
file = open(fullpath, 'r+')

destination_file_fullpath = f'{home}/_A33A_LUMO_A33A/L3•LUMO_PROTOTYPES/LUMOGARDEN_CLI_V0.1/alphabetizer_transmit.txt'
destination_file = open(destination_file_fullpath, 'r+')

lineList = [l.rstrip('\n') for l in file]
sortedList = sorted(lineList, key=lambda i: i.lower())

destination_file.write('\n')
destination_file.write('(ALPHABETIZED CONTENT)\n')
for l in sortedList:
    destination_file.write(l+'\n')

time.sleep(3)
