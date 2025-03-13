import time


def animate_pause(no_of_lines: int, speed: float = .5):
    for x in range(no_of_lines):
        print()
        time.sleep(speed)


def animate_text(text, speed: float = .025, finish_delay: float = 0):
    text_add_space = " " + text
    for n in range(len(text_add_space)):
        print(text_add_space[:n], end='\r')
        time.sleep(speed)

    print(text, end="\r")
    time.sleep(speed)
    print(text)

    if finish_delay:
        time.sleep(finish_delay)


def animate_text_fast(text):
    text_add_space = " " + text
    for n in range(len(text_add_space)):
        print(text_add_space[:n], end='\r')
        time.sleep(.02)

    print(text, end='\n')
    time.sleep(.5)


def standard_interval_printer(text_list=None, speed_interval: float = .35, animate_letters: float = 0):
    if not text_list:
        text_list = ['']

    for item in text_list:
        if animate_letters > 0:
            animate_text(item, speed=animate_letters)
        else:
            print(item)
        time.sleep(speed_interval)


if __name__ == "__main__":
    standard_interval_printer()


def fixed_interval_delay(text: str, interval: float = .35):
    animate_text(text)
    time.sleep(interval)
