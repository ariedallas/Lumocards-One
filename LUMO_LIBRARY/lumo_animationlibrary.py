import time
from typing import Optional


def animate_text(text: str, speed: float =.025, finish_delay: float=0) -> None:
    text_add_space = " " + text
    for n in range(len(text_add_space)):
        print(text_add_space[:n], end="\r")
        time.sleep(speed)

    print(text, end="\r")
    time.sleep(speed)
    print(text)

    if finish_delay:
        time.sleep(finish_delay)


def animate_text_indented(text: str, speed: float=.025, indent_amt=Optional[int], finish_delay: float=0) -> None:
    if not indent_amt:
        indent_amt = 0

    text_add_space = (" " * indent_amt) + text

    for n in range(indent_amt, len(text_add_space) + 1):
        print(text_add_space[:n], end="\r")
        time.sleep(speed)

    print(text_add_space, end="\r")
    time.sleep(speed)
    print(text_add_space)

    if finish_delay:
        time.sleep(finish_delay)


def list_printer(text_list: Optional[list[str]] = None,
                 indent_amt: int=0,
                 speed_interval: float=.35,
                 finish_delay: float=0) -> None:

    if not text_list:
        text_list = [""]

    for item in text_list:
        if indent_amt > 0:
            print(
                (" " * indent_amt)
                + item
            )
        else:
            print(item)
        time.sleep(speed_interval)

    if finish_delay > 0:
        time.sleep(finish_delay)


def list_printer_breaks(text_list: Optional[list[str]] = None,
                 indent_amt: int=0,
                        regular_break: int=0) -> None:
    space = (" " * indent_amt)
    if not text_list:
        text_list = [""]

    for idx, item in enumerate(text_list):
        print(f"{space}{item}")

        if (idx + 1) % regular_break == 0\
                and (idx + 1) != len(text_list):
            print()


if __name__ == "__main__":
    animate_text_indented("boooo!", indent_amt=2)

