import os

from argparse import ArgumentParser
from time import sleep
from subprocess import run

import lumo_filehandler as l_files

selected_sound = os.path.join(l_files.sounds_folder, "block.mp3")

suitcase = ArgumentParser()
suitcase.add_argument(
        'minutes',
        metavar='Minutes to time',
        help="How many minutes?")

options = suitcase.parse_args()
timer_duration = float(options.minutes)

def pomodoro(mins):

    time_in_secs = int((mins * 60))

    print("{} minute timer started".format(mins))
    run(f'pw-play {selected_sound}', shell=True)

    for x in range(time_in_secs):
        mins_remaining = round(mins) - (x // 60)
        mins_as_dots = "." * mins_remaining
        blinker = "." * (mins_remaining - 1)

        print(f"  {mins_as_dots}", end="\r")
        sleep(.1)
        print(" " * 30, end="\r")
        sleep(.1)

        print(f"  {mins_as_dots}", end="\r")
        sleep(.1)
        print(" " * 30, end="\r")
        sleep(.1)

        print(f"  {blinker}", end="    \r")
        sleep(.6)

    for n in range(3):
        run(f'pw-play {selected_sound}', shell=True)

def pomodoro_test(mins):

    for n in range(30):
        print(n)
        sleep(1)

pomodoro(timer_duration)


