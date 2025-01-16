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

    x = 1
    while x < time_in_secs:
        sleep(1)
        mins_remaining = round(mins - (x // 60))
        mins_as_dots = "." * mins_remaining
        mins_as_space = " " * mins_remaining
        print(f"{mins_as_dots}", end="\r")

        x += 1

    for n in range(3):
        run(f'pw-play {selected_sound}', shell=True)



def dim_os():
    pass


def lum_os():
    pass

pomodoro(timer_duration)



