import os
import subprocess

import LUMO_LIBRARY.lumo_filehandler as l_files

settings = l_files.get_json_settings()

d, m, y = l_files.today_frmttd_spaces.split()

def get_today_planner():
	if os.path.exists(l_files.today_planner_fullpath):
		print(f"Opening Planner file for {m} {d}, {y}...")
		subprocess.run([f"{l_files.micro} {l_files.today_planner_fullpath}"], shell=True)

	print("\n")

get_today_planner()
