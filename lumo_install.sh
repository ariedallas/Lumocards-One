#! /usr/bin/bash

VENV_PATH="SUPPORT_FILES/LUMO_RUNTIME"
REQUIREMENTS="SUPPORT_FILES/requirements.txt"

echo ""
echo "	Install Helper Script from Lumocards"
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
    #deactivate_venv
}

install_pkgs() {
    activate_venv
    echo "Installing features to make Lumocards to work, including options to"
    echo "work with Google Calendar, and make use of safe delete"
    pip3 install --upgrade -r $REQUIREMENTS
}

lumo_install() {
    echo "Hello"
    create_venv
    install_pkgs
}

lumo_welcome_msg() {
    echo "Welcome to Lumocards, where you decide what cards to put in focus."
}

alias lumo="activate_venv"
alias lumocards="python3 LUMO_LIBRARY/lumo_cardsrun.py"
alias locard="python3 LUMO_LIBRARY/lumo_search_cards.py"
alias newcard="python3 LUMO_LIBRARY/lumo_newcard.py"
alias lightwalks="open LIGHTWALK_CYCLES"
alias lightwalk="python3 LUMO_LIBRARY/lumo_gettoday.py"
alias pomodoro="python3 LUMO_LIBRARY/lumo_pomodoro.py"
alias outlist="python3 LUMO_LIBRARY/lumo_outlist.py"
alias checklist="python3 LUMO_LIBRARY/lumo_outlist.py"

lumo
