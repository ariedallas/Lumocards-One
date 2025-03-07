import time


def function_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(func.__name__)
        print(end - start)
        return result

    return wrapper

@function_timer
def hello():
    print("hey")
    return "baby"


stuff = hello()
print(stuff)

meow = [1, 2, 3]
meow.pop(-1)
print(meow)