import os

import LUMO_LIBRARY.lumo_filehandler as l_files

source_path = os.path.join(l_files.support_files_folder,
                           "alphabetizer_input.txt")
dest_path = os.path.join(l_files.support_files_folder,
                         "alphabetizer_output.txt")

with open(source_path) as fin:
    lines = fin.readlines()
sorted_lines = sorted(lines, key=lambda i: i.lower())

with open(dest_path, "w+") as fout:
    fout.write("ALPHABETIZED:\n")
    for l in sorted_lines:
        fout.write(l)
