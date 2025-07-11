# Lumocards

---
Lumocards One is a personal information system tool.<br /> 
It's a todo app, planner, calendar, and journal made for the CLI / Terminal application.

It's currently available for MacOS / Linux.<br />
It also requires the use of Python 3 on your computer. 

This README is meant for a wide audience of persons who may be more or less familiar with computers and software development.<br />
As such, it's a bit more wordy to explain a few more details.
---
## Requirements:
- Python version 3.12 or greater (download here: https://www.python.org/)
- Micro text editor (download here: https://micro-editor.github.io/)

## Getting Started

### The entire installation is available as a YouTube video here: <br> 
https://www.youtube.com/watch?v=rJgoYZR6Twk&t=29s 

### After downloading / cloning this folder:
- Unzip the folder, if you downloaded a zip folder.
- Open the terminal and navigate to this folder. 
- You can confirm you're in the right spot if your current working directory ends with something like: `/Lumocards-One**`
- Then depending on your computer type, enter in the following or paste the lines below.
### MacOs / Linux:

````
    python3 -m venv venv
    source venv/bin/activate
    py -m pip install -e .
````
### Windows
In Powershell:
````
    py -m venv venv
    .\venv\Scripts\Activate.ps1
    py -m pip install -e .
````
In CMD:
````
    py -m venv venv
    .\venv\Scripts\activate.bat
    py -m pip install -e .
````
### Additional Notes
Note #1: make sure to include the period shown in the last line below.

Note #2: Anytime from this point onwards, when you want to use Lumo you will first need to activate lumo.<br />
This is always done by first navigating to the Lumocards folder in the terminal and then by retyping: <br> 
`source venv/bin/activate` for Mac/Linux <br>
`.\venv\Scripts\activate` for Windows (or a similar command)

On most computers you should be able to tell if your environment is activated because your terminal prompt will change. <br>
Once activated, you are ready to use Lumo.
Lumo is a group of sub-programs that you launch with keywords.

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
