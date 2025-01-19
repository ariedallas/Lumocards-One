import os
import subprocess

import lumo_filehandler as l_files

def x():
	print("Hello from Lumo Get Today")

def get_today_file():
	for f in os.listdir("LIGHTWALK_CYCLES"):
		header = str(f)[:9]
		path_match = os.path.join(l_files.planner_folder, f)
		if header == l_files.today_frmttd.upper():
			print(f"Opening Lightwalk file for {l_files.today_frmttd}")
			subprocess.run([f'open {path_match}'], shell=True)

	print("\n")

get_today_file()

