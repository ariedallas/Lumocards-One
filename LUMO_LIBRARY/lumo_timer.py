import argparse
import os
import subprocess
import time

import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_filehandler as l_files

selected_sound = os.path.join(l_files.sounds_folder, "block.mp3")


def get_input_to_mins():
    var_mins = input("  Set timer for how many minutes? >  ")
    return var_mins


def program_header():
    print()
    print("TIMER / POMODORO")
    print()


def main(var_mins=None):
    program_header()

    if not var_mins:
        var_mins = get_input_to_mins()

    while True:
        try:
            float_mins = float(var_mins)
            break

        except ValueError as e:
            print()
            l_animators.animate_text("  Try using just numbers (decimals OK)")
            var_mins = input("  >  ")

    time_in_secs = int((float_mins * 60))

    print("  {} minute timer started".format(float_mins), end="\n  ")
    subprocess.run(f'pw-play {selected_sound}', shell=True)

    for x in range(time_in_secs):
        mins_remaining = round(float_mins) - (x // 60)
        mins_as_dots = "." * mins_remaining
        blinker = "." * (mins_remaining - 1)

        print(f"  {mins_as_dots}", end="\r")
        time.sleep(.1)
        print(" " * 30, end="\r")
        time.sleep(.1)

        print(f"  {mins_as_dots}", end="\r")
        time.sleep(.1)
        print(" " * 30, end="\r")
        time.sleep(.1)

        print(f"  {blinker}", end="    \r")
        time.sleep(.6)

    print("  Done")
    for n in range(3):
        subprocess.run(f'pw-play {selected_sound}', shell=True)

    print()
    l_animators.animate_text(f"  Quit Lumo: Pomodoro", finish_delay=.5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'minutes',
        nargs="?",
        metavar='Minutes to time',
        help="How many minutes?"
    )

    options = parser.parse_args()

    main(options.minutes)
