import argparse
import collections


def function_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(func.__name__)
        print(end - start)
        return result

    return wrapper

ALL_MENU = collections.OrderedDict([
    ("A", "Planner")
    , ("B", "New Card")
    , ("C", "Calendar")
    , ("D", "Journal")
    , ("E", "Search")
    , ("F", "Timer")
    , ("G", ":: settings ::")
    , ("H", ":: about ::")
])

length = len(ALL_MENU)
print(length)

x = "PPP"
x.lower()
print(x)

t = "a" in ["a", "b", "c"] or "b"
print(t)

for i, n in enumerate(ALL_MENU.items()):
    if i == 4:
        print()
    if i == length - 2:
        print()
    print(n, i)


