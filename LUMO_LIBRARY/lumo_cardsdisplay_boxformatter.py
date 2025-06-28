import LUMO_LIBRARY.lumo_animationlibrary as l_animators
import LUMO_LIBRARY.lumo_card_utils as l_card_utils


def display_card(var_card, simple_title, display_qty=6, length=50, height=10):
    if simple_title:
        f_card_name = var_card[0].upper()
    else:
        f_card_name = l_card_utils.format_card_title(var_card[0])

    todo_items = var_card[1]
    card_display_list = []

    card_display_list.append(("|" + ("•" * length) + "|"))

    row_position = 0
    header_breakpoint = height // 4
    content_breakpoint = height // 2.5

    while row_position < height:
        card_display_list.append("•" + (" " * length) + "•")
        row_position += 1

        if row_position == header_breakpoint:
            header_line = get_centered_line(f_card_name)
            card_display_list.append(header_line)

        if row_position == content_breakpoint:
            centered_steps = get_centered_content(todo_items, display_qty)
            card_display_list.extend(centered_steps)

    card_display_list.append(("|" + ("•" * length) + "|"))
    l_animators.list_printer(card_display_list, indent_amt=2, speed_interval=0)


def get_centered_line(content="sample_content"):
    content = content.upper()
    if len(content) > 40:
        content_truncated = content[:38] + "…"
        return ("•{:^50}•".format(content_truncated))
    else:
        return ("•{:^50}•".format(content))


def get_centered_content(card_steps, display_qty):
    centered_steps = []
    end = display_qty + 1
    qty_list = [f"{str(num)}) " for num in range(1, end)]

    for letter, item in (zip(qty_list, card_steps)):
        centered_steps.append(get_centered_line(letter + item))

    return centered_steps


def display_rectangle(length, height):
    print("\n")
    print("|" + ("•" * length) + "|")

    row_position = 0
    header_breakpoint = (height // 4)
    while row_position < height:

        # print(sidecol)
        print("•" + (" " * length) + "•")
        row_position += 1

        if row_position == header_breakpoint:
            get_centered_line()
            # print(header_breakpoint)

    print("|" + ("•" * length) + "|")


if __name__ == "__main__":
    print("Hello from Main")
