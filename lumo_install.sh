#!/usr/bin/bash

VENV_PATH="SUPPORT_FILES/LUMO_RUNTIME"
REQUIREMENTS="SUPPORT_FILES/requirements.txt"

echo ""
echo "	Install Helper for Lumocards One"
echo ""

# Activate the virtual environment
activate_venv() {
    source "$VENV_PATH/bin/activate"
}

# Create the virtual environment and install default or specified packages
create_venv() {
    echo "Creating Python virtual environment at $VENV_PATH..."
    mkdir -p "$VENV_PATH" && python3 -m venv "$VENV_PATH"
    echo "Virtual environment completed and activated."
}

#install_pkgs() {
#    activate_venv
#    echo "Installing features to make Lumocards to work, including options to"
#    echo "work with Google Calendar, and make use of safe delete"
#    pip3 install --upgrade -r $REQUIREMENTS
#}

lumo_install() {
    echo "Hello"
    create_venv
#    install_pkgs
}

lumo_welcome_msg() {
    echo "Welcome to Lumocards One"
}

alias lu="python3 -m LUMO_LIBRARY.scratch"
alias lumocards="python3 -m LUMO_LIBRARY.lumo_cards_planner"
alias locard="python3 -m LUMO_LIBRARY.lumo_search"
alias newcard="python3 -m LUMO_LIBRARY.lumo_newcard_refactor"
alias planner="open PLANNER"
alias today="python3 -m LUMO_LIBRARY.lumo_gettoday"
alias pomodoro="python3 -m LUMO_LIBRARY.lumo_pomodoro"
alias checklist="python3 -m LUMO_LIBRARY.lumo_checklist"
alias checklist="python3 -m LUMO_LIBRARY.lumo_checklist"
