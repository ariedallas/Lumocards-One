#!/bin/bash

 pyinstaller LUMO_LIBRARY/__main__.py\
 	--name Lumogarden\
	# --onedir\
	# --distpath Lumogarden_Project\
	# --contents-directory:./_int
	--add-data CARDS:./USER_DATA/CARDS\
	--add-data JOURNAL:./USER_DATA/JOURNAL\
	--add-data PLANNER:./USER_DATA/PLANNER\
	--add-data SUPPORT_FILES:./USER_DATA/SUPPORT_FILES\
	--add-binary micro:.\
