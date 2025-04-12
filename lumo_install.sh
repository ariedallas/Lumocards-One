#!/usr/bin/bash

VENV_PATH="SUPPORT_FILES/LUMO_RUNTIME"
REQUIREMENTS="SUPPORT_FILES/requirements.txt"

echo ""
echo "	Install Helper for Lumocards One"
echo ""

# Activate the virtual environment
lumo_activate() {
    source "$VENV_PATH/bin/activate"
}

# Create the virtual environment and install default or specified packages
create_venv() {
    echo "Creating Python virtual environment at $VENV_PATH..."
    mkdir -p "$VENV_PATH" && python3 -m venv "$VENV_PATH"
    echo "Virtual environment completed"
}

#install_pkgs() {
#   activate_venv
#    echo "Installing features to make Lumocards to work, including options to"
#    echo "work with Google Calendar, and make use of safe delete"
#    pip3 install --upgrade -r $REQUIREMENTS
#}

lumo_install() {
    echo "Hello"
    create_venv
}

lumo_welcome_msg() {
    echo "Welcome to Lumocards One"
}

