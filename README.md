# Lumocards

---
Lumocards One is the first stable version of a particular information system tool.<br /> 
It's like a todo app, a calendar, and planner rolled into a CLI / Terminal application. [needs link]<br />

It's currently available for MacOS / Linux.<br />
It also requires the use of Python 3 on your computer. 

This README is meant for a wide audience of persons who may be more or less familiar with computers and software development.<br />
As such, it's a bit more wordy to explain a few more details.

## Getting Started

After downloading / cloning this folder:
- Unzip the folder, if you downloaded a zip folder.
- Open the terminal.
- Navigate to where this folder is on your computer. (This can be googled if unclear).
- Alternatively, you can open the folder in your file browser and right click to open it in the terminal. 
- You can confirm your ready by printing the current working directory which should end with: `/Lumocards-One**`


- If that looks good, type in the following or paste the lines below.
- Note: make sure to include the period shown in the last line below.


````
    source ./lumo_install.sh && lumo_install
    lumo_activate
    python3 -m pip install -e .
````
Anytime from this point onwards, when you want to start a Lumo session, you will first need to activate lumo.<br />
This is always done by first navigating to the Lumocards folder in the terminal and then by retyping: `source ./lumo_install.sh && lumo_activate`.<br />

Once activated, you are ready to use Lumo.
Lumo is a group of sub-programs that you launch with keywords.

**Optional Reading: This activation step starts a virtual environment, which Lumo uses to keep your computer tidy.
On most computers you should be able to tell if your environment is activated because your terminal prompt will change.

[I don't understand why it will currently break without the -e]

## How to: Using Keywords
If the previous section goes well, the following keywords are now available:
````
	lumo           ->  Launches the main Lumo Menu: 'LUMOCARDS' .
	
	lumo all       ->  Show all the Lumo sub-programs.
	
	lumo calendar  ->  Launch the calendar program to schedule events (cards).
	    (note this will require additional setup)	    
	    
	lumo checklist ->  Launch a program to review checklists and processes.
	lumo journal   ->  Create or continue a journal entry for today.
	lumo newcard   ->  Create a new card in Lumo
	lumo planner   ->  Launches the daily planner to review Near Focus Cards.
	lumo pomodoro  ->  Set up a focus timer and a break timer
	lumo search    ->  Search for a card
	lumo settings  ->  Open the settings menu; adjust various settings
	lumo timer     ->  Set a single custom timer
````

### About the Lumo Keyword
The Lumo keyword `lumo` is only used to start a session from the terminal.<br /> Once you are inside the Lumo Menu, you can access the keywords by<br />
typing them without the prefix 'lumo'. For example,  you would just type 'timer' instead of 'lumo timer'. 

### About Shortcut Letters
Sub-programs, i.e. the keywords in the Lumo Menu are paired with shortcut letters that appears to the left of the keyword.<br />
You can use these shortcut letters by typing the letter (lower or uppercase) and pressing enter.

### Keyword: All
Use `lumo all` from the terminal -or- `all` from  the Lumo Menu


This keyword shows a full menu of every sub-program that is available. 

### Keyword: Calendar
Use `lumo calendar` from the terminal -or- `calendar` from the Lumo Menu.

### Keyword: Checklist
...
### Keyword: Journal
...
### Keyword: Newcard
Use `lumo newcard` from the terminal -or- `newcard`, `new card` from inside the Lumo Menu.
### Keyword: Planner
...
### Keyword: Pomodoro
...
### Keyword: Search
...
### Keyword: Settings
...
### Keyword: Timer
...
<br />

---

## Settings
### Json Settings Etc.
...
<br />

---

## About
Hopefully this tool can be of help to you. 
