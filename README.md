# Lumocards

---
Lumocards One is a personal information system tool.<br /> 
It's a todo app, planner, calendar, and journal made for the CLI / Terminal application.
It's meant to offer a single application that can be a reference for everything you need to be tracking. 

It's currently available for MacOS / Linux / Windows.<br />

## Preview Video:
https://www.youtube.com/watch?v=B6Djui-SRJE

<a href="https://www.youtube.com/watch?v=B6Djui-SRJE"><img width="512" height="296" alt="hey" src="https://github.com/user-attachments/assets/f06b780c-32b7-4a34-879e-9bf529b41d93"></a>

---

---
## Requirements:
- Python version 3.12 or greater (download here: https://www.python.org/)
- Micro text editor (download here: https://micro-editor.github.io/)

## Getting Started

### The entire installation and tutorial is available on YouTube. 
Text-based instructions continue below and mirror the YouTube video. 

https://www.youtube.com/watch?v=rJgoYZR6Twk&t=29s 


<a href="https://www.youtube.com/watch?v=rJgoYZR6Twk&t=29s"><img width="512" height="296" alt="hey" src="https://github.com/user-attachments/assets/57ed6d60-8b77-4952-9ac3-d3d76841b17c"></a>


### After downloading / cloning this folder:
- Unzip the folder, if you downloaded a zip folder.
- Open the terminal and navigate to this folder. 
- You can confirm you're in the right spot if your current working directory ends with something like: `/Lumocards-One**`
- Then depending on your computer type, enter in the following or paste the lines below.
### MacOs / Linux:

````
    python3 -m venv venv
````
Then,
````
    source venv/bin/activate
````
Then,
````
    py -m pip install -e .
````
### Windows
**In Powershell:**
````
    py -m venv venv
````
Then,
````
    .\venv\Scripts\Activate.ps1
````
Then,
````
    py -m pip install -e .
````
**In CMD:** <br>
Do the same as Powershell except activate with the line below.
````
    .\venv\Scripts\activate.bat
````
### Additional Notes
Note #1: make sure to include the period shown in the last line below (after the '-e')

Note #2: Anytime from this point onwards, when you want to use Lumo, you will first need to activate lumo. This is always done by first navigating to the Lumocards folder in the terminal and then by retyping: <br> 
`source venv/bin/activate` for Mac/Linux <br>
`.\venv\Scripts\activate.ps1` for Windows, or a similar command like `\activate.bat`

This activation process can be simplified by adding lines to a .bashrc file on Mac/Linux <br>
or a $PROFILE file on Windows, or by making a custom script. 

On most computers you should be able to tell if your environment is activated because your terminal prompt will change. <br>

Once activated, you are ready to use Lumo.

## How to: Using Keywords
To test if everything is working well, type `lumo` into the terminal / command line. You should see a menu come up like this:

<img width="959" height="483" alt="lumo_menu" src="https://github.com/user-attachments/assets/d7a979ca-3814-42b3-bbae-d13920fdcfb8" />


### Available keywords
````
	
	about     ->  Show the about section.
	all       ->  Show all the Lumo sub-programs.
	agenda    ->  Show the agenda created for today.
	calendar  ->  Launch the calendar program to view events in days or weeks format.
   	              (note this will require additional setup, see the YouTube video)	    
	    
	checklist ->  Launch a program to review checklists and processes.
	journal   ->  Create or continue a journal entry for today.
	newcard   ->  Create a new card in Lumo.
	planner   ->  Launches the daily planner to review Near Focus Cards.
	pomodoro  ->  Set up a focus timer and a break timer.
	search    ->  Search for a card.
	settings  ->  Edit categories for cards.
````

### About the Lumo Keyword
The Lumo keyword `lumo` is only used to launch the main menu or to directly launch subprograms keywords by<br />
 such as `lumo journal`. Once you are inside the main menu however, you launch subprograms with the keyword alone, i.e. `journal`

### Keyword: About
Type `about` from inside the Lumo Menu.
### Keyword: All
Type `lumo all` from the terminal -or- `all` from  the Lumo Menu.

This keyword shows a full menu of every sub-program that is available. 

### Keyword: Calendar
Type `lumo calendar` from the terminal -or- `calendar` from the Lumo Menu.

This keyword show a basic representation of your connected Google Calendar with limited features. 
### Keyword: Checklist
Type `lumo checklist` from the terminal -or- `checklist` from the Lumo Menu.

This keyword launches a checklist menu which you can use to review routine checklists that you set up as 'cards'.
### Keyword: Journal
Type `lumo journal` from the terminal -or- `journal` from the Lumo Menu. 

This keyword launches a text editor with today's date already printed in the file and creates a .txt file with the date <br> included in the name. 
I.e. 2025_A_Jan_01_journal.txt. (The captial A is to keep all of January files together, and B for February and so on.)
### Keyword: Newcard
Type `lumo newcard` from the terminal -or- `newcard`, `new card` from inside the Lumo Menu.<br>

You can also make cards directly from the terminal with `lumo newcard <category> <card title>`.<br> Such as `lumo newcard b my shopping list` where 'b' represents the card category and 'my shopping list' is the title. <br>
Note: you cannot type `newcard <category> <card title>` from the Lumo Menu, only `newcard`.

This keyword starts the process to create new cards which take a card category and a card title, along with optional steps for each card. 
Cards can be made for various locations: 
- Near Focus 
- Middle Focus
- Distant Focus
- Recurring
- Checklist

### Keyword: Planner
Type `lumo planner` or `lumo cards` or `lumo cards planner` from the terminal or `planner` or `cards` or `cards planner` from  the Lumo Menu. 

This keyword launches the process to setup a daily agenda which reviews three card categories and combines them to create a finished planner.txt file that users can reference when organizing their day. The three categories of cards are:
- Near Focus Cards
- Recurring Cards
- Calendar Cards

### Keyword: Pomodoro
Type `lumo pomodoro` from the terminal or `pomodoro` from the Lumo Menu. 

This keyword launches the pomodoro-style timer complete with two presets and a settings option.
### Keyword: Search
Type `lumo search` from the terminal or `search` from the Lumo Menu. 
<br> From the terminal you can also type: `lumo search <myterm>` to directly search for a card from the terminal. <br>

As an example `lumo search hat`. <br>
Note: the term must be one word, and cannot be more than one word. Partial words are ok! <br>
Note: you cannot type `search <searchterm>` from the Lumo Menu, only `search`.

This keyword launches the search program to look through cards.

### Keyword: Settings

---
## Additional Info and Important Reminders


### Important to Know 