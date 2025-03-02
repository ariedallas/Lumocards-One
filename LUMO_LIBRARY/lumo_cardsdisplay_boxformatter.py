import LUMO_LIBRARY.lumo_card_utils as l_card_utils


def display_card(var_card, display_qty=6, length=50, height=10):
    f_card_name = l_card_utils.format_card_title(var_card[0])
    todo_items = var_card[1]

    print("|" + ("•" * length) + "|")

    row_position = 0
    header_breakpoint = height // 4
    content_breakpoint = height // 2.5

    while row_position < height:
        print("•" + (" " * length) + "•")
        row_position += 1

        if row_position == header_breakpoint:
            display_centered_line(f_card_name)

        if row_position == content_breakpoint:
            display_centered_content(todo_items, display_qty)

    print("|" + ("•" * length) + "|")


def display_centered_line(content="sample_content"):

    content = content.upper()
    if len(content) > 40:
        content_truncated = content[:38] + "…"
        print("•{:^50}•".format(content_truncated))
    else:
        print("•{:^50}•".format(content))


def display_centered_content(card_steps, display_qty):

    qty_list = [(str(num) + ") ") for num in range(1,display_qty+1)]

    for letter, item in (zip(qty_list, card_steps)):
        display_centered_line(letter+item)


def display_rectangle(length, height):

    print("\n")
    print("|"+("•" * length)+"|")

    row_position = 0
    header_breakpoint = (height // 4)
    while row_position < height:

        # print(sidecol)
        print("•"+(" " * length)+"•")
        row_position += 1

        if row_position == header_breakpoint:
            display_centered_line()
            # print(header_breakpoint)

    print("|" + ("•" * length) + "|")


if __name__ == "__main__":
    print("Hello from Main")