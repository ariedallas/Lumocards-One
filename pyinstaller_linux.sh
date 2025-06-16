#!/bin/bash

 pyinstaller LUMO_LIBRARY/__main__.py\
 	--name Lumogarden\
	--onedir\
	--distpath Lumogarden_Project\
	--add-data ./__USER_FILES__:./__USER_FILES__\
	--add-data ./__SUPPORT_FILES__:./__SUPPORT_FILES__\
	--add-binary micro:.\
